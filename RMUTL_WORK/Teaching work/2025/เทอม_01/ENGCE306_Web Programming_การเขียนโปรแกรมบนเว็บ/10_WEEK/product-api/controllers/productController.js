const Product = require('../models/productModel'); // นำเข้า Model

// ฟังก์ชันสำหรับดึงข้อมูลสินค้าทั้งหมด
const getProducts = async (req, res) => {
  // ใช้ Model.find({}) เพื่อค้นหา document ทั้งหมดใน Collection
  const products = await Product.find({});
  res.json(products); // ส่งข้อมูลกลับไปเป็น JSON
};

const createProduct = async (req, res) => {
  // ดึงข้อมูลจาก body ของ request
  const { name, price, quantity } = req.body;
  // สร้าง instance ใหม่ของ Product แต่ยังไม่บันทึกลง DB
  const product = new Product({ name, price, quantity });
  // สั่งบันทึกข้อมูลลง DB
  const createdProduct = await product.save();
  // ส่งข้อมูลสินค้าที่สร้างเสร็จกลับไป พร้อม status 201 (Created)
  res.status(201).json(createdProduct);
};

const getProductById = async (req, res) => {
    // ค้นหาสินค้าจาก Model ด้วย ID ที่ได้จาก req.params.id
    const product = await Product.findById(req.params.id);
    if (product) {
        res.json(product); // ถ้าเจอ ให้ส่งข้อมูลกลับไป
    } else {
        // ถ้าไม่เจอ ให้ส่ง status 404 (Not Found) พร้อมข้อความ
        res.status(404).json({ message: 'Product not found' });
    }
};

const updateProduct = async (req, res) => {
    const { name, price, quantity } = req.body;
    // ค้นหาสินค้าชิ้นที่จะแก้ไขก่อน
    const product = await Product.findById(req.params.id);
    if (product) {
        // อัปเดตค่า field ต่างๆ จากข้อมูลที่ส่งมาใน body
        product.name = name || product.name;
        product.price = price || product.price;
        product.quantity = quantity || product.quantity;
        // สั่งบันทึกข้อมูลที่อัปเดตแล้ว
        const updatedProduct = await product.save();
        res.json(updatedProduct);
    } else {
        res.status(404).json({ message: 'Product not found' });
    }
};

const deleteProduct = async (req, res) => {
    const product = await Product.findById(req.params.id);
    if (product) {
        // Mongoose v6+ ใช้ .deleteOne() บน document ที่เจอ
        await product.deleteOne();
        res.json({ message: 'Product removed' });
    } else {
        res.status(404).json({ message: 'Product not found' });
    }
};

module.exports = { getProducts, createProduct, getProductById, updateProduct, deleteProduct };