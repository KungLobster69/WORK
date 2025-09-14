// พิมพ์บอกว่าสคริปต์นี้เริ่มทำงานแล้ว
console.log("📜 Long Script: START");

// จำลองการทำงานที่ใช้เวลานานมากๆ
const delay = Date.now() + 2000; // ทำงานค้างไว้ 2 วินาที
while (Date.now() < delay) {}

// พิมพ์บอกว่าทำงานเสร็จแล้ว
console.log("✅ Long Script: END");