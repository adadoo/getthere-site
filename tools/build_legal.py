"""Build the website's legal pages from what export_channels.py exported:

  terms.html      the Direct channel's terms, word for word as the app serves them
                  (my.getthere.now/terms.html). Other channels' terms live only on
                  their own addresses, never on this website.
  privacy.html    the one Privacy Notice for every channel

    python3 tools/build_legal.py
"""

import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "tools" / "channels.json").read_text())
G = DATA["global"]
PASS = DATA["pass_name"]

import datetime as _dt
EFFECTIVE_ISO = DATA["terms_effective"]          # the app's brand.TERMS_EFFECTIVE
EFFECTIVE = _dt.date.fromisoformat(EFFECTIVE_ISO).strftime("%-d %B %Y")
STATUS = "Draft for legal review"
OPERATOR = "GetThere"          # replace with the legal entity once it's set up
GOVERNING_LAW = "Singapore"

CHANNEL_PAGE = {"direct": "Direct (my.getthere.now)"}


def hours(n):
    return f"{n:g} hour" + ("" if n == 1 else "s")


def money(v):
    return f"{v:,.0f}"


def mult(x):
    return f"{x:g}"


def label(c):
    return CHANNEL_PAGE.get(c["code"], f"{c['name']} customers ({c['host']})")


def service_name(c):
    return f"GetThere for {c['partner_name']}" if c["partner_name"] else "GetThere"


def page(title, description, body, depth=1):
    up = "../" * depth
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(description)}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%230f766e'/%3E%3Cpath d='M7 18l18-7-7 16-3-6z' fill='white'/%3E%3C/svg%3E">
<link rel="stylesheet" href="{up}styles.css">
</head>
<body>
<header class="site">
  <div class="wrap">
    <a class="logo" href="{up}./">Get<span>There</span></a>
    <nav class="links">
      <a class="hide-sm" href="{up}./">For travellers</a>
      <a href="{up}issuers.html">For card issuers</a>
      <a class="pill" href="{up}terms.html">Terms</a>
    </nav>
  </div>
</header>
<section>
  <div class="wrap narrow legal-doc">
{body}
  </div>
</section>
<footer class="site">
  <div class="wrap">
    <div>
      <a class="logo" href="{up}./">Get<span>There</span></a>
      <p style="margin-top:10px;max-width:320px">Don't miss a single moment of your trip.</p>
    </div>
    <div class="cols">
      <div><b style="color:#fff">Travellers</b><a href="{up}./#forward">Get a price</a><a href="{up}./#faq">FAQ</a></div>
      <div><b style="color:#fff">Legal</b><a href="{up}terms.html">Terms</a><a href="{up}privacy.html">Privacy</a></div>
    </div>
    <div class="legal">© 2026 GetThere.</div>
  </div>
</footer>
</body>
</html>
"""


def terms():
    """The Direct channel's terms, exactly as the app serves them."""
    t = DATA["direct_terms"]
    body = (ROOT / "tools" / "direct_terms.html").read_text()
    note = (f'<p class="doc-meta">These are the terms for passes bought by forwarding to quote@my.getthere.now. '
            f'They are also at <a href="{t["current_url"]}">{t["current_url"]}</a>. If you bought through a bank or an '
            f'airline, the terms linked from your emails apply.</p>')
    return page(f"{PASS} terms · {t['version']}", f"Terms and conditions for the {PASS}.", body + note, depth=0)


