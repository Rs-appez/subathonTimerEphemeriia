const data = document.currentScript.dataset;

let show_bingo = data.show_bingo === "True";
let bingoElement = document.getElementsByClassName("bingo-show")[0];

let bingo_items;

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

function makeBingoBoard() {
    var board = document.getElementById("bingoCard");
    board.innerHTML = "";

    for (var i = 0; i < bingo_items.length; i++) {
        item = bingo_items[i];
        var cell = document.createElement("div");
        if (item["is_checked"]) {
            cell.className = "bingo-cell bingo-cell-checked";
        } else {
            cell.className = "bingo-cell";
        }
        cell.innerHTML = item["bingo_item"]["name"];
        board.appendChild(cell);
    }
}

// Websocket
var ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
var ws_url = ws_scheme + "://" + window.location.host + "/ws/bingo/";

function connect() {
    var ws = new WebSocket(ws_url);

    ws.onmessage = function(event) {
        var data_ws = JSON.parse(event.data);
        type = data_ws.type;

        if ("refresh" === type) {
            bingo_items = data_ws.bingo_items;
            makeBingoBoard();
        } else if ("display_bingo_widget" === type) {
            show_bingo = data_ws.show;
            if (show_bingo) {
                display_bingo();
            } else {
                hide_bingo();
            }
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
