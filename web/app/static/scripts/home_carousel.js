/*
* Requires carousel.js
*/

homeCarousel = new Carousel("homeSlides", "slideList", false, false, false);
homeCarousel.initialize(1);

//set current slide
function currentSlide(index) {
  showSlides(index);
}

function showSlides(index) {
    homeCarousel.advanceCarousel(index);

    homeCarousel.updateDots(homeCarousel.activeIndex);

    updateHeading(homeCarousel.activeIndex);
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