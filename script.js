const START_VALUE = 40;  // edit this for your number
const DIGITS = 6;

const counterEl = document.getElementById("lux-counter");

function buildDigits(num) {
  const padded = num.toString().padStart(DIGITS, "0");
  counterEl.textContent = padded;
}

buildDigits(START_VALUE);
