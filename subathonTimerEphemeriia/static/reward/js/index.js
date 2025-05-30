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

// Websocket
var ws_url = "ws://" + window.location.host + "/ws/reward/";

function connect() {
  var ws = new WebSocket(ws_url);

  ws.onmessage = function (event) {
    var data_ws = JSON.parse(event.data);
    reward_name = data_ws.name;
    if (reward_name) {
      switch (reward_name) {
        case "pedro":
          activePedro();
          break;
        default:
          console.log("Unknown name:", reward_name);
      }
    }
  };

  ws.onclose = function (event) {
    console.log("Connection closed");
    connect();
  };

  ws.onerror = function (event) {
    console.log("Error");
    ws.close();
  };
}

connect();
