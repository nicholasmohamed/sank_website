var domain = 'http://127.0.0.1:5000';

var cartItems = [];

//clear cart
function clearCart(){
    cartItems.length = 0
}

// add item to cart
function addToCart() {
    var addButton = document.getElementById("addButton");
    var removeButton = document.getElementById("removeButton");
    var itemId = document.getElementById("itemId").textContent;

    // add to items array
    cartItems.push({id: itemId, quantity: 1})
    // change button image
    addButton.style.display = "none"
    removeButton.style.display = "block"
}

// remove item from cart
function removeFromCart() {
    var addButton = document.getElementById("addButton");
    var removeButton = document.getElementById("removeButton");
    var itemId = document.getElementById("itemId").textContent;

    // remove from items array
    for (let i = 0, len = cartItems.length; i < len; i++) {
        if (cartItems[i].id == itemId){
            cartItems.splice(i, 1)
        }
    }
    // change button image
    addButton.style.display = "block"
    removeButton.style.display = "none"
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