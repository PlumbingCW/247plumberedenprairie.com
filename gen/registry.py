"""Page registry: every slug, kind, title, h1, meta rules. Imported by generator and validators."""
from config import *

BLOGS = [
    # slug, topic keyword (for brief), service targets (slugs)
    ("plumbing-snake-kitchen-sink-eden-prairie-mn", "plumbing snake for a kitchen sink", ["drain-cleaning", "hydro-jetting"]),
    ("cast-iron-plumbing-pipe-fittings-eden-prairie-mn", "cast iron plumbing pipe and fittings", ["sewer-line-repair", "repiping"]),
    ("battery-backup-sump-pump-installation-eden-prairie-mn", "installing a battery backup sump pump", ["sump-pump-repair", "basement-waterproofing"]),
    ("waterproof-paint-for-basement-eden-prairie-mn", "waterproof paint for a basement", ["basement-waterproofing", "sump-pump-repair"]),
    ("cost-of-installing-water-heater-eden-prairie-mn", "cost of installing a water heater", ["water-heater-installation", "water-heater-replacement"]),
    ("install-toilet-tank-bolts-eden-prairie-mn", "how to install toilet tank bolts", ["toilet-repair", "plumbing-installation"]),
    ("gas-hot-water-heater-installation-cost-eden-prairie-mn", "gas hot water heater installation cost", ["water-heater-installation", "water-heater-replacement"]),
    ("tankless-water-heater-installed-outside-eden-prairie-mn", "can a tankless water heater be installed outside", ["tankless-water-heater", "water-heater-installation"]),
    ("cctv-camera-sewer-pipe-inspection-eden-prairie-mn", "CCTV camera sewer pipe inspection", ["sewer-inspection", "sewer-line-repair"]),
    ("dye-for-leak-detection-eden-prairie-mn", "dye for leak detection", ["leak-detection", "toilet-repair"]),
    ("electronic-leak-detection-testing-eden-prairie-mn", "electronic leak detection testing", ["leak-detection", "water-line-repair"]),
    ("causes-of-clogged-drains-eden-prairie-mn", "causes of clogged drains", ["drain-cleaning", "sewer-line-cleaning"]),
    ("does-boiling-water-unclog-drains-eden-prairie-mn", "does boiling water help clogged drains", ["drain-cleaning", "hydro-jetting"]),
    ("boiler-repair-24-hour-eden-prairie-mn", "24 hour boiler repair", ["boiler-repair", "water-heater-repair"]),
    ("garbage-disposal-installation-eden-prairie-mn", "garbage disposal installation, hardware store versus plumber", ["garbage-disposal", "plumbing-installation"]),
]
BLOG_SLUGS = [b[0] for b in BLOGS]

LOC_SLUGS = [v["slug"] for v in LOCATIONS.values()]
HOOD_SLUGS = [v["slug"] for v in NEIGHBORHOODS.values()]
SERVICE_SLUGS = list(SERVICES.keys())
HUB_SLUGS = ["services", "areas", "blog", "contact", "about"]


def kind_of(slug):
    if slug in SERVICES: return "service"
    if slug in LOC_SLUGS: return "location"
    if slug in HOOD_SLUGS: return "neighborhood"
    if slug in BLOG_SLUGS: return "blog"
    if slug in ("services", "areas", "blog"): return "hub"
    if slug in ("contact", "about"): return "std"
    if slug in ("privacy", "terms"): return "legal"
    if slug == "": return "home"
    return None


def svc_title(slug):
    nav, tsvc, emerg, group = SERVICES[slug]
    if emerg:
        for suf in ("24/7 Response", "24/7"):
            t = f"Emergency {tsvc} in Eden Prairie, MN | {suf}"
            if len(t) <= 60:
                return t
        return f"Emergency {tsvc} in Eden Prairie, MN"
    for suf in ("Eden Prairie 24/7 Plumbing", "Eden Prairie 24/7", "24/7 Plumbing"):
        t = f"{tsvc} in Eden Prairie, MN | {suf}"
        if len(t) <= 60:
            return t
    return f"{tsvc} in Eden Prairie, MN | 24/7"


def svc_h1(slug):
    nav, tsvc, emerg, group = SERVICES[slug]
    return (f"Emergency {tsvc} in Eden Prairie, MN" if emerg else f"{tsvc} in Eden Prairie, MN")


def svc_emerg_faq_q(slug):
    nav, tsvc, emerg, group = SERVICES[slug]
    names = {
        "drain-cleaning": "drain cleaning", "hydro-jetting": "hydro jetting", "sewer-line-repair": "sewer line repair",
        "sewer-line-cleaning": "sewer line cleaning", "garbage-disposal": "garbage disposal", "water-heater-repair": "water heater",
        "water-heater-replacement": "water heater replacement", "boiler-repair": "boiler", "leak-detection": "leak detection",
        "burst-pipe-repair": "burst pipe", "water-line-repair": "water line", "sump-pump-repair": "sump pump",
        "toilet-repair": "toilet", "faucet-repair": "faucet and fixture", "commercial-plumbing": "commercial plumbing",
    }
    n = names.get(slug, tsvc.lower())
    return f"Do you handle {n} emergencies at night or on weekends in Eden Prairie?"


def loc_title(key):
    L = LOCATIONS[key]
    return f"Emergency Plumber {L['name']} MN {L['primary_zip']} | {L['brand_suffix']}"


def loc_h1(key):
    return f"Emergency Plumber {LOCATIONS[key]['name']} MN Near Eden Prairie"


def loc_key_from_slug(slug):
    for k, v in LOCATIONS.items():
        if v["slug"] == slug: return k


if __name__ == "__main__":
    for s in SERVICES:
        t = svc_title(s)
        print(f"{len(t):3d} {t}  | H1: {svc_h1(s)}")
    for k in LOCATIONS:
        t = loc_title(k); print(len(t), t, "|", loc_h1(k))
