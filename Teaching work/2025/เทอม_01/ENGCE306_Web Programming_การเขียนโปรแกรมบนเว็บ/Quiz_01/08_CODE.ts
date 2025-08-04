interface Movable {
  speed: number;
  move(): void;
}

class Vehicle {
  constructor(public brand: string) {}

  move(): void {
    console.log("A vehicle is moving.");
  }
}

class Car extends Vehicle implements Movable {
  speed: number = 60;

  constructor(brand: string, public doors: number) {
    super(brand);
  }

  // Overriding the move method
  move(): void {
    console.log(`The ${this.brand} car is moving at ${this.speed} km/h.`);
  }
}