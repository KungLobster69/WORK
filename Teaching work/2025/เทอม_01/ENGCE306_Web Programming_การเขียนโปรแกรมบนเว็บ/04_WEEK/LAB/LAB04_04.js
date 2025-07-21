const openBtn = document.getElementById('open-modal-btn');
const closeBtn = document.getElementById('close-modal-btn');
const modalContainer = document.getElementById('modal-container');

openBtn.addEventListener('click', () => {
    modalContainer.classList.add('show');
});

closeBtn.addEventListener('click', () => {
    modalContainer.classList.remove('show');
});