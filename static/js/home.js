let cookie = document.cookie

console.log("cookie: ", cookie)

if (cookie == "home-anim-viewed=true") {
    let fadeElements = document.getElementsByClassName("fadein")
    console.log(fadeElements)
    console.log(fadeElements.length)
    for (let i = 0; i < 8; i++) {
        elem = fadeElements.item(0)
        console.log(elem)
        elem.classList.remove("fadein")
        elem.classList.add("nofade")
    }
}

document.cookie = "home-anim-viewed=true;"
console.log("updated cookie")