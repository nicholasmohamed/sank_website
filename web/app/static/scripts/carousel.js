// change slides
function plusImages(n, htmlClass) {
    var activeIndex = getActiveImageIndex(htmlClass)
    showImages(activeIndex += n);
}

//set current slide
function currentImage(index, htmlClass) {
  showImages(index, htmlClass);
}

// get currently visible slide on the carousel
function getActiveImageIndex(htmlClass) {
    var images = document.getElementsByClassName(htmlClass);

    //get active index
    for (var i = 0; i < images.length; i++) {
        if (images[i].style.display == "block"){
            return i;
        }
    }
    return 0;
}

// Return image index
function showImages(index, htmlClass) {
    var images = document.getElementsByClassName(htmlClass);

    //If greater than max, start at zero. For looping
    if (index >= images.length) {index = 0}
    if (index < 0) {index = images.length - 1}

    //set display for all slides to none
    for (var i = 0; i < images.length; i++) {
      images[i].style.display = "none";
    }

    images[index].style.display = "block";

    return index;
}

function updateDots(index){
    var dots = document.getElementsByClassName("dotIcon");
    var dotLabels = document.getElementsByClassName("dotText");

    //set all dots to inactive
    for (var i = 0; i < dots.length; i++) {
      dots[i].className = dots[i].className.replace(" active", "");
      dotLabels[i].style.color ="transparent";
    }

    dots[index].className += " active";
    dotLabels[index].style.color = "white";
}