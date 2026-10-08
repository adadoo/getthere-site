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

// Channel setup form on the banks page
const form = document.getElementById("cfg");
if (form) channelSetup();

function channelSetup() {
  const $ = id => document.getElementById(id);
  const MULTIPLIERS = [1, 1.5, 2, 2.5, 3];
  const tiersEl = $("tiers");
  let tiers = [
    { label: "Basic", blurb: "Covers most same-day fares", cap: 1.5, badge: "RECOMMENDED", featured: true },
    { label: "Plus", blurb: "Room for last-minute prices", cap: 2, badge: "", featured: false },
  ];

  const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const py = s => JSON.stringify(String(s));
  const hex = s => /^#[0-9a-fA-F]{6}$/.test(s) ? s.toLowerCase() : null;
  const handle = () => ($("handle").value.toLowerCase().replace(/[^a-z0-9-]/g, "") || "yourbank");

  function drawTiers() {
    tiersEl.innerHTML = tiers.map((t, i) => `
      <div class="tier">
        <div class="row3">
          <div class="field"><label>Plan name</label><input type="text" data-i="${i}" data-k="label" value="${esc(t.label)}"></div>
          <div class="field"><label>Card size</label><select data-i="${i}" data-k="cap">${MULTIPLIERS.map(m =>
            `<option value="${m}" ${m === t.cap ? "selected" : ""}>${m}× fare</option>`).join("")}</select></div>
          <div class="field"><label>Badge</label><input type="text" data-i="${i}" data-k="badge" value="${esc(t.badge)}" placeholder="optional"></div>
        </div>
        <div class="field"><label>One line under the plan</label><input type="text" data-i="${i}" data-k="blurb" value="${esc(t.blurb)}"></div>
        <div class="btns" style="gap:16px">
          <label class="fine" style="font-weight:600"><input type="radio" name="featured" data-i="${i}" data-k="featured" ${t.featured ? "checked" : ""}> Highlight this plan</label>
          ${tiers.length > 1 ? `<button type="button" class="copy" data-remove="${i}">Remove</button>` : ""}
        </div>
      </div>`).join("");
    $("addTier").style.display = tiers.length >= 3 ? "none" : "";
  }

  tiersEl.addEventListener("input", e => {
    const { i, k } = e.target.dataset;
    if (i === undefined) return;
    if (k === "featured") tiers.forEach((t, j) => t.featured = j === +i);
    else tiers[i][k] = k === "cap" ? parseFloat(e.target.value) : e.target.value;
    update();
  });
  tiersEl.addEventListener("click", e => {
    if (e.target.dataset.remove === undefined) return;
    tiers.splice(+e.target.dataset.remove, 1);
    if (!tiers.some(t => t.featured)) tiers[0].featured = true;
    drawTiers(); update();
  });
  $("addTier").addEventListener("click", () => {
    tiers.push({ label: "Premium", blurb: "Business-class headroom", cap: 3, badge: "", featured: false });
    drawTiers(); update();
  });

  // Colour pickers and their text boxes stay in step
  ["accent", "ink", "soft"].forEach(k => {
    $(k + "Pick").addEventListener("input", e => { $(k).value = e.target.value; update(); });
    $(k).addEventListener("input", e => { if (hex(e.target.value)) $(k + "Pick").value = e.target.value; update(); });
  });

  let fontLink;
  function loadFont(name) {
    if (!name) return;
    if (!fontLink) { fontLink = document.createElement("link"); fontLink.rel = "stylesheet"; document.head.appendChild(fontLink); }
    fontLink.href = "https://fonts.googleapis.com/css2?family=" + encodeURIComponent(name).replace(/%20/g, "+") + ":wght@400;600;700;800&display=swap";
  }

  function settings() {
    const v = id => $(id).value.trim();
    return {
      name: v("name") || "Your Bank", handle: handle(), logo: v("logo"),
      accent: hex(v("accent")) || "#0f766e", ink: hex(v("ink")) || "#14213d", soft: hex(v("soft")) || "#e6f4f2",
      font: v("font"), radius: +v("radius"), btnRadius: +v("btnradius"),
      trigger: +v("trigger"), tech: v("tech"),
      matchUrl: v("matchurl"), pushUrl: v("pushurl"), mtls: $("mtls").checked,
    };
  }

  // The channel as it would be written in the app's channels.py
  function channelCode(s) {
    const code = s.handle.replace(/-/g, "_");
    const tierLines = tiers.map(t => {
      const tcode = (t.label.toLowerCase().replace(/[^a-z0-9]+/g, "_").replace(/^_|_$/g, "") || "plan");
      let line = `            Tier(${py(tcode)}, ${py(t.label)}, ${py(t.blurb)}, ${t.cap}`;
      if (t.featured) line += ", featured=True";
      if (t.badge.trim()) line += `, badge=${py(t.badge.trim().toUpperCase())}`;
      return line + "),";
    }).join("\n");
    const b = [
      `            partner_name=${py(s.name)},`,
      s.logo && `            partner_logo_url=${py(s.logo)},`,
      s.font && `            font_family=${py(s.font)},`,
      s.radius !== 18 && `            corner_radius=${s.radius},`,
      s.btnRadius !== 26 && `            button_radius=${s.btnRadius},`,
      `            ink=${py(s.ink)},`,
      `            accent=${py(s.accent)},`,
      `            accent_soft=${py(s.soft)},`,
    ].filter(Boolean).join("\n");
    return [
      `    ${py(code)}: Channel(`,
      `        code=${py(code)},`,
      `        version=1,`,
      `        name=${py(s.name)},`,
      `        host=f"${s.handle}.{DOMAIN}",`,
      `        tiers=(`,
      tierLines,
      `        ),`,
      `        pricing=PricingModel(partner_commission=0.0),   # from the agreement`,
      s.trigger !== 180 && `        rules=Rules(trigger_delay_minutes=${s.trigger}),`,
      s.matchUrl && `        partner_api_url=${py(s.matchUrl)},`,
      s.pushUrl && `        push_url=${py(s.pushUrl)},`,
      `        branding=Branding(`,
      b,
      `        ),`,
      `    ),`,
    ].filter(Boolean).join("\n");
  }

  function update() {
    const s = settings();
    const host = `${s.handle}.getthere.now`;
    const p = $("preview").style;
    p.setProperty("--p-accent", s.accent); p.setProperty("--p-ink", s.ink); p.setProperty("--p-soft", s.soft);
    p.setProperty("--p-r", s.radius + "px"); p.setProperty("--p-btn", s.btnRadius + "px");
    p.setProperty("--p-font", s.font ? `"${s.font}", sans-serif` : "");
    loadFont(s.font);

    $("pLogo").innerHTML = `Get<span>There</span><small>×</small>` +
      (s.logo ? `<img src="${esc(s.logo)}" alt="${esc(s.name)}" style="height:22px;vertical-align:middle">` : esc(s.name));
    const hrs = s.trigger / 60;
    $("pIntro").textContent = `If your flight is ${hrs}+ hours late or cancelled, we send you a card preloaded with money for a new flight on any airline.`;
    const fare = 1134;
    $("pPlans").innerHTML = tiers.map(t => `
      <div class="pplan ${t.featured ? "f" : ""}">
        <span><b>${esc(t.label)}</b>${t.badge.trim() ? `<span class="pbadge">${esc(t.badge.trim().toUpperCase())}</span>` : ""}<br>
        <span style="font-size:12px;color:#5c6b80">${esc(t.blurb)} · card S$${Math.round(fare * t.cap).toLocaleString()}</span></span>
        <b>S$${Math.round(8 + 11 * t.cap)}</b>
      </div>`).join("");
    $("pFine").textContent = `Questions? help@${host}`;
    $("pAddr").textContent = `quote@${host}`;
    $("pHost").textContent = host;

    const extra = [
      s.tech && `# Technical contact (keys): ${s.tech}`,
      s.mtls && `# Mutual TLS required on calls to the bank`,
    ].filter(Boolean).join("\n");
    $("out").value = channelCode(s) + (extra ? "\n" + extra : "");

    const body = `Hello GetThere,\n\nHere are our channel settings for ${s.name}.\n\n${$("out").value}\n`;
    $("send").href = `mailto:partners@getthere.now?subject=${encodeURIComponent("Channel setup: " + s.name)}&body=${encodeURIComponent(body)}`;
  }

  form.addEventListener("input", update);
  form.addEventListener("change", update);
  $("copyOut").addEventListener("click", e => copy($("out").value, e.target));
  drawTiers();
  update();
}
