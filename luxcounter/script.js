// CONFIG
const MAX_VALUE = 999999; // cap
const START_VALUE = 0;    // starting point
const TICK_MS = 120;      // how fast to count (ms per tick)

// grab the display box from the HTML
const counterEl = document.getElementById("lux-counter");

// track the current count
let currentValue = START_VALUE;

// build the 6-digit display like "000000"
function buildDigits(num) {
  const padded = num.toString().padStart(6, "0");
  counterEl.innerHTML = ""; // clear whatever was there

  for (let i = 0; i < padded.length; i++) {
    const span = document.createElement("span");
    span.className = "digit";
    span.textContent = padded[i];
    counterEl.appendChild(span);
  }
}

// set up first render
buildDigits(currentValue);

// add shimmer animation class to the whole block
counterEl.classList.add("shimmer");

// tick the counter upward until we hit MAX_VALUE
function tickUp() {
  if (currentValue >= MAX_VALUE) {
    return; // stop at the cap
  }

  currentValue++;

  const newString = currentValue.toString().padStart(6, "0");
  const digitEls = counterEl.querySelectorAll(".digit");

  for (let i = 0; i < digitEls.length; i++) {
    if (digitEls[i].textContent !== newString[i]) {
      // update digit
      digitEls[i].textContent = newString[i];

      // add pulse effect class
      digitEls[i].classList.add("pulse");

      // remove the pulse class after animation so it can pulse again
      setTimeout(() => {
        digitEls[i].classList.remove("pulse");
      }, 200);
    }
  }

  // schedule next tick
  setTimeout(tickUp, TICK_MS);
}

// start counting
tickUp();
