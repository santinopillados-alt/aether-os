"""Database models for AETHER OS projects."""

from sqlalchemy import Column, String, DateTime, JSON, Integer, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()


class Project(Base):
    """Representa un proyecto creado."""
    __tablename__ = "projects"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Metadata
    status = Column(String, default="draft")  # draft, building, deployed, archived
    github_url = Column(String, nullable=True)
    deployed_url = Column(String, nullable=True)
    
    # Relationships
    jobs = relationship("JobResult", back_populates="project")
    files = relationship("ProjectFile", back_populates="project")
    
    def __repr__(self):
        return f"<Project {self.name}>"


class JobResult(Base):
    """Resultado de un trabajo de agente."""
    __tablename__ = "job_results"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    
    agent_type = Column(String, nullable=False)  # ceo, cto, frontend, backend, etc
    agent_name = Column(String, nullable=False)
    job_name = Column(String, nullable=False)
    
    status = Column(String, default="completed")  # completed, failed
    input_data = Column(JSON)
    output_data = Column(JSON)
    error = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    duration_seconds = Column(Integer)
    
    project = relationship("Project", back_populates="jobs")
    
    def __repr__(self):
        return f"<JobResult {self.agent_name}>"


class ProjectFile(Base):
    """Archivos generados en un proyecto."""
    __tablename__ = "project_files"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)  # Ruta en disco
    file_type = Column(String)  # py, tsx, json, dockerfile, etc
    content = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by_agent = Column(String)  # Qué agente lo creó
    
    project = relationship("Project", back_populates="files")
    
    def __repr__(self):
        return f"<ProjectFile {self.filename}>"


class DeploymentLog(Base):
    """Logs de deployments."""
    __tablename__ = "deployment_logs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey("projects.id"))
    
    status = Column(String)  # pending, deploying, success, failed
    platform = Column(String)  # vercel, railway, render
    url = Column(String, nullable=True)
    error = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<DeploymentLog {self.platform}>"
