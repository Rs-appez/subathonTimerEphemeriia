const data = document.currentScript.dataset;

let show_bingo = data.show_bingo === "True";
let display = show_bingo ? `block` : `none `;

document.getElementsByClassName("bingo-show")[0].style.display = display;
