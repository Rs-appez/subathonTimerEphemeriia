const data = document.currentScript.dataset;
let total_both = data.total_both;

function updateProgress() {
  const tipProgress = document.getElementById("current-amount");

  if (tipProgress) {
    tipProgress.innerText = total_both / 5;
  }
}

const evtSource = new EventSource("/timer/events/");
evtSource.onmessage = function (event) {
  const data_ws = JSON.parse(event.data);
  total_both = data_ws.total_both;

  updateProgress();
};

updateProgress();
