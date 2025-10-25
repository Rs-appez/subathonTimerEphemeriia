const giftSVG =
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"><defs><style>.cls-1{fill:var(--gift-color-1);}.cls-2{fill:var(--gift-color-2);}</style></defs><g id="Calque_4" data-name="Calque 4"><path class="cls-1" d="M518.29,572.09,480.68,572l.26-220.54c12.56-.12,25.1-.19,37.62-.1Z"/><path class="cls-1" d="M533.68,325.44c262.93-7.62,505.1-133.53,359.67-257.84-141-120.51-361,94.63-383.83,232.28C507.18,314.06,519.3,325.84,533.68,325.44Zm161-172.85a77.25,77.25,0,1,1,77.14,77.33A77.22,77.22,0,0,1,694.71,152.59ZM635,248.48a38.31,38.31,0,1,1,38.27,38.35A38.32,38.32,0,0,1,635,248.48Zm-75.81-22.73A28.21,28.21,0,1,1,587.39,254,28.2,28.2,0,0,1,559.23,225.75Z"/><path class="cls-2" d="M902.26,406.25l-.17,145.34a21,21,0,0,1-21,20.92l-325.21-.39.26-220.3a2296.43,2296.43,0,0,1,325.46,30C893.07,383.68,902.28,394.68,902.26,406.25Z"/><path class="cls-2" d="M841.51,613.43l-.39,334.1a21,21,0,0,1-21,20.93l-264.71-.32.45-376,264.7.29A21,21,0,0,1,841.51,613.43Z"/><polygon class="cls-1" points="517.84 968.09 480.22 968.05 480.67 592.06 518.29 592.1 517.84 968.09"/><path class="cls-1" d="M465.91,325.36c14.35.44,26.5-11.32,24.19-25.49C467.6,162.15,248.15-53.5,106.84,66.67-38.91,190.64,203,317.11,465.91,325.36ZM398.17,257.6a22.65,22.65,0,1,1,22.6,22.65A22.64,22.64,0,0,1,398.17,257.6Zm-97.51-37.7a41.51,41.51,0,1,1,41.46,41.57A41.53,41.53,0,0,1,300.66,219.9ZM140.4,152a77.26,77.26,0,1,1,77.16,77.32A77.24,77.24,0,0,1,140.4,152Z"/><path class="cls-2" d="M178.35,591.7l264.7.3-.45,376-264.7-.31a21,21,0,0,1-20.92-21l.4-334.12A21,21,0,0,1,178.35,591.7Z"/><path class="cls-2" d="M117.85,381.13a2607.66,2607.66,0,0,1,325.49-29L443.08,572l-325.21-.39a20.94,20.94,0,0,1-20.93-21l.18-145.34C97.12,393.72,106.41,382.87,117.85,381.13Z"/></g></svg>';
const data = document.getElementById("campaign-data").textContent;

let campaign = JSON.parse(data);
const parser = new DOMParser();

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

        progressBar.style.width = progress + "%";
        if (progress >= 100) {
            validateGoal(goalDiv);
        }
    }
}

function initCampaign() {
    addGoalMarkers();
    updateCampaignProgress();
}

function addGoalMarkers() {
    for (let i = 0; i < campaign.goals.length; i++) {
        let goal = campaign.goals[i];
        let goalDiv = document.createElement("div");
        let goalIcon = document.createElement("div");
        goalDiv.className = "goal-marker";
        goalIcon.className = "goal-icon";

        goalIcon.innerHTML = giftSVG;
        goalDiv.appendChild(goalIcon);
        let linkedBar = document.getElementById("goal-progress-" + goal.id);
        linkedBar.appendChild(goalDiv);
    }
}

function validateGoal(goalDiv) {
    let markerDiv = goalDiv.querySelector(".goal-marker");
    if (markerDiv) {
        if (!markerDiv.classList.contains("validate-marker")) {
            markerDiv.classList.add("validate-marker");
            let iconCls1 = markerDiv.querySelectorAll(".cls-1");
            let iconCls2 = markerDiv.querySelectorAll(".cls-2");
            iconCls1.forEach((el) => {
                el.style.fill = "var(--gift-validate-color-1)";
            });
            iconCls2.forEach((el) => {
                el.style.fill = "var(--gift-validate-color-2)";
            });
        }
    }
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
    campaign.current_amount += 40;
    updateCampaignProgress();
    if (
        campaign.current_amount > campaign.goals[campaign.goals.length - 1].goal
    ) {
        campaign.current_amount = -10;
    }
}

setInterval(fakeload, 2000);
