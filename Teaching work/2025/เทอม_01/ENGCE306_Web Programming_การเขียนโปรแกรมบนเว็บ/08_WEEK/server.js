// const http = require('http');

// // สร้าง server และกำหนด callback function ที่จะทำงานเมื่อมี request
// const server = http.createServer((req, res) => {
//   res.writeHead(200, { 'Content-Type': 'text/plain' });
//   res.end('Hello World from my first server!');
// });

// const PORT = 3000;

// // ให้ server เริ่มทำงานและรอรับ request ที่ port 3000
// server.listen(PORT, () => {
//   console.log(`Server is running on http://localhost:${PORT}`);
// });

const http = require('http');

const server = http.createServer((req, res) => {
    console.log(`Request for: ${req.url}`);

    if (req.url === '/') {
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end('<h1>Welcome to our homepage</h1>');
        return;
    }

    if (req.url === '/about') {
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end('<h1>This is our short history</h1>');
        return;
    }

    res.writeHead(404, { 'Content-Type': 'text/html' });
    res.end(`
        <h1>Oops! Page not found</h1>
        <p>We can't seem to find the page you are looking for</p>
        <a href="/">Back home</a>
    `);
});

const PORT = 5000;
server.listen(PORT, () => console.log(`Server is running on http://localhost:${PORT}`));