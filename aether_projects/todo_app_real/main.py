from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional
from datetime import datetime
from uuid import uuid4
import uvicorn
from enum import Enum

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Priority = Priority.MEDIUM
    
    @validator('title')
    def title_must_not_be_empty(cls, v):
        if not v or v.isspace():
            raise ValueError('Title cannot be empty or whitespace')
        return v.strip()

class Todo(BaseModel):
    id: str
    title: str
    description: Optional[str]
    priority: Priority
    completed: bool = False
    created_at: datetime
    updated_at: datetime

class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Optional[Priority] = None
    completed: Optional[bool] = None
    
    @validator('title')
    def title_must_not_be_empty(cls, v):
        if v is not None and (not v or v.isspace()):
            raise ValueError('Title cannot be empty or whitespace')
        return v.strip() if v else v

app = FastAPI(
    title="TODO API",
    version="1.0.0",
    description="Simple TODO application with CRUD functionality"
)

todos: Dict[str, Todo] = {}

@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "TODO API", "version": "1.0.0"}

@app.get("/todos", response_model=List[Todo], status_code=status.HTTP_200_OK)
async def get_todos(
    completed: Optional[bool] = None,
    priority: Optional[Priority] = None,
    limit: int = Field(100, ge=1, le=1000),
    offset: int = Field(0, ge=0)
):
    filtered_todos = list(todos.values())
    
    if completed is not None:
        filtered_todos = [t for t in filtered_todos if t.completed == completed]
    
    if priority is not None:
        filtered_todos = [t for t in filtered_todos if t.priority == priority]
    
    filtered_todos.sort(key=lambda x: x.created_at, reverse=True)
    
    return filtered_todos[offset:offset + limit]

@app.get("/todos/{todo_id}", response_model=Todo, status_code=status.HTTP_200_OK)
async def get_todo(todo_id: str):
    if todo_id not in todos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    return todos[todo_id]

@app.post("/todos", response_model=Todo, status_code=status.HTTP_201_CREATED)
async def create_todo(todo_data: TodoCreate):
    try:
        todo_id = str(uuid4())
        current_time = datetime.utcnow()
        
        todo = Todo(
            id=todo_id,
            title=todo_data.title,
            description=todo_data.description,
            priority=todo_data.priority,
            completed=False,
            created_at=current_time,
            updated_at=current_time
        )
        
        todos[todo_id] = todo
        return todo
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create todo"
        )

@app.put("/todos/{todo_id}", response_model=Todo, status_code=status.HTTP_200_OK)
async def update_todo(todo_id: str, todo_update: TodoUpdate):
    if todo_id not in todos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    
    try:
        existing_todo = todos[todo_id]
        update_data = todo_update.dict(exclude_unset=True)
        
        if update_data:
            for field, value in update_data.items():
                setattr(existing_todo, field, value)
            existing_todo.updated_at = datetime.utcnow()
            
        return existing_todo
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update todo"
        )

@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: str):
    if todo_id not in todos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    
    try:
        del todos[todo_id]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete todo"
        )

@app.delete("/todos", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_todos():
    try:
        todos.clear()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete all todos"
        )

@app.patch("/todos/{todo_id}/complete", response_model=Todo, status_code=status.HTTP_200_OK)
async def complete_todo(todo_id: str):
    if todo_id not in todos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    
    try:
        todos[todo_id].completed = True
        todos[todo_id].updated_at = datetime.utcnow()
        return todos[todo_id]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to complete todo"
        )

@app.get("/todos/stats/summary", status_code=status.HTTP_200_OK)
async def get_stats():
    total = len(todos)
    completed = sum(1 for t in todos.values() if t.completed)
    pending = total - completed
    
    priority_count = {
        Priority.LOW: sum(1 for t in todos.values() if t.priority == Priority.LOW),
        Priority.MEDIUM: sum(1 for t in todos.values() if t.priority == Priority.MEDIUM),
        Priority.HIGH: sum(1 for t in todos.values() if t.priority == Priority.HIGH)
    }
    
    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "completion_rate": round((completed / total * 100), 2) if total > 0 else 0,
        "priority_distribution": priority_count
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)