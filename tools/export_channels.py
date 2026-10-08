"""Export from the app what the website's legal pages need: each channel's
settings (channels.json, for the Privacy Notice) and the Direct channel's terms
exactly as the app serves them on my.getthere.now (direct_terms.html). Other
channels' terms are only on their own addresses. Run from the site folder after
a channel or the terms wording changes:

    python3 tools/export_channels.py ../getthere     (path to the app checkout)
    python3 tools/build_legal.py
"""

import dataclasses
import json
import sys
from pathlib import Path

app = Path(sys.argv[1] if len(sys.argv) > 1 else "../getthere").resolve()
sys.path.insert(0, str(app))
from getthere import brand, channels, legal, risk  # noqa: E402

R = risk.RISK
out = {
    "product": brand.PRODUCT_NAME,
    "pass_name": brand.PASS_NAME,
    "terms_effective": brand.TERMS_EFFECTIVE,     # with each channel's version, names the terms page
    "global": {
        "sales_close_hours": R.sales_close_hours,
        "quote_valid_hours": R.quote_valid_hours,
        "card_validity_hours": R.card_validity_hours,
        "max_claims_per_year": R.max_claims_per_year,
        "max_fare_vs_market": R.max_fare_vs_market,
        "verify_booking_before_payout": R.verify_booking_before_payout,
    },
    "channels": [],
}
for c in channels.CHANNELS.values():
    r, b = c.rules, c.branding
    out["channels"].append({
        "code": c.code,
        "name": c.name,
        "version": c.version,
        "host": c.host,
        "site_url": c.site_url,
        "forward_to": c.inbound_addresses[0],
        "support_email": c.support_email,
        "from_address": c.from_address,
        "partner_name": b.partner_name,
        "tiers": [{"label": t.label, "cap": t.cap_multiplier} for t in c.tiers],
        "trigger_minutes": r.trigger_delay_minutes,
        "watch_from_hours": r.watch_from_hours,
        "allow_topup": r.allow_topup,
        "phone_required": r.phone_required,
        "takeoff_signoff": r.takeoff_signoff,
        "min_booking_value": r.min_booking_value,
        "max_booking_value": r.max_booking_value,
        "max_other_people_bookings_per_year": r.max_other_people_bookings_per_year,
        "excluded_airports": list(r.excluded_airports),
        "purchase_match": bool(c.partner_api_url),
        "app_push": bool(c.push_url),
    })

direct = channels.CHANNELS["direct"]
out["direct_terms"] = {"url": direct.terms_url, "current_url": f"{direct.site_url}/terms.html",
                       "version": legal.version_id(direct)}
Path(__file__).with_name("direct_terms.html").write_text(legal.body(direct))

dest = Path(__file__).with_name("channels.json")
dest.write_text(json.dumps(out, indent=2) + "\n")
print(f"{len(out['channels'])} channels -> {dest}")
