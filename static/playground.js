window.onload = function() {
    var element = document.getElementById("scroll-logo-basic");
    setTimeout(createCopy(element), 5000)
    console.log("test")
};

function createCopy(e) {
    let elementCopy = e.cloneNode(true);
    e.classList.add("follow-class");
    e.after(elementCopy);

}

/*var copy = element.cloneNode(true);
var destination = document.getElementById('destination');
node.cloneNode(true);
destination.appendChild(copy);*/
