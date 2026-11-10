from config import *
import registry as R
from util import *

FAQS = [
    ("Is there an emergency plumber available at night in Eden Prairie?",
     ["Yes. Our dispatch line answers 24/7, including nights, weekends and holidays. Tell the dispatcher what is happening and they will book the soonest appointment that is open, and same-day appointments are available when a slot is open.",
      "While you wait, shut off the main water valve if water is escaping, stop using any drain that is backing up, and keep people away from wet electrical areas, then [[call|call (952) 866-9120]]."]),
    ("What should I do while I wait for the plumber?",
     ["For a burst pipe or active leak, close the main shutoff valve, which is usually near the water meter in the basement. Open a faucet on the lowest floor to drain the lines, and move valuables out of the wet area.",
      "For a sewer backup, stop running water in the house and do not use chemical drain cleaners. If you smell gas, leave the building first and call the gas utility or 911 from outside."]),
    ("Which Eden Prairie ZIP codes do you cover?",
     ["We cover all three Eden Prairie ZIP codes: 55344, 55346 and 55347. Dispatch also reaches nearby ZIP codes in Minnetonka, Hopkins, Chanhassen and Bloomington, which each have their own page on this site."]),
    ("Which nearby towns do you serve besides Eden Prairie?",
     ["The same 24/7 line covers [[plumber-minnetonka|Minnetonka]], [[plumber-hopkins|Hopkins]], [[plumber-chanhassen|Chanhassen]] and [[plumber-bloomington|Bloomington]]. Calls from Edina and Chaska are welcome too, so tell the dispatcher your address and they will confirm the appointment."]),
    ("How does pricing work?",
     ["You get a clear price before work starts. The final number depends on the problem, the parts, the access to the pipe and the time of day, so the dispatcher or technician explains it before anyone picks up a tool."]),
    ("Do you handle commercial properties in Eden Prairie?",
     ["Yes. [[commercial-plumbing|Commercial plumbing]] calls for offices, restaurants, retail and multi-unit buildings use the same 24/7 line. Tell the dispatcher the type of building and where the shutoff valves are if you know."]),
    ("How can I check that a plumber is licensed in Minnesota?",
     ["The Minnesota Department of Labor and Industry runs a license and registration lookup on its website. It searches by a complete license number, so ask any plumber for theirs before work starts. State rules also require a plumbing contractor to keep a licensed master plumber in charge of its plumbing work."]),
]

SERVICE_BLURBS = {
    "drain-cleaning": "Clogs in sinks, tubs and floor drains cleared with cables, jetters and cameras.",
    "sewer-line-cleaning": "Main line backups cleared fast, with a plan so they do not return.",
    "water-heater-repair": "Leaks, no hot water and pilot problems on gas, electric and hybrid tanks.",
    "water-heater-replacement": "A failed tank swapped, sized and vented, often the same day when a slot is open.",
    "leak-detection": "Meter running, wet ceilings and slab leaks found without tearing out walls first.",
    "burst-pipe-repair": "Burst and frozen pipes shut down, repaired and dried out.",
    "toilet-repair": "Running, leaking and clogged toilets repaired or replaced.",
    "faucet-repair": "Dripping faucets, failed supply valves and shower valves fixed.",
    "sump-pump-repair": "Sump and ejector pumps repaired, replaced and backed up.",
    "hydro-jetting": "High-pressure water scours grease, scale and roots out of stubborn lines.",
    "garbage-disposal": "Jammed, humming and leaking disposals repaired or replaced.",
    "sewer-line-repair": "Cracked, rooted and collapsed sewer lines repaired or relined.",
}
HOME_SERVICES = list(SERVICE_BLURBS.keys())


