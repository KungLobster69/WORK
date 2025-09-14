function toggleText() {
    // ดึง element ที่มี id="messageText"
    let textElement = document.getElementById("messageText");

    // ตรวจสอบข้อความปัจจุบันแล้วสลับ
    if (textElement.innerHTML === "สวัสดี!") {
        textElement.innerHTML = "ลาก่อน!";
    } else {
        textElement.innerHTML = "สวัสดี!";
    }
}