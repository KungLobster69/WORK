const mongoose = require('mongoose');

// 1. กำหนด Schema (โครงสร้าง)
const productSchema = mongoose.Schema({
  // field `name` ต้องเป็น String และต้องมีข้อมูลเสมอ
  name: { type: String, required: true },
  // field `price` ต้องเป็น Number, ต้องมี, และถ้าไม่ระบุให้เป็น 0
  price: { type: Number, required: true, default: 0 },
  quantity: { type: Number, required: true, default: 0 },
}, {
  // ตัวเลือกเสริม: ให้ Mongoose เพิ่ม field createdAt และ updatedAt อัตโนมัติ
  timestamps: true
});

// 2. สร้าง Model จาก Schema
// Mongoose จะสร้าง Collection ชื่อ 'products' (พหูพจน์) ใน DB ให้เอง
const Product = mongoose.model('Product', productSchema);
module.exports = Product; // Export Model ไปใช้