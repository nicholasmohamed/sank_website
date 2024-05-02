var domain = '';

var cartItems = [];

function setDomain(new_domain){
    domain = new_domain;
}

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
    var itemMaxQuantity = item.querySelector("#itemMaxQuantity").textContent;
    var itemImage = item.querySelector("#itemImage").src;
    var itemSize =  item.querySelector("#itemSize").textContent;

    // Extract item size
    itemSize.replace("\n", "")
    itemSize = itemSize.trim();

    if (itemSize == "None") {
        itemSize = "";
    }

    // Extract item name
    itemName = itemName.split(/\u2013/g)[0].trim()

    var cartItem = {
        id: itemId,
        name: itemName,
        price: itemPrice,
        description: itemDescription,
        image: itemImage,
        size: itemSize,
        quantity: 1,
        maxQuantity: itemMaxQuantity,
    };

    // add to items array
    cartItems.push(cartItem);

    sessionStorage.setItem("cart", JSON.stringify(cartItems));

    return cartItem;
}

// remove item from cart
function removeFromCart(itemId) {
    // remove from items array
    for (let i = 0, len = cartItems.length; i < len; i++) {
        if (cartItems[i].id == itemId){
            cartItems.splice(i, 1)
            break;
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

// gets shipping data then sends to checkout
function proceedToCheckout(){
    var shipping = document.querySelector('input[name="deliveryOption"]:checked');

    console.log("Shipping value: " + shipping.value);

    checkoutData = {'cart': cartItems,
                    'shipping': shipping.value};

    submitCheckout(checkoutData)
}

function submitCheckout(checkoutData) {
    getStripePublishableKey()
    fetch(domain + '/create-checkout-session', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(checkoutData),
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