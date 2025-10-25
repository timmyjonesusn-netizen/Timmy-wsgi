// Final static mode
const START_VALUE = 40; // change to your live count
const DIGITS = 6;

const counterEl = document.getElementById("lux-counter");

function buildDigits(num) {
  const padded = num.toString().padStart(DIGITS, "0");
  counterEl.textContent = padded;
}

buildDigits(START_VALUE);
