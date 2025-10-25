// FINAL STATIC MODE – no loops, no runaway
const START_VALUE = 40;   // <- change this to your current count
const DIGITS = 6;         // show 6 digits (000040)

const counterEl = document.getElementById("lux-counter");

function buildDigits(num) {
  const padded = num.toString().padStart(DIGITS, "0");
  counterEl.innerHTML = "";
  for (let i = 0; i < padded.length; i++) {
    const span = document.createElement("span");
    span.className = "digit";
    span.textContent = padded[i];
    counterEl.appendChild(span);
  }
}

// shimmer effect so it still glows
counterEl.classList.add("shimmer");

// render once – no loop
buildDigits(START_VALUE);
