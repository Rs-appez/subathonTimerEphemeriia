const data = document.getElementById("campaign-data").textContent;
let campaign = JSON.parse(data);

const progressBar = document.getElementById("progress-campaign");
const rightAmount = document.getElementById("goal-right");
function updateCampaignProgress() {
    if (progressBar) {
        progressBar.value =
            (campaign.current_amount / campaign.target_amount) * 100;
    }
}

function initCampaign() {
    updateCampaignProgress();
    var markerContainer = document.getElementById("markers-container");
    markerContainer.innerHTML = "";
    rightAmount.innerHTML = campaign.target_amount;
    for (var goal of campaign.goals) {
        var goalMarker = document.createElement("div");
        goalMarker.className = "goal-marker";
        var position = (goal.goal / campaign.target_amount) * 100;
        goalMarker.style.left = position + "%";
        markerContainer.appendChild(goalMarker);
    }
}

// Websocket
var ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
var ws_url =
    ws_scheme +
    "://" +
    window.location.host +
    "/ws/campaigns/" +
    campaign.id +
    "/";

function connect() {
    var ws = new WebSocket(ws_url);

    ws.onmessage = function(event) {
        var data_ws = JSON.parse(event.data);

        if (data_ws.type == "progress_update") {
            campaign.current_amount = data_ws.current_amount;
            updateCampaignProgress();
        } else if (data_ws.type == "campaign_update") {
            campaign = data_ws.campaign;
            initCampaign();
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
initCampaign();
