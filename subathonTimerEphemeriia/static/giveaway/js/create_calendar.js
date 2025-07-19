import { getCookie } from "/static/general/js/utils.js";

function createCalendar(btn) {
    btn.disabled = true;
    let title = document.getElementById("calendar-name").value;
    let base_calendar =
        document.querySelector('input[name="calendar-size"]:checked')?.value || "";
    //let img = document.getElementById("calendar-image").value;

    if (title === "" || base_calendar === "") {
        alert("Please fill all fields");
        btn.disabled = false;
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
        }),
    })
        .then((response) => response.json())
        .then((data) => {
            console.log("Success:", data);
            window.location.href = `/giveaway/admin/${data.calendar.id}/`;
        })
        .catch((error) => {
            console.error("Error:", error);
            btn.disabled = false;
        });
}

const createButton = document.getElementById("create-calendar");
createButton.addEventListener("click", () => createCalendar(createButton));
