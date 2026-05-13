import pytest
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4
from enum import Enum


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


@dataclass
class Todo:
    id: str
    title: str
    description: str = ""
    completed: bool = False
    priority: Priority = Priority.MEDIUM
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "priority": self.priority.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class TodoNotFoundError(Exception):
    pass


class InvalidTodoDataError(Exception):
    pass


class TodoApp:
    def __init__(self):
        self._todos: Dict[str, Todo] = {}

    def add_todo(self, title: str, description: str = "", priority: Priority = Priority.MEDIUM) -> Todo:
        if not title or not title.strip():
            raise InvalidTodoDataError("Title cannot be empty")
        
        if len(title) > 200:
            raise InvalidTodoDataError("Title cannot exceed 200 characters")
        
        if len(description) > 1000:
            raise InvalidTodoDataError("Description cannot exceed 1000 characters")
        
        todo = Todo(
            id=str(uuid4()),
            title=title.strip(),
            description=description.strip(),
            priority=priority
        )
        self._todos[todo.id] = todo
        return todo

    def delete_todo(self, todo_id: str) -> None:
        if todo_id not in self._todos:
            raise TodoNotFoundError(f"Todo with id {todo_id} not found")
        del self._todos[todo_id]

    def get_todo(self, todo_id: str) -> Todo:
        if todo_id not in self._todos:
            raise TodoNotFoundError(f"Todo with id {todo_id} not found")
        return self._todos[todo_id]

    def get_all_todos(self) -> List[Todo]:
        return list(self._todos.values())

    def update_todo(self, todo_id: str, **kwargs) -> Todo:
        if todo_id not in self._todos:
            raise TodoNotFoundError(f"Todo with id {todo_id} not found")
        
        todo = self._todos[todo_id]
        
        if "title" in kwargs:
            if not kwargs["title"] or not kwargs["title"].strip():
                raise InvalidTodoDataError("Title cannot be empty")
            if len(kwargs["title"]) > 200:
                raise InvalidTodoDataError("Title cannot exceed 200 characters")
            todo.title = kwargs["title"].strip()
        
        if "description" in kwargs:
            if len(kwargs["description"]) > 1000:
                raise InvalidTodoDataError("Description cannot exceed 1000 characters")
            todo.description = kwargs["description"].strip()
        
        if "completed" in kwargs:
            todo.completed = bool(kwargs["completed"])
        
        if "priority" in kwargs:
            todo.priority = kwargs["priority"]
        
        todo.updated_at = datetime.now()
        return todo

    def complete_todo(self, todo_id: str) -> Todo:
        return self.update_todo(todo_id, completed=True)

    def uncomplete_todo(self, todo_id: str) -> Todo:
        return self.update_todo(todo_id, completed=False)

    def clear_all(self) -> None:
        self._todos.clear()

    def get_todos_by_priority(self, priority: Priority) -> List[Todo]:
        return [todo for todo in self._todos.values() if todo.priority == priority]

    def get_completed_todos(self) -> List[Todo]:
        return [todo for todo in self._todos.values() if todo.completed]

    def get_pending_todos(self) -> List[Todo]:
        return [todo for todo in self._todos.values() if not todo.completed]

    def count_todos(self) -> Dict[str, int]:
        todos = list(self._todos.values())
        return {
            "total": len(todos),
            "completed": len([t for t in todos if t.completed]),
            "pending": len([t for t in todos if not t.completed])
        }


@pytest.fixture
def todo_app():
    return TodoApp()


@pytest.fixture
def sample_todo(todo_app):
    return todo_app.add_todo("Test Todo", "Test Description", Priority.HIGH)


class TestTodoApp:
    def test_add_todo_success(self, todo_app):
        todo = todo_app.add_todo("Buy groceries", "Milk, bread, eggs", Priority.HIGH)
        assert todo.title == "Buy groceries"
        assert todo.description == "Milk, bread, eggs"
        assert todo.priority == Priority.HIGH
        assert not todo.completed
        assert todo.id is not None

    def test_add_todo_with_minimal_data(self, todo_app):
        todo = todo_app.add_todo("Simple task")
        assert todo.title == "Simple task"
        assert todo.description == ""
        assert todo.priority == Priority.MEDIUM

    def test_add_todo_empty_title_raises_error(self, todo_app):
        with pytest.raises(InvalidTodoDataError, match="Title cannot be empty"):
            todo_app.add_todo("")
        
        with pytest.raises(InvalidTodoDataError, match="Title cannot be empty"):
            todo_app.add_todo("   ")

    def test_add_todo_title_too_long_raises_error(self, todo_app):
        long_title = "a" * 201
        with pytest.raises(InvalidTodoDataError, match="Title cannot exceed 200 characters"):
            todo_app.add_todo(long_title)

    def test_add_todo_description_too_long_raises_error(self, todo_app):
        long_description = "a" * 1001
        with pytest.raises(InvalidTodoDataError, match="Description cannot exceed 1000 characters"):
            todo_app.add_todo("Valid title", long_description)

    def test_add_todo_strips_whitespace(self, todo_app):
        todo = todo_app.add_todo("  Trimmed Title  ", "  Trimmed Description  ")
        assert todo.title == "Trimmed Title"
        assert todo.description == "Trimmed Description"

    def test_delete_todo_success(self, todo_app, sample_todo):
        todo_id = sample_todo.id
        todo_app.delete_todo(todo_id)
        with pytest.raises(TodoNotFoundError):
            todo_app.get_todo(todo_id)

    def test_delete_nonexistent_todo_raises_error(self, todo_app):
        with pytest.raises(TodoNotFoundError, match="Todo with id nonexistent not found"):
            todo_app.delete_todo("nonexistent")

    def test_get_todo_success(self, todo_app, sample_todo):
        retrieved_todo = todo_app.get_todo(sample_todo.id)
        assert retrieved_todo.id == sample_todo.id
        assert retrieved_todo.title == sample_todo.title

    def test_get_nonexistent_todo_raises_error(self, todo_app):
        with pytest.raises(TodoNotFoundError, match="Todo with id nonexistent not found"):
            todo_app.get_todo("nonexistent")

    def test_get_all_todos(self, todo_app):
        todo1 