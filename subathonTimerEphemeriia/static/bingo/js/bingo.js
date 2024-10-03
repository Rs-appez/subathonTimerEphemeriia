const data = document.currentScript.dataset;
const bingo_length = JSON.parse(data.bingo_lenght);

document.getElementById('bingoCard').style.gridTemplateColumns = `repeat(${bingo_length}, 1fr)`;

const bingoItems = document.querySelectorAll('.bingo-cell');
bingoItems.forEach(item => {
    item.addEventListener('click', () => {
        item.classList.toggle('free');
    });
});