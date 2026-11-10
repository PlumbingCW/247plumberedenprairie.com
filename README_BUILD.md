# Eden Prairie 24/7 Plumbing: generator source

Python 3.10+ with Pillow and numpy (`pip install -r requirements.txt`).

Build:
    python3 gen/assets.py     # brand logo, icons, gradient heroes, OG image -> site/img
    python3 gen/build.py      # renders all pages -> site/
Validate copy: `python3 tools/check_md.py content/*/*.md`
Deploy: upload the contents of `site/` (flat root) to Cloudflare Pages.

Layout: gen/ (config.py = brand, phone, services, locations, NEIGHBORHOODS), content/ (pages, blogs, locs, hoods, misc in the EPMD markdown dialect), images/ (photos by slug), brand/ (logo and icon).
Neighborhood pages: add an entry to NEIGHBORHOODS in gen/config.py and a matching content/hoods/<slug>.md.
