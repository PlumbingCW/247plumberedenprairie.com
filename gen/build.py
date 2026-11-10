#!/usr/bin/env python3
import os, re, sys, json, shutil, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import *
import registry as R
from util import *
from mdparse import parse
from blocks import render_nodes
import chrome

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SITE = os.path.join(ROOT, "site")
CONTENT = os.path.join(ROOT, "content")
IMAGES = os.path.join(ROOT, "images")  # VA photos land here as <slug>.webp
GEN = os.path.join(ROOT, "gen")

HERO_FALLBACK = {"home": "hero-home", "service": "hero-service", "location": "hero-location", "blog": "hero-blog", "hub": "hero-hub", "std": "hero-hub", "legal": "hero-hub", "contact": "hero-contact"}
HERO_ALT = {
    "hero-home": "Abstract berry and dark plum gradient with soft circles behind the Eden Prairie 24/7 Plumbing headline",
    "hero-service": "Abstract berry and dark plum gradient header graphic with water-drop shapes",
    "hero-location": "Abstract berry and dark plum gradient header graphic with soft map-pin rings",
    "hero-blog": "Abstract berry and dark plum gradient header graphic with pipe-line curves",
    "hero-hub": "Abstract berry and dark plum gradient header graphic with soft circles",
    "hero-contact": "Abstract berry and dark plum gradient header graphic with a phone-ring pattern",
}


def hero_for(slug, kind):
    """Return dict(src,w,h,alt). Uses a VA photo if images/<slug>.webp exists, else the designed gradient fallback."""
    try:
        from PIL import Image
    except Exception:
        Image = None
    name = slug or "home"
    vp = os.path.join(IMAGES, name + ".webp")
    if os.path.exists(vp) and Image:
        im = Image.open(vp)
        os.makedirs(os.path.join(SITE, "img"), exist_ok=True)
        shutil.copy(vp, os.path.join(SITE, "img", name + ".webp"))
        alt_file = os.path.join(IMAGES, name + ".alt.txt")
        alt = open(alt_file).read().strip() if os.path.exists(alt_file) else f"Photo for {name}"
        return {"src": f"/img/{name}.webp", "w": im.width, "h": im.height, "alt": alt}
    key = HERO_FALLBACK.get(kind, "hero-hub")
    return {"src": f"/img/{key}.webp", "w": 1600, "h": 640, "alt": HERO_ALT[key]}


def hero_img(h):
    return f'<img class="hero-bg" src="{h["src"]}" alt="{attr(h["alt"])}" width="{h["w"]}" height="{h["h"]}" fetchpriority="high" decoding="async">'


def crumbs_html(crumbs):
    parts = []
    for i, (n, u) in enumerate(crumbs):
        if i < len(crumbs) - 1:
            parts.append(f'<a href="{u}">{esc(n)}</a>')
        else:
            parts.append(f'<span aria-current="page">{esc(n)}</span>')
    return '<nav class="crumb" aria-label="Breadcrumb">' + " &rsaquo; ".join(parts) + "</nav>"


def pagehead(p, chips=None, extra="", herocall=False, badge=False, zips=None, byline=None):
    h = p["hero_src"]
    s = [f'<div class="pagehead has-hero">{hero_img(h)}<div class="wrap"><div>', crumbs_html(p["crumbs"])]
    if badge:
        s.append(f'<span class="badge{" badge-alt" if p["kind"]=="location" else ""}">24/7 Emergency Line Open</span>')
    s.append(f'<h1>{esc(p["h1"])}</h1>')
    if p.get("lede"):
        s.append(f'<p class="lede">{esc(p["lede"])}</p>')
    if chips:
        s.append('<ul class="chips">' + "".join(f'<li class="chip">{esc(c)}</li>' for c in chips) + "</ul>")
    if zips:
        s.append('<div class="zips"><span class="zips-label">ZIP codes served</span>' + "".join(f'<span class="zip-chip">{z}</span>' for z in zips) + "</div>")
    if byline:
        s.append(f'<p class="byline">{byline}</p>')
    s.append("</div>")
    if herocall:
        s.append(f'<div class="herocall"><span class="lbl">24/7 emergency line</span><span class="num">{PHONE_DISPLAY}</span>'
                 f'<a class="btn berry block" href="{tel()}">Call now</a></div>')
    s.append("</div></div>")
    return "".join(s)


