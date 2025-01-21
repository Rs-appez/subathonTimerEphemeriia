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
    if (show_bingo) {
        bingoElement.classList.add("visible");
    } else {
        bingoElement.classList.remove("visible");
    }
}

document.getElementById("showBingo").addEventListener("click", toggle_bingo);
