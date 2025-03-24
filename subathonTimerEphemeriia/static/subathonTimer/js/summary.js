const data = document.currentScript.dataset;
var time = data.time;

function formatTime(seconds) {
    var hours = Math.floor(seconds / 3600);
    hours = hours < 10 ? "0" + hours : hours;
    var minutes = Math.floor((seconds % 3600) / 60);
    minutes = minutes < 10 ? "0" + minutes : minutes;
    var seconds = Math.floor(seconds % 60);
    seconds = seconds < 10 ? "0" + seconds : seconds;

    return `${hours}:${minutes}:${seconds}`;
}

function setTime() {
    const timeElement = document.getElementById("time");
    if (!timeElement) {
        return;
    }
    timeElement.innerHTML = formatTime(time);
}

setTime();
