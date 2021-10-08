var ASSETS = "";

function setAssetPath (path){
    ASSETS = path;
}

function clearCartList(){
    var cart = document.getElementById("cartList");

    // Remove all children from tag
    cart.innerHTML = '';
}

function openCart() {
    document.getElementById("rightSidebar").style.width = "700px";

    for (var i = 0; i < cartItems.length; i++){
        var item = cartItems[i];

        createCartItem(item);
    }
}

function closeCart() {
    document.getElementById("rightSidebar").style.width = "0";
    clearCartList();
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

    //Add image
    imageTag.src = item.image;

    //Add buttons
    var plusButton = document.createElement("input");
    plusButton.type = "image";
    plusButton.src = ASSETS + "math_plus.svg";

    //Add to containing div
    // Structure: cartItem < cartItemImage and cartInfo < cartName() and cartQuantity()
    nameContainer.appendChild(nameTag);
    nameContainer.appendChild(priceTag);
    quantityContainer.appendChild(descriptionTag);
    quantityContainer.appendChild(quantityTag);

    infoContainer.appendChild(nameContainer);
    infoContainer.appendChild(quantityContainer);
    itemContainer.appendChild(imageTag);
    itemContainer.appendChild(infoContainer);

    // Add to existing tag
    var cart = document.getElementById("cartList");
    cart.appendChild(itemContainer);
}