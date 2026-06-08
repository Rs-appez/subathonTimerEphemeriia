const data = document.currentScript.dataset;
let total_both = data.total_both;

function updateProgress() {
  const tipProgress = document.getElementById("current-amount");

  if (tipProgress) {
    tipProgress.innerText = ceilTo2Formatted(total_both / 5);
  }
}

function ceilTo2Formatted(num) {
  const n = Math.floor(Number(num) * 100) / 100;
  return n.toLocaleString(undefined, { maximumFractionDigits: 2 });
}

const evtSource = new EventSource("/timer/events/");
evtSource.onmessage = function (event) {
  const data_ws = JSON.parse(event.data);
  total_both = data_ws.total_both;

  updateProgress();
};

updateProgress();
