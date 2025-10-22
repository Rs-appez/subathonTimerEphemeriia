const data = document.getElementById("campaign-data").textContent;
let campaign = JSON.parse(data);

let test = document.getElementById("test");
function updateCampaignProgress() {
    test.textContent = campaign.current_amount;
    let previousGoal = 0;
    for (let i = 0; i < campaign.goals.length; i++) {
        let goal = campaign.goals[i];
        let goalDiv = document.getElementById("goal-progress-" + goal.id);
        let progress = Math.min(
            100,
            Math.max(
                0,
                ((campaign.current_amount - previousGoal) /
                    (goal.goal - previousGoal)) *
                100,
            ),
        );
        previousGoal = goal.goal;
        let progressBar = goalDiv.querySelector(".progress-bar-fill");

        // progressBar.style.transitionDelay = i * 0.5 + "s";
        progressBar.style.width = progress + "%";
    }
}

function initCampaign() {
    updateCampaignProgress();
}

// Websocket
let ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
let ws_url =
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

// connect();
initCampaign();

function fakeload() {
    campaign.current_amount += 3;
    updateCampaignProgress();
    if (
        campaign.current_amount > campaign.goals[campaign.goals.length - 1].goal
    ) {
        campaign.current_amount = -10;
    }
}

setInterval(fakeload, 2000);
