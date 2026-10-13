"""Build the website's Privacy Notice (privacy.html, one for every channel) from
tools/channels.json (see export_channels.py).

The website has no copy of any terms: its Terms links go to the Direct channel's
terms on the app, https://my.getthere.now/terms.html, so they are always the same
page. terms.html, legal.html and terms/direct.html redirect there.

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
# The notice's own changes (offer page visits and their campaign tags, Dadoo 2026-10-12; the Underwriter
# and its card issuing partner as recipients, a partner's pass as the Underwriter's policy, 2026-10-13) take effect on this date, or on the terms' date
# when that is later.
PRIVACY_CHANGED_ISO = "2026-10-13"
EFFECTIVE = _dt.date.fromisoformat(max(EFFECTIVE_ISO[:10], PRIVACY_CHANGED_ISO)).strftime("%-d %B %Y")
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
      <a class="pill" href="https://my.getthere.now/terms.html">Terms</a>
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
      <p style="margin-top:10px;max-width:320px">When your flight is delayed, we help you get there.</p>
    </div>
    <div class="cols">
      <div><b style="color:#fff">Travellers</b><a href="{up}./#forward">Get a price</a><a href="{up}./#faq">FAQ</a></div>
      <div><b style="color:#fff">Legal</b><a href="https://my.getthere.now/terms.html">Terms</a><a href="{up}privacy.html">Privacy</a></div>
    </div>
    <div class="legal">Pre-loaded rescue cards are funded by the company your pass's terms name.<br>© 2026 GetThere.</div>
  </div>
</footer>
</body>
</html>
"""


