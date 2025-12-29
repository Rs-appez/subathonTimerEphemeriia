const data = document.currentScript.dataset;
let total_tips = data.total_tips;
let last_goal = data.last_goal;

function updateTipProgress() {
    const tipProgress = document.getElementById("progress-tip");
    const tipLeft = document.getElementById("tip-left");
    const tipRight = document.getElementById("tip-right");

    if (tipProgress && tipLeft && tipRight) {
        next_goal = last_goal;

        tipProgress.value = (total_tips / next_goal) * 100;
        tipLeft.innerText = total_tips + " €";
        // tipRight.innerHTML = next_goal;
    }
}

const evtSource = new EventSource("/timer/events/");
evtSource.onmessage = function(event) {
    const data_ws = JSON.parse(event.data);
    total_tips = data_ws.total_tips;
    total_subscriptions = data_ws.total_subscriptions;

    updateTipProgress();
};

updateTipProgress();
