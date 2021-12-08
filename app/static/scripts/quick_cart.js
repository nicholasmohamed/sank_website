/* All buttons associated with the UI and cart functionality */

var ASSETS = "";

function setAssetPath (path){
    ASSETS = path;
}

// Show buttons for sizing
function selectSize() {
    var index = shopCarousel.activeIndex;
    var merch = document.getElementsByClassName("merch");
    // Check if there are size options. If there are options, show buttons. Otherwise, add to cart
    var size = merch[index].querySelector("#itemSize").textContent;
    size.replace("\n", "")
    size = size.trim();

    if (size == "None") {
        quickAddItem();
    } else {
        var sizeButtons = merch[index].querySelector("#itemSizeButtons");
        var sizingFactor = -0.95;
        sizeButtons.style.visibility = "visible";
        sizeButtons.style.top = String(sizingFactor * merch[index].getBoundingClientRect().height) + "px";
    }
}

function sizeButtonPressed(size) {
    var index = shopCarousel.activeIndex;
    var merch = document.getElementsByClassName("merch");

    // Set size corresponding to button pressed
    var sizeText = merch[index].querySelector("#itemSize");
    sizeText.textContent = size;

    // Hide the size buttons
    var sizeButtons = merch[index].querySelector("#itemSizeButtons");
    sizeButtons.style.visibility = "hidden";

    quickAddItem();
}

// Add item to cart
function quickAddItem(){
    //get item from merch list
    var index = shopCarousel.activeIndex;
    var merch = document.getElementsByClassName("merch");

    //If there is no quantity, don't add to cart
    var itemQuantity = merch[index].querySelector("#itemMaxQuantity").textContent;
    if (itemQuantity <= 0) {
        return;
    }

    var item = addToCart(merch[index]);

    // Update cart listing (UI)
    addToCartList(item);

    //Update cart total
    updateCartTotal();

    // Set checkout button
    setCheckoutButton();

    // Add notification dot
    setCartNotification(false);

    // hide size buttons
    var sizeButtons = merch[index].querySelector("#itemSize");
    sizeButtons.style.visibility = "hidden";
}

