"""Single source of truth for the Eden Prairie 24/7 Plumbing build (city 71, master v14)."""

CITY = "Eden Prairie"
STATE = "MN"
STATE_FULL = "Minnesota"
COUNTY = "Hennepin County"
DOMAIN = "247plumberedenprairie.com"
SITE_URL = "https://" + DOMAIN
BRAND = "Eden Prairie 24/7 Plumbing"
BRAND_SHORT = "Eden Prairie 24/7"
ADDRESS_STREET = "7500 Flying Cloud Dr"
ADDRESS_LOCALITY = "Eden Prairie"
ADDRESS_REGION = "MN"
ADDRESS_ZIP = "55344"
ADDRESS_LINE = "7500 Flying Cloud Dr, Eden Prairie, MN 55344"
EMAIL = "contact@" + DOMAIN

# ONE phone variable. Swap here later for a local number.
PHONE_E164 = "+19528669120"
PHONE_DIGITS = "19528669120"
PHONE_DISPLAY = "(952) 866-9120"

PUBLISHED = "2026-10-16"
MODIFIED = "2026-10-16"
PUBLISHED_HUMAN = "October 16, 2026"

# Primary ZIPs of the city (the three ZIPs in the Section 1b table)
CITY_ZIPS = ["55344", "55346", "55347"]

# service slug -> (nav name, title service, emergency?, group)
# group is used for the services hub layout only.
SERVICES = {
    "drain-cleaning":            ("Drain Cleaning", "Drain Cleaning", True, "Drains and sewer"),
    "hydro-jetting":             ("Hydro Jetting", "Hydro Jetting", True, "Drains and sewer"),
    "sewer-line-repair":         ("Sewer Line Repair", "Sewer Line Repair", True, "Drains and sewer"),
    "sewer-line-cleaning":       ("Sewer Line Cleaning", "Sewer Line Cleaning", True, "Drains and sewer"),
    "sewer-inspection":          ("Sewer Inspection", "Sewer Inspection", False, "Drains and sewer"),
    "garbage-disposal":          ("Garbage Disposal", "Garbage Disposal Repair", True, "Fixtures and kitchen"),
    "water-heater-repair":       ("Water Heater Repair", "Water Heater Repair", True, "Water heaters and heat"),
    "water-heater-replacement":  ("Water Heater Replacement", "Water Heater Replacement", True, "Water heaters and heat"),
    "water-heater-installation": ("Water Heater Installation", "Water Heater Installation", False, "Water heaters and heat"),
    "tankless-water-heater":     ("Tankless Water Heater", "Tankless Water Heater", False, "Water heaters and heat"),
    "boiler-repair":             ("Boiler Repair", "Boiler Repair", True, "Water heaters and heat"),
    "leak-detection":            ("Leak Detection", "Leak Detection", True, "Leaks and water lines"),
    "burst-pipe-repair":         ("Burst Pipe Repair", "Burst Pipe Repair", True, "Leaks and water lines"),
    "water-line-repair":         ("Water Line Repair", "Water Line Repair", True, "Leaks and water lines"),
    "repiping":                  ("Repiping", "Repiping", False, "Leaks and water lines"),
    "sump-pump-repair":          ("Sump Pump Repair", "Sump Pump Repair", True, "Basement and water control"),
    "basement-waterproofing":    ("Basement Waterproofing", "Basement Waterproofing", False, "Basement and water control"),
    "toilet-repair":             ("Toilet Repair", "Toilet Repair", True, "Fixtures and kitchen"),
    "faucet-repair":             ("Faucet Repair", "Faucet Repair", True, "Fixtures and kitchen"),
    "plumbing-installation":     ("Plumbing Installation", "Plumbing Installation", False, "Fixtures and kitchen"),
    "commercial-plumbing":       ("Commercial Plumbing", "Commercial Plumbing", True, "Commercial and water quality"),
    "water-softener-filtration": ("Water Softener and Filtration", "Water Softener and Filtration", False, "Commercial and water quality"),
}

# Top 3 services by national volume that sit by name in the Services dropdown/mobile menu
TOP3 = ["water-heater-replacement", "drain-cleaning", "water-heater-repair"]

# location slug -> dict. Decisions recorded in the Batch 0 report.
LOCATIONS = {
    "minnetonka": {
        "name": "Minnetonka", "primary_zip": "55345", "zips": ["55345", "55305"],
        "county": "Hennepin County", "map_q": "Minnetonka, MN", "map_z": 13,
        "brand_suffix": "Eden Prairie 24/7", "top2": ["drain cleaning", "water heater repair"],
        "slug": "plumber-minnetonka",
    },
    "chanhassen": {
        "name": "Chanhassen", "primary_zip": "55317", "zips": ["55317"],
        "county": "Carver County", "map_q": "Chanhassen, MN", "map_z": 13,
        "brand_suffix": "Eden Prairie 24/7", "top2": ["water softeners", "sump pump repair"],
        "slug": "plumber-chanhassen",
    },
    "bloomington": {
        "name": "Bloomington", "primary_zip": "55438", "zips": ["55438", "55437", "55431"],
        "county": "Hennepin County", "map_q": "Bloomington, MN", "map_z": 13,
        "brand_suffix": "Eden Prairie 24/7", "top2": ["leak detection", "sewer line cleaning"],
        "slug": "plumber-bloomington",
    },
    "hopkins": {
        "name": "Hopkins", "primary_zip": "55343", "zips": ["55343", "55305"],
        "county": "Hennepin County", "map_q": "Hopkins, MN", "map_z": 14,
        "brand_suffix": "Eden Prairie 24/7", "top2": ["repiping", "burst pipe repair"],
        "slug": "plumber-hopkins",
    },
}