def sidecard(p):
    side = p["side"]
    bullets = ["Clear price before work starts", "Same-day appointments when available",
               f"Serving {side.get('place', 'Eden Prairie')} and nearby towns", "Licensed and insured"]
    if p["kind"] == "location":
        bullets.insert(0, "24/7 emergency line")
    tgt, label = [x.strip() for x in side["link"].split("|")]
    return (f'<aside class="sidecard" aria-label="Call {attr(BRAND)}"><span class="kick">24/7 Emergency Line Open</span>'
            f'<h3>{esc(side["h3"])}</h3><p>{esc(side["copy"])}</p>'
            f'<a class="btn" href="{tel()}">Call {PHONE_DISPLAY}</a>'
            f'<ul>' + "".join(f"<li>{esc(b)}</li>" for b in bullets) + '</ul>'
            f'<a class="side-link" href="{url(tgt)}">{esc(label)} &rarr;</a></aside>')


def ctaband(title, copy):
    return (f'<section class="ctaband"><div class="wrap"><h2>{esc(title)}</h2><p>{esc(copy)}</p>'
            f'<a class="btn" href="{tel()}">Call {PHONE_DISPLAY}</a></div></section>')


def local_map(L):
    q = L["map_q"].replace(" ", "+")
    return (f'<div class="localmap"><iframe title="Map of {attr(L["name"])}, MN" aria-label="Map of {attr(L["name"])}, MN" '
            f'src="https://maps.google.com/maps?q={q}&amp;output=embed&amp;z={L["map_z"]}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>')


def wrap_page(p, main_html):
    return "\n".join([chrome.head(p), "<body>", chrome.header_html(p), '<main id="main-content">', main_html, "</main>",
                      chrome.sitemap_map_html(), chrome.footer_html(), "</body>", "</html>"]) + "\n"


# ---------- index builders for hub pages ----------
SVC_FM = {}
BLOG_FM = {}


def blog_thumb(slug):
    """480x192 thumbnail for the blog index, cut from the same image the post header uses."""
    from PIL import Image
    src = os.path.join(IMAGES, slug + ".webp")
    if not os.path.exists(src):
        return ""
    os.makedirs(os.path.join(SITE, "img"), exist_ok=True)
    Image.open(src).convert("RGB").resize((480, 192), Image.LANCZOS).save(os.path.join(SITE, "img", "thumb-" + slug + ".webp"), "WEBP", quality=78, method=6)
    af = os.path.join(IMAGES, slug + ".alt.txt")
    alt = open(af).read().strip() if os.path.exists(af) else "Plumbing guide"
    return f'<img class="mini-thumb" src="/img/thumb-{slug}.webp" alt="{attr(alt)}" width="480" height="192" loading="lazy" decoding="async">'


def hub_index(kind):
    if kind == "services":
        groups = {}
        for s, (nav, t, em, g) in SERVICES.items():
            groups.setdefault(g, []).append(s)
        out = []
        for g, slugs in groups.items():
            out.append(f'<div class="index-group"><h2>{esc(g)}</h2><div class="mini-cards">')
            for s in slugs:
                tag = "Emergency service" if SERVICES[s][2] else "Planned service"
                out.append(f'<a class="mini-card" href="{url(s)}"><span class="tag">{tag}</span><b>{esc(SERVICES[s][0])}</b><span>{esc(SVC_FM[s]["hero"])}</span></a>')
            out.append("</div></div>")
        return "".join(out)
    if kind == "areas":
        out = ['<div class="mini-cards">']
        for k, L in LOCATIONS.items():
            fm = LOC_FM[k]
            out.append(f'<a class="mini-card" href="{url(L["slug"])}"><span class="tag">{esc(L["county"])} &middot; ZIP {L["primary_zip"]}</span><b>{esc(L["name"])}</b><span>{esc(fm["hero"])}</span></a>')
        out.append("</div>")
        return "".join(out)
    if kind == "blog":
        out = ['<div class="mini-cards">']
        for slug, topic, _ in R.BLOGS:
            fm = BLOG_FM[slug]
            th = blog_thumb(slug)
            out.append(f'<a class="mini-card has-thumb" href="{url(slug)}">{th}<span class="tag">Guide</span><b>{esc(fm["title"])}</b><span>{esc(fm["hero"])}</span></a>')
        out.append("</div>")
        return "".join(out)
    raise ValueError(kind)


