const DATA = document.getElementById("tracker-data").textContent;
let tracker = JSON.parse(DATA);

function updateProgress() {
    console.log(tracker);
    let progressBar = document.getElementById("progress-bar-fill");
    let progress = Math.min(
        100,
        (tracker.current_level / tracker.target_level) * 100,
    );
    progressBar.style.width = progress + "%";

    let levelAmount = document.getElementById("current-level").querySelector("p");
    levelAmount.textContent = `Lv ${tracker.current_level}`;
}

// Websocket
let ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
let ws_url =
    ws_scheme +
    "://" +
    window.location.host +
    "/ws/levelTrackers/" +
    tracker.id +
    "/";

function connect() {
    var ws = new WebSocket(ws_url);

    ws.onmessage = function(event) {
        var data_ws = JSON.parse(event.data);
        console.log("data_ws : ", data_ws);

        if (data_ws.type == "level_update") {
            tracker.current_level = data_ws.level.current_level;
            tracker.target_level = data_ws.level.target_level;

            updateProgress();
        }

        ws.onclose = function(event) {
            console.log("Connection closed");
            connect();
        };

        ws.onerror = function(event) {
            console.log("Error");
            ws.close();
        };
    };
}

connect();
updateProgress();
