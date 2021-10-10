/* All buttons associated with the UI and cart functionality */

var ASSETS = "";

function setAssetPath (path){
    ASSETS = path;
}

// Add item to cart and change buttons
function quickAddItem(){
    var addButton = document.getElementById("addButton");
    var removeButton = document.getElementById("removeButton");

    //get item from merch list
    var index = getActiveImageIndex("merch");
    var merch = document.getElementsByClassName("merch");

    var item = addToCart(merch[index]);

    // Update cart listing (UI)
    addToCartList(item);

    //Update cart total
    updateCartTotal();

    // Set checkout button
    setCheckoutButton();

    // change button image
    addButton.style.display = "none";
    removeButton.style.display = "block";
}

// Remove item from cart and change buttons
function quickRemoveItem(){
    var addButton = document.getElementById("addButton");
    var removeButton = document.getElementById("removeButton");

    //get item from merch list
    var index = getActiveImageIndex("merch");
    var merch = document.getElementsByClassName("merch");

    removeFromCart(merch[index]);

    // Update cart listing (UI)
    regenerateCartList();

    // Update total
    updateCartTotal();

    // Set checkout button
    setCheckoutButton();

    // change button image
    addButton.style.display = "block"
    removeButton.style.display = "none"

    // Update cart number
    //updateCartNumber(-1);
}

function addToCartList(item) {
    createCartItem(item);
}

// TODO find way to remove specific item from cart list without regenerating
function regenerateCartList() {
    clearCartList();

    for (var i = 0; i < cartItems.length; i++){
        var item = cartItems[i];

        createCartItem(item);
    }
}

function clearCartList(){
    var cart = document.getElementById("cartList");

    // Remove all children from tag
    cart.innerHTML = '';
}

//  Update cart number in nav bar
function updateCartNumber(increment){
    var cartListText = document.getElementById("cartListText");
    var cartItemNumber = parseInt(cartListText.textContent);

    cartItemNumber += increment;
    cartListText.innerHTML = cartItemNumber;
}

function openCart() {
    document.getElementById("rightSidebar").style.width = "700px";
    var cart = document.getElementById("cartList");

    cart.style.display = "block";
}

function closeCart() {
    document.getElementById("rightSidebar").style.width = "0";
    var cart = document.getElementById("cartList");

    cart.style.display = "none";
}

function createCartItem(item) {
    // Create a container div (for styling)
    var itemContainer = document.createElement("div");
    itemContainer.classList.add("cartItem");
    // Create a container for item descriptors
    var infoContainer = document.createElement("div");
    infoContainer.classList.add("cartInfo");
    // Create div for name and price
    var nameContainer = document.createElement("div");
    nameContainer.classList.add("cartName");
    // Create div for description and quantity
    var descriptionContainer = document.createElement("div");
    descriptionContainer.classList.add("cartDescription");
    // Create div for quantity buttons
    var quantityContainer = document.createElement("div");
    quantityContainer.classList.add("cartQuantity");

    // Create text elements
    var imageTag = document.createElement("img");
    var nameTag = document.createElement("h4");
    var priceTag = document.createElement("h4");
    var quantityTag = document.createElement("h4");
    var descriptionTag = document.createElement("h5");

    // Add classes to elements
    imageTag.classList.add("cartItemImage");
    nameTag.classList.add("cartItemName");
    priceTag.classList.add("cartItemPrice");
    quantityTag.classList.add("cartItemQuantity");
    descriptionTag.classList.add("cartItemDescription");

    // Add text
    var name = document.createTextNode(item.name);
    nameTag.appendChild(name);
    var price = document.createTextNode(item.price);
    priceTag.appendChild(price);
    var description = document.createTextNode(item.description);
    descriptionTag.appendChild(description);

    var quantity = document.createTextNode(item.quantity);
    quantityTag.appendChild(quantity);
    quantityTag.id = item.name + "-" + item.id;


    //Add image
    imageTag.src = item.image;

    //Add buttons for quantity
    var minusButton = document.createElement("input");
    minusButton.type = "image";
    minusButton.src = ASSETS + "quantity_minus.svg";
    minusButton.onclick = function() {updateQuantityNumber(quantityTag.id, item.id, -1);};

    var plusButton = document.createElement("input");
    plusButton.type = "image";
    plusButton.src = ASSETS + "quantity_plus.svg";
    plusButton.onclick = function() {updateQuantityNumber(quantityTag.id, item.id, 1);};

    // Add to containing div
    // Structure: cartItem < cartItemImage and cartInfo < cartName()
    // and (cartDescription < cartItemDescription and cartquantity())
    nameContainer.appendChild(nameTag);
    nameContainer.appendChild(priceTag);
    descriptionContainer.appendChild(descriptionTag);

    quantityContainer.appendChild(minusButton);
    quantityContainer.appendChild(quantityTag);
    quantityContainer.appendChild(plusButton);
    descriptionContainer.appendChild(quantityContainer);

    infoContainer.appendChild(nameContainer);
    infoContainer.appendChild(descriptionContainer);
    itemContainer.appendChild(imageTag);
    itemContainer.appendChild(infoContainer);

    // Add to existing tag
    var cart = document.getElementById("cartList");
    cart.appendChild(itemContainer);
}

// Updated quantity number UI and cart
function updateQuantityNumber(id, cartId, increment) {
    var quantity = document.getElementById(id);
    if (quantity.textContent == "1"){
        if (increment == -1){
            return;
        }
    }
    if (quantity.textContent == "9"){
        if (increment == 1){
            return;
        }
    }

    // Update UI
   quantity.textContent = parseInt(quantity.textContent) + increment;

   // Update cart
   for (var i = 0; i < cartItems.length; i++){
        var item = cartItems[i];

        if (item.id == cartId) {
            item.quantity = quantity.textContent;
            updateCartTotal();
            return;
        }
    }

    console.log("Error: cartId not found.");
}

// Update cart total
function updateCartTotal() {
    var total = 0;

    // calculate total by all items in cart
    for (var i = 0; i < cartItems.length; i++){
        var item = cartItems[i];

        total += parseFloat(item.price.substring(1)) * item.quantity;
    }

    var totalText = document.getElementById("cartTotal");
    totalText.textContent = "$" + total;
}

// Disables checkout button if no items in cart
function setCheckoutButton(){
    var checkout = document.getElementById("checkoutButton");

    if (cartItems.length == 0){
        checkout.disabled = "disabled";
    } else {
        checkout.disabled = "";
    }
}