def privacy():
    help_ = '<a href="mailto:help@my.getthere.now">help@my.getthere.now</a>'
    banks = [c for c in DATA["channels"] if c["partner_name"] and (c["purchase_match"] or c["app_push"])]
    bank_items = ""
    for c in banks:
        p = escape(c["partner_name"])
        uses = []
        if c["purchase_match"]:
            uses.append(f"to confirm the booking was paid with your {p} card: we send only your email address, the airline, "
                        f"the amount, the currency and the booking date range, and {p} answers yes or no, sharing no "
                        "transaction data with us")
        if c["app_push"]:
            uses.append(f"to show alerts about your pass in {p}'s app: we send your email address and the alert's wording "
                        "and link, and you can turn these alerts off in the app")
        bank_items += f"<li><b>{p}</b>, if you bought through {escape(c['host'])}: " + "; and ".join(uses) + ".</li>"
    bank_section = (f"""
    <h2>5. If you bought through a bank</h2>
    <p>Some banks offer the {PASS} to their customers. The bank is a separate organisation with its own privacy notice.
    We share data with it only as follows:</p>
    <ul>{bank_items}</ul>""" if bank_items else "")
    n = 6 if bank_items else 5
    body = f"""
    <p class="eyebrow">Privacy notice</p>
    <h1>How we use your data</h1>
    <p class="doc-meta">Every channel · Effective {EFFECTIVE} · <span class="draft">{STATUS}</span><br>
    Your terms are linked from every email we send you.</p>

    <div class="callout key">
      <b>The short version.</b> We use the booking you forward to price your pass, watch your flights and send your
      card. We don't sell your data and we don't send you marketing.
    </div>

    <h2>1. Who we are</h2>
    <p>{OPERATOR} ("we", "us") runs the {PASS}, including when it's offered under a partner's name such as
    "GetThere for &lt;partner&gt;", and is responsible for the personal data described here. Contact us at {help_},
    or at the help address in any email we've sent you.</p>

    <h2>2. What we collect</h2>
    <ul>
      <li><b>The booking email you forward</b>, including its attachments: the names of the travellers, the booking
      reference, flights, fare and taxes, and anything else the airline put in it, such as contact details or the last
      digits of the card used.</li>
      <li>Your <b>name and email address</b>, from the email you forward.</li>
      <li>Your <b>mobile number</b>, if you give it at checkout so we can send your card there.</li>
      <li><b>Payment details</b>, handled by our payment provider. We don't see or store your full card number.</li>
      <li><b>Your rebooking card's use</b>: where it was used, the amount and when.</li>
      <li><b>Flight status</b> for your flights, from flight-data providers.</li>
      <li>Delivery records for the messages we send you, and basic technical logs.</li>
    </ul>

    <h2>3. Why we use it</h2>
    <ul>
      <li>To price your pass and decide whether we can offer one, including checks that the booking and fare are real.</li>
      <li>To watch your flights and send your card when a flight is delayed or cancelled.</li>
      <li>To send you your price, pass, alerts and card, and to answer your questions.</li>
      <li>To prevent fraud and misuse, and to meet legal and accounting obligations.</li>
    </ul>
    <p>We use your data because it's needed to provide the service you ask for, for our legitimate interest in
    preventing fraud, and where the law requires it.</p>

    <h2>4. Who we share it with</h2>
    <ul>
      <li>Service providers who work for us under contract: hosting (Render, servers in Singapore), file storage,
      email delivery (Postmark), messaging (WhatsApp and text messages, through Twilio), payments and card issuing,
      and flight data (FlightAware).</li>
      <li>The airline, to check your booking is still active before we send a card.</li>
      <li>Authorities, when the law requires it.</li>
    </ul>
    <p>We don't sell your data or use it for advertising.</p>
    {bank_section}

    <h2>{n}. Where it's stored</h2>
    <p>Our servers are in Singapore. Some of our providers may process data in other countries; when they do, we use
    contracts that protect it.</p>

    <h2>{n + 1}. How long we keep it</h2>
    <ul>
      <li>Links in our emails to your pass and card keep working for 12 months after your trip, then stop.</li>
      <li>We keep booking emails and booking data for 12 months after your last flight, then delete them.</li>
      <li>We keep payment and card records for as long as the law requires.</li>
    </ul>

    <h2>{n + 2}. Your choices and rights</h2>
    <p>You can ask us for a copy of your data, to correct it, or to delete it, by emailing {help_}. Depending on where
    you live, you may also have the right to object to some uses or to complain to your data-protection regulator.</p>
    <p>Forward a booking only if you are a traveller on it or have the travellers' agreement to share their details with us.</p>

    <h2>{n + 3}. Cookies</h2>
    <p>Our pages don't use cookies for tracking or advertising.</p>

    <h2>{n + 4}. Changes</h2>
    <p>We'll post any changes to this notice on this page with a new effective date.</p>
"""
    return page("Privacy notice · GetThere", "How GetThere uses your data, on every channel.", body, depth=0)


(ROOT / "terms.html").write_text(terms())
(ROOT / "privacy.html").write_text(privacy())
print("built terms.html", DATA["direct_terms"]["version"], "and privacy.html")
