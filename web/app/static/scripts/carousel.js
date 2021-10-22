class Carousel {
    constructor(htmlClass, containerClass, showMultiple = false, infinite = false, vertical = false) {
        this.htmlClass = htmlClass;
        this.containerClass = containerClass;
        this.showMultiple = showMultiple;
        this.infinite = infinite;
        this.xTranslation = 1000;
        this.yTranslation = 1015;
        this.vertical = vertical;
        this.activeIndex = 0;
    }

    initialize(index){
        this.activeIndex = index;
        this.updateImageIndex();
   }

    advanceCarousel(index){
        var currentIndex = this.activeIndex;
        this.activeIndex = index;
        this.updateImageIndex();
        this.updateImageClasses();
        // travel to active index based on current index. If difference is 0, do nothing
        this.goToImage(currentIndex);
    }

    // For vertical carousel, translate images
    translateVertical(translateUpwards, numImages, duration){
        var slideList = document.getElementById(this.containerClass);
        if (translateUpwards){
            slideList.style.transform += "translate(0px, " + (numImages * (-1) * this.yTranslation) + "px)";
            slideList.style.transitionDuration = duration + "s";
        } else {
            slideList.style.transform += "translate(0px, " + (numImages * this.yTranslation) + "px)";
            slideList.style.transitionDuration = duration + "s";
        }
    }

    // For vertical carousel, translate images
    translateHorizontal(translateUpwards, numImages, duration){
        var slideList = document.getElementById(this.containerClass);
        if (translateUpwards){
            slideList.style.transform += "translate(" + numImages * (-1) * this.yTranslation + "px,  0px)";
            slideList.style.transitionDuration = duration + "s";
        } else {
            slideList.style.transform += "translate(" + numImages * this.yTranslation + "px,  0px)";
            slideList.style.transitionDuration = duration + "s";
        }
    }

    // Return image index
    updateImageIndex() {
        var images = document.getElementsByClassName(this.htmlClass);

        if (this.infinite){
            //If greater than max, start at zero. For looping
            if (this.activeIndex >= images.length) {
                this.activeIndex = 0;
            }
            if (this.activeIndex < 0) {
                this.activeIndex = images.length - 1
            }
        } else {
            // Do not loop and stop at bounds
            if (this.activeIndex >= images.length) {
                this.activeIndex = images.length - 1;
            }
            if (this.activeIndex < 0) {
                this.activeIndex = 0;
            }
        }
    }

    updateImageClasses() {
        var images = document.getElementsByClassName(this.htmlClass);

        // set previous and next image
        if (this.showMultiple){
           var previousImage;
           var nextImage;
           if (this.infinite){
                if (this.activeIndex <= 0){
                    previousImage = images[images.length-1];
                    previousImage.classList.add("inactiveImage");
                    previousImage.classList.remove("currentImage");
                } else if (this.activeIndex >= images.length){
                    nextImage = images[0];
                    nextImage.classList.remove("currentImage");
                    nextImage.classList.add("inactiveImage");
                }
           }
            if (this.activeIndex != 0){
                previousImage = images[this.activeIndex - 1];
                previousImage.classList.add("inactiveImage");
                previousImage.classList.remove("currentImage");
            }
            if (this.activeIndex != images.length - 1) {
                nextImage = images[this.activeIndex + 1];
                nextImage.classList.remove("currentImage");
                nextImage.classList.add("inactiveImage");
            }

            images[this.activeIndex].classList.remove("inactiveImage");
            images[this.activeIndex].classList.add("currentImage");
        } else {
            for (var i = 0; i < images.length; i++) {
                images[i].classList.remove("inactiveImage");
                images[i].classList.remove("currentImage");
            }

            images[this.activeIndex].classList.add("currentImage");
        }
    }

    // travel to active index based on current index. If difference is 0, do nothing
    goToImage(index){
        var images = document.getElementsByClassName(this.htmlClass);

        var travel = this.activeIndex - index;
        var direction = false;
        if (travel > 0){
            direction = true;
        } else if (travel == 0){
            return;
        } else {
            direction = false;
        }

         // If sliding through with many images
        if (this.showMultiple){
            // If the images are vertical, translate vertically
            if (this.vertical) {
                // if at the end of the list, go to the beginning. Else, translate vertically
                if (travel > 1){
                    this.translateVertical(direction, Math.abs(travel), 0);
                } else {
                    this.translateVertical(direction, Math.abs(travel), 1);
                }
            } else {
                // if at the end of the list, go to the beginning. Else, translate vertically
                if (travel > 1){
                    this.translateHorizontal(direction, Math.abs(travel), 0);
                } else {
                    this.translateHorizontal(direction, Math.abs(travel), 1);
                }
            }
        } else {
            for (var i = 0; i < images.length; i++) {
                images[i].style.display = "none";
            }

            images[this.activeIndex].style.display = "block";
        }
    }

    updateDots(index){
        var dots = document.getElementsByClassName("dotIcon");
        var dotLabels = document.getElementsByClassName("dotText");

        //set all dots to inactive
        for (var i = 0; i < dots.length; i++) {
          dots[i].className = dots[i].className.replace(" active", "");
          dotLabels[i].style.color ="transparent";
        }

        dots[this.activeIndex].className += " active";
        dotLabels[this.activeIndex].style.color = "white";
    }
}