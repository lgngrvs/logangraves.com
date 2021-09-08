function menuChange() {
    var top = document.getElementById("hamburger-top");
    var mid = document.getElementById("hamburger-mid");
    var bottom = document.getElementById("hamburger-bottom");
    if (top.classList.contains("is-active")) {
        top.classList.remove("is-active")
        mid.classList.remove("is-active")
        bottom.classList.remove("is-active")
    } else {
        top.classList.add("is-active")
        mid.classList.add("is-active")
        bottom.classList.add("is-active")
    }
}