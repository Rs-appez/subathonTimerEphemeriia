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
var total_subscriptions = data.total_subscriptions;
var tip_goal_values = JSON.parse(data.tip_goal_values);
var sub_goal_values = JSON.parse(data.sub_goals_values);
var remainingTime = end_timer - new Date().getTime() / 1000;

var skip_tip_animation = false;
var skip_sub_animation = false;


// Tip goal

function triggerAnimationTip() {
    const imageElements = document.querySelectorAll('.tip_image_to_move');

    // Remove the animation class to reset the animation
    imageElements.forEach(image => {
        image.classList.remove('moving-image');
        // Force reflow to restart the animation
        void image.offsetWidth;
        // Add the animation class to trigger the animation
        image.classList.add('moving-image');
    });
}

function removeFirstImageTip() {
    const imageElements = document.querySelectorAll('.tip_image_to_move');
    if (imageElements.length > 0) {
        imageElements[0].remove();
    }
}

function updateTipGoal() {
    triggerAnimationTip();
    setTimeout(removeFirstImageTip, 1999);
}

function checkTipGoal() {

    if (total_tips >= tip_goal_values[0] && !skip_tip_animation) {
        skip_tip_animation = true;
        tip_goal_values.shift();
        updateTipGoal();
        setTimeout(function () {
            skip_tip_animation = false;
            checkTipGoal();
        }, 2001);
    }

}

// Subs Goal

function triggerAnimationSub() {
    const imageElements = document.querySelectorAll('.sub_image_to_move');

    // Remove the animation class to reset the animation
    imageElements.forEach(image => {
        image.classList.remove('moving-image');
        // Force reflow to restart the animation
        void image.offsetWidth;
        // Add the animation class to trigger the animation
        image.classList.add('moving-image');
    });
}

function removeFirstImageSub() {
    const imageElements = document.querySelectorAll('.sub_image_to_move');
    if (imageElements.length > 0) {
        imageElements[0].remove();
    }
}

function updateSubGoal() {
    triggerAnimationSub();
    setTimeout(removeFirstImageSub, 1999);
}

function checkSubGoal() {
    if (total_subscriptions >= sub_goal_values[0] && !skip_sub_animation) {
        skip_sub_animation = true;
        sub_goal_values.shift();
        updateSubGoal();
        setTimeout(function () {
            skip_sub_animation = false;
            checkSubGoal();
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
        checkSubGoal();
        // updateTipProgress();

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