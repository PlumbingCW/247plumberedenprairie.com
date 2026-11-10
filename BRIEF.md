# WRITER BRIEF: Eden Prairie 24/7 Plumbing (static site, call-only, Minnesota)

You write page copy as `.md` files in a small markdown dialect. A generator turns them into HTML. A validator checks your file. **Run the validator on every file you write and fix every ERROR before you finish:**

    python3 /home/claude/build/ep/tools/check_md.py /home/claude/build/ep/content/pages/<slug>.md      (service pages)
    python3 /home/claude/build/ep/tools/check_md.py /home/claude/build/ep/content/blogs/<slug>.md      (blog posts)

Read `/home/claude/build/ep/tools/check_md.py` once so you know every rule it enforces. Do not edit it, the generator, or anyone else's files. Write only the files assigned to you.

## 1. The business and the hard rules
Brand: **Eden Prairie 24/7 Plumbing**. Eden Prairie, MN (Hennepin County). 24/7 emergency dispatch by phone, call-only (the generator adds every phone button; you write one inline call link, see below). Nearby towns with their own pages: Minnetonka, Hopkins, Chanhassen, Bloomington.

Absolute rules (a violation is Critical):
- NO em dashes, en dashes, semicolons, or the characters `$`. Use commas, periods, parentheses and colons instead. No spaced hyphens used as dashes.
- NO prices or dollar amounts. Talk about cost factors in words only.
- NO invented trust: no reviews, testimonials, star ratings, customer counts, "years in business", "family owned", awards, licence numbers, insurer names, named technicians or owners, case studies of jobs that did not happen. Allowed wording: "licensed plumbers", "licensed and insured", "Clear price before work starts", "Same-day appointments when available".
- NO "free estimate", "free quote", "guarantee", "no obligation", no promised arrival time or response window.
- Never quote a caller or paraphrase it as a customer story. Describe situations generally ("a toilet that keeps running after you flush", "a water bill that jumps with no change in habits").
- Local facts: you may state a local fact ONLY if it is in section 3 (FACTS) below. If a fact is not there, do not invent it. For anything about permits, code rules or sump discharge rules, write that rules vary and the reader should ask the Eden Prairie building department or Utilities Division. Never state a water hardness figure other than the ones in FACTS. Never state a plumbing code requirement from memory. You may cite the Minnesota Plumbing Code (Minnesota Rules chapter 4714) by name only.
- General plumbing knowledge (how a trap works, what a flapper does, typical life of a tank water heater of roughly 8 to 12 years, why a sump pump fails) is fine when it is accurate and stable. Do not give exact repair prices, pipe-material dates, or code numbers you are not sure of.
- Banned phrases (validator enforces): delve into, comprehensive, robust, seamless, cutting-edge, state-of-the-art, meticulous, leverage, rest assured, peace of mind, top-notch, nestled, boasts, game-changer, a wide range of, when it comes to, in conclusion, furthermore, moreover, whether you're X or Y, look no further, at the forefront, "it's important to note". Also avoid "It's not just X, it's Y" patterns, lists of three adjectives for padding, and openers like "Understanding..." on more than 1 in 7 paragraphs.
- Paragraphs: 2 to 4 sentences, never more than 80 words. Vary sentence length (some 5 words, some 25). Plain, specific, confident, second person. Every local detail must close the loop with a practical consequence in the same paragraph.
- Concrete beats vague: name the part, the tool, the symptom, the sound, the number of fixtures affected. Aim for at least 2 concrete facts per 100 words.
- Use the Eden Prairie / MN entity pair naturally. Mention a real landmark or road from FACTS only where it genuinely fits.
- Every page must read as written for THIS page. Do not reuse the same H2 titles, sentences or openings as other pages. Use your own distinct structure for each page (the required elements below can be arranged and worded differently on every page).

## 2. File format (EPMD)
Each file begins with front matter between `---` lines, then the body.

