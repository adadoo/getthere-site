# getthere-site

The GetThere marketing website, served by GitHub Pages from the `main` branch.
Plain HTML, CSS and a little JavaScript; no build step.

| Page | For |
| --- | --- |
| `index.html` | Travellers: what the Flight Delay Pass is and how to forward a booking to `quote@my.getthere.now`. |
| `banks.html` | Banks that have signed the agreement: getting started, channel setup form with live preview, API reference. |

The channel setup form writes the channel as it would appear in the app's
`getthere/channels.py` and opens an email to partners@getthere.now with it.

Preview locally with `python3 -m http.server` in this folder.