# Mention-only places (no page)
MENTION_ONLY = ["Edina", "Chaska", "Shakopee", "Excelsior", "Victoria", "Shorewood"]

STANDARD_PAGES = ["about", "contact", "privacy", "terms"]
HUBS = ["services", "areas", "blog"]

MAP_SITEWIDE_Q = "Eden Prairie, MN"
MAP_SITEWIDE_Z = 11
MAP_CONTACT_Q = "7500 Flying Cloud Dr, Eden Prairie, MN 55344"
MAP_CONTACT_Z = 15


# Neighborhood pages (added in the neighborhood expansion). slug -> data.
# kind: "residential" or "commercial". Types and evidence are recorded in reports/neighborhood-research-report.md
NEIGHBORHOODS = {
    "the-preserve": {
        "slug": "plumber-the-preserve", "name": "The Preserve", "kind": "residential",
        "title": "Plumber in The Preserve, Eden Prairie MN | Plumbing",
        "h1": "Plumber in The Preserve, Eden Prairie, MN",
        "meta": "Plumbing help in The Preserve, a planned neighborhood in southeastern Eden Prairie. Single-family, townhome and condo plumbing. Call (952) 866-9120.",
        "map_q": "The Preserve, Eden Prairie, MN", "map_z": 14, "link": "The Preserve",
        "blurb": "Planned neighborhood with houses, townhomes and apartments",
        "cta": "Tell us whether it is a house, townhome or apartment and where the water is showing.",
    },
    "bearpath": {
        "slug": "plumber-bearpath", "name": "Bearpath", "kind": "residential",
        "title": "Plumber in Bearpath, Eden Prairie MN | Plumbing Services",
        "h1": "Plumber in Bearpath, Eden Prairie, MN",
        "meta": "Plumbing help in Bearpath, the gated golf community in Eden Prairie. Gate access, larger homes and water heaters. Call (952) 866-9120.",
        "map_q": "Bearpath, Eden Prairie, MN", "map_z": 14, "link": "Bearpath",
        "blurb": "Gated golf community with larger homes and villas",
        "cta": "Mention the gate procedure and how large the house is, then describe the problem.",
    },
    "staring-lake": {
        "slug": "plumber-staring-lake", "name": "Staring Lake", "kind": "residential",
        "title": "Plumber near Staring Lake, Eden Prairie MN | Plumbing",
        "h1": "Plumber near Staring Lake, Eden Prairie, MN",
        "meta": "Plumbing help for homes near Staring Lake in Eden Prairie. Sump pumps, drains and water heaters. Call (952) 866-9120 to ask about service.",
        "map_q": "Staring Lake Park, Eden Prairie, MN", "map_z": 14, "link": "Staring Lake",
        "blurb": "Homes near the lake and park, with sump pump and drain advice",
        "cta": "Say whether it is a sump pump, a drain or a water heater, and what you have noticed.",
    },
    "round-lake": {
        "slug": "plumber-round-lake", "name": "Round Lake", "kind": "residential",
        "title": "Plumber near Round Lake, Eden Prairie MN | Plumbing",
        "h1": "Plumber near Round Lake, Eden Prairie, MN",
        "meta": "Plumbing help for homes near Round Lake and Valley View Road in Eden Prairie. Drains, fixtures and water heaters. Call (952) 866-9120.",
        "map_q": "Round Lake Park, Eden Prairie, MN", "map_z": 14, "link": "Round Lake",
        "blurb": "Family households along Valley View Road and the park",
        "cta": "Describe the fixture or drain that is giving you trouble and how long it has been happening.",
    },
    "golden-triangle": {
        "slug": "plumber-golden-triangle", "name": "Golden Triangle", "kind": "commercial",
        "title": "Commercial Plumber in Golden Triangle, Eden Prairie MN",
        "h1": "Commercial Plumber in the Golden Triangle, Eden Prairie, MN",
        "meta": "Commercial plumbing for offices, light industrial and mixed-use buildings in Eden Prairie's Golden Triangle. Call (952) 866-9120 to ask about service.",
        "map_q": "Golden Triangle, Eden Prairie, MN", "map_z": 13, "link": "Golden Triangle",
        "blurb": "Business and industrial district, commercial plumbing only",
        "cta": "Give the building type, your role as tenant, owner or manager, and where the water is.",
    },
}