```
---
slug: drain-cleaning
kw: drain cleaning
meta: <140 to 160 characters exactly, includes Eden Prairie, MN and ends with a call prompt like "Call (952) 866-9120.">
hero: <one sentence, 20 to 35 words, shown under the H1>
side_h3: <topic-specific heading for the sticky call card, under 45 chars>
side_copy: <one line for the card, under 110 chars>
side_link: sewer-line-cleaning | Sewer line cleaning
---
Body starts here. The H1 is generated, do not write one.

First paragraph (2 to 4 sentences). Inline links look like [[sewer-line-cleaning|sewer line cleaning]] and always point to a slug from section 5.

## An H2 section title
A paragraph. Another paragraph.

- bullet item (short)
- bullet item

1. numbered item

:::signs Optional title
### Sign title
One or two sentences (under 50 words).
### Another sign
Text.
:::

:::cards
### Card title
Text.
:::

:::table
Column A | Column B | Column C
Row 1 cell | cell | cell
Row 2 cell | cell | cell
:::

:::factors
Cost factor name: one-sentence explanation (4 or 5 of these)
Another factor: explanation
:::

:::steps
Step name: one sentence
:::

:::callout Short callout title
A paragraph or two.
:::

:::localnote Eden Prairie local note title
Paragraphs of verified local facts.
:::

:::faq
Q: Question text?
A: Answer paragraph. A second paragraph may follow after a blank line.

Q: Next question?
A: Answer.
:::
```
Rules of the format: one directive per block, closed by a line with only `:::`. Items inside `:::signs/cards/prep` start with `### `. Items in `:::factors/steps` are `Name: text` on one line each. Tables need a header row and 3 to 5 rows, cells under 25 words. Inline bold is `**text**` (use rarely). Internal links only as `[[slug|anchor text]]`. The single phone link is `[[call|call (952) 866-9120]]` (see below). No raw HTML, no images, no markdown links.

### The generator adds automatically (do not write these)
H1, breadcrumb, hero chips, the sticky call card (from your `side_*` fields), a mid-page call band, a closing call band, the FAQ rendering, schema, the map, header and footer. You write the article body only.

## 3. FACTS: the only local facts you may use (all from city, county, state or utility sources)
Phrase them as what the city/utility says. Never add numbers, dates or details beyond these. Do not give out phone numbers of other agencies.

