#!/usr/bin/env python3
"""Validator for EPMD page copy. Usage: check_md.py FILE.md [FILE.md ...]   (exit 1 if any ERROR)"""
import re, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gen"))
from mdparse import parse, iter_text, LINK_RE
import registry as R
from config import SERVICES, LOCATIONS

BANNED = ["delve into", "navigate the complexities", "in today's fast-paced", "it's important to note", "it is important to note", "it's worth noting",
          "it is worth noting", "tapestry", "realm", "landscape", "robust", "comprehensive", "seamless", "cutting-edge", "state-of-the-art", "meticulous",
          "underscore", "leverage", "elevate your", "transform your", "unlock your", "at the forefront", "whether you're", "whether you are", "look no further",
          "rest assured", "we pride ourselves", "peace of mind", "top-notch", "nestled", "boasts", "game-changer", "a wide range of", "when it comes to",
          "world-class", "second to none", "unparalleled", "dive into", "ever-evolving", "in conclusion", "furthermore", "moreover"]
FORBID_RE = [
    (r"\$", "dollar sign / price figure"),
    (r"free (estimate|quote|inspection|diagnos|consult)", "free estimate language"),
    (r"no[- ]obligation", "no-obligation language"),
    (r"guarantee", "guarantee language"),
    (r"\b\d+\+?\s+years\b", "years-of-experience style claim"),
    (r"years of experience|years in business|family[- ]owned|locally owned|since \d{4}|jobs completed|customers served|five-star|5-star|award", "fabricated trust"),
    (r"within \d+ (minutes|hours)|in \d+ minutes|in under an hour|arrive (within|in)|arrival (time|window)", "arrival promise"),
    (r"\blicense (number|#)|\blicen[sc]e no", "licence number"),
    (r"click here|learn more", "generic anchor/phrase"),
    (r"[—–]", "em/en dash"),
    (r";", "semicolon"),
    (r"<[a-z/]", "raw html"),
]
URGENCY_ACTION = re.compile(r"shut off|turn off|stop using|stop running|keep (people|kids|children|pets)|unplug|avoid|do not|don't|clear the area|move (valuables|items)", re.I)
SAME_DAY = re.compile(r"same-day|same day|after[- ]hours|overnight|weekend|at night|middle of the night|holiday", re.I)


def words(s):
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'/%\-]*", s))


def plain(s):
    s = LINK_RE.sub(lambda m: m.group(2), s)
    return s.replace("**", "")