LOC_FM = {}
HOOD_FM = {}
PAGES = {}  # slug -> html


def load_md(path):
    with open(path, encoding="utf-8") as f:
        return parse(f.read())


def build_service(slug):
    fm, nodes = load_md(os.path.join(CONTENT, "pages", slug + ".md"))
    SVC_FM[slug] = fm
    nav, tsvc, emerg, grp = SERVICES[slug]
    p = {"slug": slug, "kind": "service", "title": R.svc_title(slug), "meta": fm["meta"], "h1": R.svc_h1(slug), "lede": fm["hero"],
         "crumbs": [("Home", "/"), ("Services", "/services/"), (nav, url(slug))], "hero_src": hero_for(slug, "service"),
         "side": {"h3": fm["side_h3"], "copy": fm["side_copy"], "link": fm["side_link"]}}
    ctx = {"faq_title": f"{nav} questions in Eden Prairie", "mid_title": f"Talk to a dispatcher about {nav.lower()}",
           "mid_copy": "Dispatch answers 24/7 and books same-day appointments when one is open."}
    body, faqs = render_nodes(nodes, ctx)
    p["faqs"] = faqs
    chips = ["Clear price before work starts", "Same-day appointments when available", "Licensed and insured"]
    html_main = (pagehead(p, chips=chips, badge=emerg) + '<section class="sec"><div class="wrap twocol"><article class="prose">' + body +
                 "</article>" + sidecard(p) + "</div></section>" +
                 ctaband(f"{'Emergency ' if emerg else ''}{tsvc} in Eden Prairie", "Call the 24/7 line and a dispatcher will talk through your situation."))
    return p, html_main


def build_blog(slug):
    fm, nodes = load_md(os.path.join(CONTENT, "blogs", slug + ".md"))
    BLOG_FM[slug] = fm
    p = {"slug": slug, "kind": "blog", "title": fm["title"], "meta": fm["meta"], "h1": fm["title"], "lede": fm["hero"],
         "crumbs": [("Home", "/"), ("Blog", "/blog/"), (fm["title"], url(slug))], "hero_src": hero_for(slug, "blog"),
         "side": {"h3": fm["side_h3"], "copy": fm["side_copy"], "link": fm["side_link"]}}
    ctx = {"faq_title": "Eden Prairie homeowner questions", "mid_title": "Rather have a plumber look at it?",
           "mid_copy": "Our 24/7 line is open now, and same-day appointments are available when a slot is open."}
    body, faqs = render_nodes(nodes, ctx)
    p["faqs"] = faqs
    by = f'By the {esc(BRAND)} team &middot; Updated {PUBLISHED_HUMAN}'
    html_main = (pagehead(p, byline=by) + '<section class="sec"><div class="wrap twocol"><article class="prose">' + body +
                 "</article>" + sidecard(p) + "</div></section>" +
                 ctaband("Plumbing trouble in Eden Prairie?", "Call the 24/7 line and a dispatcher will help you decide what to do next."))
    return p, html_main


def build_location(key):
    L = LOCATIONS[key]; slug = L["slug"]
    fm, nodes = load_md(os.path.join(CONTENT, "locs", slug + ".md"))
    LOC_FM[key] = fm
    meta = (f"Licensed 24/7 emergency plumber serving {L['name']}, MN from Eden Prairie-based {BRAND}. "
            f"{L['top2'][0]} and {L['top2'][1]}. Call now.")
    meta = meta[0].upper() + meta[1:] if False else meta
    p = {"slug": slug, "kind": "location", "title": R.loc_title(key), "meta": meta, "h1": R.loc_h1(key), "lede": fm["hero"],
         "crumbs": [("Home", "/"), ("Areas", "/areas/"), (L["name"], url(slug))], "hero_src": hero_for(slug, "location"),
         "side": {"h3": fm["side_h3"], "copy": fm["side_copy"], "link": fm["side_link"], "place": L["name"]}}
    ctx = {"faq_title": f"{L['name']} plumbing questions", "mid_title": f"Emergency plumber for {L['name']}",
           "mid_copy": f"Dispatch from Eden Prairie answers 24/7 and books same-day appointments for {L['name']} when one is open.",
           "midcta": True}
    body, faqs = render_nodes(nodes, ctx)
    p["faqs"] = faqs
    chips = ["Clear price before work starts", "Same-day appointments when available", "Licensed and insured"]
    html_main = (pagehead(p, chips=chips, badge=True, zips=L["zips"]) + '<section class="sec"><div class="wrap twocol"><article class="prose">' + body +
                 f'<h2 id="map-{key}">{esc(L["name"])} on the map</h2>' + local_map(L) +
                 "</article>" + sidecard(p) + "</div></section>" +
                 ctaband(f"Emergency plumber for {L['name']}, MN", "Call the 24/7 line from Eden Prairie dispatch."))
    return p, html_main


