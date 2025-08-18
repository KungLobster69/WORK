const button = document.getElementById('myButton');
const text = document.getElementById('myText');
button.addEventListener('click', () => {
  text.style.color = 'red';
});

const [isClicked, setIsClicked] = useState(false);
return (
  <p style={{ color: isClicked ? 'red' : 'black' }}>
    Some Text
  </p>
);


