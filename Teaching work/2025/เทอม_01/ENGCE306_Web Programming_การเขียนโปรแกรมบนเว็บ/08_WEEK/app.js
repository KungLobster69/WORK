console.log("Hello, Node.js!");

// app.js
// นำเข้าฟังก์ชัน log จากไฟล์ logger.js
const log = require('./logger.js');

log("This is a message from app.js");
log("Another message.");

const utils = require('./utils.js');

console.log(utils.PI); // 3.14
console.log(utils.add(5, 3)); // 8