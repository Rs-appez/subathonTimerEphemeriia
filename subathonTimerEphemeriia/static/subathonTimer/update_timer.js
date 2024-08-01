// Update the timer every second
function update(){
    remainingTime = end_timer - new Date().getTime() / 1000;
    if(remainingTime <= 0){
        document.getElementById('time').innerHTML = 'FINI !!!!!';
        return;
    }
    document.getElementById('time').innerHTML = formatTime(remainingTime);
}
setInterval(update, 1000);

function formatTime(seconds){
    var hours = Math.floor(seconds / 3600);
    var minutes = Math.floor((seconds % 3600) / 60);
    minutes = minutes < 10 ? '0' + minutes : minutes;
    var seconds = Math.floor(seconds % 60);
    seconds = seconds < 10 ? '0' + seconds : seconds;

    return `${hours}:${minutes}:${seconds}`;
}

const data = document.currentScript.dataset;
var end_timer = data.time_left;
var remainingTime = end_timer - new Date().getTime() / 1000;


// Websocket
var ws_url = 'ws://' + window.location.host + '/ws/ticks/';

function connect(){
    var ws = new WebSocket(ws_url);

    ws.onmessage = function(event){
        var data_ws = JSON.parse(event.data);
        end_timer = data_ws.time_end;
        update();
    }

    ws.onclose = function(event){
        console.log('Connection closed');
        connect();

    }

    ws.onerror = function(event){
        console.log('Error');
        ws.close();
    }
}

connect();
