from util import *
from config import *


def render_nodes(nodes, ctx):
    out, faqs = [], []
    h2_total = sum(1 for n in nodes if n[0] == "h2")
    mid_at = 5 if h2_total >= 7 else max(3, h2_total - 1)
    h2_seen = 0
    for n in nodes:
        k = n[0]
        if k == "h2":
            h2_seen += 1
            if h2_seen == mid_at and ctx.get("midcta", True):
                out.append(midcta(ctx))
            out.append(f'<h2 id="{slugify(n[1])}">{inline(n[1])}</h2>')
        elif k == "p":
            out.append(f"<p>{inline(n[1])}</p>")
        elif k in ("ul", "ol"):
            out.append(f"<{k}>" + "".join(f"<li>{inline(i)}</li>" for i in n[1]) + f"</{k}>")
        elif k == "signs":
            if n[1]:
                out.append(f'<h3>{inline(n[1])}</h3>')
            out.append('<div class="boxgrid">' + "".join(
                f'<div class="sign"><h3>{inline(t)}</h3>' + "".join(f"<p>{inline(x)}</p>" for x in ps) + "</div>" for t, ps in n[2]) + "</div>")
        elif k == "cards":
            out.append(f'<div class="cards cards-{3 if len(n[2])==3 else 2}">' + "".join(
                f'<div class="card"><h3>{inline(t)}</h3>' + "".join(f"<p>{inline(x)}</p>" for x in ps) + "</div>" for t, ps in n[2]) + "</div>")
        elif k == "prep":
            if n[1]:
                out.append(f'<h3>{inline(n[1])}</h3>')
            out.append('<div class="prepgrid">' + "".join(
                f'<div class="prep"><span class="n">{i+1}</span><h3>{inline(t)}</h3>' + "".join(f"<p>{inline(x)}</p>" for x in ps) + "</div>"
                for i, (t, ps) in enumerate(n[2])) + "</div>")
        elif k == "table":
            rows = n[2]
            head = "<tr>" + "".join(f"<th scope=\"col\">{inline(c)}</th>" for c in rows[0]) + "</tr>"
            body = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rows[1:])
            out.append(f'<div class="table-wrap"><table><thead>{head}</thead><tbody>{body}</tbody></table></div>')
        elif k == "factors":
            out.append('<div class="factors">' + "".join(
                (f'<div class="factor"><b>{inline(t)}</b>{inline(x)}</div>' if t else f'<div class="factor">{inline(x)}</div>') for t, x in n[2]) + "</div>")
        elif k == "steps":
            out.append('<ol class="stepper">' + "".join(
                f'<li><b>{inline(t)}</b> {inline(x)}</li>' if t else f"<li>{inline(x)}</li>" for t, x in n[2]) + "</ol>")
        elif k == "callout":
            out.append(f'<div class="callout"><h3>{inline(n[1])}</h3>' + "".join(f"<p>{inline(x)}</p>" for x in n[2]) + "</div>")
        elif k == "localnote":
            out.append(f'<section class="localnote"><span class="kick">Local note</span><h2 id="{slugify(n[1])}">{inline(n[1])}</h2>'
                       + "".join(f"<p>{inline(x)}</p>" for x in n[2]) + "</section>")
        elif k == "faq":
            title = n[1] or ctx.get("faq_title", "Frequently asked questions")
            items = []
            for i, (q, ans) in enumerate(n[2]):
                fid = f"faq-{len(faqs)+1}"
                items.append(f'<div class="faq-item{" open" if len(faqs)==0 else ""}"><h3 class="faq-q"><button type="button" aria-expanded="{"true" if len(faqs)==0 else "false"}" aria-controls="{fid}">{inline(q)}</button></h3>'
                             f'<div class="faq-answer" id="{fid}"><div class="faq-answer-in">' + "".join(f"<p>{inline(a)}</p>" for a in ans) + "</div></div></div>")
                faqs.append((plain(q), [plain(a) for a in ans]))
            out.append(f'<section class="faq-sec"><h2 id="faq">{inline(title)}</h2>' + "".join(items) + "</section>")
        elif k == "index":
            out.append(ctx["index"](n[1]))
        else:
            raise ValueError(k)
    return "\n".join(out), faqs


def midcta(ctx):
    t = ctx.get("mid_title", "Need a plumber now?")
    c = ctx.get("mid_copy", "Our dispatcher answers 24/7 and can book a same-day appointment when one is open.")
    return (f'<div class="midcta"><div><h3>{esc(t)}</h3><p>{esc(c)}</p></div>'
            f'<a class="btn" href="{tel()}">Call {PHONE_DISPLAY}</a></div>')
