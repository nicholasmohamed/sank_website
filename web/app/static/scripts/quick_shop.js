var domain = 'http://127.0.0.1:5000';

var cartItems = [];

//clear cart
function clearCart(){
    cartItems.length = 0
}

// Add item to cart and change buttons
function quickAddItem(){
    var addButton = document.getElementById("addButton");
    var removeButton = document.getElementById("removeButton");

    //get item from merch list
    var index = getActiveImageIndex("merch");
    var merch = document.getElementsByClassName("merch");

    addToCart(merch[index]);

    // change button image
    addButton.style.display = "none"
    removeButton.style.display = "block"

    // Update cart number
    updateCartNumber(1);
}

// Remove item from cart and change buttons
function quickRemoveItem(){
    var addButton = document.getElementById("addButton");
    var removeButton = document.getElementById("removeButton");

    //get item from merch list
    var index = getActiveImageIndex("merch");
    var merch = document.getElementsByClassName("merch");

    removeFromCart(merch[index]);

    // change button image
    addButton.style.display = "block"
    removeButton.style.display = "none"

    // Update cart number
    updateCartNumber(-1);
}

//  Update cart number in nav bar
function updateCartNumber(increment){
    var cartListText = document.getElementById("cartListText");
    var cartItemNumber = parseInt(cartListText.textContent);

    cartItemNumber += increment;
    cartListText.innerHTML = cartItemNumber;
}

// add item to cart
function addToCart(item) {
    // Get item information
    var itemId = item.querySelector("#itemId").textContent;
    var itemName = item.querySelector("#itemName").textContent;
    var itemPrice = item.querySelector("#itemPrice").textContent;
    var itemImage = item.querySelector("#itemImage").src;

    // add to items array
    cartItems.push({id: itemId, name: itemName, price: itemPrice, image: itemImage, quantity: 1})
}

// remove item from cart
function removeFromCart(item) {
    //get itemId
    var itemId = item.querySelector("#itemId").textContent;

    // remove from items array
    for (let i = 0, len = cartItems.length; i < len; i++) {
        if (cartItems[i].id == itemId){
            cartItems.splice(i, 1)
        }
    }
}

function getStripePublishableKey() {
    fetch(domain + '/stripe-config')
        .then((result) => result.json())
        .then((data) => {
        // Initialize Stripe.js
        this.stripe = Stripe(data.publicKey);
    });
}

function submitCheckout() {
    getStripePublishableKey()
    fetch(domain + '/create-checkout-session', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(cartItems),
    })
        .then((result) => result.json())
        .then((data) => {
            console.log(data);
            // Redirect to Stripe Checkout
            return this.stripe.redirectToCheckout({ sessionId: data.sessionId });
    })
    .then((res) => {
      console.log(res);
    });
}