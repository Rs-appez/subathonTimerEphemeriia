const data = document.currentScript.dataset;
var total_subs = data.total_subs;

function updateSub() {
    const subs = document.getElementById("subs");

    if (subs) {
        subs.innerHTML = total_subs;
    }
}

// Websocket
var ws_url = "wss://" + window.location.host + "/ws/ticks/";

function connect() {
    var ws = new WebSocket(ws_url);

    ws.onmessage = function(event) {
        var data_ws = JSON.parse(event.data);
        total_subs = data_ws.total_subscriptions;

        updateSub();
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