def build(hero_for, hero_img, ctaband, sidecard, crumbs_html):
    import build as B
    h = hero_for("", "home")
    p = {"slug": "", "kind": "home", "title": "Emergency Plumber in Eden Prairie, MN | 24/7 Plumbing",
         "meta": "Emergency plumber in Eden Prairie, MN open 24/7. Burst pipes, sewer backups, leaks and water heaters handled by licensed plumbers. Call " + PHONE_DISPLAY + ".",
         "h1": "Emergency Plumber in Eden Prairie, MN", "crumbs": [("Home", "")], "hero_src": h}
    p["faqs"] = [(plain(q), [plain(a) for a in ans]) for q, ans in FAQS]
    top = "".join(f'<a class="prow" href="{url(s)}">{esc(SERVICES[s][0])}<b>&rarr;</b></a>' for s in TOP3)
    cards = "".join(
        f'<div class="card"><div class="ic" aria-hidden="true">{i+1}</div><h3>{esc(SERVICES[s][0])}</h3><p>{esc(SERVICE_BLURBS[s])}</p>'
        f'<a class="more" href="{url(s)}">{"Emergency " if SERVICES[s][2] else ""}{esc(SERVICES[s][0])} in Eden Prairie &rarr;</a></div>'
        for i, s in enumerate(HOME_SERVICES))
    areas = "".join(f'<a href="{url(v["slug"])}">{esc(v["name"])}</a>' for v in LOCATIONS.values())
    hoods = "".join(f'<a href="{url(v["slug"])}">{esc(v["link"])}</a>' for v in NEIGHBORHOODS.values())
    faq_html = ""
    for i, (q, ans) in enumerate(FAQS):
        faq_html += (f'<div class="faq-item{" open" if i==0 else ""}"><h3 class="faq-q"><button type="button" aria-expanded="{"true" if i==0 else "false"}" aria-controls="hf-{i}">{inline(q)}</button></h3>'
                     f'<div class="faq-answer" id="hf-{i}"><div class="faq-answer-in">' + "".join(f"<p>{inline(a)}</p>" for a in ans) + "</div></div></div>")
    main = f'''<div class="hero has-hero">{hero_img(h)}<div class="wrap"><div>
<span class="badge">24/7 Emergency Line Open</span>
<h1>Emergency Plumber in Eden Prairie, MN <span>Open 24/7</span></h1>
<p class="lede">Burst pipe, sewer backup, active leak or a water heater that quit? {esc(BRAND)} dispatches licensed plumbers around the clock across Eden Prairie and nearby towns.</p>
<div class="cta-row"><a class="btn" href="{tel()}">Call {PHONE_DISPLAY}</a><a class="btn ghost" href="/services/">See all services</a></div>
<ul class="trustrow"><li>24/7 dispatch</li><li>Licensed and insured</li><li>Clear price before work starts</li></ul>
</div>
</div></div>
<div class="strip"><div class="wrap"><div class="stripitem"><span class="ic" aria-hidden="true">&#9679;</span>Dispatch answers 24/7</div><div class="stripitem"><span class="ic" aria-hidden="true">&#9679;</span>Same-day appointments when available</div><div class="stripitem"><span class="ic" aria-hidden="true">&#9679;</span>Licensed and insured</div><div class="stripitem"><span class="ic" aria-hidden="true">&#9679;</span>Clear price before work starts</div></div></div>
<section class="emergency" aria-labelledby="em-h"><div class="wrap"><div><h2 id="em-h">Water on the floor or a drain backing up right now?</h2>
<p>Close the main shutoff valve, stop using the drain, keep people away from wet electrical areas, and call. An emergency plumber is on the line at any hour.</p></div>
<a class="btn" href="{tel()}">Call the 24/7 line</a></div></section>
<section class="sec" id="services"><div class="wrap"><span class="kick">What we fix</span><h2 class="sec-title">24/7 emergency plumbing services in Eden Prairie</h2>
<p class="lead">Most emergency calls fall into a short list: water that will not stop, drains that will not clear, and hot water that has gone cold. Each service below has its own page with symptoms, repair options and what to do while you wait.</p>
<div class="cards">{cards}</div>
<p class="lead">Planned work is covered too, from [[water-heater-installation|water heater installation]] and [[repiping|repiping]] to [[commercial-plumbing|commercial plumbing]], and the full list is on the [[services|services page]].</p></div></section>'''
    main = main.replace("[[water-heater-installation|water heater installation]]", f'<a href="{url("water-heater-installation")}">water heater installation</a>') \
               .replace("[[repiping|repiping]]", f'<a href="{url("repiping")}">repiping</a>') \
               .replace("[[commercial-plumbing|commercial plumbing]]", f'<a href="{url("commercial-plumbing")}">commercial plumbing</a>') \
               .replace("[[services|services page]]", f'<a href="{url("services")}">services page</a>')
    main += f'''
<section class="sec soft" id="why"><div class="wrap"><span class="kick">Why call us</span><h2 class="sec-title">What a call to Eden Prairie 24/7 Plumbing looks like</h2>
<div class="why">
<div class="whycard"><div class="num">1</div><h3>One number, any hour</h3><p>The same dispatch line answers at 2 a.m. on a holiday and at noon on a weekday.</p></div>
<div class="whycard"><div class="num">2</div><h3>Price before work</h3><p>You hear the price before anyone starts, so there is nothing to argue about later.</p></div>
<div class="whycard"><div class="num">3</div><h3>Same-day when open</h3><p>Dispatch books the soonest slot available and says so plainly when a slot is not open.</p></div>
<div class="whycard"><div class="num">4</div><h3>Local pipe knowledge</h3><p>Eden Prairie homes, water and winters shape the diagnosis, and we say what applies.</p></div>
</div></div></section>
<section class="sec" id="local"><div class="wrap"><div class="prose">
<span class="kick">Eden Prairie plumbing, locally</span><h2 class="sec-title">What Eden Prairie homeowners should know before a plumbing emergency</h2>
<p>Eden Prairie grew from about 2,000 residents in 1960 to almost 60,000 by 2000, according to the City, with Interstate 494 and Eden Prairie Center arriving in the mid-1970s. That means most homes date from the 1970s onward, so many plumbing problems here come from fixtures, water heaters and sump pumps wearing out rather than from very old pipe.</p>
<p>The City also says its tap water is softened at the treatment plant to about 5 grains per gallon, down from roughly 21 in the well water. For homeowners that means scale builds up slowly, so a water heater that fails early is more likely a sediment, anode or fitting problem than a hard-water one. Our <a href="{url("water-heater-repair")}">water heater repair</a> page covers the checks.</p>
<p>Your water meter sits inside the house, usually in the basement near the water heater, and the City says it will look into suspected meter problems at no charge. Knowing where that meter and its two shutoff valves are is the fastest way to stop a burst pipe, and it is also where a hidden leak shows up first. We use the same spot for <a href="{url("leak-detection")}">leak detection</a>.</p>
<p>Our dispatch address is {esc(ADDRESS_LINE)}, and calls from the 55344, 55346 and 55347 ZIP codes get the same 24/7 line. Landmarks like Flying Cloud Airport, Staring Lake and Purgatory Creek Park help dispatchers pin down a neighborhood when you are not sure of the cross street.</p>
</div></div></section>
<section class="sec soft" id="how"><div class="wrap"><span class="kick">How it works</span><h2 class="sec-title">From phone call to fixed pipe</h2>
<div class="steps">
<div class="step"><div class="n">1</div><h3>You call</h3><p>Describe what you see and hear. The dispatcher asks where the shutoff is.</p></div>
<div class="step"><div class="n">2</div><h3>Stop the damage</h3><p>You get simple steps to limit water or sewage until help arrives.</p></div>
<div class="step"><div class="n">3</div><h3>Clear price</h3><p>The plumber explains the problem and the price before work starts.</p></div>
<div class="step"><div class="n">4</div><h3>Fixed and tested</h3><p>The repair is made, tested under pressure or flow, and explained.</p></div>
</div></div></section>
<section class="sec" id="areas"><div class="wrap"><span class="kick">Where we work</span><h2 class="sec-title">Emergency plumber for Eden Prairie and nearby towns</h2>
<p class="lead">The Eden Prairie dispatch line covers the whole city and the towns around it. Each town below has its own page with local water facts and the ZIP codes we serve.</p>
<div class="areas">{areas}</div>
<p class="lead">We also take calls from Edina and Chaska, and the full list is on the <a href="{url("areas")}">service areas page</a>.</p></div></section>
<section class="sec" id="neighborhoods"><div class="wrap"><span class="kick">Around the city</span><h2 class="sec-title">Neighborhoods We Serve in Eden Prairie</h2>
<p class="lead">Some parts of Eden Prairie have plumbing questions of their own, from gated homes to a planned neighborhood and the Golden Triangle business district. Pick yours for local notes.</p>
<div class="areas">{hoods}</div></div></section>
<section class="sec soft" id="faq-home"><div class="wrap"><div class="prose"><span class="kick">Quick answers</span><h2 class="sec-title">Emergency plumbing questions in Eden Prairie</h2>
<section class="faq-sec">{faq_html}</section></div></div></section>
''' + ctaband("Emergency plumber in Eden Prairie, MN", "Call the 24/7 line and a dispatcher will get a plumber moving.")
    return p, main
