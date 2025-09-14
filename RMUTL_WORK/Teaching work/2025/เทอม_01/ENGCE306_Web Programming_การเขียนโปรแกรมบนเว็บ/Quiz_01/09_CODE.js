const userData = [
  { name: 'Alice', age: 25, isActive: true },
  { name: 'Bob', age: 17, isActive: false },
  { name: 'Charlie', age: 32, isActive: true },
  { name: 'David', age: 15, isActive: true }
];

const activeUsers = [];
for (const user of userData) {
  if (user.age >= 18 && user.isActive) {
    activeUsers.push(user);
  }
}

const activeUserNames = activeUsers.map(user => user.name.toUpperCase());

console.log(activeUserNames);