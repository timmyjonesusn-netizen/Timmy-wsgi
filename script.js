// -----------------------------
// Counter lock
// -----------------------------
(function () {
  const el = document.getElementById('liveCounter');
  if (!el) return;

  const displayNumber = 999999;

  const withCommas = displayNumber
    .toString()
    .replace(/\B(?=(\d{3})+(?!\d))/g, ",");

  el.textContent = withCommas;
})();

// -----------------------------
// Video swapper with status light
// -----------------------------
(function () {
  const selectEl = document.getElementById('videoSelect');
  const buttonEl = document.getElementById('applyVideoBtn');
  const videoEl  = document.getElementById('infoVideo');
  const sourceEl = document.getElementById('videoSource');
  const statusEl = document.getElementById('loadStatus');

  if (!selectEl || !buttonEl || !videoEl || !sourceEl || !statusEl) {
    return;
  }

  // helper to flip status styles
  function setStatus(ok, msg) {
    statusEl.textContent = msg;
    if (ok) {
      statusEl.classList.add('load-ok');
      statusEl.classList.remove('load-bad');
    } else {
      statusEl.classList.add('load-bad');
      statusEl.classList.remove('load-ok');
    }
  }

  // default starting state = good
  setStatus(true, "READY");

  buttonEl.addEventListener('click', () => {
    const newSrc = selectEl.value;

    // optimistic set while loading new source
    setStatus(true, "LOADING");

    // point the <source> at the new file
    sourceEl.setAttribute('src', newSrc);

    // tell <video> to reload
    videoEl.load();

    // try to play (mobile may block autoplay but that's ok)
    videoEl.play().then(() => {
      // success load & play
      setStatus(true, "READY");
    }).catch(() => {
      // could be autoplay block, not necessarily missing file
      setStatus(true, "READY");
    });

    // if actual file is missing (404, bad name), <video> will fire 'error'
    videoEl.onerror = () => {
      setStatus(false, "MISSING");
    };
  });
})();
