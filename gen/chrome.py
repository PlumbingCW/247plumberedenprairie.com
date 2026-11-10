import json
from config import *
import registry as R
from util import *

FONTS = "https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Nunito+Sans:wght@400;600;700;800&display=swap"
CSS_V = "1"

KNOWS = [
    # services
    *[v[1] for v in SERVICES.values()],
    # topics
    "Emergency plumbing", "24 hour plumber", "Same-day plumbing", "Clogged drains", "Drain snaking", "Drain cabling", "Kitchen sink clogs", "Shower and tub drains",
    "Floor drains", "Main sewer line backups", "Sewer cleanouts", "Tree root intrusion", "Trenchless pipe lining", "Pipe bursting", "Cast iron drain pipe",
    "Sewer camera inspection", "Pipe locating", "Slab leaks", "Water meter high-bill leaks", "Ceiling and wall leaks", "Crawlspace leaks", "Buried water line leaks",
    "Irrigation leaks", "Acoustic leak detection", "Thermal imaging", "Moisture meters", "Pressure testing", "Tracer gas testing", "Frozen pipes", "Burst pipes",
    "Copper pipe repair", "PEX piping", "CPVC piping", "Galvanized pipe replacement", "Polybutylene pipe", "Water service lines", "Curb stops and meter valves",
    "Low water pressure", "Pressure reducing valves", "Expansion tanks", "Tank water heaters", "Gas water heaters", "Electric water heaters", "Hybrid heat pump water heaters",
    "Tankless water heater flushing", "Anode rods", "T&P relief valves", "Water heater venting", "Hydronic boilers", "Boiler circulator pumps", "Sump pumps",
    "Battery backup sump pumps", "Sewage ejector pumps", "Interior drain tile", "Basement moisture", "Toilet flanges", "Wax rings", "Fill valves and flappers",
    "Faucet cartridges", "Shower valves", "Angle stop valves", "Garbage disposals", "Backflow testing", "Grease trap cleaning", "Storm drain cleaning",
    "Water softeners", "Whole-house water filtration", "Reverse osmosis systems", "Minnesota Plumbing Code",
    # local
    "Eden Prairie, Minnesota", "Hennepin County, Minnesota", "Eden Prairie Center", "Flying Cloud Airport", "Staring Lake", "Purgatory Creek", "Round Lake", "Lake Riley",
    "Bryant Lake Regional Park", "Minnesota River Bluffs", "Interstate 494", "U.S. Highway 169", "U.S. Highway 212", "Minnesota Highway 5",
    "Minnetonka, Minnesota", "Hopkins, Minnesota", "Chanhassen, Minnesota", "Bloomington, Minnesota", "Edina, Minnesota", "Chaska, Minnesota",
    "ZIP code 55344", "ZIP code 55346", "ZIP code 55347",
]


def abs_img(path):
    return SITE_URL + path


def business_node():
    return {
        "@context": "https://schema.org",
        "@type": "Plumber",
        "@id": SITE_URL + "/#business",
        "name": BRAND,
        "url": SITE_URL + "/",
        "telephone": PHONE_E164,
        "email": EMAIL,
        "image": abs_img("/img/og-default.png"),
        "logo": abs_img("/img/logo.png"),
        "priceRange": "$$",
        "description": f"24/7 emergency plumbing dispatch in {CITY}, {STATE} and nearby Hennepin and Carver County towns.",
        "address": {"@type": "PostalAddress", "streetAddress": ADDRESS_STREET, "addressLocality": ADDRESS_LOCALITY,
                    "addressRegion": ADDRESS_REGION, "postalCode": ADDRESS_ZIP, "addressCountry": "US"},
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
                                       "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                                       "opens": "00:00", "closes": "23:59"}],
        "areaServed": [{"@type": "City", "name": n, "containedInPlace": {"@type": "AdministrativeArea", "name": "Minnesota"}}
                       for n in ["Eden Prairie", "Minnetonka", "Hopkins", "Chanhassen", "Bloomington", "Edina", "Chaska"]],
        "knowsAbout": KNOWS,
    }


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "</script>"


