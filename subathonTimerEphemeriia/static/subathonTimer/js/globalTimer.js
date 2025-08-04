const data = document.currentScript.dataset;
var time = data.time;

function update() {
    console.log(time);
    const timeElement = document.getElementById("time");
    if (!timeElement) {
        return;
    }
    if (time !== "0") {
        remainingTime = new Date().getTime() / 1000 - time;
        timeElement.innerHTML = formatTime(remainingTime);
    } else {
        timeElement.innerHTML = "SOON !!!!!";
    }
}
setInterval(update, 1000);

function formatTime(seconds) {
    var hours = Math.floor(seconds / 3600);
    hours = hours < 10 ? "0" + hours : hours;
    var minutes = Math.floor((seconds % 3600) / 60);
    minutes = minutes < 10 ? "0" + minutes : minutes;
    var seconds = Math.floor(seconds % 60);
    seconds = seconds < 10 ? "0" + seconds : seconds;

    return `${hours}:${minutes}:${seconds}`;
}

// Websocket
var ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
var ws_url = ws_scheme + "://" + window.location.host + "/ws/global_timer/";

function connect() {
    var ws = new WebSocket(ws_url);

    ws.onmessage = function(event) {
        var data_ws = JSON.parse(event.data);
        time = data_ws.time;

        update();
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
