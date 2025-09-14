const fs = require('fs');
const path = require('path');

const content = 'This content was written by Node.js!';
// path.join จะสร้าง path ไปยังไฟล์ output.txt ในโฟลเดอร์ปัจจุบัน
const outputPath = path.join(__dirname, 'output.txt');
console.log(`กำลังจะเขียนไฟล์ไปที่: ${outputPath}`);

fs.writeFile(outputPath, content, 'utf8', (err) => {
  if (err) {
    console.error('เกิดข้อผิดพลาดในการเขียนไฟล์:', err);
    return;
  }
  console.log('บันทึกไฟล์เรียบร้อยแล้ว!');
});