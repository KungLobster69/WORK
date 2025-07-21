// 1. สร้าง Array ของสีที่ต้องการ
const colors = ["#FF5733", "#33FF57", "#3357FF", "green", "red", "rgba(133,122,200)"];

// 2. เลือกปุ่มและ body มาเก็บในตัวแปร
const btn = document.getElementById('color-btn');
const body = document.body;

// 3. สร้างฟังก์ชันสำหรับสุ่มตัวเลข Index จาก Array
function getRandomNumber() {
    return Math.floor(Math.random() * colors.length);
}

// 4. เพิ่ม Event Listener ให้กับปุ่ม
btn.addEventListener('click', () => {
    // 4.1 สุ่ม Index
    const randomIndex = getRandomNumber();
    // 4.2 เปลี่ยนสีพื้นหลังของ body
    body.style.backgroundColor = colors[randomIndex];
});