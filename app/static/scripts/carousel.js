class Carousel {
    constructor(htmlClass, containerClass, showMultiple = false, infinite = false, vertical = false) {
        this.htmlClass = htmlClass;
        this.containerClass = containerClass;
        this.showMultiple = showMultiple;
        this.infinite = infinite;
        this.xTranslation = 0;
        this.yTranslation = 0;
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

    // Sets the translation amount for sliding
    setTranslation() {
        var images = document.getElementsByClassName(this.htmlClass);

        if (images.length > 1){
            var image1Size = images[0].getBoundingClientRect();
            var image2Size = images[1].getBoundingClientRect();

            // get image1's center point
            var image1x = image1Size.left + image1Size.width/2;
            var image1y = image1Size.top + image1Size.height/2;

            // get image2's center point
            var image2x = image2Size.left + image2Size.width/2;
            var image2y = image2Size.top + image2Size.height/2;

            // calculate the distance using the Pythagorean Theorem (a^2 + b^2 = c^2)
            var distanceSquared = Math.pow(image1x - image2x, 2) + Math.pow(image1y - image2y, 2);
            var distance = Math.sqrt(distanceSquared);

            this.yTranslation = distance;
        } else {
            this.yTranslation = 0;
        }
    }

    // For vertical carousel, translate images
    translateVertical(translateUpwards, numImages, duration){
        var slideList = document.getElementById(this.containerClass);

        // Find translation amount if there is none
        if (this.yTranslation == 0) {
            this.setTranslation();
        }

        if (translateUpwards){
            slideList.style.transform += "translate(0px, " + (numImages * (-1) * this.yTranslation) + "px)";
            slideList.style.transitionDuration = duration + "s";
        } else {
            slideList.style.transform += "translate(0px, " + (numImages * this.yTranslation) + "px)";
            slideList.style.transitionDuration = duration + "s";
        }
    }

    // For vertical carousel, translate images
    translateHorizontal(translateRight, numImages, duration){
        var slideList = document.getElementById(this.containerClass);
        if (translateRight){
            slideList.style.transform += "translate(" + numImages * (-1) * this.yTranslation + "px,  0px)";
            slideList.style.transitionDuration = duration + "s";
        } else {
            slideList.style.transform += "translate(" + numImages * this.yTranslation + "px,  0px)";
            slideList.style.transitionDuration = duration + "s";
        }
    }

    // Transition the image with a slide in and out
    transitionImage (index, directionPositive, duration) {
        var images = document.getElementsByClassName(this.htmlClass);
        var direction = 100;

        // Determine if moving right or left
        if (directionPositive){
            direction = -100;
        }

        //Reset transform for active image
        images[this.activeIndex].style.transform = "translate(0%,  0%)";

        //Reset transform for all images
        for (var i = 0; i < images.length; i++) {
            images[i].style.marginLeft = "0%";
            images[i].style.transform = "translate(0%,  0%)";
        }

        // move current image off screen
        images[index].style.transform = "translate(" + direction + "%,  0%)";
        images[index].style.transitionDuration = duration + "s";

        //Set up activeImage
        var aIndex = this.activeIndex;

        //After first transition, set all image displays to none
        window.setTimeout( function(){
            for (var i = 0; i < images.length; i++) {
                images[i].style.display = "none";
            }

           images[aIndex].style.display = "block";
        }, duration * 1000); // timed to match animation-duration
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

    // set class of current image and inactive images. For styling
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

        // Set direction to and travel distance for active image
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
            this.transitionImage(index, direction, 0.5);
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
        dotLabels[this.activeIndex].style.color = "black";
    }
}