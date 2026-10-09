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
  const $ = id => document.getElementById(id);
  const num = s => parseFloat(String(s).replace(/[^0-9.]/g, ""));
  const money = n => n >= 1e9 ? "$" + +(n / 1e9).toFixed(2) + "B"
    : n >= 1e6 ? "$" + +(n / 1e6).toFixed(2) + "M"
    : n >= 1e3 ? "$" + Math.round(n / 1e3) + "K" : "$" + Math.round(n);
  const count = n => Math.round(n).toLocaleString("en-US");
  const update = () => {
    const airfare = num($("airfare").value) * +$("unit").value;
    const takeup = num($("takeup").value) / 100;
    $("takeupPresets").querySelectorAll("button").forEach(b => b.setAttribute("aria-pressed", +b.dataset.v === takeup * 100));
    if (!(airfare > 0) || !(takeup > 0) || takeup > 1) {
      $("share").textContent = "–"; $("passes").textContent = "–"; $("rescues").textContent = "–";
      return;
    }
    const passes = airfare / 500 * takeup;
    $("share").textContent = money(airfare * takeup * 0.0675 * 0.15);
    $("passes").textContent = count(passes);
    $("rescues").textContent = count(passes * 0.02);
  };
  ["airfare", "unit", "takeup"].forEach(id => $(id).addEventListener("input", update));
  $("takeupPresets").addEventListener("click", e => {
    if (!e.target.dataset.v) return;
    $("takeup").value = e.target.dataset.v;
    update();
  });
  update();
}

// Carousels on the card issuers page: one step at a time, with buttons and step tabs
document.querySelectorAll(".carousel").forEach(car => {
  const track = car.querySelector(".car-track");
  const slides = [...track.children];
  const nav = document.createElement("div");
  nav.className = "car-nav";
  const prev = Object.assign(document.createElement("button"), { className: "arrow", innerHTML: "&larr;", ariaLabel: "Previous step" });
  const next = Object.assign(document.createElement("button"), { className: "arrow", innerHTML: "&rarr;", ariaLabel: "Next step" });
  const steps = document.createElement("div");
  steps.className = "car-steps";
  const count = document.createElement("span");
  count.className = "car-count";
  const tabs = slides.map((s, i) => {
    const b = document.createElement("button");
    b.textContent = `${i + 1}. ${s.querySelector("h3").textContent}`;
    b.addEventListener("click", () => go(i));
    steps.append(b);
    return b;
  });
  nav.append(prev, steps, count, next);
  car.append(nav);
  let current = 0;
  const go = i => track.scrollTo({ left: Math.max(0, Math.min(i, slides.length - 1)) * track.clientWidth });
  const mark = () => {
    current = Math.round(track.scrollLeft / track.clientWidth);
    tabs.forEach((t, i) => t.setAttribute("aria-current", i === current));
    slides.forEach((s, i) => s.setAttribute("aria-hidden", i !== current));
    prev.disabled = current === 0;
    next.disabled = current === slides.length - 1;
    count.textContent = `${current + 1} of ${slides.length}`;
  };
  prev.addEventListener("click", () => go(current - 1));
  next.addEventListener("click", () => go(current + 1));
  track.addEventListener("scroll", () => requestAnimationFrame(mark), { passive: true });
  window.addEventListener("resize", () => go(current));
  mark();
});
