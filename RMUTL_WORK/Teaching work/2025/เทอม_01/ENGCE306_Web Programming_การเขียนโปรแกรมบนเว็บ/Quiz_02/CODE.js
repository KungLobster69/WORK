// App.tsx (Component แม่)
import UserCard from './UserCard';

function App() {
  const userA = {
    name: 'Somsri',
    role: 'Admin',
    isActive: true
  };
  
  return (
    <div>
      <h1>User List</h1>
      <UserCard user={userA} />
      <UserCard user={{ name: 'Sompong', role: 'Editor', isActive: false }} />
    </div>
  );
}

// UserCard.tsx (Component ลูก)
function UserCard(props) {
  const { name, role, isActive } = props.user;
  
  return (
    <div style={{ border: '1px solid black', margin: '10px' }}>
      <p>Name: {name}</p>
      <p>Role: {role}</p>
      <p>Status: {isActive ? 'Online' : 'Offline'}</p>
    </div>
  );
}