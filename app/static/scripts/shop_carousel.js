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
        var soldOut = merch[i].querySelector("#soldText");
        var size = merch[i].querySelector("#itemSizeButtons");
        var itemDescriptions = merch[i].querySelector("#visibleDescriptions")

        if (i == shopCarousel.activeIndex){
            name.style.visibility = "visible";
            price.style.visibility = "visible";
            if (soldOut != null){
                soldOut.style.visibility = "visible";
            }
            itemDescriptions.style.visibility = "visible";
        } else {
            name.style.visibility = "hidden";
            price.style.visibility = "hidden";
            if (size != null) {
                 size.style.visibility = "hidden";
            }
            if (soldOut != null){
                soldOut.style.visibility = "hidden";
            }
            itemDescriptions.style.visibility = "hidden";
        }
    }
}

