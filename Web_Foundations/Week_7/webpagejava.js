const productButtons = document.querySelectorAll(".product-button");

// Each button's data-target attribute holds the id of the placeholder it should update
productButtons.forEach((button) => {
    button.addEventListener("click", () => {
        const placeholder = document.getElementById(button.dataset.target);
        placeholder.textContent = `${button.textContent} go here!`;
    });
});

/* Add long-winded counting function for shopping cart for assignment 7) */

// Shopping cart: written out long-form, no functions/loops, to be refactored later
let cartCount = 0;
const cartCountDisplay = document.getElementById("cart-count");

const addLaserButton = document.getElementById("addLaserButton");
addLaserButton.addEventListener("click", () => {
    cartCount = cartCount + 1;
    cartCountDisplay.textContent = "Cart: " + cartCount + " items";
});

const addJewelryButton = document.getElementById("addJewelryButton");
addJewelryButton.addEventListener("click", () => {
    cartCount = cartCount + 1;
    cartCountDisplay.textContent = "Cart: " + cartCount + " items";
});

const addBobaButton = document.getElementById("addBobaButton");
addBobaButton.addEventListener("click", () => {
    cartCount = cartCount + 1;
    cartCountDisplay.textContent = "Cart: " + cartCount + " items";
});


/* This now handles all three buttons generically instead of one hardcoded pair, keeping the DRY principle intact.
Linking is done via the data-target attribute on each button matching the id of its placeholder box. */