def privacy():
    help_ = '<a href="mailto:privacy@getthere.now">privacy@getthere.now</a>'
    # Generic: no partner is named, whichever channels exist. Purchase checks and app alerts
    # have no setting (a partner's address turns each on, in the admin), so both are listed.
    bank_items = (
        "\n      <li><b>To confirm the booking was paid with that partner's card:</b> we send only your email address, "
        "the airline, the amount, the currency and the booking date range. The partner answers yes or no and "
        "shares no transaction data with us.</li>"
        "\n      <li><b>To show alerts about your pass in the partner's app:</b> we send your email address and the "
        "alert's wording and link. You can turn these alerts off in the app.</li>")
    bank_section = (f"""
    <h2>5. If you bought through a partner</h2>
    <p>Some partners, such as banks, offer the {PASS} to their customers. The partner is a separate organisation with its own privacy notice.
    If you bought through a partner's GetThere page, we share data with it only as follows:</p>
    <ul>{bank_items}
    </ul>""" if bank_items else "")
    n = 6 if bank_items else 5
    body = f"""
    <p class="eyebrow">Privacy notice</p>
    <h1>How we use your data</h1>
    <p class="doc-meta">For every pass, wherever you bought it · Effective {EFFECTIVE} · <span class="draft">{STATUS}</span><br>
    Your terms are linked from every email we send you.</p>

    <div class="callout key">
      <b>The short version.</b> We use the booking you forward to price your pass, track your flights and send your
      pre-loaded rescue card. We don't sell your data and we don't send you marketing.
    </div>

    <h2>1. Who we are</h2>
    <p>The {PASS} is sold by the company your pass's terms name as selling it and funding your pre-loaded rescue
    cards. On a partner's page, that is the Underwriter, such as an insurer, and the pass is a policy it issues.
    Passes from GetThere's own page are a consumer demo: GetThere does not currently represent a licensed insurer.
    {OPERATOR} ("we", "us") runs the service for that company, including when it's offered under a partner's
    name, and is responsible for the personal data described here. The selling company is also responsible for the
    data it receives (section 4). Contact us at {help_}, or at the help address in any email we've sent you.</p>

    <h2>2. What we collect</h2>
    <ul>
      <li><b>The booking email you forward</b>, including its attachments: the names of the travellers, the booking
      reference, flights, fare and taxes, and anything else the airline put in it, such as contact details or the last
      digits of the card used.</li>
      <li>Your <b>name and email address</b>, from the email you forward.</li>
      <li>Your <b>mobile number</b>, which you give at checkout so we can send your pre-loaded rescue card there. We send a
      code to it on WhatsApp to check it's yours, and we only send you WhatsApp messages once you've entered that code.</li>
      <li>Your <b>legal name, date of birth, home address and the country you live in</b>, which you give at checkout
      so the pre-loaded rescue card can be issued in your name.</li>
      <li><b>Payment details</b>: you type your card details into the payment form of the selling company's payment
      provider, embedded on our checkout page. We never see or store your card number; we get only the payment's
      result and amount.</li>
      <li><b>Your pre-loaded rescue card's use</b>: where it was used, the amount and when.</li>
      <li><b>Flight status</b> for your flights, from flight-data providers.</li>
      <li>When you open an offer page, such as one linked from a partner's app or an ad: your <b>IP address</b>, your
        <b>browser's details</b> (its user agent), the page you came from, any campaign tags in the link you followed
        (where the link was shared and which campaign it belongs to, such as utm_source), and when. A booking you
        forward from that page is linked to the visit.</li>
      <li>Delivery records for the messages we send you, and basic technical logs.</li>
    </ul>

    <h2>3. Why we use it</h2>
    <ul>
      <li>To price your pass and decide whether we can offer one, including checks that the booking and fare are real.</li>
      <li>To track your flights and send your pre-loaded rescue card when a flight is delayed or cancelled.</li>
      <li>To send you your price, pass, alerts and pre-loaded rescue card, and to answer your questions.</li>
      <li>To count how many people see an offer and go on to forward a booking, which links and sites bring them
        there, and to tell real visits apart from automated ones (bots and link previews).</li>
      <li>To prevent fraud and misuse, and to meet legal and accounting obligations.</li>
    </ul>
    <p>We use your data because it's needed to provide the service you ask for, for our legitimate interest in
    preventing fraud, and where the law requires it.</p>

    <h2>4. Who we share it with</h2>
    <ul>
      <li>Service providers who work for us under contract: hosting (Render, servers in Singapore), file storage,
      email delivery (Postmark), messaging (WhatsApp messages, through Twilio), and flight data (FlightAware).</li>
      <li>When you forward a booking from an airline or travel site we haven't seen before, an AI service
      (Anthropic's Claude) reads it for us to find the flights, travellers and fare.</li>
      <li>The company that sells your pass, and its payment provider and card issuer (Airwallex, for passes sold by
      GetThere), receive your legal name, date of birth, home address, email address and mobile number when you buy a
      pass, to take your payment, check your identity (including sanctions screening), and fund and issue the
      pre-loaded rescue card in your name. The card issuer may ask for an identity document if it can't confirm who
      you are.</li>
      <li>The airline, to check your booking is still active before we send a pre-loaded rescue card.</li>
      <li>Authorities, when the law requires it.</li>
    </ul>
    <p>We don't sell your data or use it for advertising.</p>
    {bank_section}

    <h2>{n}. Where it's stored</h2>
    <p>Our servers are in Singapore. Some of our providers may process data in other countries; when they do, we use
    contracts that keep it safe.</p>

    <h2>{n + 1}. How long we keep it</h2>
    <ul>
      <li>Links in our emails to your pass and pre-loaded rescue card keep working for 12 months after your trip, then stop.</li>
      <li>We keep booking emails and booking data for 12 months after your last flight, then delete them.</li>
      <li>We keep offer page visits for 12 months. Then we delete the visit, or, if you forwarded a booking from it,
        delete its IP address, browser details, the page you came from and its campaign tags, and keep only the link
        between your booking and the offer.</li>
      <li>We keep payment and pre-loaded rescue card records for as long as the law requires.</li>
    </ul>

    <h2>{n + 2}. Your choices and rights</h2>
    <p>You can ask us for a copy of your data, to correct it, or to delete it, by emailing {help_}. Depending on where
    you live, you may also have the right to object to some uses or to complain to your privacy regulator.</p>
    <p>Forward a booking only if you are a traveller on it or have the travellers' agreement to share their details with us.</p>

    <h2>{n + 3}. Cookies</h2>
    <p>Our pages don't use cookies for tracking or advertising.</p>

    <h2>{n + 4}. Changes</h2>
    <p>We'll post any changes to this notice on this page with a new effective date.</p>
"""
    return page("Privacy notice · GetThere", "How GetThere uses your data, wherever you bought your pass.", body, depth=0)


(ROOT / "privacy.html").write_text(privacy())
print("built privacy.html")