def head(p):
    slug = p["slug"]
    canon = abs_url(slug)
    hero = p.get("hero_src")
    out = ['<!doctype html>', '<html lang="en-US" class="nojs">', '<head>', '<meta charset="utf-8">',
           '<meta name="viewport" content="width=device-width,initial-scale=1">',
           f'<title>{esc(p["title"])}</title>',
           f'<meta name="description" content="{attr(p["meta"])}">',
           (f'<link rel="canonical" href="{canon}">' if not p.get("noindex") else ''),
           '<meta name="robots" content="index,follow,max-image-preview:large">' if not p.get("noindex") else '<meta name="robots" content="noindex,follow">',
           '<meta name="theme-color" content="#241522">',
           f'<meta property="og:type" content="{"article" if p["kind"]=="blog" else "website"}">',
           f'<meta property="og:site_name" content="{attr(BRAND)}">',
           f'<meta property="og:title" content="{attr(p["title"])}">',
           f'<meta property="og:description" content="{attr(p["meta"])}">',
           f'<meta property="og:url" content="{canon}">',
           f'<meta property="og:image" content="{abs_img("/img/og-default.png")}">',
           '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">',
           f'<meta property="og:image:alt" content="{attr(BRAND)}: 24/7 emergency plumbing in Eden Prairie, MN">',
           '<meta property="og:locale" content="en_US">',
           '<meta name="twitter:card" content="summary_large_image">',
           f'<meta name="twitter:title" content="{attr(p["title"])}">',
           f'<meta name="twitter:description" content="{attr(p["meta"])}">',
           f'<meta name="twitter:image" content="{abs_img("/img/og-default.png")}">',
           '<link rel="icon" href="/favicon.ico" sizes="any">',
           '<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">',
           '<link rel="apple-touch-icon" href="/apple-touch-icon.png">',
           '<link rel="manifest" href="/site.webmanifest">',
           '<link rel="preconnect" href="https://fonts.googleapis.com">',
           '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>']
    if hero:
        out.append(f'<link rel="preload" as="image" href="{hero["src"]}" fetchpriority="high">')
    out.append(f'<link rel="stylesheet" href="{FONTS}">')
    out.append(f'<link rel="stylesheet" href="/assets/main.css?v={CSS_V}">')
    out.append(ld(schema_graph(p)))
    out.append('</head>')
    return "\n".join(out)


