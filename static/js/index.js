function addOnClick(element) {
    let linkLocation = JSON.stringify(element.getAttribute("data-link-location")).replaceAll('"','');
    element.addEventListener('click', function(){
        window.location=linkLocation
    });
    console.log("added event listener for " + linkLocation)
};

document.addEventListener('DOMContentLoaded', function() {
    let indexRows = document.querySelectorAll(".index-row");
    indexRows.forEach((element) => addOnClick(element));
});