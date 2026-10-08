"""Build the Terms and Privacy pages from tools/channels.json (see
export_channels.py). Writes:

  terms/<code>/<effective>-v<channel version>.html   one page per terms version. The app
      records this URL on every policy sold, so once published it never changes: the
      build refuses to overwrite one with different content. Change the wording by
      bumping brand.TERMS_EFFECTIVE in the app (and EFFECTIVE below), then re-export.
  terms/<code>.html     the current version, for the website's own links
  privacy.html          one privacy policy for every channel
  legal.html            the list of channels

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
      <a href="{up}banks.html">For card issuers</a>
      <a class="pill" href="{up}legal.html">Legal</a>
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
      <div><b style="color:#fff">Legal</b><a href="{up}terms/direct.html">Terms</a><a href="{up}privacy.html">Privacy</a><a href="{up}legal.html">All channels</a></div>
    </div>
    <div class="legal">© 2026 GetThere.</div>
  </div>
</footer>
</body>
</html>
"""


def version_id(c):
    return f"{EFFECTIVE_ISO}-v{c['version']}"


def meta(c):
    return (f'<p class="doc-meta">{escape(label(c))} · Version {version_id(c)} · Effective {EFFECTIVE}'
            f' · <span class="draft">{STATUS}</span><br>'
            f'If you bought a pass, the terms linked from your pass and emails are the ones that apply to it. '
            f'How we use your data is in our <a href="{{up}}privacy.html">Privacy Policy</a>.</p>')


def value_table(c):
    rows = "".join(
        f"<tr><td>{cur}</td><td>{money(lo)}</td><td>{money(c['max_booking_value'].get(cur, 0))}</td></tr>"
        for cur, lo in c["min_booking_value"].items())
    return ('<div class="table-scroll"><table><tr><th>Currency</th><th>Smallest booking</th><th>Largest booking</th></tr>'
            f"{rows}</table></div>")


