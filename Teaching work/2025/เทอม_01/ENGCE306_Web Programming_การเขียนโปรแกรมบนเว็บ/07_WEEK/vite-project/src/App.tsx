import React, { useState, useEffect } from 'react';
import './App.css';

// กำหนด Type สำหรับข้อมูล To-Do 1 ชิ้น
interface Todo {
  id: number;
  text: string;
  completed: boolean;
}

function App() {
  // State สำหรับเก็บรายการ To-Do ทั้งหมด
  const [todos, setTodos] = useState<Todo[]>([]);
  // State สำหรับเก็บข้อความที่ผู้ใช้กำลังพิมพ์ใน input
  const [newTodoText, setNewTodoText] = useState<string>('');

  // --- useEffect Hooks for Local Storage ---

  // โหลดข้อมูลจาก localStorage (ทำงานครั้งเดียว)
  useEffect(() => {
    const savedTodos = localStorage.getItem('todos');
    if (savedTodos) {
      setTodos(JSON.parse(savedTodos) as Todo[]);
    }
  }, []);

  // บันทึกข้อมูลลง localStorage (ทำงานทุกครั้งที่ todos เปลี่ยน)
  useEffect(() => {
    localStorage.setItem('todos', JSON.stringify(todos));
  }, [todos]);

  // --- Handler Functions ---

  const handleAddTodo = (e: React.FormEvent) => {
    e.preventDefault();
    if (newTodoText.trim() === '') return;

    const newTodo: Todo = {
      id: Date.now(),
      text: newTodoText,
      completed: false
    };

    setTodos(prevTodos => [...prevTodos, newTodo]);
    setNewTodoText('');
  };

  const handleDeleteTodo = (idToDelete: number) => {
    setTodos(prevTodos => prevTodos.filter(todo => todo.id !== idToDelete));
  };

  const handleToggleTodo = (idToToggle: number) => {
    setTodos(prevTodos =>
      prevTodos.map(todo =>
        todo.id === idToToggle
          ? { ...todo, completed: !todo.completed }
          : todo
      )
    );
  };

  // --- JSX ---

  return (
    <div className="container">
      <h1>To-Do List</h1>

      <form onSubmit={handleAddTodo}>
        <input
          type="text"
          value={newTodoText}
          onChange={e => setNewTodoText(e.target.value)}
          placeholder="What needs to be done?"
        />
        <button type="submit">Add Todo</button>
      </form>

      <ul>
        {todos.map(todo => (
          <li key={todo.id}>
            <input
              type="checkbox"
              checked={todo.completed}
              onChange={() => handleToggleTodo(todo.id)}
            />
            <span style={{ textDecoration: todo.completed ? 'line-through' : 'none' }}>
              {todo.text}
            </span>
            <button onClick={() => handleDeleteTodo(todo.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
