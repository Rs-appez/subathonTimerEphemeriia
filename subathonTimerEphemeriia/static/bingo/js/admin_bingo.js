const data_admin = document.currentScript.dataset;

const backend = window.location.host;

const formattedData = data_admin.bingo_items
    .replace(/{'/g, '{"')
    .replace(/': '/g, '": "')
    .replace(/, '/g, ', "')
    .replace(/'}/g, '"}')
    .replace(/':/g, '":')
    .replace(/False/g, "false")
    .replace(/True/g, "true");

var bingo_items = JSON.parse(formattedData);

var bingoBoard = document.querySelectorAll(".bingo-cell");
let showButton = document.getElementById("showBingo");
let hideButton = document.getElementById("hideBingo");

bingoBoard.forEach((item) => {
    item.addEventListener("click", clickCell);
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function makeBingoBoard() {
    var board = document.getElementById("bingoCard");
    board.innerHTML = "";
    //length = Math.sqrt(bingo_items.length);
    //board.style.gridTemplateColumns = "repeat(" + length + ", 1fr)";

    for (var i = 0; i < bingo_items.length; i++) {
        item = bingo_items[i];
        var cell = document.createElement("div");
        if (item["is_checked"]) {
            cell.className = "bingo-cell bingo-cell-checked";
        } else {
            cell.className = "bingo-cell";
        }
        cell.innerHTML = item["bingo_item"]["name"];
        cell.addEventListener("click", clickCell);
        board.appendChild(cell);
    }
}

function clickCell() {
    var item = this;
    var cellIndex = Array.from(item.parentNode.children).indexOf(item);
    var item = bingo_items[cellIndex];

    console.log(item);

    var csrftoken = getCookie("csrftoken");

    fetch("http://" + backend + "/bingo/api/bingo_item_user/check_item_admin/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({ bingo_item: item["bingo_item"]["name"] }),
    })
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            bingo_items = data["bingo_items"];
            makeBingoBoard();
        })
        .catch((error) => {
            console.error("Error:", error);
        });
}

function sendToWidget(show) {
    console.log(show);
    var csrftoken = getCookie("csrftoken");

    fetch("http://" + backend + "/bingo/api/bingo/display_bingo_widget/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({
            show: show,
            user: "Ephemeriia",
        }),
    })
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
        })
        .catch((error) => {
            console.error("Error:", error);
        });
}

showButton.addEventListener("click", function() {
    sendToWidget(true);
});
hideButton.addEventListener("click", function() {
    sendToWidget(false);
});
