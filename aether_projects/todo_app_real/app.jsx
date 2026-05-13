import React, { useState, useCallback, useMemo } from 'react';
import PropTypes from 'prop-types';

const TodoItem = ({ todo, onDelete }) => {
  const handleDelete = useCallback(() => {
    onDelete(todo.id);
  }, [todo.id, onDelete]);

  return (
    <li className="todo-item">
      <span>{todo.text}</span>
      <button 
        onClick={handleDelete}
        className="delete-btn"
        aria-label={Delete ${todo.text}}
      >
        Delete
      </button>
    </li>
  );
};

TodoItem.propTypes = {
  todo: PropTypes.shape({
    id: PropTypes.string.isRequired,
    text: PropTypes.string.isRequired
  }).isRequired,
  onDelete: PropTypes.func.isRequired
};

const TodoApp = () => {
  const [todos, setTodos] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [error, setError] = useState('');

  const generateId = useCallback(() => 
    ${Date.now()}-${Math.random().toString(36).substr(2, 9)}, 
  []);

  const handleInputChange = useCallback((e) => {
    setInputValue(e.target.value);
    if (error) setError('');
  }, [error]);

  const addTodo = useCallback((e) => {
    e.preventDefault();
    
    try {
      const trimmedValue = inputValue.trim();
      
      if (!trimmedValue) {
        setError('Please enter a todo item');
        return;
      }
      
      if (trimmedValue.length > 100) {
        setError('Todo item must be less than 100 characters');
        return;
      }
      
      const newTodo = {
        id: generateId(),
        text: trimmedValue
      };
      
      setTodos(prevTodos => [...prevTodos, newTodo]);
      setInputValue('');
      setError('');
    } catch (err) {
      setError('Failed to add todo. Please try again.');
      console.error('Error adding todo:', err);
    }
  }, [inputValue, generateId]);

  const deleteTodo = useCallback((id) => {
    try {
      setTodos(prevTodos => prevTodos.filter(todo => todo.id !== id));
    } catch (err) {
      setError('Failed to delete todo. Please try again.');
      console.error('Error deleting todo:', err);
    }
  }, []);

  const todoCount = useMemo(() => todos.length, [todos]);

  return (
    <div className="todo-app">
      <h1>Todo List</h1>
      
      <form onSubmit={addTodo} className="todo-form">
        <input
          type="text"
          value={inputValue}
          onChange={handleInputChange}
          placeholder="Enter a new todo"
          className="todo-input"
          maxLength="100"
          aria-label="New todo input"
        />
        <button 
          type="submit" 
          className="add-btn"
          disabled={!inputValue.trim()}
        >
          Add Todo
        </button>
      </form>
      
      {error && (
        <div className="error-message" role="alert">
          {error}
        </div>
      )}
      
      {todoCount > 0 && (
        <div className="todo-count">
          Total: {todoCount} {todoCount === 1 ? 'item' : 'items'}
        </div>
      )}
      
      {todos.length === 0 ? (
        <p className="empty-state">No todos yet. Add one above!</p>
      ) : (
        <ul className="todo-list">
          {todos.map(todo => (
            <TodoItem
              key={todo.id}
              todo={todo}
              onDelete={deleteTodo}
            />
          ))}
        </ul>
      )}
    </div>
  );
};

export default TodoApp;