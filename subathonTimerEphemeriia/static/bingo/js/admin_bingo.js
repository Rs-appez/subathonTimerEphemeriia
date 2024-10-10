const data_admin = document.currentScript.dataset;
console.log(data_admin.bingo_items);
const bingo_items = JSON.parse(data_admin.bingo_items);

const bingoItems = document.querySelectorAll('.bingo-cell');


bingoItems.forEach(item => {
    item.addEventListener('click', () => {
        clickCell(item);
    });
});



function clickCell(item){
    var cellIndex = Array.from(item.parentNode.children).indexOf(item);
    var item = bingo_items[cellIndex];

    console.log(item);
    // fetch(backend+"/bingo/api/bingo_item_user/check_item/", {
    //   method: "POST",
    //   headers: {
    //     "Content-Type": "application/json",
    //   },
    //   body: JSON.stringify({token: token, bingo_item: item['bingo_item']['name']}),
    // })
    // .then(response => response.json())
    // .then((data) => {
    //   bingoBoard = data["bingo_items"];
    //   makeBingoBoard();
    // })
    // .catch((error) => {
    //   console.error('Error:', error);
    //   });
  }
  