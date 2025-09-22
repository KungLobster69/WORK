// server.js
const express = require('express');
const app = express();
const port = 3000;

// Middleware ที่จำเป็นสำหรับอ่าน JSON body
app.use(express.json());

// ข้อมูลจำลองของเรา (In-memory database)
let books = [
  { id: 1, title: 'Book 1', author: 'Author A' },
  { id: 2, title: 'Book 2', author: 'Author B' },
  { id: 3, title: 'Book 3', author: 'Author C' },
];

// Route ต้อนรับ
app.get('/', (req, res) => {
    res.send('Welcome to the Books API!');
});

// --- เราจะเพิ่มโค้ด CRUD Endpoints ของเราตรงนี้ ---

// GET all books (จากสไลด์ 35)
app.get('/books', (req, res) => {
  res.status(200).json(books);
});

// GET a single book by id (โค้ดที่เพิ่มในสไลด์ 37)
app.get('/books/:id', (req, res) => {
  const bookId = parseInt(req.params.id);
  const book = books.find(b => b.id === bookId);

  if (!book) {
    return res.status(404).json({ message: 'Book not found' });
  }
  
  res.status(200).json(book);
});

// CREATE a new book
app.post('/books', (req, res) => {
  const { title, author } = req.body;

  if (!title || !author) {
    return res.status(400).json({ message: 'Title and author are required' });
  }

  const newBook = {
    id: books.length + 1, // Simple ID generation
    title: title,
    author: author
  };

  books.push(newBook);
  res.status(201).json(newBook);
});

// UPDATE a book
app.put('/books/:id', (req, res) => {
  const bookId = parseInt(req.params.id);
  const book = books.find(b => b.id === bookId);

  if (!book) {
    return res.status(404).json({ message: 'Book not found' });
  }

  const { title, author } = req.body;
  if (!title || !author) {
    return res.status(400).json({ message: 'Title and author are required' });
  }

  book.title = title;
  book.author = author;

  res.status(200).json(book);
});

// DELETE a book
app.delete('/books/:id', (req, res) => {
  const bookId = parseInt(req.params.id);
  const bookIndex = books.findIndex(b => b.id === bookId);

  if (bookIndex === -1) {
    return res.status(404).json({ message: 'Book not found' });
  }

  books.splice(bookIndex, 1);
  res.sendStatus(204);
});

// สั่งให้ Server เริ่มทำงาน
app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});