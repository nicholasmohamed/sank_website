var timeouts = []

// change slides
function plusSlides(n) {
    var activeIndex = getActiveSlideIndex()
    showSlides(activeIndex += n);
}

//set current slide
function currentSlide(index) {
  showSlides(index);
}

// get currently visible slide on the carousel
function getActiveSlideIndex() {
    var slides = document.getElementsByClassName("homeSlides");

    //get active index
    for (var i = 0; i < slides.length; i++) {
        if (slides[i].style.display == "block"){
            return i;
        }
    }
    return 0;
}

// clear active timeouts
function clearActiveTimeouts(){
    for (var i = 0; i < timeouts.length; i++) {
      clearTimeout(timeouts[i]);
    }
}

function showSlides(index) {
    var slides = document.getElementsByClassName("homeSlides");
    var dots = document.getElementsByClassName("dot");
    if (index >= slides.length) {index = 0}
    if (index < 0) {index = slides.length - 1}

    //set display for all slides to none
    for (var i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
    }
    //set all dots to inactive
    for (var i = 0; i < dots.length; i++) {
      dots[i].className = dots[i].className.replace(" active", "");
    }

    slides[index].style.display = "block";
    dots[index].className += " active";

    // clear existing timeouts
    clearActiveTimeouts();

    // have slides cycle automatically
    index++;
    timeouts.push(setTimeout(showSlides, 4000, index)); // Change image every 4 seconds
}