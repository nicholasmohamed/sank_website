/*
* Requires carousel.js
*/

// change slides
function plusSlides(n) {
    var activeIndex = getActiveImageIndex("homeSlides");
    showSlides(activeIndex += n);
}

//set current slide
function currentSlide(index) {
  showSlides(index);
}

function showSlides(index) {
    index = showImages(index, "homeSlides");

    updateDots(index);
}