def check(path):
    errs, warns = [], []
    raw = open(path, encoding="utf-8").read()
    fm, nodes = parse(raw)
    slug = fm.get("slug") or os.path.splitext(os.path.basename(path))[0]
    kind = R.kind_of(slug)
    if kind is None:
        errs.append(f"unknown slug {slug}")
        return errs, warns, {}
    all_text = list(iter_text(nodes))
    full = " ".join(plain(t) for k, t in all_text)
    wc = words(full)

    # front matter
    need = ["slug", "meta", "hero", "side_h3", "side_copy", "side_link"] if kind in ("service", "blog", "location", "neighborhood") else ["slug", "meta", "hero"]
    if kind in ("location", "neighborhood"): need.remove("meta")
    if kind in ("service", "blog"): need += ["kw"]
    if kind == "blog": need += ["title"]
    for k in need:
        if not fm.get(k): errs.append(f"front matter missing: {k}")
    meta = fm.get("meta", "")
    if kind in ("service", "blog", "std", "hub", "legal", "home"):
        if not (140 <= len(meta) <= 160): errs.append(f"meta length {len(meta)} (need 140-160)")
    if kind == "blog":
        t = fm.get("title", "")
        if len(t) > 65: errs.append(f"blog title {len(t)} chars > 65")
        if "Eden Prairie" not in t: errs.append("blog title lacks Eden Prairie")
    for k in ("meta", "hero", "side_h3", "side_copy", "title"):
        v = fm.get(k, "")
        for pat, why in FORBID_RE:
            if re.search(pat, v, re.I): errs.append(f"front matter {k}: {why}")
    if fm.get("side_link"):
        tgt = fm["side_link"].split("|")[0].strip()
        if R.kind_of(tgt) != "service": errs.append(f"side_link must be a service slug, got {tgt}")

    # floors
    floors = {"service": 1000, "blog": 1150, "location": 1000, "home": 1200, "std": 450, "hub": 250, "legal": 350}
    if wc < floors.get(kind, 0): errs.append(f"words {wc} < target {floors[kind]}")

    # forbidden patterns & banned phrases
    lower = full.lower()
    for b in BANNED:
        if b in lower: errs.append(f"banned phrase: {b}")
    for pat, why in FORBID_RE:
        for m in re.finditer(pat, full, re.I):
            errs.append(f"{why}: ...{full[max(0,m.start()-30):m.end()+30]}...")
            break
    if re.search(r"\s-\s", full): warns.append("spaced hyphen ' - ' (looks like a dash)")

    # paragraphs
    paras = [plain(t) for k, t in all_text if k in ("p", "a")]
    longp = [p for p in paras if words(p) > 80]
    for p in longp: errs.append(f"paragraph {words(p)} words: {p[:60]}...")
    cardp = [plain(t) for k, t in all_text if k == "cardp"]
    for p in cardp:
        if words(p) > 70: errs.append(f"card text {words(p)} words: {p[:60]}...")
    ger = sum(1 for p in paras if re.match(r"^[A-Z][a-z]+ing\b", p))
    if paras and ger / len(paras) > 0.15: warns.append(f"gerund openers {ger}/{len(paras)}")
    for p in paras:
        n = len(re.findall(r"[.!?](\s|$)", p))
        if n > 5: warns.append(f"paragraph with {n} sentences: {p[:50]}...")

    # links
    links = LINK_RE.findall(raw)
    tgts = []
    calls = 0
    for tgt, anchor in links:
        if tgt == "call": calls += 1; continue
        if tgt == "home": continue
        k2 = R.kind_of(tgt)
        if k2 is None: errs.append(f"link to unknown slug: {tgt}"); continue
        tgts.append((tgt, k2, anchor))
        if tgt == slug: errs.append(f"self link {tgt}")
        if kind in ("service", "location", "std", "hub", "legal", "home") and k2 == "blog": errs.append(f"silo: money page links to blog {tgt}")
        if kind == "blog" and k2 not in ("service", "location"): errs.append(f"blog may link only to service/location pages, got {tgt}")
    ks = [k for _, k, _ in tgts]
    if kind == "service":
        if ks.count("service") < 2: errs.append(f"needs >=2 sibling service links (has {ks.count('service')})")
        if ks.count("location") < 1: errs.append("needs >=1 location link")
        if len(tgts) < 3: errs.append("needs >=3 body links")
    if kind == "blog":
        if ks.count("service") < 2: errs.append(f"blog needs >=2 service links (has {ks.count('service')})")
        if len(set(t for t, k, _ in tgts if k == "location")) < 2: errs.append("blog needs links to 2 different location pages")
    if kind == "location":
        if len(set(t for t, k, _ in tgts if k == "service")) < 3: errs.append("location needs >=3 distinct service links")
        if len(set(t for t, k, _ in tgts if k == "location")) < 2: errs.append("location needs 2 nearby location links")
    if kind in ("service", "blog", "location"):
        if len(tgts) > wc / 60: warns.append(f"link density high: {len(tgts)} links / {wc} words")
        if calls < 1: errs.append("needs one [[call|...]] inline phone link")
        if calls > 2: errs.append(f"too many inline call links ({calls}); keep 1")
    anchors = [a.lower() for _, _, a in tgts]
    for a in set(anchors):
        if anchors.count(a) > 2: warns.append(f"anchor repeated {anchors.count(a)}x: {a}")
    # same target linked repeatedly
    for t in set(x[0] for x in tgts):
        c = [x[0] for x in tgts].count(t)
        if c > 3: warns.append(f"target {t} linked {c}x")

    # structure
    h2s = [t for k, t in all_text if k == "h2"]
    dirs = [n[0] for n in nodes]
    faqs = [n for n in nodes if n[0] == "faq"]
    nq = sum(len(n[2]) for n in faqs)
    if kind == "service":
        meta_ok = True
        if len(h2s) < 7: errs.append(f"only {len(h2s)} H2 sections (need >=7)")
        if "signs" not in dirs: errs.append("needs a :::signs block")
        if "table" not in dirs: errs.append("needs a :::table comparison/decision table")
        if dirs.count("factors") != 1: errs.append("needs exactly one :::factors pricing block")
        if nq < 6: errs.append(f"FAQ has {nq} questions (need >=6)")
        emerg = SERVICES[slug][2]
        qs = [q for n in faqs for q, a in n[2]]
        if emerg:
            eq = R.svc_emerg_faq_q(slug)
            if eq not in qs: errs.append(f"missing exact emergency FAQ question: {eq}")
            if not any("emergency" in h.lower() for h in h2s): errs.append("no H2 containing 'emergency'")
            first = next((plain(t) for k, t in all_text if k == "p"), "")
            if "24/7" not in first: errs.append("first paragraph lacks 24/7")
            if not re.search(r"emergenc|urgent|right now|active", first, re.I): errs.append("first paragraph lacks urgency wording")
            if not URGENCY_ACTION.search(first): errs.append("first paragraph lacks a what-to-do-while-waiting action")
            if len(SAME_DAY.findall(full)) < 3: errs.append("same-day/after-hours language <3 places")
        else:
            if re.search(r"^emergency", fm.get("hero", ""), re.I): warns.append("non-emergency page hero starts with Emergency")
        kw = fm.get("kw", "").lower()
        first100 = " ".join(plain(t) for k, t in all_text if k == "p")
        first100 = " ".join(first100.split()[:100]).lower()
        if kw and kw not in first100: errs.append(f"kw '{kw}' not in first 100 words")
        if "eden prairie" not in first100: warns.append("Eden Prairie not in first 100 words")
        zips = re.findall(r"\b5534[467]\b", full)
        if len(set(zips)) < 3: errs.append("service page must name the Eden Prairie ZIPs 55344, 55346 and 55347 in one body sentence")
    if kind == "blog":
        if "localnote" not in dirs: errs.append("needs :::localnote block")
        if nq < 5: errs.append(f"blog FAQ has {nq} questions (need >=5)")
        if fm.get("local_faq") and not any(fm["local_faq"] == q for n in faqs for q, a in n[2]): errs.append("local_faq question not found in FAQ")
        if not fm.get("local_faq"): errs.append("front matter local_faq (exact text of the Eden Prairie specific question) missing")
        if len(h2s) < 6: errs.append(f"only {len(h2s)} H2 (need >=6)")
        if "eden prairie" not in lower: errs.append("no Eden Prairie mention")
        ln = [n for n in nodes if n[0] == "localnote"]
        if ln and "Eden Prairie" not in ln[0][1]: errs.append("localnote title must name Eden Prairie")
        if ln and fm.get("local_sources", "") == "": errs.append("front matter local_sources (source TYPE list) missing")
    if kind == "location":
        for need_d in ("prep", "faq"):
            if need_d not in dirs: errs.append(f"needs :::{need_d}")
        key = R.loc_key_from_slug(slug)
        L = LOCATIONS[key]
        qs = [q for n in faqs for q, a in n[2]]
        zq = f"Do you cover every ZIP code in {L['name']}?"
        eq = f"Is emergency service available in {L['name']}?"
        if zq not in qs: errs.append(f"missing FAQ: {zq}")
        if eq not in qs: errs.append(f"missing FAQ: {eq}")
        for z in L["zips"]:
            if z not in full: errs.append(f"ZIP {z} not in body")
        if len(len(re.findall(r"emergency|24/7|around the clock", full, re.I)) * [1]) < 6: errs.append("emergency weave: <6 mentions in body")
        if nq < 6: errs.append(f"FAQ has {nq} questions (need >=6)")
    stats = {"slug": slug, "kind": kind, "words": wc, "h2": len(h2s), "faq": nq, "links": len(tgts), "calls": calls}
    return errs, warns, stats


def main():
    bad = 0
    for p in sys.argv[1:]:
        errs, warns, st = check(p)
        print(f"== {os.path.basename(p)} {st}")
        for e in errs: print("  ERROR:", e)
        for w in warns: print("  warn :", w)
        if errs: bad += 1
    print(f"\n{len(sys.argv)-1} files, {bad} with errors")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
