"""Project storage and management system."""

import os
import json
from pathlib import Path
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from aether_os.core.models import Base, Project, JobResult, ProjectFile, DeploymentLog


class ProjectManager:
    """Gestiona proyectos y almacenamiento."""
    
    def __init__(self, workspace_dir: str = "aether_workspace", db_url: str = None):
        self.workspace_dir = Path(workspace_dir)
        self.workspace_dir.mkdir(exist_ok=True)
        
        self.db_url = db_url or f"sqlite:///{self.workspace_dir}/aether.db"
        self.engine = create_engine(self.db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def create_project(self, name: str, description: str = "") -> str:
        """Crear nuevo proyecto."""
        session = self.Session()
        project = Project(name=name, description=description)
        session.add(project)
        session.commit()
        project_id = project.id
        session.close()
        
        project_dir = self.workspace_dir / project_id
        project_dir.mkdir(exist_ok=True)
        
        return project_id
    
    def get_project(self, project_id: str) -> Project:
        """Obtener proyecto."""
        session = self.Session()
        project = session.query(Project).filter(Project.id == project_id).first()
        session.close()
        return project
    
    def save_job_result(self, project_id: str, agent_type: str, agent_name: str, job_name: str, output_data: dict, error: str = None, duration: int = 0):
        """Guardar resultado de un trabajo."""
        session = self.Session()
        job = JobResult(
            project_id=project_id,
            agent_type=agent_type,
            agent_name=agent_name,
            job_name=job_name,
            output_data=output_data,
            error=error,
            duration_seconds=duration,
            status="failed" if error else "completed"
        )
        session.add(job)
        session.commit()
        session.close()
    
    def create_file(self, project_id: str, filename: str, content: str, file_type: str, created_by: str):
        """Crear archivo en proyecto."""
        session = self.Session()
        
        project_dir = self.workspace_dir / project_id
        file_path = project_dir / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Escribir con encoding UTF-8
        try:
            file_path.write_text(content, encoding='utf-8')
        except Exception as e:
            print(f"Error writing file {filename}: {e}")
            # Fallback: write only ASCII
            clean_content = content.encode('ascii', 'ignore').decode('ascii')
            file_path.write_text(clean_content, encoding='utf-8')
        
        project_file = ProjectFile(
            project_id=project_id,
            filename=filename,
            filepath=str(file_path),
            file_type=file_type,
            content=content[:1000] if len(content) > 1000 else content,
            created_by_agent=created_by
        )
        session.add(project_file)
        session.commit()
        session.close()
        
        return str(file_path)
    
    def get_project_files(self, project_id: str) -> list:
        """Obtener archivos del proyecto."""
        session = self.Session()
        files = session.query(ProjectFile).filter(ProjectFile.project_id == project_id).all()
        session.close()
        return files
    
    def get_project_status(self, project_id: str) -> dict:
        """Estado del proyecto."""
        session = self.Session()
        project = session.query(Project).filter(Project.id == project_id).first()
        jobs = session.query(JobResult).filter(JobResult.project_id == project_id).all()
        files = session.query(ProjectFile).filter(ProjectFile.project_id == project_id).all()
        session.close()
        
        return {
            "id": project.id,
            "name": project.name,
            "status": project.status,
            "created_at": project.created_at.isoformat(),
            "jobs_count": len(jobs),
            "files_count": len(files),
            "github_url": project.github_url,
            "deployed_url": project.deployed_url
        }
