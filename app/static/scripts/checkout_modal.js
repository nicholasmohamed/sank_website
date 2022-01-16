// Opens delivery modal window on checkoutClicked
function checkoutClicked(){
    // Get the modal window for checkout
    var modal = document.getElementById("checkoutModal");

    modal.style.display = "flex";

    //Set initial modal text
    var pickupButton = document.getElementById("pickupButton");
    pickupButton.checked = true;

    var deliveryMtlText = document.getElementById("deliveryMtlText");
    var deliveryCanText = document.getElementById("deliveryCanText");
    deliveryMtlText.style.display = "none";
    deliveryCanText.style.display = "none";

    // Set on click function for radio buttons
    var radioButtonGroup = document.getElementById("deliveryOptionsGroup");
    radioButtonGroup.addEventListener("click", onRadioButtonGroupClick);
    radioButtonGroup.addEventListener("touchend", onRadioButtonGroupClick);
}

// Closes open shipping modal
function closeShippingModal() {
    var modal = document.getElementById("checkoutModal");
    modal.style.display = "none";
}

// Changes modal text of radio button click
function onRadioButtonGroupClick(){
    var pickupButton = document.getElementById("pickupButton");
    var deliveryMtlButton = document.getElementById("deliveryMtlButton");
    var deliveryCanButton = document.getElementById("deliveryCanButton");

    var pickupText = document.getElementById("pickupText");
    var deliveryMtlText = document.getElementById("deliveryMtlText");
    var deliveryCanText = document.getElementById("deliveryCanText");

    // Based on radio button checked, change the text of the modal
    if (pickupButton.checked == true){
        pickupText.style.display = "block";
        deliveryMtlText.style.display = "none";
        deliveryCanText.style.display = "none";
    } else if (deliveryMtlButton.checked == true){
        pickupText.style.display = "none";
        deliveryMtlText.style.display = "block";
        deliveryCanText.style.display = "none";
    } else {
        pickupText.style.display = "none";
        deliveryMtlText.style.display = "none";
        deliveryCanText.style.display = "block";
    }
}