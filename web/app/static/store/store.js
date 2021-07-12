var domain = 'http://127.0.0.1:5000';

// add item to cart
function addToCart() {
    var cartButton = document.getElementById("cartButton");
    // change button value and text
    cartButton.setAttribute( "onclick", "javascript: removeFromCart();" );
    cartButton.innerHTML = "Remove From Cart";
}

// remove item from cart
function removeFromCart() {
    var cartButton = document.getElementById("cartButton");
    // change button value and text
    cartButton.setAttribute( "onclick", "javascript: addToCart();" );
    cartButton.innerHTML = "Add To Cart";
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
        body: JSON.stringify({ ids: merchIds }),
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