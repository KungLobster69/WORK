// solution.ts

// 1. ใช้ Enum เพื่อกำหนดสถานะสินค้า
enum ProductStatus {
    Available,      // 0
    OutOfStock,     // 1
    Discontinued    // 2
}

// 2. กำหนดชนิดข้อมูลให้ชัดเจน
const productStatus: ProductStatus = ProductStatus.Available;
const productData: [number, string, number] = [101, "Gaming Mouse", 1499.99]; // Tuple
let productNotes: unknown = "This is a best-selling item."; // ใช้ unknown เพื่อความปลอดภัย

// 3. กำหนดชนิดข้อมูลให้ฟังก์ชัน
function displayProduct(data: [number, string, number]): void {
    console.log(`Product ID: ${data[0]}, Name: ${data[1]}, Price: ${data[2]}`);
}

function logNotes(notes: unknown): void {
    // ต้องตรวจสอบชนิดข้อมูลก่อนใช้งาน
    if (typeof notes === 'string') {
        console.log(`Notes: ${notes.toUpperCase()}`);
    }
}

// 4. ตรวจสอบและใช้งานข้อมูลอย่างปลอดภัย
if (productStatus === ProductStatus.Available) {
    displayProduct(productData);
    logNotes(productNotes);
}