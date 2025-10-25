// ===== CONFIG =====
const MAX_VALUE = 999999; // show "/ 999,999" to match
const START_VALUE = 0;    // where we begin
const TICK_MS = 120;      // speed of count-up (smaller = faster)

// ===== SETUP =====
const counterEl = document.getElementById("lux-counter");

// create 6 digits to start "000000"
let currentValue = START_VALUE;

function buildDigits(num) {
  const str = num.toString().padStart(6, "0");
  counterEl.innerHTML = ""; // clear
  for (let i = 0; i < str.length; i++) {
    const d = document.createElement("span");
    d.className = "digit";
    d.textContent = str[i];
    counterEl.appendChild(d);
  }
}

// call once on load
buildDigits(currentValue);

// shimmer class for the sweep animation
counterEl.classList.add("shimmer");

// ===== ANIMATION LOOP =====
function tickUp() {
  if (currentValue >= MAX_VALUE) {
    return; // stop at cap
  }

  currentValue++;

  // update digits visually
  const newStr = currentValue.toString().padStart(6, "0");
  const digitEls = counterEl.querySelectorAll(".digit");

  for (let i = 0; i < digitEls.length; i++) {
    if (digitEls[i].textContent !== newStr[i]) {
      digitEls[i].textContent = newStr[i];

      // pulse effect
      digitEls[i].classList.add("pulse");
      // remove pulse after animation so it can trigger again
      setTimeout(() => {
        digitEls[i].classList.remove("pulse");
      }, 200);
    }
  }

  // queue next tick
  setTimeout(tickUp, TICK_MS);
}

// start the count
tickUp();
