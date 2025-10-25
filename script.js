function openPlaylist(which) {
  const map = {
    1: "https://suno.com/playlist/2ec04889-1c23-4e2d-9c27-8a2b6475da4b",
    2: "https://suno.com/playlist/e95ddd12-7e37-43e2-b3e0-fe342085a19f",
    3: "https://suno.com/playlist/01b65a04-d231-4574-bbb6-713997ca5b44",
    4: "https://suno.com/playlist/457d7e00-938e-4bf0-bd59-f070729200df",
    5: "https://suno.com/playlist/08492edd-e0ba-4aea-a3f8-bb92220b28f2",
    "feature": "https://suno.com/playlist/feature",
    "single": "https://suno.com/playlist/single"
  };
  const url = map[which];
  if (url) window.open(url, "_blank");
}

// =====================================================
// COUNTER
// =====================================================
const counterEl = document.getElementById("counter");
let currentVal = 0;
const goalVal = 123485;
const ease = 0.03; // slow ease up

function animateCounter() {
  const diff = goalVal - currentVal;
  if (Math.abs(diff) < 1) currentVal = goalVal;
  else currentVal += diff * ease;

  counterEl.textContent = Math.floor(currentVal).toLocaleString("en-US");

  if (currentVal < goalVal) requestAnimationFrame(animateCounter);
}
animateCounter();

// =====================================================
// BUBBLES
// =====================================================
const canvas = document.getElementById("bubbleCanvas");
const ctx = canvas.getContext("2d");

function sizeCanvas() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}
sizeCanvas();
window.addEventListener("resize", sizeCanvas);

const bubbleColors = [
  "rgba(255, 102, 255, 0.15)",
  "rgba(255, 128, 0, 0.15)",
  "rgba(100, 100, 255, 0.15)",
  "rgba(255, 255, 255, 0.07)"
];

function makeBubble() {
  return {
    x: Math.random() * canvas.width,
    y: canvas.height + Math.random() * canvas.height,
    r: 5 + Math.random() * 25,
    speed: 0.3 + Math.random() * 1.0,
    color: bubbleColors[Math.floor(Math.random() * bubbleColors.length)],
    drift: (Math.random() - 0.5) * 0.4
  };
}

const bubbles = [];
for (let i = 0; i < 50; i++) {
  bubbles.push(makeBubble());
}

function drawBubbles() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  for (let b of bubbles) {
    ctx.beginPath();
    ctx.arc(b.x, b.y, b.r, 0, Math.PI * 2);
    ctx.fillStyle = b.color;
    ctx.fill();

    b.y -= b.speed;
    b.x += b.drift;

    if (b.y + b.r < 0) {
      b.x = Math.random() * canvas.width;
      b.y = canvas.height + b.r + Math.random() * canvas.height * 0.3;
      b.r = 5 + Math.random() * 25;
      b.speed = 0.3 + Math.random() * 1.0;
      b.color = bubbleColors[Math.floor(Math.random() * bubbleColors.length)];
      b.drift = (Math.random() - 0.5) * 0.4;
    }
  }

  requestAnimationFrame(drawBubbles);
}

drawBubbles();
