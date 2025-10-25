// TIMMYTIME MASTER SCRIPT
// RULE: replace whole file, do not splice
// build v2.1

(async function () {
  const buildTagEl = document.getElementById("buildTag");
  const statusEl = document.getElementById("statusLine");
  const visitorEl = document.getElementById("visitorCount");

  // what this page THINKS it is
  const currentVersion = buildTagEl
    ? buildTagEl.getAttribute("data-version")
    : null;

  // helper: safe text set
  function setTextSafe(el, value) {
    if (el) el.textContent = value;
  }

  // 1. AUTO-CORRECT + COUNTER
  // we try to increment visit count.
  // if that fails, we do not embarrass the page.
  async function loadVisitorCount() {
    try {
      // hit /visit to increment
      const res = await fetch("/visit", { cache: "no-store" });
      const data = await res.json();

      if (data && typeof data.count === "number") {
        setTextSafe(visitorEl, data.count.toString());
      } else {
        // fallback: readable instead of broken
        setTextSafe(visitorEl, "…");
        setTextSafe(statusEl, "status: safe mode (counter)");
      }
    } catch (err) {
      // still show page gracefully
      setTextSafe(visitorEl, "…");
      setTextSafe(statusEl, "status: safe mode (counter offline)");
    }
  }

  // 2. AUTO-UPDATE
  // ask server what version it SHOULD be, compare,
  // and if different, force-refresh with cache-bust.
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
      // if version check fails, don't spam status, just chill
      // app should still run; no white screen
    }
  }

  // run visitor count once on load
  loadVisitorCount();

  // run update check now
  checkForUpdate();

  // keep checking for new code every 10 seconds
  setInterval(checkForUpdate, 10000);
})();
