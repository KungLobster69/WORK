function setupCounter() {
  let count = 0;
  const counterButton = document.getElementById('myButton');

  counterButton.addEventListener('click', function() {
    count++;
    counterButton.textContent = `Clicked ${count} times`;
  });
}

setupCounter();