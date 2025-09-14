"use strict";
function greet(user) {
    return `Hello, ${user.name}!`;
}
// IDE จะขีดเส้นใต้สีแดงที่ age ทันที
// เพราะใน interface User ไม่มี property ชื่อ age
greet({ name: 'John', age: 30 });
// Error: Property 'age' does not exist on type 'User'.
