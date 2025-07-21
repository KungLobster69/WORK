// 1. เลือก elements ทั้งหมดที่ต้องใช้
const num1Input = document.getElementById('num1');
const num2Input = document.getElementById('num2');
const addBtn = document.getElementById('add-btn');
const subtractBtn = document.getElementById('subtract-btn');
const multiplyBtn = document.getElementById('multiply-btn');
const divideBtn = document.getElementById('divide-btn');
const resultSpan = document.getElementById('result');

// ฟังก์ชันสำหรับอ่านค่าจาก input และแปลงเป็นตัวเลข
function getNumbers() {
    const num1 = parseFloat(num1Input.value) || 0;
    const num2 = parseFloat(num2Input.value) || 0;
    return { num1, num2 };
}

// เพิ่ม Event Listener ให้แต่ละปุ่ม
addBtn.addEventListener('click', () => {
    const { num1, num2 } = getNumbers();
    resultSpan.textContent = num1 + num2;
});

subtractBtn.addEventListener('click', () => {
    const { num1, num2 } = getNumbers();
    resultSpan.textContent = num1 - num2;
});

multiplyBtn.addEventListener('click', () => {
    const { num1, num2 } = getNumbers();
    resultSpan.textContent = num1 * num2;
});

divideBtn.addEventListener('click', () => {
    const { num1, num2 } = getNumbers();
    // โจทย์ท้าทาย: ตรวจสอบการหารด้วย 0
    if (num2 === 0) {
        resultSpan.textContent = 'หารด้วย 0 ไม่ได้';
    } else {
        resultSpan.textContent = (num1 / num2).toFixed(2); // toFixed(2) เพื่อจำกัดทศนิยม
    }
});