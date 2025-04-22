import { getCookie } from "/static/general/js/utils.js";

const rawCellData = document.getElementById("calendar-cells-data").textContent;
const cellsData = JSON.parse(rawCellData);

function handleClick(event) {
    event.preventDefault();
    // Your click handling logic here
    const cellNumber = event.target.id.split("_")[1];

    let cell_img = document.getElementById(`cell_${cellNumber}`);

    cell_img.addEventListener("animationend", function() {
        event.target.remove();
        cell_img.remove();
    });
    addRandomEffect(cell_img);

    console.log(cellNumber);

    var csrftoken = getCookie("csrftoken");
    fetch(`/giveaway/api/cell/${cellNumber}/open_cell/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
    })
        .then((response) => response.json())
        .then((data) => {
            console.log("Success:", data);
            // Handle the response data here
        })
        .catch((error) => {
            console.error("Error:", error);
        });
}

function addRandomEffect(element) {
    const effects = ["fade-out", "go-up", "go-down", "go-left", "go-right"];
    const randomEffect = effects[Math.floor(Math.random() * effects.length)];

    // add specific effect
    switch (randomEffect) {
        case "go-up":
        case "go-down":
        case "go-left":
        case "go-right":
            element.style.setProperty("z-index", "1");
            break;
        default:
            break;
    }

    element.classList.add(randomEffect);
}

function scaleImage() {
    cellsData.forEach(function(cell) {
        console.log(cell);
        var img = document.getElementById(`cell_${cell.id}`);
        if (!img) {
            return;
        }
        var imgWidth = img.width;
        var imgHeight = img.height;

        var originalCoords = cell.cell.coordonates.split(",").map(Number);
        var coords = originalCoords.map(function(coord, index) {
            return index % 2 === 0 ? coord * imgWidth : coord * imgHeight;
        });

        var area = document.getElementById(`cell_${cell.id}_area`);
        area.setAttribute("coords", coords.join(","));
    });
}
window.addEventListener("load", () => {
    scaleImage();

    // Attach handleClick to all areas
    const cells = document.querySelectorAll("area");
    cells.forEach((cell) => {
        cell.addEventListener("click", handleClick);
    });
});
