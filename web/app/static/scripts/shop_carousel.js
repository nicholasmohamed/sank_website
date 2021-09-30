/*
* Requires carousel.js
*/

var timeouts = []

// change slides
function plusMerch(n) {
    var activeIndex = getActiveImageIndex("merch");
    showMerch(activeIndex += n);
}

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
    index = showImages(index, "merch")

    // Update the UI
    updateUI(index);

    // reset change merch timer
    index++;
    resetTimeout(4000, index);
}

function updateUI(index){
    var merch = document.getElementsByClassName("merch");

    // Get ID of merch item
    var itemId = merch[index].querySelector("#itemId").textContent;

    var addButton = document.getElementById("addButton");
    var removeButton = document.getElementById("removeButton");

    // Check if itemId is in cart, if in cart then set button to remove.
    for (let i = 0, len = cartItems.length; i < len; i++) {
        if (cartItems[i].id == itemId){
            addButton.style.display = "none"
            removeButton.style.display = "block"
            return;
        }
    }
    addButton.style.display = "block"
    removeButton.style.display = "none"
}