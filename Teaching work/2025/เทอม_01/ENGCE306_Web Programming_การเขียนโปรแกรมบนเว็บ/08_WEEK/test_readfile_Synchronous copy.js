const fs = require('fs');
const path = require('path');

// สร้างไฟล์ชื่อ 'hello.txt' ในโฟลเดอร์ 08_WEEK ของคุณ
const filePath = path.join(__dirname, 'hello.txt');
console.log(`กำลังพยายามอ่านไฟล์จาก: ${filePath}`);

try {
  const data = fs.readFileSync(filePath, 'utf8');
  console.log('เนื้อหาในไฟล์:', data);
} catch (err) {
  console.error('เกิดข้อผิดพลาดในการอ่านไฟล์:', err);
}

console.log('คำสั่งนี้จะแสดงผลออกมาทีหลัง!');