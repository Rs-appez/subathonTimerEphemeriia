const pedro = document.getElementById("pedro");
const pedroAudio = new Audio(window.PEDRO_AUDIO_URL);
let pedroWidth, pedroHeight;

let width = window.innerWidth;
let height = window.innerHeight;

function refreshWidth() {
  width = window.innerWidth;
  height = window.innerHeight;
}

function activePedro() {
  refreshWidth();
  const x = Math.floor(Math.random() * (width - pedroWidth));
  const y = Math.floor(Math.random() * (height - pedroHeight));
  pedro.style.left = `${x}px`;
  pedro.style.top = `${y}px`;

  pedro.classList.add("active");
  pedroAudio.play().catch((error) => {
    console.error("Error playing audio:", error);
    pedro.classList.remove("active");
  });
}

pedro.addEventListener("load", () => {
  pedroWidth = pedro.naturalWidth;
  pedroHeight = pedro.naturalHeight;
});
pedroAudio.onended = () => {
  pedro.classList.remove("active");
};

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
