// Copy buttons
document.querySelectorAll("[data-copy]").forEach(btn => {
  btn.addEventListener("click", () => copy(btn.dataset.copy, btn));
});

function copy(text, btn) {
  const done = () => { const t = btn.textContent; btn.textContent = "Copied"; setTimeout(() => btn.textContent = t, 1500); };
  if (navigator.clipboard) navigator.clipboard.writeText(text).then(done, () => {});
}

// Mail-app tabs on the home page
document.querySelectorAll(".tabs button").forEach(tab => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".tabs button").forEach(t => t.setAttribute("aria-selected", t === tab));
    document.querySelectorAll(".tabpanel").forEach(p => p.hidden = p.id !== "tab-" + tab.dataset.tab);
  });
});

// Share calculator on the card issuers page
const calc = document.querySelector(".calc");
if (calc) {
  const pick = group => +group.querySelector("[aria-pressed=true]").dataset.v;
  const money = n => n >= 1e6 ? "$" + (n / 1e6).toFixed(2).replace(/\.?0+$/, "") + "M" : "$" + Math.round(n / 1e3) + "K";
  const update = () => {
    document.getElementById("share").textContent = money(pick(airfare) * pick(takeup) * 0.0675 * 0.2);
  };
  const airfare = document.getElementById("airfare"), takeup = document.getElementById("takeup");
  [airfare, takeup].forEach(group => group.addEventListener("click", e => {
    if (!e.target.dataset.v) return;
    group.querySelectorAll("button").forEach(b => b.setAttribute("aria-pressed", b === e.target));
    update();
  }));
  update();
}
