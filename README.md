# getthere-site

The GetThere marketing website, served at https://getthere.now by GitHub Pages from the `gh-pages` branch, which
`.github/workflows/publish.yml` copies from `main` on every push. Edit `main`.
Plain HTML, CSS and a little JavaScript; no build step.

| Page | For |
| --- | --- |
| `index.html` | Travellers: what the Flight Delay Pass is and how to forward a booking to `quote@my.getthere.now`. The same page, design and wording as each channel's home and offer page in the app (`getthere/templates/landing.html`); its stylesheet `traveller.css` is the app's `_traveller.css`, kept identical. |
| `issuers.html` | Card issuers: the Flight Delay Pass story from the Head of Cards deck, a share calculator and the pilot offer. Contact us goes to partner@getthere.now. |
| `api.html` | API reference for card issuers: the calls a card issuer makes to GetThere and the calls GetThere makes to the card issuer. |
| `404.html` | Page not found, for any address the site doesn't have. |

Phone screens in `images/` come from the Head of Cards deck.

The website is the Direct channel's app. Like a card issuer's app, it gets each visitor's forward address
from GetThere's partner API (`GET /partner/v1/offer`), with the page's utm tags and referring site, so a booking
forwarded from the site is traced to that visit in the admin's Offers. The partner key is a secret, so a small
server holds it: `server/server.py` (standard library only), deployed on Render from `render.yaml` with the Direct
channel's key from the admin in `GETTHERE_PARTNER_KEY`. `site.js` calls it when the home page opens; if it can't
be reached, the page keeps the plain `quote@my.getthere.now` address.

The website holds no terms. Every channel's terms are served by the app on that
channel's own address, and the website's Terms links go to the Direct channel's page,
https://my.getthere.now/terms.html, so the website and the app always show the same terms.
`privacy.html` is the one Privacy Notice for every channel.

After a channel's settings change, rebuild the Privacy Notice and push:

    python3 tools/export_channels.py ../getthere   # path to the app checkout
    python3 tools/build_legal.py

Preview locally with `python3 -m http.server` in this folder.
