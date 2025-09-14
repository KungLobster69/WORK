// รอให้ HTML โหลดเสร็จก่อนเริ่มทำงานกับ DOM
document.addEventListener('DOMContentLoaded', function() {

    // --- ข้อ 1.2: ระบบสลับธีม (Dark Mode Toggle) ---
    const themeToggleButton = document.getElementById('theme-toggle');
    
    themeToggleButton.addEventListener('click', function() {
        // สลับคลาส 'dark-mode' ที่ body
        document.body.classList.toggle('dark-mode');
    });

    // --- ข้อ 3.2: การสร้างเนื้อหาแบบไดนามิก (Dynamic Content Generation) ---
    const projects = [
        {
            name: 'เว็บไซต์ชมรมถ่ายภาพ',
            description: 'เว็บไซต์สำหรับแสดงผลงานภาพถ่ายของสมาชิกชมรม สร้างด้วย HTML และ CSS'
        },
        {
            name: 'โปรเจกต์เครื่องคิดเลขอย่างง่าย',
            description: 'เครื่องคิดเลขบนเว็บที่สามารถบวกลบคูณหารได้ พัฒนาด้วย JavaScript'
        },
        {
            name: 'เกมทายคำศัพท์ (ใหม่)',
            description: 'เกมทายคำศัพท์ภาษาอังกฤษอย่างง่ายที่สร้างขึ้นเพื่อฝึกฝนการใช้ DOM Manipulation'
        }
    ];

    const projectTableBody = document.querySelector('.project-table tbody');

    // วนลูปสร้างแถวในตารางจากข้อมูล projects
    projects.forEach(function(project) {
        // สร้าง element <tr> (table row)
        const row = document.createElement('tr');
        
        // เพิ่ม HTML เข้าไปใน row
        row.innerHTML = `
            <td>${project.name}</td>
            <td>${project.description}</td>
        `;
        
        // นำ row ที่สร้างเสร็จไปต่อท้ายใน tbody
        projectTableBody.appendChild(row);
    });

    // --- ข้อ 2: การตรวจสอบข้อมูลฟอร์ม (Form Validation) ---
    const contactForm = document.getElementById('contact-form');

    contactForm.addEventListener('submit', function(event) {
        // ป้องกันไม่ให้ฟอร์มส่งข้อมูลและรีเฟรชหน้า
        event.preventDefault();

        // ดึงค่าจาก input fields
        const nameInput = document.getElementById('name').value.trim();
        const emailInput = document.getElementById('email').value.trim();
        const messageInput = document.getElementById('message').value.trim();

        // ตรวจสอบว่ามีช่องไหนว่างหรือไม่
        if (nameInput === '' || emailInput === '' || messageInput === '') {
            alert('กรุณากรอกข้อมูลให้ครบทุกช่อง');
        } else {
            alert('ขอบคุณสำหรับการติดต่อ! เราจะตอบกลับโดยเร็วที่สุด');
            // ล้างข้อมูลในฟอร์ม
            contactForm.reset();
        }
    });

    // --- ข้อ 4: เพิ่มปฏิสัมพันธ์กับรูปภาพ (Interactive Profile Image) ---
    const profileImage = document.querySelector('.profile-img');
    const figcaption = document.querySelector('figcaption');
    const originalFigcaptionText = figcaption.textContent; // เก็บข้อความเดิมไว้

    // เมื่อเมาส์ชี้บนรูป
    profileImage.addEventListener('mouseover', function() {
        figcaption.textContent = 'เป้าหมายของผมคือการเป็นนักพัฒนาเว็บไซต์มืออาชีพ';
    });

    // เมื่อเมาส์ออกจากรูป
    profileImage.addEventListener('mouseout', function() {
        figcaption.textContent = originalFigcaptionText; // นำข้อความเดิมกลับมาแสดง
    });

});
