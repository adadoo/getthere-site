# getthere-site

The GetThere marketing website, served by GitHub Pages from the `gh-pages` branch, which
`.github/workflows/publish.yml` copies from `main` on every push. Edit `main`.
Plain HTML, CSS and a little JavaScript; no build step.

| Page | For |
| --- | --- |
| `index.html` | Travellers: what the Flight Delay Pass is and how to forward a booking to `quote@my.getthere.now`. |
| `banks.html` | Card issuers: the Flight Delay Pass story from the Head of Cards deck, a share calculator and the pilot offer. Contact us goes to partner@getthere.now. |

Phone screens in `images/` come from the Head of Cards deck.

Terms, the Privacy Notice (`privacy.html`, every channel) and `legal.html` are
built from the app's channel settings. Each terms version gets its own page,
`terms/<channel>/<effective date>-v<channel version>.html`, which the app records
on every pass sold, so a published version is never changed (the build and the
Publish workflow both refuse). `terms/<channel>.html` is the current version.

After a channel's version changes in the app, re-run both commands and push
before deploying the app. To change the wording, edit `tools/build_legal.py`
and bump `TERMS_EFFECTIVE` in the app's `getthere/brand.py` first:

    python3 tools/export_channels.py ../getthere   # path to the app checkout
    python3 tools/build_legal.py

Preview locally with `python3 -m http.server` in this folder.
