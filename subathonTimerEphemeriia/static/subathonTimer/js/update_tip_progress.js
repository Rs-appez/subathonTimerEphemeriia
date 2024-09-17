const data = document.currentScript.dataset;
var total_tips = data.total_tips;

function updateTipProgress() {
    const tipProgress = document.getElementById('progress-tip');
    const tipLeft = document.getElementById('tip-left');
    const tipRight = document.getElementById('tip-right');

    if (tipProgress && tipLeft && tipRight) {
        next_goal = 1000;

        tipProgress.value = (total_tips / next_goal * 100); 
        tipLeft.innerHTML = total_tips;
        tipRight.innerHTML = next_goal;
    }

}

// Websocket
var ws_url = 'wss://' + window.location.host + '/ws/ticks/';

function connect() {
    var ws = new WebSocket(ws_url);

    ws.onmessage = function (event) {
        var data_ws = JSON.parse(event.data);
        total_tips = data_ws.total_tips;
        total_subscriptions = data_ws.total_subscriptions;

        updateTipProgress();

    }

    ws.onclose = function (event) {
        console.log('Connection closed');
        connect();

    }

    ws.onerror = function (event) {
        console.log('Error');
        ws.close();
    }
}

connect();
updateTipProgress();