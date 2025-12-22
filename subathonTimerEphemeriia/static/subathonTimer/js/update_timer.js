const data = document.currentScript.dataset;
let end_timer = data.time_left;
let total_tips = data.total_tips;
let total_subscriptions = data.total_subscriptions;

let tip_goal_values = JSON.parse(data.tip_goal_values);
let sub_goal_values = JSON.parse(data.sub_goals_values);

let tip_nb_goals = parseInt(data.tip_nb_goals) || 3;
let sub_nb_goals = parseInt(data.sub_nb_goals) || 3;

let sub_validated = JSON.parse(
    data.sub_validated.replace(/True/g, "true").replace(/False/g, "false"),
);
let tip_validated = JSON.parse(
    data.tip_validated.replace(/True/g, "true").replace(/False/g, "false"),
);

let remainingTime = end_timer - new Date().getTime() / 1000;

let skip_tip_animation = false;
let skip_sub_animation = false;

let timer_paused = data.timer_paused === "True";
let paused_time = data.paused_time;

// Timer update function
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
    for (let i = 1; i < tip_nb_goals; i++) {
        setTimeout(updateTipGoal, i * 2201);
    }

    setTimeout(
        function() {
            tip_validated = new Array(tip_nb_goals).fill(false);
            if (tip_goal_values.length >= tip_nb_goals) {
                tip_goal_values.splice(0, tip_nb_goals);
                if (tip_goal_values.length === 0) {
                    document.querySelector("#tips").style.display = "none";
                }
            }
            skip_tip_animation = false;
            checkTipGoal();
        },
        500 + tip_nb_goals * 2201,
    );
}

function validateTipGoal() {
    let tips = document.querySelector("#tips").children;
    let firstElements = Array.prototype.slice.call(tips, 0, tip_nb_goals);
    firstElements.forEach((element, index) => {
        if (tip_validated[index] == false && skip_tip_animation == false) {
            if (total_tips >= tip_goal_values[index]) {
                skip_tip_animation = true;
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
    if (skip_tip_animation) {
        return;
    }
    if (tip_validated.every((value) => value == true)) {
        removeFirstTreeTip();
    } else {
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
    for (let i = 1; i < sub_nb_goals; i++) {
        setTimeout(updateSubGoal, i * 2201);
    }

    setTimeout(
        function() {
            sub_validated = new Array(sub_nb_goals).fill(false);
            if (sub_goal_values.length >= sub_nb_goals) {
                sub_goal_values.splice(0, sub_nb_goals);
            }
            skip_sub_animation = false;
            checkSubGoal();
        },
        500 + sub_nb_goals * 2201,
    );
}

function validateSubGoal() {
    let subs = document.querySelector("#subs").children;
    let firstElements = Array.prototype.slice.call(subs, 0, sub_nb_goals);
    firstElements.forEach((element, index) => {
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

// Generals functions
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
        animation.play().catch((error) => {
            console.error("Error playing animation:", error);
        });
        setTimeout(() => {
            goalSquare.classList.add("validated");
            animation.style.display = "none";
        }, 3550);
    } else {
        console.log("Goal square not found for ID:", goalId);
    }
}

function resizeDisplayGoals() {
    document.documentElement.style.setProperty(
        "--display-nb-tip-goals",
        tip_nb_goals * 150 + "px",
    );
    document.documentElement.style.setProperty(
        "--display-nb-sub-goals",
        sub_nb_goals * 150 + "px",
    );
}

function refreshAll() {
    update();
    checkTipGoal();
    checkSubGoal();
    // resizeDisplayGoals();
}

const evtSource = new EventSource("/timer/events/");
evtSource.onmessage = function(event) {
    const data_ws = JSON.parse(event.data);
    end_timer = data_ws.time_end;
    total_tips = data_ws.total_tips;
    total_subscriptions = data_ws.total_subscriptions;
    timer_paused = data_ws.timer_paused;
    paused_time = data_ws.paused_time;

    refreshAll();
};

resizeDisplayGoals();
