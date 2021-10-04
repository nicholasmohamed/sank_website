function clearCartList(){
    var cart = document.getElementById("cartList");

    // Remove all children from tag
    cart.innerHTML = '';
}

function openCart() {
    document.getElementById("rightSidebar").style.width = "200px";

    for (var i = 0; i < cartItems.length; i++){
        var item = cartItems[i];

        // Create a container div (for styling)
        var itemContainer = document.createElement("div");
        itemContainer.classList.add("<cartI></cartI>tem");

        // Create text elements
        var nameTag = document.createElement("h4");
        var priceTag = document.createElement("h4");
        var quantityTag = document.createElement("h4");

        // Add classes to elements
        nameTag.classList.add("cartItemName")
        priceTag.classList.add("cartItemPrice")
        quantityTag.classList.add("cartItemQuantity")

        // Add text
        var name = document.createTextNode(item.name);
        nameTag.appendChild(name);
        var price = document.createTextNode(item.price);
        priceTag.appendChild(price);

        // Add to containing div
        itemContainer.appendChild(nameTag);
        itemContainer.appendChild(priceTag);

        // Add to existing tag
        var cart = document.getElementById("cartList");
        cart.appendChild(itemContainer);
    }
}

function closeCart() {
    document.getElementById("rightSidebar").style.width = "0";
    clearCartList();
}