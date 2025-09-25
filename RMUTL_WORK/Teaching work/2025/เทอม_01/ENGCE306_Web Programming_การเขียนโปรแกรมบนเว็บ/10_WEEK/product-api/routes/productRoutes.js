const express = require('express');
const router = express.Router();
const { 
  getProducts, 
  createProduct,
  getProductById,
  updateProduct,
  deleteProduct // เพิ่มเข้ามา
} = require('../controllers/productController');

router.route('/').get(getProducts).post(createProduct);
router.route('/:id')
    .get(getProductById)
    .put(updateProduct)
    .delete(deleteProduct); // เพิ่ม .delete()

module.exports = router;