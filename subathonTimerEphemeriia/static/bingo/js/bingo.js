const data = document.currentScript.dataset;

let show_bingo = data.show_bingo === "True";
let bingoElement = document.getElementsByClassName("bingo-show")[0];

if (show_bingo) {
    bingoElement.classList.add("visible");
} else {
    bingoElement.classList.remove("visible");
}

function toggle_bingo() {
    show_bingo = !show_bingo;
    animate_bingo();
}

function show_bingo() {
    bingoElement.classList.add("visible");
    animate_bingo();
}

function hide_bingo() {
    bingoElement.classList.remove("visible");
    animate_bingo();
}

function animate_bingo() {
    if (show_bingo) {
        bingoElement.classList.add("visible");
    } else {
        bingoElement.classList.remove("visible");
    }
}

document.getElementById("showBingo").addEventListener("click", toggle_bingo);
