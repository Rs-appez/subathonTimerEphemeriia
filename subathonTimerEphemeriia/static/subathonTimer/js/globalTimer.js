const data = document.currentScript.dataset;
var startedTime = data.time;

function update() {
    const timeElement = document.getElementById("time");
    if (timeElement) {
        remainingTime = new Date().getTime() / 1000 - startedTime;
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
