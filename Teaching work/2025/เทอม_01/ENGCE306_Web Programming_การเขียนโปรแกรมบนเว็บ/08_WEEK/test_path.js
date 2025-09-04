const path = require('path');

// สมมติว่าไฟล์นี้ทำงานอยู่ในโฟลเดอร์:
// C:\...\ENGCE306_Web Programming_การเขียนโปรแกรมบนเว็บ\08_WEEK
// ตัวแปร __dirname จะเก็บ path เต็มของโฟลเดอร์นี้โดยอัตโนมัติ
console.log('Path ปัจจุบัน (__dirname):', __dirname);

// เราใช้ path.join เพื่อสร้าง path ไปยังไฟล์อย่างถูกต้อง ไม่ว่าจะเป็น OS อะไรก็ตาม
const filePath = path.join(__dirname, 'files', 'data.txt');
console.log('Path ที่สร้างขึ้น:', filePath);

console.log('ชื่อไฟล์ (basename):', path.basename(filePath));
console.log('ชื่อไดเรกทอรี (dirname):', path.dirname(filePath));
console.log('นามสกุลไฟล์ (extname):', path.extname(filePath));