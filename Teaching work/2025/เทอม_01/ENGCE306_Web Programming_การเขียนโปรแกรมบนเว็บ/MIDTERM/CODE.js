function createGreeter(greeting) {
  return function(name) {
    console.log(`${greeting}, ${name}!`);
  };
}

const helloGreeter = createGreeter('Hello');
const welcomeGreeter = createGreeter('Welcome');

helloGreeter('Alice');
welcomeGreeter('Bob');

const employees = [
  { name: 'Alex', title: 'Senior', salary: 90000, isActive: true },
  { name: 'Beth', title: 'Junior', salary: 55000, isActive: true },
  { name: 'Chris', title: 'Senior', salary: 105000, isActive: false },
  { name: 'Dana', title: 'Senior', salary: 120000, isActive: true },
];
