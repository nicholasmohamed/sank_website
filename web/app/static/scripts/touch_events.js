/*
* Touch Events
*/
// Result of touch event moves slide to the left or right
function xResult(increment) {
    console.log(increment);
    plusSlides(increment);
}

function yResult(increment) {
    console.log(increment);
    plusMerch(increment);

    var index = getActiveImageIndex("merch");
    index++;
    resetTimeout(4000, index);
}

// Simple click
document.addEventListener('click', function(){xResult(0);}, false);

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
};

function handleTouchStart(evt) {
  xDown = evt.touches[0].clientX;
  yDown = evt.touches[0].clientY;
};

function handleTouchEnd(evt) {
  handleEnd(evt.touches[0].clientX, evt.touches[0].clientY);
}

function handleDragEnd(evt) {
  handleEnd(evt.clientX, evt.clientY);
}

function handleEnd(xUp, yUp) {
  if ( !xDown ) { return; }
  var xDiff = xDown - xUp;
  var yDiff = yDown - yUp;
  // if large enough swipe, change image
  if ( xDiff > 20 ) xResult(1);
  else if ( xDiff < -20 ) xResult(-1);
  else if ( yDiff > 2 ) yResult(1);
  else if ( yDiff < -2 ) yResult(-1);
  xDown = null;
  yDown = null;
};