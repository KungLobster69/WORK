// const express = require('express');
// const dotenv = require('dotenv');
// const connectDB = require('./config/db');

// dotenv.config(); // สั่งให้ dotenv อ่านไฟล์ .env
// connectDB(); // เรียกใช้ฟังก์ชันเชื่อมต่อฐานข้อมูล

// const app = express(); // สร้าง Express app
// const PORT = process.env.PORT || 5000;

// // สร้าง Route พื้นฐานสำหรับทดสอบ
// app.get('/', (req, res) => res.send('API is running...'));

// // สั่งให้ Server เริ่มทำงาน
// app.listen(PORT, () => console.log(`Server running on port ${PORT}`));

const express = require('express');
const dotenv = require('dotenv');
const connectDB = require('./config/db');
const productRoutes = require('./routes/productRoutes'); // <--- 1. นำเข้าไฟล์ routes

dotenv.config();
connectDB();

const app = express();
const PORT = process.env.PORT || 5000;

app.use(express.json()); // <--- 2. เพิ่ม Middleware เพื่อให้ server อ่าน JSON ได้

app.get('/', (req, res) => res.send('API is running...'));

// <--- 3. ติดตั้ง routes ของเรา
app.use('/api/products', productRoutes); 

app.listen(PORT, () => console.log(`Server running on port ${PORT}`));