window.onload = function() {
    let element = document.getElementById("scroll-logo-basic");
    for (var i = 1; i < 23; i++) {
        time = i * 430
        setTimeout(function() {
            createCopy(element);
            console.log("new element");
        }, time)
    }
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
