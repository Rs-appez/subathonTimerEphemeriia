const canvas = document.getElementById("wheel");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
const ctx = canvas.getContext("2d");
const segments = 9;
const colors = [
    "#ccbadb",
    "#a88fc2",
    "#8454a9",
    "#602990",
    "#8454a9",
    "#a88fc2",
];
let angle = 0;
let spinning = false;

function drawWheel() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = Math.min(canvas.width, canvas.height) / 2.2;
    for (let i = 0; i < segments; i++) {
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.arc(
            centerX,
            centerY,
            radius,
            angle + (i * 2 * Math.PI) / segments,
            angle + ((i + 1) * 2 * Math.PI) / segments,
        );
        ctx.closePath();
        ctx.fillStyle = colors[i % colors.length];
        ctx.fill();
        ctx.strokeStyle = "black";
        ctx.lineWidth = 2;
        ctx.stroke();
    }
}

function spinWheel() {
    if (spinning) return;
    spinning = true;
    const spinSpeed = Math.random() * 0.2 + 0.3;
    const spinTime = 2000 + Math.random() * 1000;
    const start = Date.now();

    function animate() {
        const elapsed = Date.now() - start;
        if (elapsed < spinTime) {
            angle += spinSpeed * (1 - elapsed / spinTime);
            drawWheel();
            requestAnimationFrame(animate);
        } else {
            spinning = false;
        }
    }
    animate();
}

document.getElementById("spinButton").addEventListener("click", spinWheel);
drawWheel();
window.addEventListener("resize", () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    drawWheel();
});