def schema_graph(p):
    slug = p["slug"]; canon = abs_url(slug); kind = p["kind"]
    g = [business_node()]
    g.pop(0)
    nodes = [business_node()]
    nodes[0].pop("@context")
    nodes.append({"@type": "WebSite", "@id": SITE_URL + "/#website", "url": SITE_URL + "/", "name": BRAND, "inLanguage": "en-US",
                  "publisher": {"@id": SITE_URL + "/#business"}})
    wp = {"@type": "WebPage", "@id": canon, "url": canon, "name": p["title"], "description": p["meta"], "inLanguage": "en-US",
          "isPartOf": {"@id": SITE_URL + "/#website"}, "about": {"@id": SITE_URL + "/#business"},
          "breadcrumb": {"@id": canon + "#breadcrumb"}}
    if p.get("hero_src"):
        wp["primaryImageOfPage"] = {"@type": "ImageObject", "url": SITE_URL + p["hero_src"]["src"]}
    nodes.append(wp)
    crumbs = p["crumbs"]
    nodes.append({"@type": "BreadcrumbList", "@id": canon + "#breadcrumb",
                  "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n,
                                       "item": SITE_URL + u if u else canon} for i, (n, u) in enumerate(crumbs)]})
    if kind == "service":
        nodes.append({"@type": "Service", "@id": canon + "#service", "name": p["h1"], "serviceType": SERVICES[slug][1], "url": canon,
                      "provider": {"@id": SITE_URL + "/#business"},
                      "areaServed": {"@type": "City", "name": "Eden Prairie", "containedInPlace": {"@type": "AdministrativeArea", "name": "Minnesota"}}})
    if kind == "location":
        L = LOCATIONS[R.loc_key_from_slug(slug)]
        nodes.append({"@type": "Service", "@id": canon + "#service", "name": f"Emergency plumbing in {L['name']}, MN", "serviceType": "Plumbing", "url": canon,
                      "provider": {"@id": SITE_URL + "/#business"},
                      "areaServed": {"@type": "City", "name": L["name"], "containedInPlace": {"@type": "AdministrativeArea", "name": "Minnesota"}}})
    if kind == "neighborhood":
        nb = [v for v in NEIGHBORHOODS.values() if v["slug"] == slug][0]
        nodes.append({"@type": "Service", "@id": canon + "#service", "name": nb["h1"], "serviceType": "Plumbing", "url": canon,
                      "provider": {"@id": SITE_URL + "/#business"},
                      "areaServed": {"@type": "Place", "name": nb["name"] + ", Eden Prairie, MN",
                                     "containedInPlace": {"@type": "City", "name": "Eden Prairie"}}})
    if kind == "blog":
        nodes.append({"@type": "Article", "@id": canon + "#article", "headline": p["h1"], "description": p["meta"],
                      "image": [SITE_URL + p["hero_src"]["src"]] if p.get("hero_src") else [abs_img("/img/og-default.png")],
                      "author": {"@type": "Organization", "name": BRAND, "url": SITE_URL + "/"},
                      "publisher": {"@type": "Organization", "name": BRAND, "logo": {"@type": "ImageObject", "url": abs_img("/img/logo.png")}},
                      "datePublished": PUBLISHED, "dateModified": MODIFIED, "inLanguage": "en-US", "mainEntityOfPage": {"@id": canon}})
    if p.get("faqs"):
        nodes.append({"@type": "FAQPage", "@id": canon + "#faq",
                      "mainEntity": [{"@type": "Question", "name": q,
                                      "acceptedAnswer": {"@type": "Answer", "text": " ".join(a)}} for q, a in p["faqs"]]})
    return {"@context": "https://schema.org", "@graph": nodes}


LW, LH = 244, 44
LOGO_MARK = ('<svg class="logo-mark" viewBox="0 0 40 40" width="40" height="40" aria-hidden="true" focusable="false">'
             '<rect width="40" height="40" rx="12" fill="#C21A6B"/>'
             '<path d="M20 7.5C20 7.5 10.5 18.6 10.5 25.2a9.5 9.5 0 0 0 19 0C29.5 18.6 20 7.5 20 7.5Z" fill="#fff"/>'
             '<path d="M21.6 17.5 16.6 25h3.6l-1.4 5.8 5.4-8h-3.7l1.1-5.3Z" fill="#C21A6B"/>'
             '<circle cx="31.5" cy="9" r="3.6" fill="#F4E028"/></svg>')


