const DATA = document.getElementById("tracker-data").textContent;
let tracker = JSON.parse(DATA);

function updateProgress() {
    let progressBar = document.getElementById("progress-bar-fill");
    let progress = Math.min(
        100,
        (tracker.current_level / tracker.target_level) * 100,
    );

    progressBar.style.width = progress + "%";
}

updateProgress();