def terms(c, depth=1):
    svc = escape(service_name(c))
    partner = c["partner_name"]
    trig = hours(c["trigger_minutes"] / 60)
    tiers = "".join(f"<li><b>{escape(t['label'])}</b>: a card for up to {mult(t['cap'])} times the fare you paid.</li>"
                    for t in c["tiers"])
    help_ = f'<a href="mailto:{c["support_email"]}">{c["support_email"]}</a>'
    excluded = (f" We don't offer passes for flights to or from {', '.join(c['excluded_airports'])}."
                if c["excluded_airports"] else "")
    partner_intro = (
        f"<p>{escape(partner)} introduces the {PASS} to its customers. {OPERATOR} provides the service and is "
        f"responsible for it under these terms. {escape(partner)} is not a party to your agreement with us."
        + (f" Some of the {PASS}'s alerts may reach you in {escape(partner)}'s app." if c["app_push"] else "")
        + "</p>" if partner else "")
    messages = ["by email to the address you forwarded your booking from"]
    if c["phone_required"]:
        messages.append("by WhatsApp, or text message if WhatsApp isn't available, to the mobile number you give us at checkout")
    if c["app_push"]:
        messages.append(f"as notifications in {escape(partner or 'your bank')}'s app, if you use it")
    topup = (f"<li>If the new flight costs more than the card holds, you can add your own money to the card. "
             f"Anything you add and don't spend is refunded to you when the card closes.</li>" if c["allow_topup"] else "")
    takeoff = ("<p>When each covered flight takes off on time, we'll email you to say your pass for that flight is complete.</p>"
               if c["takeoff_signoff"] else "")
    body = f"""
    <p class="eyebrow">Terms and conditions</p>
    <h1>{PASS} terms</h1>
    {meta(c).replace("{up}", "../" * depth)}

    <div class="callout key">
      <b>The short version.</b> If a flight on your booking is {trig} or more late, or cancelled, we send you a virtual card
      to book a new flight on any airline. <b>The card buys new flights only and is never paid out as cash.</b>
      Buy at least {hours(G['sales_close_hours'])} before your first flight.
    </div>

    <h2>1. Who we are</h2>
    <p>These terms are an agreement between you and {OPERATOR} ("we", "us"), which runs the {PASS} as {svc}.
    You can reach us at {help_}.</p>
    {partner_intro}

    <h2>2. What the {PASS} is</h2>
    <p>The {PASS} is a paid rebooking service. If a covered flight is badly delayed or cancelled, we give you a
    single-use virtual payment card, funded by us, to buy a new flight. It is not an insurance policy, and it does
    not replace any rights you have against the airline, such as refunds, care or compensation under
    passenger-rights laws.</p>
    <p><b>The card buys new flights only and is never paid out as cash.</b> Any amount you don't spend is not paid to you.</p>

    <h2>3. Getting a price</h2>
    <ul>
      <li>Forward the booking confirmation or e-ticket email your airline sent you to
      <a href="mailto:{c['forward_to']}">{c['forward_to']}</a>. We read bookings from the airlines listed on our website.</li>
      <li>We reply by email with a price for each plan. A price holds for {hours(G['quote_valid_hours'])}, or until sales
      close if that's sooner. After that, forward the booking again for a new price.</li>
      <li>Sales close {hours(G['sales_close_hours'])} before the first flight on the booking.</li>
      <li>We can decline to offer a pass. We do this when the booking is outside the values below; the fare is more than
      {mult(G['max_fare_vs_market'])} times the usual highest fare for those flights; we can't find the flights in the
      airline's schedule or confirm the booking; disruption on the travel date is already very likely; a traveller on the
      booking has received {G['max_claims_per_year']} or more cards in the last 12 months; or you have bought passes for more
      than {c['max_other_people_bookings_per_year']} bookings in the last 12 months that you're not travelling on.{excluded}
      We'll email you if we decline.</li>
    </ul>
    {value_table(c)}

    <h2>4. Buying a pass</h2>
    <p>You choose one plan:</p>
    <ul>{tiers}</ul>
    <p>"The fare you paid" is the total shown on your booking for its flights and taxes, in the booking's currency.
    One pass covers every flight and every traveller on the booking you forwarded. You pay by card at checkout.
    {"We ask for a mobile number at checkout so we can send your card there. " if c["phone_required"] else ""}
    The information you give us, and the booking you forward, must be real and accurate.</p>

    <h2>5. When you get a card</h2>
    <ul>
      <li>We start watching each covered flight {hours(c['watch_from_hours'])} before its scheduled departure.</li>
      <li>You get a card if a covered flight departs {trig} or more after its scheduled time, or is cancelled by the airline.
      "Scheduled time" is the airline's time for the flight when we start watching it.</li>
      <li>If the airline changes the time of a flight before we start watching it, your pass moves to the new time.
      We'll email you. A schedule change like this is not a delay.</li>
      <li>One pass gives one card, for the first covered flight that is delayed or cancelled. The card is sent to the
      person who bought the pass.</li>
      <li>Before we issue a card, we may check with the airline that the booking is still active. If the airline tells us
      it was cancelled or never existed, no card is issued and the pass ends.</li>
      <li>Once a card is issued, it stands, even if the airline later shortens the delay.</li>
    </ul>
    <p>You don't get a card for a delay shorter than {trig}, a flight you miss or don't take, a booking you cancel or
    change yourself, or a flight that isn't on the booking you forwarded.</p>

    <h2>6. Using the card</h2>
    <ul>
      <li>The card holds up to your plan's multiple of the fare you paid. We tell you the amount when we send it.</li>
      <li>It works for {hours(G['card_validity_hours'])} from when we send it, at airlines and travel agencies only.</li>
      <li>It works for one purchase, then closes. Book everything you need for the rest of the trip, such as
      connections or a return, in that one purchase.</li>
      {topup}
      <li>Any amount left on the card when it closes or expires is not refunded or paid out.</li>
      <li>Airlines often cancel the rest of a booking when you don't take a flight on it. When we send your card we'll
      tell you if later flights on your booking are at risk, so you can rebook them too.</li>
    </ul>

    <h2>7. How we contact you</h2>
    <p>We send your price, your pass, alerts and your card {"; ".join(messages)}.</p>
    {takeoff}

    <h2>8. Changes and refunds</h2>
    <ul>
      <li>You can cancel your pass for a full refund until we start watching your first flight. Email {help_}.</li>
      <li>If you are charged twice for the same booking, we refund the second payment.</li>
      <li>If you change or cancel your booking with the airline, tell us. The pass doesn't move to a new booking.</li>
    </ul>

    <h2>9. Fair use</h2>
    <p>If we reasonably believe a booking, a claim or a card purchase is false or fraudulent, we can refuse a pass,
    end it without a card, stop a card, and recover any amount wrongly paid. We may also refuse future passes.</p>

    <h2>10. Our responsibility to you</h2>
    <p>We are responsible for providing the service as described in these terms. We are not responsible for what airlines
    or travel agencies do, including whether seats are available or what they charge. To the extent the law allows,
    our total liability to you for a pass is limited to the fee you paid for it plus the card amount it promised.
    Nothing in these terms limits rights you have under consumer law that can't be limited.</p>

    <h2>11. Changes to these terms</h2>
    <p>We may update these terms. A pass you've already bought stays under the terms in force when you bought it.</p>

    <h2>12. Law</h2>
    <p>These terms are governed by the laws of {GOVERNING_LAW}. Before going to court, please contact us at {help_}
    so we can try to put things right.</p>
"""
    return page(f"{PASS} terms · {label(c)} · {version_id(c)}", f"Terms and conditions for the {PASS}, {label(c)}.",
                body, depth=depth)


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
    <p class="eyebrow">Privacy policy</p>
    <h1>How we use your data</h1>
    <p class="doc-meta">Every channel · Effective {EFFECTIVE} · <span class="draft">{STATUS}</span><br>
    Terms for each channel are listed on the <a href="legal.html">legal page</a>.</p>

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
      <li>Links in our emails to your pass and card stop working 30 days after your trip or your card ends.</li>
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
    <p>We'll post any changes to this policy on this page with a new effective date.</p>