// Remove item from cart
function quickRemoveItem(itemId){
    var merch = document.getElementsByClassName("merch");

    // Remove item by ID
    removeFromCart(itemId);

    // Update cart listing (UI)
    regenerateCartList();

    // Update total
    updateCartTotal();

    // Set checkout button
    setCheckoutButton();
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

// Opens delivery modal window on checkoutClicked
function checkoutClicked(){
    // Get the modal window for checkout
    var modal = document.getElementById("checkoutModal");

    modal.style.display = "block";

    //Set initial modal text
    var pickupButton = document.getElementById("pickupButton");
    pickupButton.checked = true;

    var deliveryMtlText = document.getElementById("deliveryMtlText");
    var deliveryCanText = document.getElementById("deliveryCanText");
    deliveryMtlText.style.display = "none";
    deliveryCanText.style.display = "none";

    // Set on click function for radio buttons
    var radioButtonGroup = document.getElementById("deliveryOptionsGroup");
    radioButtonGroup.addEventListener("click", onRadioButtonGroupClick);
    radioButtonGroup.addEventListener("touchend", onRadioButtonGroupClick);
}

// Closes open shipping modal
function closeShippingModal() {
    var modal = document.getElementById("checkoutModal");
    modal.style.display = "none";
}

// Changes modal text of radio button click
function onRadioButtonGroupClick(){
    var pickupButton = document.getElementById("pickupButton");
    var deliveryMtlButton = document.getElementById("deliveryMtlButton");
    var deliveryCanButton = document.getElementById("deliveryCanButton");

    var pickupText = document.getElementById("pickupText");
    var deliveryMtlText = document.getElementById("deliveryMtlText");
    var deliveryCanText = document.getElementById("deliveryCanText");

    // Based on radio button checked, change the text of the modal
    if (pickupButton.checked == true){
        pickupText.style.display = "block";
        deliveryMtlText.style.display = "none";
        deliveryCanText.style.display = "none";
    } else if (deliveryMtlButton.checked == true){
        pickupText.style.display = "none";
        deliveryMtlText.style.display = "block";
        deliveryCanText.style.display = "none";
    } else {
        pickupText.style.display = "none";
        deliveryMtlText.style.display = "none";
        deliveryCanText.style.display = "block";
    }
}

//  Add cart notification dot in nav bar
function setCartNotification(isVisible){
    var notificationDot = document.getElementById("newNotificationCircle");

    if (isVisible){
        notificationDot.style.visibility = "hidden";
    } else {
       notificationDot.style.visibility = "visible";
    }
}

function openCart(width) {
    document.getElementById("rightSidebar").style.width = width;
    var cart = document.getElementById("cartList");

    cart.style.display = "block";

    setCartNotification(true);
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
    var specificInfoContainer = document.createElement("div");
    specificInfoContainer.classList.add("cartSpecificInfo");
    // Create div for size and description
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
    var sizeTag = document.createElement("h5");

    // Add classes to elements
    imageTag.classList.add("cartItemImage");
    nameTag.classList.add("cartItemName");
    priceTag.classList.add("cartItemPrice");
    quantityTag.classList.add("cartItemQuantity");
    descriptionTag.classList.add("cartItemDescription");
    sizeTag.classList.add("cartItemSize");

    // Add text
    var name = document.createTextNode(item.name);
    nameTag.appendChild(name);
    var price = document.createTextNode(item.price);
    priceTag.appendChild(price);
    var description = document.createTextNode(item.description);
    descriptionTag.appendChild(description);
    var size = document.createTextNode(item.size);
    sizeTag.appendChild(size);

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
    descriptionContainer.appendChild(sizeTag);
    specificInfoContainer.appendChild(descriptionContainer);

    quantityContainer.appendChild(minusButton);
    quantityContainer.appendChild(quantityTag);
    quantityContainer.appendChild(plusButton);
    specificInfoContainer.appendChild(quantityContainer);

    infoContainer.appendChild(nameContainer);
    infoContainer.appendChild(specificInfoContainer);
    itemContainer.appendChild(imageTag);
    itemContainer.appendChild(infoContainer);

    // Add to existing tag
    var cart = document.getElementById("cartList");
    cart.appendChild(itemContainer);
}

// Updated quantity number UI and cart
function updateQuantityNumber(id, cartId, increment) {
    var quantity = document.getElementById(id);
    // If user subtracts and quantity is less than one, remove from cart
    if (quantity.textContent == "1"){
        if (increment == -1){
            quickRemoveItem(cartId);
            return;
        }
    }
    if (quantity.textContent == "9"){
        if (increment == 1){
            return;
        }
    }

   // Update cart
   for (var i = 0; i < cartItems.length; i++){
        var item = cartItems[i];

        if (item.id == cartId) {
            newQuantity = parseInt(quantity.textContent) + increment;

            // make sure amount in cart is less than max quantity
            if (newQuantity <= parseInt(item.maxQuantity)) {
                // Update UI
                quantity.textContent = newQuantity;

                item.quantity = quantity.textContent;
                updateCartTotal();
                return;
            }
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
    totalText.textContent = "$" + total.toFixed(2);
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

function addRadioButtonGroup(options){
    // Create a container for buttons div (for styling)
    var buttonContainer = document.createElement("div");
    buttonContainer.classList.add("radioButtonGroup");

    for (var i = 0; i < options.length; i++){
        var label = document.createElement("label");
        label.classList.add("buttonLabel");

        // Declare button and set type
        var button = document.createElement("input");
        button.type = "radio";
        button.name = "sizeOption";
        button.autocomplete = "off";
        button.value = options[i];

        button.classList.add("radioButton");

        var textContainer = document.createElement("div");
        textContainer.classList.add("buttonStyle");

        // Round first and last buttons
        if (i == 0){
            textContainer.classList.add("firstButton");
            label.classList.add("firstButton");
            button.checked = true;
        } else if (i == options.length - 1){
            textContainer.classList.add("lastButton");
            label.classList.add("lastButton");
        }

        // Set button text
        var textTag = document.createElement("h4");
        var text = document.createTextNode(options[i]);
        textTag.classList.add("buttonText");
        textTag.appendChild(text);
        textContainer.appendChild(textTag);

        // Append button to container
        label.appendChild(button);
        label.appendChild(textContainer);
        buttonContainer.appendChild(label);
    }

    return buttonContainer;
}