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

    updateHeading(index);
}

function updateHeading(index) {
    var heading = document.getElementById("pageHeading")
    var headingText = "";
    switch (index){
        case 0:
            headingText = 'ABOUT';
            break;
        case 2:
            headingText = 'SHOP';
            break;
        default:
            headingText = '\u00A0';
    }
    heading.textContent = headingText;
}