// Update the timer every second
function update() {
    const timeElement = document.getElementById('time');
    if (timeElement) {
        remainingTime = end_timer - new Date().getTime() / 1000;
        if (remainingTime <= 0) {
            timeElement.innerHTML = 'FINI !!!!!';
            return;
        }
        timeElement.innerHTML = formatTime(remainingTime);
    }
}
setInterval(update, 1000);

function formatTime(seconds) {
    var hours = Math.floor(seconds / 3600);
    var minutes = Math.floor((seconds % 3600) / 60);
    minutes = minutes < 10 ? '0' + minutes : minutes;
    var seconds = Math.floor(seconds % 60);
    seconds = seconds < 10 ? '0' + seconds : seconds;

    return `${hours}:${minutes}:${seconds}`;
}

const data = document.currentScript.dataset;
var end_timer = data.time_left;
var total_tips = data.total_tips;
var total_subscriptions = 0;
var tip_goal_values = JSON.parse(data.tip_goal_values);
var remainingTime = end_timer - new Date().getTime() / 1000;

var skip_animation = false;


function triggerAnimation() {
    const imageElements = document.querySelectorAll('.image_to_move');

    // Remove the animation class to reset the animation
    imageElements.forEach(image => {
        image.classList.remove('moving-image');
        // Force reflow to restart the animation
        void image.offsetWidth;
        // Add the animation class to trigger the animation
        image.classList.add('moving-image');
    });
}

function removeFirstImage() {
    const imageElements = document.querySelectorAll('.image_to_move');
    if (imageElements.length > 0) {
        imageElements[0].remove();
    }
}

function updateTipGoal() {
    triggerAnimation();
    setTimeout(removeFirstImage, 1999);
}

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

function checkTipGoal() {

    if (total_tips >= tip_goal_values[0] && !skip_animation) {
        skip_animation = true;
        tip_goal_values.shift();
        updateTipGoal();
        setTimeout(function () {
            skip_animation = false;
            checkTipGoal();
        }, 2001);
    }

}

// Websocket
var ws_url = 'wss://' + window.location.host + '/ws/ticks/';

function connect() {
    var ws = new WebSocket(ws_url);

    ws.onmessage = function (event) {
        var data_ws = JSON.parse(event.data);
        end_timer = data_ws.time_end;
        total_tips = data_ws.total_tips;
        total_subscriptions = data_ws.total_subscriptions;

        update();
        checkTipGoal();
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