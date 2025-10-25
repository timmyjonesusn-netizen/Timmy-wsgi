// ===== LOCKED DISPLAY MODE =====
// This version does NOT keep counting. It shows a value and stops.

const START_VALUE = 40;   // <- put the number you want to show
const DIGITS = 6;         // forces 6 digits like 000040

const counterEl = document.getElementById("lux-counter");

// Build the digits once
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

// Add the shimmer effect to the whole counter box
counterEl.classList.add("shimmer");

// Render once and DONE (no loop, no runaway)
buildDigits(START_VALUE);
