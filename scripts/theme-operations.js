function menuChange() {
    // Each of the three hamburger menu bars has a different animation when they get the class "is-active."
    // for loops just go through and assign or remove the appropriate classes

    var top = document.getElementById("hamburger-top"),
        mid = document.getElementById("hamburger-mid"), 
        bottom = document.getElementById("hamburger-bottom"),
        nav = document.getElementById("nav")
    var all = [top, mid, bottom, nav]

    if (top.classList.contains("is-active")) {
        for (i of all) {
            i.classList.replace("is-active", "is-inactive");
        }
    } else if (top.classList.contains("is-inactive")) {
        for (i of all) {
            i.classList.replace("is-inactive", "is-active");
        }
    } else {
        console.log("This message should never appear")
    }
}