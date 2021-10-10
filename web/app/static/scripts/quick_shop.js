var domain = 'http://127.0.0.1:5000';

var cartItems = [];

//clear cart
function clearCart(){
    cartItems.length = 0
}

//load cart if data exists
function loadCart(){
    var items = JSON.parse(sessionStorage.getItem("cart"));

    if (items == null) {
        cartItems = [];
    } else {
        cartItems = items;
    }
}

// add item to cart
function addToCart(item) {
    // Get item information
    var itemId = item.querySelector("#itemId").textContent;
    var itemName = item.querySelector("#itemName").textContent;
    var itemPrice = item.querySelector("#itemPrice").textContent;
    var itemDescription = item.querySelector("#itemDescription").textContent;
    var itemImage = item.querySelector("#itemImage").src;

    var item = {
        id: itemId,
        name: itemName,
        price: itemPrice,
        description: itemDescription,
        image: itemImage,
        quantity: 1,
    };

    // add to items array
    cartItems.push(item);

    sessionStorage.setItem("cart", JSON.stringify(cartItems));

    return item;
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

    sessionStorage.setItem("cart", cartItems);
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