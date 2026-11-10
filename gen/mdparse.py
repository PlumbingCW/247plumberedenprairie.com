"""Mini markdown dialect (EPMD) used for all page copy. Parses to nodes; rendering lives in render.py."""
import re

FM_END = "---"
DIRECTIVES = {"index", "signs", "cards", "table", "factors", "steps", "callout", "prep", "localnote", "faq", "facts"}


def parse(text):
    lines = text.replace("\r\n", "\n").split("\n")
    i = 0
    fm = {}
    # front matter: lines until a line that is exactly ---
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    if i < len(lines) and lines[i].strip() == FM_END:
        i += 1
        while i < len(lines) and lines[i].strip() != FM_END:
            m = re.match(r"^([a-z_0-9]+):\s*(.*)$", lines[i])
            if m:
                fm[m.group(1)] = m.group(2).strip()
            i += 1
        i += 1
    nodes = []
    para = []
    lst = None

    def flush_para():
        nonlocal para
        if para:
            nodes.append(("p", " ".join(s.strip() for s in para)))
            para = []

    def flush_list():
        nonlocal lst
        if lst:
            nodes.append((lst[0], lst[1]))
            lst = None

    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if s == "":
            flush_para(); flush_list(); i += 1; continue
        if s.startswith("## "):
            flush_para(); flush_list()
            nodes.append(("h2", s[3:].strip())); i += 1; continue
        m = re.match(r"^:::(\w+)\s*(.*)$", s)
        if m:
            flush_para(); flush_list()
            name, arg = m.group(1), m.group(2).strip()
            body = []
            i += 1
            while i < len(lines) and lines[i].strip() != ":::":
                body.append(lines[i]); i += 1
            i += 1
            nodes.append(_directive(name, arg, body))
            continue
        if re.match(r"^- ", s):
            flush_para()
            if lst is None or lst[0] != "ul":
                flush_list(); lst = ("ul", [])
            lst[1].append(s[2:].strip()); i += 1; continue
        if re.match(r"^\d+\. ", s):
            flush_para()
            if lst is None or lst[0] != "ol":
                flush_list(); lst = ("ol", [])
            lst[1].append(re.sub(r"^\d+\.\s+", "", s)); i += 1; continue
        flush_list()
        para.append(s); i += 1
    flush_para(); flush_list()
    return fm, nodes


def _items_h3(body):
    items = []
    cur = None
    for ln in body:
        s = ln.strip()
        if s.startswith("### "):
            cur = [s[4:].strip(), []]
            items.append(cur)
        elif s and cur is not None:
            cur[1].append(s)
        elif s == "" and cur is not None and cur[1] and cur[1][-1] != "\n":
            cur[1].append("\n")
    out = []
    for t, parts in items:
        paras, buf = [], []
        for p in parts:
            if p == "\n":
                if buf: paras.append(" ".join(buf)); buf = []
            else:
                buf.append(p)
        if buf: paras.append(" ".join(buf))
        out.append((t, paras))
    return out


def _directive(name, arg, body):
    if name in ("signs", "cards", "prep"):
        return (name, arg, _items_h3(body))
    if name == "table":
        rows = [[c.strip() for c in ln.strip().split("|")] for ln in body if ln.strip()]
        return ("table", arg, rows)
    if name in ("factors", "steps"):
        items = []
        for ln in body:
            s = ln.strip()
            if not s: continue
            m = re.match(r"^([^:]{2,60}):\s+(.*)$", s)
            if m: items.append((m.group(1).strip(), m.group(2).strip()))
            else: items.append(("", s))
        return (name, arg, items)
    if name in ("callout", "localnote"):
        paras, buf = [], []
        for ln in body:
            if ln.strip() == "":
                if buf: paras.append(" ".join(buf)); buf = []
            else: buf.append(ln.strip())
        if buf: paras.append(" ".join(buf))
        return (name, arg, paras)
    if name == "faq":
        qa = []
        cur = None
        for ln in body:
            s = ln.strip()
            if s.startswith("Q:"):
                cur = [s[2:].strip(), [], []]; qa.append(cur)
            elif s.startswith("A:") and cur is not None:
                cur[2] = [s[2:].strip()]
            elif s == "" and cur is not None:
                if cur[2] and cur[2][-1] != "":
                    cur[2].append("")
            elif cur is not None and cur[2]:
                if cur[2][-1] == "": cur[2][-1] = s
                else: cur[2][-1] += " " + s
        out = []
        for q, _, a in qa:
            out.append((q, [x for x in a if x]))
        return ("faq", arg, out)
    if name == "index":
        return ("index", arg, [])
    raise ValueError("unknown directive " + name)


LINK_RE = re.compile(r"\[\[([a-z0-9\-/]+)\|([^\]]+)\]\]")


def iter_text(nodes):
    """Yield (kind, text) for every text string in nodes (for validators)."""
    for n in nodes:
        k = n[0]
        if k == "h2": yield "h2", n[1]
        elif k == "p": yield "p", n[1]
        elif k in ("ul", "ol"):
            for it in n[1]: yield "li", it
        elif k in ("signs", "cards", "prep"):
            for t, paras in n[2]:
                yield "h3", t
                for p in paras: yield "cardp", p
        elif k == "table":
            for r in n[2]:
                for c in r: yield "cell", c
        elif k in ("factors", "steps"):
            for t, x in n[2]:
                yield "h3", t; yield "cardp", x
        elif k in ("callout", "localnote"):
            yield "h3", n[1]
            for p in n[2]: yield "p", p
        elif k == "faq":
            for q, a in n[2]:
                yield "q", q
                for p in a: yield "a", p
