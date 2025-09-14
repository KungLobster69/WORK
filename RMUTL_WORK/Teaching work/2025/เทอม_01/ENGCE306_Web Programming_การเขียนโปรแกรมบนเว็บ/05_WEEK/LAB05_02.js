// starter-code.js

// Product Status: 0 = Available, 1 = Out of Stock, 2 = Discontinued
let productStatus = 0;

// Product Data: [ID, Name, Price]
let productData = [101, "Gaming Mouse", 1499.99];

// Data from an external source, could be anything
let productNotes = "This is a best-selling item.";

// A function to display product info
function displayProduct(data) {
    console.log(`Product ID: ${data[0]}, Name: ${data[1]}, Price: ${data[2]}`);
}

// A function to log notes
function logNotes(notes) {
    console.log(`Notes: ${notes}`);
}

// Check status and display
if (productStatus === 0) {
    displayProduct(productData);
    logNotes(productNotes);
}