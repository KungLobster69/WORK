const mongoose = require('mongoose'); // นำเข้า Mongoose

// สร้างฟังก์ชันแบบ async/await เพื่อจัดการกับการเชื่อมต่อ
const connectDB = async () => {
  try {
    // พยายามเชื่อมต่อไปยัง URI ที่อยู่ใน .env
    const conn = await mongoose.connect(process.env.MONGO_URI);
    // ถ้าสำเร็จ, แสดง log บอก host ที่เชื่อมต่อ
    console.log(`MongoDB Connected: ${conn.connection.host}`);
  } catch (error) {
    // ถ้าล้มเหลว, แสดง error และสั่งให้โปรแกรมหยุดทำงาน
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
};
module.exports = connectDB; // Export ฟังก์ชันนี้ไปใช้ที่อื่น