const pedro = document.getElementById("pedro");
let pedroWidth, pedroHeight;

let width = window.innerWidth;
let height = window.innerHeight;

function refreshWidth() {
    width = window.innerWidth;
    height = window.innerHeight;
}

function activePedro() {
    console.log(pedroWidth, pedroHeight, width, height);
    refreshWidth();
    const x = Math.floor(Math.random() * (width - pedroWidth));
    const y = Math.floor(Math.random() * (height - pedroHeight));
    pedro.style.left = `${x}px`;
    pedro.style.top = `${y}px`;

    pedro.classList.add("active");
    setTimeout(() => {
        pedro.classList.remove("active");
    }, 1000);
}

pedro.addEventListener("load", () => {
    pedroWidth = pedro.naturalWidth;
    pedroHeight = pedro.naturalHeight;
    activePedro();
});