def hood_sidecard(nb, fm):
    tgt, label = [x.strip() for x in fm["side_link"].split("|")]
    return (f'<aside class="sidecard" aria-label="Call {attr(BRAND)}"><span class="kick">Plumbing questions?</span>'
            f'<h3>{esc(fm["side_h3"])}</h3><p>{esc(fm["side_copy"])}</p>'
            f'<a class="btn" href="{tel()}">Call {PHONE_DISPLAY}</a>'
            f'<ul><li>Serving {esc(nb["name"])} and Eden Prairie</li><li>{esc(nb["blurb"])}</li></ul>'
            f'<a class="side-link" href="{url(tgt)}">{esc(label)} &rarr;</a></aside>')


def build_neighborhood(key):
    nb = NEIGHBORHOODS[key]; slug = nb["slug"]
    fm, nodes = load_md(os.path.join(CONTENT, "hoods", slug + ".md"))
    HOOD_FM[key] = fm
    p = {"slug": slug, "kind": "neighborhood", "title": nb["title"], "meta": nb["meta"], "h1": nb["h1"], "lede": fm["hero"],
         "crumbs": [("Home", "/"), ("Areas", "/areas/"), (nb["name"], url(slug))], "hero_src": hero_for(slug, "location")}
    ctx = {"faq_title": f"{nb['name']} plumbing questions", "mid_title": f"Plumbing question in {nb['name']}?",
           "mid_copy": nb["cta"], "midcta": True}
    body, faqs = render_nodes(nodes, ctx)
    p["faqs"] = faqs
    chips = [nb["blurb"], "Eden Prairie, MN"]
    html_main = (pagehead(p, chips=chips) + '<section class="sec"><div class="wrap twocol"><article class="prose">' + body +
                 f'<h2 id="map-{key}">{esc(nb["name"])} on the map</h2>' + local_map({"name": nb["name"], "map_q": nb["map_q"], "map_z": nb["map_z"]}) +
                 "</article>" + hood_sidecard(nb, fm) + "</div></section>" +
                 ctaband(f"Plumbing help in {nb['name']}", nb["cta"]))
    return p, html_main


def build_simple(slug, kind, title, h1=None):
    fm, nodes = load_md(os.path.join(CONTENT, "misc", slug + ".md"))
    p = {"slug": slug, "kind": kind, "title": fm.get("title", title), "meta": fm["meta"], "h1": fm.get("h1", h1 or title), "lede": fm["hero"],
         "crumbs": [("Home", "/"), (fm.get("crumb", title), url(slug))], "hero_src": hero_for(slug, "contact" if slug == "contact" else kind)}
    ctx = {"index": hub_index, "faq_title": fm.get("faq_title", "Frequently asked questions"), "midcta": False}
    body, faqs = render_nodes(nodes, ctx)
    p["faqs"] = faqs
    tail = ""
    if slug == "contact":
        q = MAP_CONTACT_Q.replace(" ", "+")
        tail = (f'<div class="localmap"><iframe title="Map of {attr(ADDRESS_LINE)}" aria-label="Map of {attr(ADDRESS_LINE)}" '
                f'src="https://maps.google.com/maps?q={q}&amp;output=embed&amp;z={MAP_CONTACT_Z}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>')
    cls = "prose legal-prose" if kind == "legal" else "prose"
    html_main = (pagehead(p, herocall=True) + f'<section class="sec"><div class="wrap"><div class="{cls}">' + body + tail + "</div></div></section>" +
                 (ctaband("Plumbing emergency in Eden Prairie?", "Call the 24/7 line now.") if kind != "legal" else ""))
    return p, html_main


