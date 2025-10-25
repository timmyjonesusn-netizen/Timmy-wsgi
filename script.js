// ===== SET THE NUMBER YOU WANT TO SHOW =====
const START_VALUE = 40;   // <-- change this to whatever you want
const DIGITS = 6;         // always show 6 digits like 000040

// grab the display box
const counterEl = document.getElementById("lux-counter");

// build those digits once and done
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

// shimmer forever because we’re glossy
counterEl.classList.add("shimmer");

// render the static value
buildDigits(START_VALUE);
