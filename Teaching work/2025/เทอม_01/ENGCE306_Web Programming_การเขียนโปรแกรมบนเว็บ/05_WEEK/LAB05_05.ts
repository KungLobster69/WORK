interface IUser {
  readonly id: number;
  username: string;
}

class User implements IUser {
  readonly id: number;
  username: string;

  constructor(id: number, username: string) {
    this.id = id;
    this.username = username;
  }
}

class Admin extends User {
  constructor(id: number, username: string) {
    super(id, username);
  }

  banUser(user: User): void {
    console.log(`Administrator '${this.username}' has banned user '${user.username}'.`);
  }
}

const adminUser = new Admin(1, "SuperAdmin");
const normalUser = new User(101, "Troublemaker");

adminUser.banUser(normalUser);