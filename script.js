// ===== CONFIG =====
const START_VALUE = 6;    // <-- put your real number here
const DIGITS = 6;         // always show 6 digits like 000006

const counterEl = document.getElementById("lux-counter");

// builds the static digits
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

// shimmer flex
counterEl.classList.add("shimmer");

// render once
buildDigits(START_VALUE);
