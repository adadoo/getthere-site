// Copy buttons
document.querySelectorAll("[data-copy]").forEach(btn => {
  btn.addEventListener("click", () => copy(btn.dataset.copy, btn));
});

// A tick and Copied once copied, as on the app's traveller page. Where the browser won't use the clipboard
// API, a hidden field holding the text is copied instead.
async function copyText(text) {
  try { await navigator.clipboard.writeText(text); return; } catch (e) {}
  const t = document.createElement("textarea");
  t.value = text; t.setAttribute("readonly", ""); t.style.cssText = "position:fixed;opacity:0";
  document.body.append(t); t.select(); document.execCommand("copy"); t.remove();
}
function copy(text, btn) {
  copyText(text).then(() => {
    btn.classList.add("copied"); btn.setAttribute("aria-label", "Copied");
    setTimeout(() => { btn.classList.remove("copied"); btn.setAttribute("aria-label", "Copy the address"); }, 2000);
  });
}

// Mail-app tabs in the home page's How to forward it
document.querySelectorAll(".tabs button").forEach(tab => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".tabs button").forEach(t => t.setAttribute("aria-selected", t === tab));
    document.querySelectorAll(".tabpanel").forEach(p => p.hidden = p.id !== "tab-" + tab.dataset.tab);
  });
});

// Pass fee calculator on the card issuers and underwriters pages
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
      ["share", "passes", "rescues", "pool", "rescueMoney"].forEach(id => $(id) && ($(id).textContent = "–"));
      return;
    }
    const passes = airfare / 500 * takeup;
    const fees = airfare * takeup * 0.075;
    $("share").textContent = money(fees);
    $("passes").textContent = count(passes);
    $("rescues").textContent = count(passes * 0.02);
    if ($("pool")) $("pool").textContent = money(fees * 0.4);              // after rescue money, card costs and the platform fee
    if ($("rescueMoney")) $("rescueMoney").textContent = money(fees * 0.4);
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
    if (s.hasAttribute("data-optional")) b.append(Object.assign(document.createElement("span"), { className: "opt", textContent: "optional" }));
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

// Airlines and travel sites we read bookings from, live from the app (learned ones included)
const airlineList = document.querySelector("[data-airlines]");
if (airlineList) {
  fetch("https://my.getthere.now/airlines.json").then(r => r.ok ? r.json() : Promise.reject()).then(data => {
    if (!data.airlines || !data.airlines.length) return;
    airlineList.replaceChildren(...data.airlines.map(a => {
      const el = document.createElement("span");
      el.className = "airline";
      if (a.code) {
        const code = document.createElement("span");
        code.className = "code";
        code.textContent = a.code;
        el.append(code);
      }
      el.append(a.name);
      return el;
    }));
    document.querySelectorAll("[data-airlines-line]").forEach(el => el.textContent = data.line);
  }).catch(() => {});   // keep the list in the page
}

// The website's own server (server/server.py), which holds the Direct partner's key.
const SITE_SERVER = "https://getthere-site-server.onrender.com";

// The Direct partner's settings the home page quotes (hours, plans, countries, booking values), from
// the app through the website's server (GET /settings: the app keeps them behind the partner key, Dadoo
// 2026-10-14), so the website says what the app's pages and the terms say. Each [data-setting] keeps
// the value it was written with if the server can't be reached.
const settingSpots = document.querySelectorAll("[data-setting]");
if (settingSpots.length) {
  fetch(SITE_SERVER + "/settings").then(r => r.ok ? r.json() : Promise.reject()).then(s => {
    settingSpots.forEach(el => {
      const v = s[el.dataset.setting];
      if (typeof v === "string" && v) el.textContent = v;
    });
    showPlans(s);
  }).catch(() => {});
}

// The Direct partner's plans, as the app's pages show them: each plan's name and badge, and its note
// ("Coverage set from your fare and flights", "1.5x the coverage of Basic"). The featured one is highlighted.
function showPlans(s) {
  if (!Array.isArray(s.plans) || !s.plans.length || !Array.isArray(s.plan_notes)) return;
  document.querySelectorAll("[data-plans]").forEach(box => {
    box.replaceChildren(...s.plans.map((p, i) => {
      const el = document.createElement("div");
      el.className = "plan" + ((p.featured ?? i === 0) ? " featured" : "");
      const name = document.createElement("div");
      name.className = "name";
      name.textContent = p.label;
      if (p.badge) name.append(Object.assign(document.createElement("span"), { className: "badge", textContent: p.badge }));
      const note = Object.assign(document.createElement("div"), { className: "note", textContent: s.plan_notes[i] || "" });
      el.append(name, note);
      return el;
    }));
  });
}

// The forward address on the home page: the website is the Direct partner's app, so it gets a new
// offer from the partner API through its own server (server/server.py holds the key), as a card
// issuer's app does. The offer's code rides in the address, so a booking forwarded from here is traced
// to this visit, with this page's utm_* tags and referring site, in the admin's Offers. Kept for the
// visit, so a reload isn't a second offer. The plain address stays if the server can't be reached.
const forwardSpots = document.querySelectorAll("[data-forward]");
if (forwardSpots.length) {
  // The page shows the plain quote@ address, easier on the eye; only a copy carries the +code (Dadoo,
  // 2026-10-14). The shown address can't be selected: tapping anywhere on it copies what the Copy button
  // does. Typed by hand, the plain address still gets a price, counted as a plain forward.
  const btn = document.querySelector("[data-forward-copy]");
  document.querySelectorAll(".addr").forEach(box => box.addEventListener("click", e => {
    if (!e.target.closest(".copy")) btn.click();
  }));
  document.querySelectorAll("b.fwd").forEach(el => el.addEventListener("click", () => {
    copyText(btn.dataset.copy).then(() => { el.classList.add("copied"); setTimeout(() => el.classList.remove("copied"), 2000); });
  }));
  const show = offer => {
    document.querySelectorAll("[data-forward-copy]").forEach(el => el.dataset.copy = offer.forward_to);
    document.querySelectorAll("[data-reference]").forEach(el => el.textContent = offer.reference);
    document.querySelectorAll("[data-reference-line]").forEach(el => el.hidden = false);
  };
  let kept = null;
  try { kept = JSON.parse(sessionStorage.getItem("getthere.offer")); } catch (e) {}
  if (kept && kept.forward_to) {
    show(kept);
  } else {
    const tags = new URLSearchParams();
    const page = new URLSearchParams(location.search);
    ["utm_source", "utm_medium", "utm_campaign", "src"].forEach(k => { if (page.get(k)) tags.set(k, page.get(k)); });
    if (document.referrer && new URL(document.referrer).host !== location.host) tags.set("ref", document.referrer);
    fetch(SITE_SERVER + "/offer?" + tags, { method: "POST" })
      .then(r => r.ok ? r.json() : Promise.reject())
      .then(offer => {
        if (!offer.forward_to) return;
        show(offer);
        try { sessionStorage.setItem("getthere.offer", JSON.stringify(offer)); } catch (e) {}
      }).catch(() => {});
  }
}

// The header's menu button on narrow screens (nav.css): opens and closes the list of audiences.
document.querySelectorAll(".menu-btn").forEach(btn => {
  const header = btn.closest("header");
  const set = open => { header.classList.toggle("open", open); btn.setAttribute("aria-expanded", open); };
  btn.addEventListener("click", () => set(!header.classList.contains("open")));
  header.querySelectorAll(".menu a").forEach(a => a.addEventListener("click", () => set(false)));
  document.addEventListener("keydown", e => { if (e.key === "Escape") set(false); });
});
