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
        var img = document.getElementById(`cell_${cell.number}`);
        var imgWidth = img.width;
        var imgHeight = img.height;

        var originalCoords = cell.coordonates.split(",").map(Number);
        var coords = originalCoords.map(function(coord, index) {
            return index % 2 === 0 ? coord * imgWidth : coord * imgHeight;
        });

        var area = document.getElementById(`cell_${cell.number}_area`);
        area.setAttribute("coords", coords.join(","));
    });
}

window.addEventListener("load", scaleImage);
