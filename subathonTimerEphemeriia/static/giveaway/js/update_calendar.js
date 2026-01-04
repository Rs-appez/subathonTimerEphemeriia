import { getCookie } from "/static/general/js/utils.js";

const csrftoken = getCookie("csrftoken");

document.body.addEventListener("htmx:configRequest", (event) => {
    event.detail.headers["X-CSRFToken"] = csrftoken;
});
