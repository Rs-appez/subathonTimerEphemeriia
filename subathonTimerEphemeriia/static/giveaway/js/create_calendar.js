import { getCookie } from "/static/general/js/utils.js";

function createCalendar() {
    let title = document.getElementById("calendar-name").value;
    let base_calendar =
        document.querySelector('input[name="calendar-size"]:checked')?.value || "";
    let img = document.getElementById("calendar-image").value;
    console.log(title, base_calendar, img);

    if (title === "" || base_calendar === "" || img === "") {
        alert("Please fill all fields");
        return;
    }

    var csrftoken = getCookie("csrftoken");

    fetch("/giveaway/api/calendar/create/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({
            title: title,
            base_calendar_id: base_calendar,
            background_url: img,
        }),
    })
        .then((response) => response.json())
        .then((data) => {
            console.log("Success:", data);
            //window.location.reload();
        })
        .catch((error) => {
            console.error("Error:", error);
        });
}

const createButton = document.getElementById("create-calendar");
createButton.addEventListener("click", createCalendar);
