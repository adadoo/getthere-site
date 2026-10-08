# getthere-site

The GetThere marketing website, served by GitHub Pages from the `gh-pages` branch, which
`.github/workflows/publish.yml` copies from `main` on every push. Edit `main`.
Plain HTML, CSS and a little JavaScript; no build step.

| Page | For |
| --- | --- |
| `index.html` | Travellers: what the Flight Delay Pass is and how to forward a booking to `quote@my.getthere.now`. |
| `issuers.html` | Card issuers: the Flight Delay Pass story from the Head of Cards deck, a share calculator and the pilot offer. Contact us goes to partner@getthere.now. |
| `api.html` | API reference for card issuers: the calls a bank makes to GetThere and the calls GetThere makes to the bank. |
| `banks.html` | Redirects to `issuers.html`, so old links keep working. |

Phone screens in `images/` come from the Head of Cards deck.

`terms.html` is the Direct channel's terms, word for word as the app serves them at
my.getthere.now/terms.html. Every other channel's terms live only on that channel's own
address (for example sq.getthere.now/terms.html), served by the app; they are never on
this website. `privacy.html` is the one Privacy Notice for every channel.
`legal.html` and `terms/direct.html` redirect to `terms.html`.

`terms/<channel>/<version>.html` are terms pages passes were sold under before the
terms moved to the app. The app's `initdb` moves those passes to their channel's
address, word for word; the files can be deleted once that has run in production.

After the terms wording (the app's `getthere/legal.py`, with `TERMS_EFFECTIVE` bumped in
`getthere/brand.py`) or the Direct channel's settings change, rebuild and push:

    python3 tools/export_channels.py ../getthere   # path to the app checkout
    python3 tools/build_legal.py

Preview locally with `python3 -m http.server` in this folder.
