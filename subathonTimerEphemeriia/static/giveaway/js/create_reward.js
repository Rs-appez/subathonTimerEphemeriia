import { getCookie } from "/static/general/js/utils.js";

async function createReward(btn) {
    btn.disabled = true;
    let name = document.getElementById("reward-name").value;
    let img = document.getElementById("reward-image").files[0];

    if (name === "") {
        alert("Please fill all fields");
        btn.disabled = false;
        return;
    }

    var csrftoken = getCookie("csrftoken");
    let formData = new FormData();
    formData.append("name", name);
    if (img) {
        formData.append("image", img);
    }

    try {
        const response = await fetch("/giveaway/api/reward/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
            },
            body: formData,
        });

        let data;
        try {
            data = await response.json();
        } catch {
            throw new Error("Invalid server response");
        }

        if (!response.ok) {
            const err = new Error(data.detail || "Error " + response.status);
            err.response = JSON.stringify(data);
            throw err;
        }

        console.log("Success:", data);
        window.location.href = `/giveaway/admin/`;
    } catch (error) {
        alert("Error: " + error.response);
        console.error("Error:", error);
        btn.disabled = false;
    }
}

const createButton = document.getElementById("create-reward");
createButton.addEventListener("click", () => createReward(createButton));
