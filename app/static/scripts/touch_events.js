/*
* Touch Events
*/
// Result of touch event moves slide to the left or right
function xResult(increment) {
    console.log(increment);
    dotClick(homeCarousel.activeIndex + increment);
}

function yResult(increment) {
    console.log(increment);

    if (homeCarousel.activeIndex == 2){
        var merch = document.getElementsByClassName("merch");

        // If at the end of the carousels, do not move
        if (shopCarousel.activeIndex == 0 && increment < 0){
        } else if (shopCarousel.activeIndex == (merch.length - 1) && increment > 0) {
        } else {
            showMerch(shopCarousel.activeIndex + increment);
        }
    }
}

/*
var lastScrollTop = 0;
function setScroll(){
    // element should be replaced with the actual target element on which you have applied scroll, use window in case of no target element.
    window.addEventListener("scroll", scrollEvent, false);
}

function scrollEvent(){
    var increment = 0;
    var st = window.pageYOffset || document.documentElement.scrollTop; // Credits: "https://github.com/qeremy/so/blob/master/so.dom.js#L426"
    if (st > lastScrollTop){
      increment = -1;
    } else {
      increment = 1;
    }
    advanceMerch(increment);
    lastScrollTop = st <= 0 ? 0 : st; // For Mobile or negative scrolling
}*/

function xResultClick(increment) {
}

function yResultClick(increment) {
    advanceMerch(increment);
}

// Simple click
//document.addEventListener('click', function(){xResult(0);}, false);

// Click and drag (non-touch-screen)
document.addEventListener('dragstart', handleDragStart, false);
document.addEventListener('dragend', handleDragEnd, false);

// On mobile swipe action
document.addEventListener('touchstart', handleTouchStart, false);
document.addEventListener('touchmove', handleTouchEnd, false);

var xDown = null;
var yDown = null;

function handleDragStart(evt) {
  xDown = evt.clientX;
  yDown = evt.clientY;
}

function handleTouchStart(evt) {
  xDown = evt.touches[0].clientX;
  yDown = evt.touches[0].clientY;
}

function handleTouchEnd(evt) {
    if (getScreenOrientation() == "landscape-primary"){
        var xThreshold = 10;
        var yThreshold = 10;
    } else {
        var xThreshold = 20;
        var yThreshold = 20;
    }
    handleEnd(evt.touches[0].clientX, evt.touches[0].clientY, xThreshold, yThreshold);
}

function handleDragEnd(evt) {
    var xThreshold = 30;
    var yThreshold = 5;

    handleClickEnd(evt.clientX, evt.clientY, xThreshold, yThreshold);
}

// Handle what happens on click end
function handleClickEnd(xUp, yUp, xThreshold, yThreshold){
      // If there is no ending x
      if ( !xDown ) { return; }

      // Calculate difference (ending x minus starting x)
      var xDiff = xDown - xUp;
      var yDiff = yDown - yUp;
      // if large enough swipe, change image
      if ( xDiff > xThreshold ) xResultClick(1);
      else if ( xDiff < -xThreshold ) xResultClick(-1);
      else if ( yDiff > yThreshold ) yResultClick(1);
      else if ( yDiff < -yThreshold ) yResultClick(-1);
      xDown = null;
      yDown = null;
}

function handleEnd(xUp, yUp, xThreshold, yThreshold) {

  // If there is no ending x
  if ( !xDown ) { return; }

  // Calculate difference (ending x minus starting x)
  var xDiff = xDown - xUp;
  var yDiff = yDown - yUp;
  // if large enough swipe, change image
  if ( xDiff > xThreshold ) xResult(1);
  else if ( xDiff < -xThreshold ) xResult(-1);
  else if ( yDiff > yThreshold ) yResult(1);
  else if ( yDiff < -yThreshold ) yResult(-1);
  xDown = null;
  yDown = null;
}

// If using safari, detects portrait/landscape based off height and width
function getScreenOrientation(){
    try {
        return screen.orientation.type;
    } catch (e){
        if (window.innerHeight > window.innerWidth)
            return "portrait-primary";
        else
            return "landscape-primary";
    }
}