def write(slug, html_text):
    d = SITE if slug == "" else os.path.join(SITE, slug)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_text)


def main():
    if os.path.exists(SITE):
        # keep generated assets folder
        for name in os.listdir(SITE):
            if name in ("assets", "img") or name.startswith("favicon") or name in ("apple-touch-icon.png", "icon-192.png", "icon-512.png", "site.webmanifest"):
                continue
            pth = os.path.join(SITE, name)
            shutil.rmtree(pth) if os.path.isdir(pth) else os.remove(pth)
    os.makedirs(os.path.join(SITE, "assets"), exist_ok=True)
    shutil.copy(os.path.join(GEN, "main.css"), os.path.join(SITE, "assets", "main.css"))
    shutil.copy(os.path.join(GEN, "main.js"), os.path.join(SITE, "assets", "main.js"))

    built = {}
    # pre-load front matter for hub indexes
    for s in SERVICES: SVC_FM[s] = load_md(os.path.join(CONTENT, "pages", s + ".md"))[0]
    for b, _, _ in R.BLOGS: BLOG_FM[b] = load_md(os.path.join(CONTENT, "blogs", b + ".md"))[0]
    for k in LOCATIONS: LOC_FM[k] = load_md(os.path.join(CONTENT, "locs", LOCATIONS[k]["slug"] + ".md"))[0]

    for s in SERVICES: built[s] = build_service(s)
    for b, _, _ in R.BLOGS: built[b] = build_blog(b)
    for k in LOCATIONS: built[LOCATIONS[k]["slug"]] = build_location(k)
    for k in NEIGHBORHOODS: built[NEIGHBORHOODS[k]["slug"]] = build_neighborhood(k)
    for slug, kind, title in [("services", "hub", "Services"), ("areas", "hub", "Service Areas"), ("blog", "hub", "Blog"),
                              ("about", "std", "About"), ("contact", "std", "Contact"), ("privacy", "legal", "Privacy Policy"), ("terms", "legal", "Terms of Service")]:
        built[slug] = build_simple(slug, kind, title)
    import home
    built[""] = home.build(hero_for, hero_img, ctaband, sidecard, crumbs_html)
    for slug, (p, m) in built.items():
        write(slug, wrap_page(p, m))
    # 404
    p404 = {"slug": "404-page", "kind": "std", "title": "Page Not Found | Eden Prairie 24/7 Plumbing", "meta": "The page you are looking for is not here. Call Eden Prairie 24/7 Plumbing for emergency plumbing help in Eden Prairie, MN any time.",
            "h1": "Page not found", "crumbs": [("Home", "/"), ("Page not found", "")], "hero_src": None, "noindex": True}
    m404 = (f'<section class="notfound"><div class="wrap"><h1>That page is not here</h1><p>The link may be old or mistyped. If you have a plumbing emergency in Eden Prairie, skip the search and call our 24/7 line.</p>'
            f'<a class="btn" href="{tel()}">Call {PHONE_DISPLAY}</a> <a class="btn ghost" href="/">Back to home</a></div></section>')
    with open(os.path.join(SITE, "404.html"), "w", encoding="utf-8") as f:
        f.write(wrap_page(p404, m404))
    # sitemap etc
    urls = [("", "1.0")] + [(s, "0.9" if R.kind_of(s) in ("service", "location") else ("0.8" if R.kind_of(s) == "neighborhood" else "0.7")) for s in built if s != ""]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for s, pr in urls:
        sm.append(f"<url><loc>{abs_url(s)}</loc><lastmod>{MODIFIED}</lastmod><priority>{pr}</priority></url>")
    sm.append("</urlset>")
    open(os.path.join(SITE, "sitemap.xml"), "w").write("\n".join(sm) + "\n")
    open(os.path.join(SITE, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
    open(os.path.join(SITE, "_redirects"), "w").write("# Intentionally empty. Cloudflare Pages serves slug/index.html natively.\n")
    open(os.path.join(SITE, "_headers"), "w").write(
        "/*\n  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n"
        "  Permissions-Policy: camera=(), microphone=(), geolocation=()\n  X-Frame-Options: SAMEORIGIN\n\n/assets/*\n  Cache-Control: public, max-age=86400\n\n/img/*\n  Cache-Control: public, max-age=86400\n")
    print(f"built {len(built)+1} html pages")


if __name__ == "__main__":
    main()
