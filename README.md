# getthere-site

The GetThere marketing website, served at https://getthere.now by GitHub Pages from the `gh-pages` branch, which
`.github/workflows/publish.yml` copies from `main` on every push. Edit `main`.
Plain HTML, CSS and a little JavaScript; no build step.

| Page | For |
| --- | --- |
| `index.html` | Travellers: what the Flight Delay Pass is and how to forward a booking to `quote@my.getthere.now`. |
| `issuers.html` | Card issuers: the Flight Delay Pass story from the Head of Cards deck, a share calculator and the pilot offer. Contact us goes to partner@getthere.now. |
| `api.html` | API reference for card issuers: the calls a bank makes to GetThere and the calls GetThere makes to the bank. |
| `404.html` | Page not found, for any address the site doesn't have. |

Phone screens in `images/` come from the Head of Cards deck.

The website holds no terms. Every channel's terms are served by the app on that
channel's own address, and the website's Terms links go to the Direct channel's page,
https://my.getthere.now/terms.html, so the website and the app always show the same terms.
`privacy.html` is the one Privacy Notice for every channel.

After a channel's settings change, rebuild the Privacy Notice and push:

    python3 tools/export_channels.py ../getthere   # path to the app checkout
    python3 tools/build_legal.py

Preview locally with `python3 -m http.server` in this folder.