"""
    return page("Privacy policy · GetThere", "How GetThere uses your data, on every channel.", body, depth=0)


def index():
    rows = "".join(
        f'<tr><td>{escape(label(c))}</td><td><a href="terms/{c["code"]}.html">Terms</a></td>'
        '</tr>' for c in DATA["channels"])
    body = f"""
    <p class="eyebrow">Legal</p>
    <h1>Terms and privacy</h1>
    <p class="muted">Each place you can buy the {PASS} has its own terms, built from that channel's plans and rules. If you forwarded your booking to quote@my.getthere.now, the Direct pages apply.</p>
    <div class="table-scroll"><table><tr><th>Where you bought</th><th></th></tr>{rows}</table></div>
    <p style="margin-top:24px">One <a href="privacy.html">Privacy Policy</a> covers every channel.</p>
"""
    return page("Terms and privacy · GetThere", "Terms and privacy policies for every GetThere channel.", body, depth=0)


for c in DATA["channels"]:
    (ROOT / "terms" / c["code"]).mkdir(parents=True, exist_ok=True)
    (ROOT / "terms" / f"{c['code']}.html").write_text(terms(c))
    versioned = ROOT / "terms" / c["code"] / f"{version_id(c)}.html"
    html = terms(c, depth=2)
    if versioned.exists() and versioned.read_text() != html:
        raise SystemExit(f"{versioned.relative_to(ROOT)} is already published and policies point at it. "
                         "Bump TERMS_EFFECTIVE (app) or the channel's version instead of changing it.")
    versioned.write_text(html)
(ROOT / "privacy.html").write_text(privacy())
(ROOT / "legal.html").write_text(index())
print("built", ", ".join(f"{c['code']} {version_id(c)}" for c in DATA["channels"]))
