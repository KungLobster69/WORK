// 1. เลือก elements
const taskForm = document.getElementById('task-form');
const taskInput = document.getElementById('task-input');
const taskList = document.getElementById('task-list');

// 2. Logic การเพิ่มงาน
taskForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const taskText = taskInput.value.trim();
    if (taskText !== "") {
        addTask(taskText);
        taskInput.value = "";
        taskInput.focus();
    }
});

// 3. ฟังก์ชันสร้างและเพิ่ม Task
function addTask(text) {
    const li = document.createElement('li');
    li.textContent = text;

    const deleteBtn = document.createElement('button');
    deleteBtn.textContent = 'ลบ';
    deleteBtn.className = 'delete-btn';

    li.appendChild(deleteBtn);
    taskList.appendChild(li);
}

// 4. Logic การลบงาน (Event Delegation)
taskList.addEventListener('click', (event) => {
    if (event.target.classList.contains('delete-btn')) {
        const liToDelete = event.target.parentElement;
        liToDelete.remove();
    }
});