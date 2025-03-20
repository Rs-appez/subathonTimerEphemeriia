const rawCellData = document.getElementById("calendar-cells-data").textContent;
const cellsData = JSON.parse(rawCellData);

function handleClick(event) {
  event.preventDefault();
  // Your click handling logic here
  const cellNumber = event.target.id.split("_")[1];

  console.log(cellNumber);
}

function scaleImage() {
  cellsData.forEach(function (cell) {
    var img = document.getElementById(`cell_${cell.number}`);
    var imgWidth = img.width;
    var imgHeight = img.height;

    var originalCoords = cell.coordonates.split(",").map(Number);
    var coords = originalCoords.map(function (coord, index) {
      return index % 2 === 0 ? coord * imgWidth : coord * imgHeight;
    });

    var area = document.getElementById(`cell_${cell.number}_area`);
    area.setAttribute("coords", coords.join(","));
  });
}

window.addEventListener("load", scaleImage);
