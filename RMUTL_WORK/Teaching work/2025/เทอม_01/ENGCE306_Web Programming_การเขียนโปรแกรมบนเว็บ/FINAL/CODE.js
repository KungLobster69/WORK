// 04
interface User {
  readonly userId: number;
  username: string;
  email: string;
  isActive: boolean;
  lastLogin?: Date; // Optional
}

const newUser = {
  userId: 'U001',
  username: 'testuser',
  email: 'test@example.com',
  isActive: 'true'
};

// 06
const http = require('http');
const server = http.createServer((req, res) => {
  if (req.url === '/') {
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end('<h1>Homepage</h1>');
  } else if (req.url === '/about') {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('About Us page');
  } else {
    res.writeHead(404, { 'Content-Type': 'text/html' });
    res.end('<h2>404 - Not Found</h2>');
  }
});
server.listen(8080);

// 07
// Route 1
app.get('/api/users', (req, res) => { /* ... */ });
// Route 2
app.post('/api/users', (req, res) => { /* ... */ });
// Route 3
app.get('/api/users/:userId', (req, res) => { /* ... */ });
// Route 4
app.delete('/api/users/:userId', (req, res) => { /* ... */ });
// Route 5
app.put('/api/users/:userId', (req, res) => { /* ... */ });

// 09
const productSchema = new mongoose.Schema({
  productName: { type: String, required: true, unique: true },
  price: { type: Number, required: true, default: 0 },
  tags: { type: [String] },
  onSale: { type: Boolean, default: false }
});


