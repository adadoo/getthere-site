# getthere-site

The GetThere marketing website, served at https://getthere.now by GitHub Pages from the `gh-pages` branch, which
`.github/workflows/publish.yml` copies from `main` on every push. Edit `main`.
Plain HTML, CSS and a little JavaScript; no build step.

| Page | For |
| --- | --- |
| `index.html` | Travellers: what the Flight Delay Pass is and how to forward a booking to `quote@my.getthere.now`. The same page, design and wording as each partner's home and offer page in the app (`getthere/templates/landing.html`); its stylesheet `traveller.css` is the app's `_traveller.css`, kept identical. |
| `issuers.html` | Card issuers: the Flight Delay Pass story from the Head of Cards deck, a pass-fee calculator and the pilot offer. Contact us goes to partner@getthere.now. |
| `underwriters.html` | Underwriters (insurers): why and how to underwrite the Flight Delay Pass on GetThere: the three buckets of risk (what GetThere captures, what the underwriter controls, what each partner decides), exposure limits, claims, the fee split, rolling out to partners, the monthly reports, money and data, getting started. Built from the underwriter concerns list (Claude Doc, 13 Oct 2026); it claims none of the gaps that list names. |
| `travel-sites.html` | Online travel agencies: the Flight Delay Pass on the booking confirmation page, from one partner API call (`POST /partner/v1/quotes` after the booking is confirmed, returning `merchandising_url`, a plans page the site frames or links, whose plans open a checkout filled in with the customer details sent; `POST /partner/v1/checkouts` for a site that shows the plans itself), with the calls documented on the page, a pass-fee calculator and getting started. No airline page: airlines see disruption as a brand negative and won't rebook on other airlines (Dadoo, 14 Oct 2026). |
| `api.html` | API reference for card issuers: the calls a card issuer makes to GetThere and the calls GetThere makes to the card issuer. |
| `404.html` | Page not found, for any address the site doesn't have. |

Phone screens in `images/` come from the Head of Cards deck.

Every page's header lists the four audiences, Traveller, Card Issuer, Online Travel Agency and Underwriter
(Dadoo, 14 Oct 2026), behind a menu button on narrow screens (`nav.css`, opened by `site.js`), and every footer
has a column for each. They're written into the pages by `python3 tools/site_nav.py`: change them there, run it,
and commit the pages.

The website is the Direct partner's app. Like a card issuer's app, it gets each visitor's forward address
from GetThere's partner API (`GET /partner/v1/offer`), with the page's utm tags and referring site, so a booking
forwarded from the site is traced to that visit in the admin's Offers. The partner key is a secret, so a small
server holds it: `server/server.py` (standard library only), deployed on Render from `render.yaml` with the Direct
partner's key from the admin in `GETTHERE_PARTNER_KEY`. `site.js` calls it when the home page opens; if it can't
be reached, the page keeps the plain `quote@my.getthere.now` address.

The website holds no terms. Every partner's terms are served by the app on that
partner's own address, and the website's Terms links go to the Direct partner's page,
https://my.getthere.now/terms.html, so the website and the app always show the same terms.
`privacy.html` is the one Privacy Notice for every partner.

After a partner's settings change, rebuild the Privacy Notice and push:

    python3 tools/export_partners.py ../getthere   # path to the app checkout
    python3 tools/build_legal.py

Preview locally with `python3 -m http.server` in this folder.