def header_html(p):
    slug = p["slug"]
    top3 = [(s, SERVICES[s][0]) for s in TOP3]
    dd = "".join(f'<li><a href="{url(s)}">{esc(n)}</a></li>' for s, n in top3)
    dd += '<li><a href="/services/">All Services</a></li>'
    da = "".join(f'<li><a href="{url(v["slug"])}">{esc(v["name"])}</a></li>' for v in LOCATIONS.values())
    da += '<li><a href="/areas/">All Service Areas</a></li>'
    cur = lambda s: ' aria-current="page"' if slug == s else ""
    drawer = ('<li><a href="/">Home</a></li><li><a href="/services/">Services</a></li>'
              + "".join(f'<li class="drawer-sub"><a href="{url(s)}">{esc(n)}</a></li>' for s, n in top3)
              + '<li class="drawer-sub"><a href="/services/">All Services</a></li>'
              + '<li><a href="/areas/">Service Areas</a></li>'
              + "".join(f'<li class="drawer-sub"><a href="{url(v["slug"])}">{esc(v["name"])}</a></li>' for v in LOCATIONS.values())
              + '<li><a href="/blog/">Blog</a></li><li><a href="/about/">About</a></li><li><a href="/contact/">Contact</a></li>'
              + f'<li><a class="drawer-cta" href="{tel()}">Call {PHONE_DISPLAY}</a></li>')
    return f'''<a class="skip" href="#main-content">Skip to main content</a>
<header role="banner">
<div class="topbar"><div class="wrap"><span class="topbar-hours"><b>24/7</b> emergency plumbing dispatch in {CITY}, {STATE}</span><a href="{tel()}">Call {PHONE_DISPLAY}</a></div></div>
<nav id="site-nav" class="site-nav" role="navigation" aria-label="Main navigation"><div class="wrap nav-inner">
<a class="logo" href="/" aria-label="{attr(BRAND)} home"><img class="logo-img" src="/img/logo.png" width="{LW}" height="{LH}" alt="{attr(BRAND)}"></a>
<ul class="nav-links" role="list">
<li><a href="/"{cur("")}>Home</a></li>
<li class="has-dropdown"><a href="/services/" aria-haspopup="true">Services <span class="dd-arrow" aria-hidden="true">&#9662;</span></a><ul class="dropdown" role="list">{dd}</ul></li>
<li class="has-dropdown"><a href="/areas/" aria-haspopup="true">Areas <span class="dd-arrow" aria-hidden="true">&#9662;</span></a><ul class="dropdown" role="list">{da}</ul></li>
<li><a href="/blog/"{cur("blog")}>Blog</a></li>
<li><a href="/contact/"{cur("contact")}>Contact</a></li>
<li><a class="nav-cta" href="{tel()}">Call Now</a></li>
</ul>
<button class="hamburger" id="mob-toggle" type="button" aria-expanded="false" aria-controls="mob-drawer" aria-label="Open navigation menu"><span></span><span></span><span></span></button>
</div></nav>
</header>
<div class="mob-drawer" id="mob-drawer" role="dialog" aria-modal="true" aria-label="Navigation menu" hidden>
<button class="drawer-close" id="drawer-close" type="button" aria-label="Close navigation menu">&#10005;</button>
<ul role="list">{drawer}</ul></div>
<div class="mob-overlay" id="mob-overlay" aria-hidden="true"></div>'''


def sitemap_map_html():
    q = MAP_SITEWIDE_Q.replace(" ", "+")
    return f'''<section class="sitemap-map" aria-labelledby="map-h"><div class="wrap">
<h2 id="map-h">Our 24/7 service area around Eden Prairie</h2>
<p>Emergency dispatch covers Eden Prairie and nearby towns including Minnetonka, Hopkins, Chanhassen and Bloomington.</p>
<iframe title="Map of the Eden Prairie, MN plumbing service area" aria-label="Map of the Eden Prairie, MN plumbing service area" src="https://maps.google.com/maps?q={q}&amp;output=embed&amp;z={MAP_SITEWIDE_Z}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
</div></section>'''


def footer_html():
    top3 = "".join(f'<a href="{url(s)}">{esc(SERVICES[s][0])}</a>' for s in TOP3)
    areas = "".join(f'<a href="{url(v["slug"])}">{esc(v["name"])}</a>' for v in LOCATIONS.values())
    return f'''<footer class="site-footer" role="contentinfo"><div class="wrap">
<div class="foot-brand"><a class="logo" href="/" aria-label="{attr(BRAND)} home"><img class="logo-img" src="/img/logo.png" width="{LW}" height="{LH}" alt="{attr(BRAND)}"></a>
<p>{esc(BRAND)}<br>{esc(ADDRESS_LINE)}</p>
<p><a href="{tel()}">{PHONE_DISPLAY}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
<div><h2 class="foot-h">Services</h2>{top3}<a href="/services/">All Services</a></div>
<div><h2 class="foot-h">Service Areas</h2>{areas}<a href="/areas/">All Service Areas</a></div>
<div><h2 class="foot-h">Company</h2><a href="/about/">About</a><a href="/blog/">Blog</a><a href="/contact/">Contact</a><a href="/privacy/">Privacy Policy</a><a href="/terms/">Terms of Service</a></div>
<p class="copyline">&copy; 2026 {esc(BRAND)}. All rights reserved.</p>
</div></footer>
<div class="sticky-cta"><a href="{tel()}">Call 24/7: {PHONE_DISPLAY}</a></div>
<script src="/assets/main.js" defer></script>'''
