// Update the timer every second
function update() {
    const timeElement = document.getElementById("time");
    if (timeElement) {
        if (!timer_paused) {
            remainingTime = end_timer - new Date().getTime() / 1000;
        } else {
            remainingTime = end_timer - paused_time;
        }
        if (remainingTime <= 0) {
            timeElement.innerHTML = "FINI !!!!!";
            return;
        }
        timeElement.innerHTML = formatTime(remainingTime);
    }
}
setInterval(update, 1000);

function formatTime(seconds) {
    var hours = Math.floor(seconds / 3600);
    var minutes = Math.floor((seconds % 3600) / 60);
    minutes = minutes < 10 ? "0" + minutes : minutes;
    var seconds = Math.floor(seconds % 60);
    seconds = seconds < 10 ? "0" + seconds : seconds;

    return `${hours}:${minutes}:${seconds}`;
}

const data = document.currentScript.dataset;
var end_timer = data.time_left;
var total_tips = data.total_tips;
var total_subscriptions = data.total_subscriptions;

var tip_goal_values = JSON.parse(data.tip_goal_values);
var sub_goal_values = JSON.parse(data.sub_goals_values);

var sub_validated = JSON.parse(
    data.sub_validated.replace(/True/g, "true").replace(/False/g, "false"),
);
var tip_validated = JSON.parse(
    data.tip_validated.replace(/True/g, "true").replace(/False/g, "false"),
);

var remainingTime = end_timer - new Date().getTime() / 1000;

var skip_tip_animation = false;
var skip_sub_animation = false;

var timer_paused = data.timer_paused === "True";
var paused_time = data.paused_time;

// Tip goal

function triggerAnimationTip() {
    const imageElements = document.querySelectorAll(".tip_image_to_move");

    // Remove the animation class to reset the animation
    imageElements.forEach((image) => {
        image.classList.remove("moving-image");
        // Force reflow to restart the animation
        void image.offsetWidth;
        // Add the animation class to trigger the animation
        image.classList.add("moving-image");
    });
}

function removeFirstImageTip() {
    const imageElements = document.querySelectorAll(".tip_image_to_move");
    if (imageElements.length > 0) {
        imageElements[0].remove();
    }
}

function updateTipGoal() {
    triggerAnimationTip();
    setTimeout(removeFirstImageTip, 2000);
}
function removeFirstTreeTip() {
    skip_tip_animation = true;
    updateTipGoal();
    setTimeout(() => {
        updateTipGoal();
        setTimeout(() => {
            updateTipGoal();
        }, 2201);
    }, 2201);

    setTimeout(function() {
        tip_validated = [false, false, false];
        if (tip_goal_values.length >= 3) {
            tip_goal_values.splice(0, 3);
            if (tip_goal_values.length === 0) {
                document.querySelector("#tips").style.display = "none";
            }
        }
        skip_tip_animation = false;
        checkTipGoal();
    }, 7000);
}

function validateTipGoal() {
    let tips = document.querySelector("#tips").children;
    let firstThreeElements = Array.prototype.slice.call(tips, 0, 3);
    firstThreeElements.forEach((element, index) => {
        console.log("Checking tip goal " + element.id);
        if (tip_validated[index] == false && skip_tip_animation == false) {
            if (total_tips >= tip_goal_values[index]) {
                skip_tip_animation = true;
                console.log("Validating tip goal " + element.id);
                tip_validated[index] = true;
                validateGoal(element.id);

                setTimeout(function() {
                    skip_tip_animation = false;
                    checkTipGoal();
                }, 2201);
            }
        }
    });
}
function checkTipGoal() {
    console.log("Checking tip goal");
    if (skip_tip_animation) {
        console.log("Skipping tip animation");
        return;
    }
    console.log("Checking tip animation");
    if (tip_validated.every((value) => value == true)) {
        console.log("Removing first tree tip");
        removeFirstTreeTip();
    } else {
        console.log("Validating tip goal");
        validateTipGoal();
    }
}

// Subs Goal

function triggerAnimationSub() {
    const imageElements = document.querySelectorAll(".sub_image_to_move");

    // Remove the animation class to reset the animation
    imageElements.forEach((image) => {
        image.classList.remove("moving-image");
        // Force reflow to restart the animation
        void image.offsetWidth;
        // Add the animation class to trigger the animation
        image.classList.add("moving-image");
    });
}

function removeFirstImageSub() {
    const imageElements = document.querySelectorAll(".sub_image_to_move");
    if (imageElements.length > 0) {
        imageElements[0].remove();
    }
}

function updateSubGoal() {
    triggerAnimationSub();
    setTimeout(removeFirstImageSub, 2000);
}

function removeFirstTreeSub() {
    skip_sub_animation = true;
    updateSubGoal();
    setTimeout(() => {
        updateSubGoal();
        setTimeout(() => {
            updateSubGoal();
        }, 2201);
    }, 2201);

    setTimeout(function() {
        sub_validated = [false, false, false];
        if (sub_goal_values.length >= 3) {
            sub_goal_values.splice(0, 3);
        }
        skip_sub_animation = false;
        checkSubGoal();
    }, 7000);
}

function validateSubGoal() {
    let subs = document.querySelector("#subs").children;
    let firstThreeElements = Array.prototype.slice.call(subs, 0, 3);
    firstThreeElements.forEach((element, index) => {
        if (sub_validated[index] == false && skip_sub_animation == false) {
            if (total_subscriptions >= sub_goal_values[index]) {
                skip_sub_animation = true;
                sub_validated[index] = true;
                validateGoal(element.id);

                setTimeout(function() {
                    skip_sub_animation = false;
                    checkSubGoal();
                }, 2201);
            }
        }
    });
}

function checkSubGoal() {
    if (skip_sub_animation) {
        return;
    }
    if (sub_validated.every((value) => value == true)) {
        removeFirstTreeSub();
    } else {
        validateSubGoal();
    }
}

// Goal validation
function validateGoal(goalId) {
    const goalSquare = document.querySelector(`[id="${goalId}"] .validate`);
    const animation = document.querySelector(
        `[id="${goalId}"] .butterfly_animation`,
    );
    const image = document.querySelector(`[id="${goalId}"] #default`);
    const validatedImage = document.querySelector(`[id="${goalId}"] #validated`);

    if (goalSquare && animation && image && validatedImage) {
        image.classList.add("hidden");
        validatedImage.classList.remove("hidden");
        animation.style.display = "block";
        animation.play();
        console.log("Goal square found for ID:", goalId);
        setTimeout(() => {
            goalSquare.classList.add("validated");
            animation.style.display = "none";
        }, 3550);
    } else {
        console.log("Goal square not found for ID:", goalId);
    }
}

// Websocket
var ws_url = 'wss://' + window.location.host + '/ws/ticks/';

function connect() {
    var ws = new WebSocket(ws_url);

    ws.onmessage = function(event) {
        var data_ws = JSON.parse(event.data);
        end_timer = data_ws.time_end;
        total_tips = data_ws.total_tips;
        total_subscriptions = data_ws.total_subscriptions;
        timer_paused = data_ws.timer_paused;
        paused_time = data_ws.paused_time;

        update();
        checkTipGoal();
        checkSubGoal();
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