**F1 Water source.** Eden Prairie's tap water comes from the City's 15 deep wells (average depth about 398 feet) in the Jordan-Prairie du Chien aquifer group. The City runs the water system.
**F2 Hardness.** The City softens water with lime at its treatment plant: untreated well water averages roughly 21 grains per gallon (about 360 mg/L), the tap averages about 5 grains per gallon (about 90 mg/L). The City says residents do not need a home water softener, that hardness is mainly a nuisance (not regulated), that softened water is not recommended for people on sodium-restricted diets, and that salt-softened water is not recommended for houseplants or irrigation.
**F3 Treatment sellers.** The City says to install a home water treatment system only if a specific need is identified, and warns about false claims and scare tactics from some sellers.
**F4 Additives.** Fluoride is added as state law requires. Chlorine is the disinfectant.
**F5 Lead and copper.** The City says no homes in Eden Prairie have tested positive for lead or copper in drinking water (2020 report: 0 of 30 tested sites over the action levels). Lead usually enters water inside the home through lead solder or brass fixtures, and most Eden Prairie homes were built after code safeguards against lead and copper were in place.
**F6 Water appearance.** Rusty or reddish water can occur during the City's spring flushing of mains: run cold taps for about five minutes. Pink residue is the airborne bacterium Serratia marcescens and black growth is also bacteria: clean with chlorine bleach. Calcium buildup on fixtures: clean with vinegar or a calcium and lime remover. Cloudy winter water is tiny air bubbles. Odors can have many causes including an aging water heater.
**F7 Meters.** Water meters are inside the home, usually in the basement near the water heater (sometimes crawl space or utility room), not outside. The City reads them remotely, offers a program called EyeOnWater for residents to track use, maintains the meter, and investigates suspected meter problems at no charge.
**F8 Ownership.** Property owners maintain all piping on their property, including the underground water service to the property line.
**F9 Leak checks.** City method: record the meter reading at bedtime, use no water overnight (irrigation and water-using appliances off), read it in the morning, and a changed reading means a leak. Toilet leaks: put dye tablets or food coloring in the tank, and a deteriorated flapper is a common cause. The City's utility FAQ says rebates may be available for repairing irrigation, faucet or toilet leaks through its Water Conservation Rebate Programs page (check current terms there).
**F10 Usage.** The City says one person typically uses about 5,000 to 7,000 gallons per quarter and a family of three about 22,000. Average residential use is about 74 gallons per person per day.
**F11 Shutoffs.** Most meters have two shutoff valves, one on each side (some have one). The curb stop is a street-side valve that lets the City shut off service to the home: keep it uncovered, and the City will adjust it to ground level and replace the cap at no charge (call the Utilities Division). For scheduled repairs the City notifies residents door-to-door at least 24 hours ahead, and for emergencies crews try to notify residents door-to-door before shutting water off.
**F12 Who handles what.** The City Utilities Division handles leaks, meter issues, water shutoffs and frozen-pipe advice on weekdays during business hours (7 a.m. to 3:30 p.m.). After 3:30 p.m. on weekdays and on weekends the City directs leak or frozen-pipe reports to the Police Department.
**F13 Systems.** The Utilities Division oversees water, sanitary sewer and storm sewer. Sanitary sewer: 262 miles of main, 23 lift stations, thousands of manholes, with sewage treatment handled through a user-fee system by the Metropolitan Council. Storm sewer: over 700 stormwater ponds, 687 stormwater basins and 209 miles of stormwater pipe. The utility is funded entirely by user fees. (The City does not state who owns or maintains a home's sewer service line. For that question tell readers to ask the Utilities Division.)
**F15 Permits.** The City's Building Inspections Division issues the Sewer and Water Permit (the application covers sewer, water, storm (commercial), inside water meters, and repair-only work). Required inspections listed on that form: rough-in visual, final, meter and air test. A permit becomes void if the authorized work is not started within 180 days. Whether a particular job needs a permit varies: tell readers to ask the Eden Prairie building department.
**F16 State rules and licensing.** Minnesota Rules chapter 4714 is the Minnesota Plumbing Code, administered by the Minnesota Plumbing Board. The Minnesota Department of Labor and Industry (DLI) says a plumbing contractor must always have a licensed master plumber as its responsible individual and must maintain a bond and insurance, and that employees without a license work under direct supervision. Homeowners can verify a plumber with DLI's license and registration lookup, which searches by a complete license number. Under Minnesota Statutes 326B.46 a person without a plumber's licence may do plumbing work meeting the Plumbing Board's minimum standards on premises they own and actually occupy as a residence, though a local ordinance may forbid it.
**F17 Growth.** Per the City: the town board first met in 1858. Population was about 2,000 in 1960 and almost 60,000 in 2000, and is now more than 64,000 residents in nearly 25,000 households. Flying Cloud Airport opened in 1946, and Interstate 494 and Eden Prairie Center were added in the mid-1970s. So most homes date from the 1970s onward, with some older farm-era buildings.
**F18 Historic house.** The brick Cummins-Phipps-Grill House was built in 1879 to 1880, and its first bathroom was installed in 1946 (Eden Prairie Historical Society, which runs the house under a lease with the City).
**F19 Landmarks and roads.** Eden Prairie Center, Flying Cloud Airport, Staring Lake Park, Purgatory Creek Park, Round Lake, Lake Riley, Miller Park, Bryant Lake Regional Park, the Minnesota River Bluffs Regional Trail, Hennepin Technical College (Eden Prairie campus), Interstate 494, US 169, US 212 and Minnesota Highway 5. ZIP codes of the city: 55344, 55346, 55347. The city sits on the north side of the Minnesota River valley.
**F20 Minnetonka.** Its own groundwater system: a city drinking water report (2017 data) lists 18 wells 405 to 575 feet deep in the Prairie du Chien-Jordan aquifer, with chlorine and fluoride added. That report does not give hardness.
**F21 Chanhassen.** City water treatment page: groundwater with naturally occurring iron, manganese and hardness. Two plants (East and West). Treatment removes nearly all iron and manganese but does not reduce hardness: 21 grains per gallon. The City does not soften the water, and says most residents benefit from a home water softener. Fluoride 0.7 ppm. Chanhassen is mostly in Carver County with a small part in Hennepin County. Hard water causes calcium buildup on fixtures and spots on dishes.
**F22 Hopkins.** City water plan: three active wells (500 to 548 feet) feed the Elmo Park Water Treatment Plant (built 1967, gravity filtration and chemicals to remove iron and manganese). It does not buy water regularly and has emergency interconnections with Minnetonka, St. Louis Park and Edina. The plan says the remaining aging and undersized watermains (about 25 percent of the system) are slated for replacement over 20 years. Hardness is not reported in the plan.
**F23 Bloomington.** City water report: six deep wells plus finished water bought from Minneapolis (Mississippi River), blended. The City softens with lime from about 19 grains per gallon to about 5.2. The City has inventoried its water services and found no lead service lines. City meters are usually in the basement, 12 to 24 inches above the floor. Bloomington has a 24-hour sewer-backup emergency line (do not give a number).
**F24 Chaska.** Chaska's city website advises setting a home softener to 29 grains per gallon.

If you need a fact that is not here, write the sentence without it or tell readers to test their tap and ask their water utility for its annual water quality report.

## 4. What every SERVICE page needs (validator checks most of this)
- **Length:** at least 1,000 words of body (leak-detection 1,500+). The H1 and hero line are extra.
- **First paragraph:** includes the page keyword (`kw:`) and "Eden Prairie". For EMERGENCY pages (marked E below) the first paragraph must also say it is an emergency/urgent, say 24/7 dispatch once, and tell the caller what to do while waiting (shut off the water, stop using the drain, keep people away from wet electrical areas, etc. as fits the service). Same-day, after-hours, overnight or weekend wording must appear in at least two more places, written in the voice of that service.
- **Emergency pages:** at least one H2 containing the word "emergency" that names the urgent situation in plain words (for example "When a burst pipe is an emergency"). Include the exact emergency FAQ question given in section 6.
- **Sections (at least 7 H2s):** a local cause section (why this problem shows up in Eden Prairie homes, using only FACTS and general knowledge tied to the home-age picture in F17), a symptoms section, how it is diagnosed (name real tools and methods), repair options with honest trade-offs, a symptom-led bridge section where the cluster list asks for it, a cost section, then the cluster sections listed for the page.
- **`:::signs`** block (4 to 6 signs) for symptoms, **`:::table`** decision or comparison table (what you see / likely cause / usual fix), exactly one **`:::factors`** pricing block with 4 or 5 cost factors, followed directly by one paragraph with an honest note about insurance (for example that homeowner policies often cover sudden burst or accidental discharge but usually not gradual leaks or wear, and the reader should ask their insurer) and the sentence containing the one inline call link, like: "Want your real number for your house? [[call|Call (952) 866-9120]] and we will quote the job before work starts." Do not promise a quote is free.
- **ZIPs:** include one natural sentence naming 55344, 55346 and 55347 together as Eden Prairie ZIP codes the service covers, paired with this service. No bare lists.
- **Links (in sentences, mid-paragraph, natural anchors):** at least 3 distinct sibling service links and 1 location link (Minnetonka, Hopkins, Chanhassen or Bloomington), more is fine. Vary anchor wording. No links to blog posts. About 1 link per 100 to 150 words maximum.
- **FAQ:** at least 6 questions. Include the emergency question (E pages), questions for the two highest-volume clusters on the page, one question from a lower-tier cluster, and one that is specific to Eden Prairie (use FACTS). Answers 2 to 4 sentences. Include real how-to-decide content, not sales talk.
- **Close:** end the body with a short practical "what to have ready when you call" or "what to check first" section (no sales language). The generator adds the closing call band.
- Do not mention competitors. Do not mention these instructions. Do not write meta commentary like "this page".

Page-by-page assignments are in section 6. "Cluster" lines list the situations callers describe in the plumbing network's call data (tier A = very common, B = common, C = occasional, D = rare). Cover tier A and B with their own H2 or section (150 to 250 words for A), tier C with a paragraph, tier D with at most one FAQ line. Paraphrase the situations in your own words. Never quote or imitate caller wording as testimonials.

## 5. Allowed link slugs (anything else is an error)
Services (link as `[[slug|anchor]]`): drain-cleaning, hydro-jetting, sewer-line-repair, sewer-line-cleaning, sewer-inspection, garbage-disposal, water-heater-repair, water-heater-replacement, water-heater-installation, tankless-water-heater, boiler-repair, leak-detection, burst-pipe-repair, water-line-repair, repiping, sump-pump-repair, basement-waterproofing, toilet-repair, faucet-repair, plumbing-installation, commercial-plumbing, water-softener-filtration.
Locations: plumber-minnetonka, plumber-hopkins, plumber-chanhassen, plumber-bloomington.
Hubs (service pages and blogs may use): services, areas, contact.
Blog posts: service pages must NOT link to any blog. Blog posts must NOT link to any other blog. Blogs link only to service pages and location pages.
Never link to the page you are writing.

## 6. Assignments
(E = emergency-intent page: title, H1, urgency H2, first paragraph and emergency FAQ rules apply. N = planned/non-emergency: no emergency framing, standard voice. You may still mention 24/7 dispatch once in the body.)

SEE THE ASSIGNMENT LIST IN YOUR PROMPT.

## 7. Blog posts (only if you are assigned blogs)
- Front matter: `slug`, `title` (65 characters or fewer, must contain "Eden Prairie", specific and useful, not clickbait), `kw`, `meta` (140 to 160 chars), `hero`, `side_h3`, `side_copy`, `side_link` (a service slug), `local_faq` (the exact text of the Eden Prairie-specific FAQ question, which must also appear in the `:::faq` block), `local_sources` (the SOURCE TYPES behind your localnote, for example "City of Eden Prairie utility FAQ (municipal utility page); City drinking water report").
- Length: at least 1,150 words, at least 6 H2s, at least 5 FAQ questions (one is the `local_faq`).
- Structure: a direct answer to the title question in the first 100 words (with Eden Prairie, MN), a practical how-to or decision section, one `:::table`, one `:::localnote Eden Prairie ... ` block (title names Eden Prairie) built ONLY from the FACTS suggested for your post (2 to 4 facts, each with a practical tie-back), and a FAQ.
- Links: at least 2 service links and links to at least 2 different location pages (natural sentences such as "We also cover Hopkins and Minnetonka homes with the same 24/7 line", in the body, not a list). One inline `[[call|...]]` call link. No other blogs, no hubs.
- Informational but never medical or legal advice. Safety first for gas, electrical and structural issues.
- Informational intent: answer the question honestly, including when DIY is reasonable and when to call. Do not hide the answer to sell.
- Byline is generated (the team). No author names.

When finished, reply with ONLY a short list: each file written, word count, and the validator result line. Do not paste the content back.

## 8. Extra allowed general facts (not local)
- Minnesota's call-before-you-dig service is 811 (Gopher State One Call). You may tell readers to call 811 before any excavation.
- Polybutylene supply pipe was installed in some homes built from the late 1970s through the mid-1990s. Galvanized steel supply pipe is mostly in much older homes.
- Gas smell: leave the building first, then call the gas utility or 911 from outside. Never operate switches, phones or flames inside. Do not promise any response time.
- CO alarm sounding: get everyone outside and call 911.
- WaterSense is the EPA's label for water-efficient toilets, faucets and showerheads.
- Typical tank water heater service life is roughly 8 to 12 years. Anode rods protect the tank. T&P (temperature and pressure relief) valves must discharge safely.
- Minnesota winters regularly bring below-zero cold, which is why exposed or exterior-wall pipes freeze.
