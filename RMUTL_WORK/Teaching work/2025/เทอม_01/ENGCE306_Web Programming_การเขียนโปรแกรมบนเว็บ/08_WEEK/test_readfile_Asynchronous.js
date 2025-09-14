const fs = require('fs');
const path = require('path');

// สร้างไฟล์ชื่อ 'hello.txt' ในโฟลเดอร์ 08_WEEK ของคุณ
const filePath = path.join(__dirname, 'hello.txt');
console.log(`กำลังพยายามอ่านไฟล์จาก: ${filePath}`);

fs.readFile(filePath, 'utf8', (err, data) => {
  if (err) {
    console.error('เกิดข้อผิดพลาดในการอ่านไฟล์:', err);
    return;
  }
  console.log('เนื้อหาในไฟล์:', data);
});

console.log('คำสั่งนี้จะแสดงผลออกมาก่อน!');