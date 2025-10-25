// TIMMYTIME MASTER SCRIPT
// RULE: replace whole file, do not splice
// build v2.2

(function () {
  const buildTagEl = document.getElementById("buildTag");
  const statusEl = document.getElementById("statusLine");
  const nowServingEl = document.getElementById("nowServingNumber");
  const bubbleField = document.getElementById("bubbleField");

  // what this page THINKS it is
  const currentVersion = buildTagEl
    ? buildTagEl.getAttribute("data-version")
    : null;

  // ------------------------------------------------------------------
  // 1. BUBBLES
  // We'll generate a handful of animated bubbles with random size,
  // color, start X, and animation duration, all floating upward.
  // We keep the count modest for smooth performance.
  // ------------------------------------------------------------------
  function spawnBubbles() {
    if (!bubbleField) return;
    const COLORS = ["var(--bubble-purple)", "var(--bubble-pink)", "var(--bubble-orange)"];

    const BUBBLE_COUNT = 14; // light but alive
    for (let i = 0; i < BUBBLE_COUNT; i++) {
      const b = document.createElement("div");
      b.className = "bubble";

      // size
      const size = 20 + Math.random() * 60; // 20px - 80px
      b.style.width = size + "px";
      b.style.height = size + "px";

      // pick a glow color
      const color = COLORS[Math.floor(Math.random() * COLORS.length)];
      b.style.background = `
        radial-gradient(circle at 30% 30%, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0) 60%),
        ${color}
      `;

      // horizontal position
      const startX = Math.random() * 100; // vw-ish %
      b.style.left = startX + "vw";

      // animation duration + delay so they drift at different speeds
      const dur = 10 + Math.random() * 10; // 10s - 20s
      const delay = -Math.random() * dur;  // so they start mid-flight
      b.style.animationDuration = dur + "s";
      b.style.animationDelay = delay + "s";

      bubbleField.appendChild(b);
    }
  }

  // ------------------------------------------------------------------
  // 2. COUNTER / "NOW SERVING"
  // We'll try to increment the counter on load.
  // If it works, we show the real number:
  //   "Now Serving #12 of 999,999"
  // If it fails, we show "—" and go safe mode.
  // ------------------------------------------------------------------
  async function loadNowServing() {
    if (!nowServingEl) return;
    try {
      const res = await fetch("/visit", { cache: "no-store" });
      const data = await res.json();

      if (data && typeof data.count === "number") {
        nowServingEl.textContent = `#${data.count}`;
      } else {
        nowServingEl.textContent = "—";
        if (statusEl) {
          statusEl.textContent = "status: safe mode (counter)";
          statusEl.style.color = "#ffea00";
        }
      }
    } catch (err) {
      nowServingEl.textContent = "—";
      if (statusEl) {
        statusEl.textContent = "status: safe mode (counter offline)";
        statusEl.style.color = "#ffea00";
      }
    }
  }

  // ------------------------------------------------------------------
  // 3. AUTO-UPDATE
  // After the page is already visible, check if the server is on
  // a newer BUILD_VERSION. If so, force-reload with cache-bust.
  // We stagger this so first paint feels instant.
  // ------------------------------------------------------------------
  async function checkForUpdate() {
    try {
      const res = await fetch("/version", { cache: "no-store" });
      const data = await res.json();
      const serverVersion = data.version;

      if (serverVersion && currentVersion && serverVersion !== currentVersion) {
        // different version? reload hard with unique query so Safari/CDN must fetch new
        window.location.href =
          window.location.pathname + "?autoupdate=" + Date.now();
      }
    } catch (err) {
      // stay quiet, we don't scare users
    }
  }

  // ------------------------------------------------------------------
  // 4. INIT
  // ------------------------------------------------------------------
  function init() {
    spawnBubbles();
    loadNowServing();

    // run update check after a short delay,
    // then keep checking in the background every 10s
    setTimeout(checkForUpdate, 1500);
    setInterval(checkForUpdate, 10000);
  }

  init();
})();
