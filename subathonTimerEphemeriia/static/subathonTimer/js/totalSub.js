const data = document.currentScript.dataset;
let total_subs = data.total_subs;

function updateSub() {
    const subs = document.getElementById("subs");

    if (subs) {
        subs.innerHTML = total_subs;
    }
}

const evtSource = new EventSource("/timer/events/");
evtSource.onmessage = function(event) {
    const data_ws = JSON.parse(event.data);
    total_subs = data_ws.total_subscriptions;

    updateSub();
};
