import { getCookie } from "/static/general/js/utils.js";

const csrftoken = getCookie("csrftoken");

const calendarContainer = document.getElementById("cells-container");
const shuffleButton = document.getElementById("shuffle-button");
const closeAllButton = document.getElementById("close-all-button");

document.body.addEventListener("htmx:configRequest", (event) => {
    event.detail.headers["X-CSRFToken"] = csrftoken;
});

function loadingCalendar() {
    calendarContainer.classList.add("loading");
    shuffleButton.disabled = true;
    closeAllButton.disabled = true;
}

function loadedCalendar() {
    calendarContainer.classList.remove("loading");
    shuffleButton.disabled = false;
    closeAllButton.disabled = false;
}

function onRequest(event) {
    if (["shuffle-button", "close-all-button"].includes(event.target.id)) {
        loadingCalendar();
    }
}

function onResponse(event) {
    if (
        ["shuffle-button", "close-all-button"].includes(event.requestConfig.elt.id)
    ) {
        loadedCalendar();
    }
}

document.body.addEventListener("htmx:beforeRequest", onRequest);
document.body.addEventListener("htmx:afterSwap", onResponse);
