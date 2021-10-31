/*
* Requires carousel.js
*/

const TIMEOUT_DURATION = 35000;
var timeouts = []
var shopCarousel = new Carousel("merch", "merchList", true, true, true);
shopCarousel.initialize(0);

//set current slide
function currentMerch(index) {
  showMerch(index);
}

// clear active timeouts
function clearActiveMerchImageTimeouts(){
    for (var i = 0; i < timeouts.length; i++) {
      clearTimeout(timeouts[i]);
    }
}

// reset timeout
function resetTimeout(milliseconds, index){
    clearActiveMerchImageTimeouts();
    timeouts.push(setTimeout(showMerch, milliseconds, index));
}

function showMerch(index){
    shopCarousel.advanceCarousel(index);

    // Update the UI
    updateUI(shopCarousel.activeIndex);

    // reset change merch timer
    resetTimeout(TIMEOUT_DURATION, shopCarousel.activeIndex + 1);
}

function updateUI(index){
    var merch = document.getElementsByClassName("merch");

    // removing text for inactive images
    for (let i = 0, len = merch.length; i < len; i++) {
        var name = merch[i].querySelector("#itemName");
        var price = merch[i].querySelector("#itemPrice");

        if (i == shopCarousel.activeIndex){
            name.style.visibility = "visible";
            price.style.visibility = "visible";
        } else {
            name.style.visibility = "hidden";
            price.style.visibility = "hidden";
        }
    }

    // Get ID of merch item
    var itemId = merch[index].querySelector("#itemId").textContent;

    var addButton = document.getElementById("addButton");
    var removeButton = document.getElementById("removeButton");

    // Check if itemId is in cart, if in cart then set button to remove.
    for (let i = 0, len = cartItems.length; i < len; i++) {
        if (cartItems[i].id == itemId){
            addButton.style.display = "none";
            removeButton.style.display = "block";
            return;
        }
    }

    addButton.style.display = "block";
    removeButton.style.display = "none";
}

