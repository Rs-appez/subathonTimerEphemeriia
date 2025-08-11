const container = document.getElementById("wheelContainer");
const canvas = document.getElementById("wheel");
const ctx = canvas.getContext("2d");
const data = [
    "test1",
    "test2",
    "test3",
    "test4",
    "test5",
    "test6",
    "test7",
    "test8",
    "test9",
];
const segments = data.length;
const colors = [
    "#ccbadb",
    "#a88fc2",
    "#8454a9",
    "#602990",
    "#8454a9",
    "#a88fc2",
];
let spinning = false;

let angle = -Math.PI / 2;
let centerX, centerY, radius;

function drawWheel() {
    centerX = canvas.width / 2;
    centerY = canvas.height / 2;
    radius = Math.min(canvas.width, canvas.height) / 2.2;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
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

        const textAngle = angle + ((i + 0.5) * 2 * Math.PI) / segments;
        ctx.save();
        ctx.translate(centerX, centerY);
        ctx.rotate(textAngle);
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillStyle = "black";
        ctx.font = `${Math.floor(radius / 10)}px Arial`;
        ctx.fillText(data[i], radius * 0.65, 0);
        ctx.restore();
    }
    drawPointer();
}
function drawPointer() {
    ctx.save();
    ctx.translate(centerX, centerY);
    ctx.beginPath();
    ctx.moveTo(0, -radius + 10);
    ctx.lineTo(-15, -radius - 10);
    ctx.lineTo(15, -radius - 10);
    ctx.closePath();
    ctx.fillStyle = "#e74c3c";
    ctx.fill();
    ctx.restore();
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
            getWinningPartition();
        }
    }
    animate();
}

function getWinningPartition() {
    if (spinning) return null;
    let normalizedAngle = (angle - -Math.PI / 2) % (2 * Math.PI);
    if (normalizedAngle < 0) normalizedAngle += 2 * Math.PI;
    const winningIndex = Math.floor(
        (segments - (normalizedAngle * segments) / (2 * Math.PI)) % segments,
    );
    console.log("Winning partition : ", data[winningIndex]);
    return data[winningIndex];
}

function resizeCanvas() {
    canvas.height = window.innerHeight;
    canvas.width = window.innerHeight;

    // container.style.width = `${canvas.width}px`;
    // container.style.height = `${canvas.height}px`;
}

document.getElementById("spinButton").addEventListener("click", spinWheel);
window.addEventListener("resize", () => {
    resizeCanvas();
    drawWheel();
});

resizeCanvas();
drawWheel();
