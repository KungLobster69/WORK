// 1. เลือก textarea และ span สำหรับแสดงผล
const messageInput = document.getElementById('message-input');
const charCountSpan = document.getElementById('char-count');

// (ไม่จำเป็น แต่ช่วยให้อ่านโค้ดง่ายขึ้น)
const maxLength = 20;

// 2. เพิ่ม Event Listener แบบ 'input' ให้กับ textarea
messageInput.addEventListener('input', () => {
    // 3.1 นับจำนวนอักขระปัจจุบัน
    const currentLength = messageInput.value.length;

    // 3.2 อัปเดตตัวเลขใน span
    charCountSpan.textContent = currentLength;

    // 4. (เพิ่มเติม) เปลี่ยนสีตัวอักษรเมื่อใกล้เต็ม
    if (currentLength > 10) {
        charCountSpan.style.color = 'red';
    } else {
        charCountSpan.style.color = 'black';
    }
});