import { getCookie } from "/static/general/js/utils.js";

const shuffleButton = document.getElementById("shuffle-button");
const closeAllButton = document.getElementById("close-button");
const calendarId = document.getElementById("calendar-id-data").textContent;

const csrftoken = getCookie("csrftoken");

function shuffle() {
    fetch(`/giveaway/api/calendar/${calendarId}/shuffle_reward/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
    })
        .then((response) => response.json())
        .then((data) => {
            console.log("Success:", data);
            window.location.reload();
        })
        .catch((error) => {
            console.error("Error:", error);
        });
}

function closeAll() {
    fetch(`/giveaway/api/calendar/${calendarId}/close_all/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
    })
        .then((response) => response.json())
        .then((data) => {
            console.log("Success:", data);
            window.location.reload();
        })
        .catch((error) => {
            console.error("Error:", error);
        });
}

shuffleButton.addEventListener("click", shuffle);
closeAllButton.addEventListener("click", closeAll);
