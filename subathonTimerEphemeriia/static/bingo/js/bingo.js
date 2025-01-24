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

function display_bingo() {
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

// Websocket
var ws_url = "ws://" + window.location.host + "/ws/bingo/";

function connect() {
    var ws = new WebSocket(ws_url);

    ws.onmessage = function(event) {
        var data_ws = JSON.parse(event.data);
        show_bingo = data_ws.show;
        user = data_ws.user;

        if (show_bingo) {
            display_bingo();
        } else {
            hide_bingo();
        }
    };

    ws.onclose = function(event) {
        console.log("Connection closed");
        connect();
    };

    ws.onerror = function(event) {
        console.log("Error");
        ws.close();
    };
}

connect();
