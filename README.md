# getthere-site

The GetThere marketing website, served by GitHub Pages from the `gh-pages` branch, which
`.github/workflows/publish.yml` copies from `main` on every push. Edit `main`.
Plain HTML, CSS and a little JavaScript; no build step.

| Page | For |
| --- | --- |
| `index.html` | Travellers: what the Flight Delay Pass is and how to forward a booking to `quote@my.getthere.now`. |
| `banks.html` | Card issuers: the Flight Delay Pass story from the Head of Cards deck, a share calculator and the pilot offer. Contact us goes to partner@getthere.now. |

Phone screens in `images/` come from the Head of Cards deck.

Terms (one page per channel, `terms/<code>.html`), the Privacy Policy
(`privacy.html`, every channel) and `legal.html` are built from the app's
channel settings. Re-run both after a channel changes, and edit wording in
`tools/build_legal.py`, not in the generated pages:

    python3 tools/export_channels.py ../getthere   # path to the app checkout
    python3 tools/build_legal.py

Preview locally with `python3 -m http.server` in this folder.
