"""Write the same header audiences and footer columns into every page (no build step: run it after changing
them, then commit the pages). Audiences, in this order (Dadoo, 14 and 16 Oct 2026): Traveller, Card Issuer,
Loyalty Program, Travel Site, Travel Platform, Underwriter.

    python3 tools/site_nav.py
"""

import os
import re

ROOT = os.path.join(os.path.dirname(__file__), "..")
AUDIENCES = (("Traveller", "./", "index.html"), ("Card Issuer", "issuers.html", "issuers.html"),
             ("Loyalty Program", "loyalty-programs.html", "loyalty-programs.html"),
             ("Travel Site", "travel-sites.html", "travel-sites.html"),
             ("Travel Platform", "travel-platforms.html", "travel-platforms.html"),
             ("Underwriter", "underwriters.html", "underwriters.html"))
COLUMNS = (("Traveller", (("Get a price", "./#forward"), ("How it works", "./#how"), ("FAQ", "./#faq"))),
           ("Card Issuer", (("The product", "issuers.html"), ("The numbers", "issuers.html#numbers"),
                            ("API reference", "api-issuers.html"))),
           ("Loyalty Program", (("The product", "loyalty-programs.html"), ("Award bookings", "loyalty-programs.html#award"),
                                ("The numbers", "loyalty-programs.html#numbers"))),
           ("Travel Site", (("The product", "travel-sites.html#product"), ("The numbers", "travel-sites.html#numbers"),
                                     ("API reference", "api-travel-sites.html"))),
           ("Travel Platform", (("The product", "travel-platforms.html#product"),
                                ("Company cover", "travel-platforms.html#company"),
                                ("The numbers", "travel-platforms.html#numbers"))),
           ("Underwriter", (("Risk", "underwriters.html#risk"), ("Rollout", "underwriters.html#rollout"),
                            ("Reports", "underwriters.html#reports"))))
# Which audience each page belongs to, for aria-current; and the last footer column, the page's own.
CURRENT = {"index.html": "index.html", "issuers.html": "issuers.html", "api.html": "issuers.html", "api-issuers.html": "issuers.html",
           "api-travel-sites.html": "travel-sites.html", "loyalty-programs.html": "loyalty-programs.html",
           "travel-sites.html": "travel-sites.html", "travel-platforms.html": "travel-platforms.html",
           "underwriters.html": "underwriters.html"}
LAST = {"privacy.html": ("Legal", (("Terms", "https://my.getthere.now/terms.html"), ("Privacy", "privacy.html"))),
        "404.html": ("Help", (("help@getthere.now", "mailto:help@getthere.now"),))}
CONTACT = ("Contact", (("partner@getthere.now", "mailto:partner@getthere.now"),))
BUTTON = ('<button class="menu-btn" type="button" aria-label="Menu" aria-expanded="false" aria-controls="menu">'
          '<svg class="bars" width="20" height="20" viewBox="0 0 20 20" aria-hidden="true"><path d="M3 5h14M3 10h14M3 15h14" '
          'stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
          '<svg class="close" width="20" height="20" viewBox="0 0 20 20" aria-hidden="true"><path d="M5 5l10 10M15 5L5 15" '
          'stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button>')


def href(link, page):
    """404.html is served at any path, so its links start at the root."""
    if page != "404.html" or link.startswith(("http", "mailto:")):
        return link
    return "/" + (link[2:] if link.startswith("./") else link)


def menu(page):
    links = "".join(f'<a href="{href(h, page)}"{" aria-current=\"page\"" if CURRENT.get(page) == f else ""}>{label}</a>'
                    for label, h, f in AUDIENCES)
    return f'<div class="menu" id="menu">{links}</div>'


def columns(page):
    cols = (*COLUMNS, LAST.get(page, CONTACT))
    return "\n".join(f'      <div><b style="color:#fff">{title}</b>'
                     + "".join(f'<a href="{href(h, page)}">{label}</a>' for label, h in links) + "</div>"
                     for title, links in cols)


def rewrite(page):
    path = os.path.join(ROOT, page)
    with open(path) as f:
        html = f.read()
    # Header: the menu, then the page's own button (Get a price, Contact us...), then the menu button.
    def nav(m):
        pill = re.search(r'<a class="pill"[^>]*>.*?</a>', m.group(2))
        return f'{m.group(1)}\n    {menu(page)}\n    {pill.group(0) if pill else ""}\n    {BUTTON}\n  </nav>'
    html, n = re.subn(r'(<nav[^>]*>)(.*?)\s*</nav>', nav, html, count=1, flags=re.S)
    assert n == 1, page
    html = re.sub(r'(<div class="cols">\n).*?(\n    </div>)', lambda m: m.group(1) + columns(page) + m.group(2),
                  html, count=1, flags=re.S)
    css = '<link rel="stylesheet" href="/nav.css">' if page == "404.html" else '<link rel="stylesheet" href="nav.css">'
    if "nav.css" not in html:
        html = re.sub(r'(<link rel="stylesheet" href="/?(?:styles|traveller)\.css">)', r"\1\n" + css, html, count=1)
    with open(path, "w") as f:
        f.write(html)


if __name__ == "__main__":
    for page in ("index.html", "issuers.html", "loyalty-programs.html", "travel-sites.html", "travel-platforms.html",
                 "underwriters.html", "api.html", "api-issuers.html", "api-travel-sites.html", "privacy.html", "404.html"):
        rewrite(page)
