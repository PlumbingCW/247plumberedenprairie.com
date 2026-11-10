import html, re
from config import *
from mdparse import LINK_RE


def esc(s):
    return html.escape(s, quote=False)


def attr(s):
    return html.escape(s, quote=True)


def url(slug):
    return "/" if slug in ("", None) else f"/{slug}/"


def abs_url(slug):
    return SITE_URL + url(slug)


def tel():
    return f"tel:{PHONE_E164}"


def inline(s):
    s = esc(s)

    def rep(m):
        tgt, anchor = m.group(1), m.group(2)
        if tgt == "call":
            return f'<a href="{tel()}">{anchor}</a>'
        if tgt == "home":
            return f'<a href="/">{anchor}</a>'
        return f'<a href="{url(tgt)}">{anchor}</a>'
    s = LINK_RE.sub(rep, s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return s


def plain(s):
    s = LINK_RE.sub(lambda m: m.group(2), s)
    return s.replace("**", "")


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def tel_btn(label=None, cls="btn", extra=""):
    label = label or f"Call {PHONE_DISPLAY}"
    return f'<a class="{cls}" href="{tel()}"{extra}>{esc(label)}</a>'
