#!/usr/bin/env python3
"""Generate logo, favicon set, OG image and gradient hero fallbacks with Pillow."""
import os, math, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SITE = os.path.join(ROOT, "site"); IMG = os.path.join(SITE, "img")
os.makedirs(IMG, exist_ok=True)
BERRY = (194, 26, 107); BERRY_D = (156, 19, 84); BERRY_DD = (110, 13, 58); VOLT = (244, 224, 40); INK = (36, 21, 34)
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
if not os.path.exists(FB):
    import glob
    FB = glob.glob("/usr/share/fonts/**/DejaVuSans-Bold.ttf", recursive=True)[0]


def mark(size=512, bg=True):
    S = 4
    n = size * S
    im = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if bg:
        d.rounded_rectangle([0, 0, n - 1, n - 1], radius=int(n * 0.3), fill=BERRY)
    # drop: circle + triangle
    cx, cy, r = n * 0.5, n * 0.64, n * 0.255
    apex = (n * 0.5, n * 0.18)
    ang = math.asin(r / (cy - apex[1]))
    # tangent points
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255, 255))
    L = math.sqrt((cy - apex[1]) ** 2 - r ** 2)
    t1 = (cx - r * math.cos(ang), cy - r * math.sin(ang))
    t2 = (cx + r * math.cos(ang), cy - r * math.sin(ang))
    d.polygon([apex, t1, t2], fill=(255, 255, 255, 255))
    # bolt
    b = [(0.54, 0.43), (0.42, 0.65), (0.50, 0.65), (0.46, 0.83), (0.60, 0.59), (0.51, 0.59), (0.57, 0.43)]
    d.polygon([(x * n, y * n) for x, y in b], fill=BERRY)
    d.ellipse([n * 0.74 - n * 0.09, n * 0.22 - n * 0.09, n * 0.74 + n * 0.09, n * 0.22 + n * 0.09], fill=VOLT)
    return im.resize((size, size), Image.LANCZOS)


def logo(path, dark_text):
    W, H = 760, 200
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    m = mark(170)
    im.paste(m, (10, 15), m)
    d = ImageDraw.Draw(im)
    f1 = ImageFont.truetype(FB, 62); f2 = ImageFont.truetype(FB, 26)
    c1 = INK if dark_text else (255, 255, 255)
    d.text((205, 28), "Eden Prairie", font=f1, fill=c1)
    w = d.textlength("Eden Prairie ", font=f1)
    d.text((205 + w, 28), "24/7", font=f1, fill=BERRY if dark_text else VOLT)
    d.text((208, 112), "P L U M B I N G", font=f2, fill=(94, 83, 97) if dark_text else (235, 216, 228))
    im.save(path)


def gradient(w, h, kind):
    im = Image.new("RGB", (w, h))
    px = im.load()
    for y in range(h):
        for x in range(w):
            t = (x / w * 0.8 + y / h * 0.4) / 1.2
            if t < 0.55:
                u = t / 0.55; a, b = INK, BERRY_DD
            else:
                u = (t - 0.55) / 0.45; a, b = BERRY_DD, BERRY_D
            px[x, y] = tuple(int(a[i] + (b[i] - a[i]) * u) for i in range(3))
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    seeds = {"home": [(1250, 120, 230, 70), (160, 560, 150, 40), (900, 520, 90, 30)],
             "service": [(1300, 90, 210, 60), (260, 600, 120, 40), (700, 80, 60, 30)],
             "location": [(1200, 160, 170, 50), (1200, 160, 110, 50), (1200, 160, 50, 70), (200, 560, 130, 35)],
             "blog": [(1350, 540, 200, 45), (150, 90, 100, 40), (1000, 100, 50, 40)],
             "hub": [(1280, 100, 190, 55), (120, 560, 110, 35)],
             "contact": [(1300, 320, 230, 40), (1300, 320, 160, 50), (1300, 320, 90, 70), (200, 560, 90, 30)]}[kind]
    for i, (cx, cy, r, a) in enumerate(seeds):
        col = VOLT if kind != "location" or i == 2 else (255, 255, 255)
        if kind in ("location", "contact") and i < 3:
            d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col + (a,), width=6)
        else:
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col + (a,))
    ov = ov.filter(ImageFilter.GaussianBlur(1.5))
    im = im.convert("RGBA"); im.alpha_composite(ov)
    return im.convert("RGB")


BRAND = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "brand")


def brand_logos():
    """Use the supplied primary logo. Light variant recolours the text for dark backgrounds."""
    src = Image.open(os.path.join(BRAND, "logo-primary.png")).convert("RGBA")
    src = src.crop(src.split()[3].getbbox())
    src.save(os.path.join(IMG, "logo.png"), optimize=True)


def brand_icons():
    ic = Image.open(os.path.join(BRAND, "icon.png")).convert("RGBA")
    ic.resize((512, 512), Image.LANCZOS).save(os.path.join(SITE, "icon-512.png"), optimize=True)
    ic.resize((192, 192), Image.LANCZOS).save(os.path.join(SITE, "icon-192.png"), optimize=True)
    ic.resize((32, 32), Image.LANCZOS).save(os.path.join(SITE, "favicon-32.png"), optimize=True)
    flat = Image.new("RGB", (180, 180), (178, 27, 92))
    t = ic.resize((180, 180), Image.LANCZOS); flat.paste(t, (0, 0), t); flat.save(os.path.join(SITE, "apple-touch-icon.png"), optimize=True)
    ic.save(os.path.join(SITE, "favicon.ico"), format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])
    svg = os.path.join(SITE, "favicon.svg")
    if os.path.exists(svg):
        os.remove(svg)


def main():
    for k in ("home", "service", "location", "blog", "hub", "contact"):
        gradient(1600, 640, k).save(os.path.join(IMG, f"hero-{k}.webp"), "WEBP", quality=82)
    brand_logos()
    brand_icons()
    json.dump({"name": "Eden Prairie 24/7 Plumbing", "short_name": "EP 24/7 Plumbing", "start_url": "/", "display": "standalone",
               "background_color": "#ffffff", "theme_color": "#241522",
               "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"}]},
              open(os.path.join(SITE, "site.webmanifest"), "w"), indent=1)
    # OG image
    W, H = 1200, 630
    og = gradient(W, H, "home").convert("RGBA")
    d = ImageDraw.Draw(og)
    mk = mark(150); og.paste(mk, (70, 70), mk)
    fa = ImageFont.truetype(FB, 40); fb = ImageFont.truetype(FB, 74); fc = ImageFont.truetype(FB, 36)
    d.text((245, 85), "Eden Prairie 24/7 Plumbing", font=fa, fill=(255, 255, 255))
    d.text((70, 250), "Emergency Plumber", font=fb, fill=(255, 255, 255))
    d.text((70, 340), "in Eden Prairie, MN", font=fb, fill=VOLT)
    d.text((70, 470), "Open 24/7  |  (952) 866-9120", font=fc, fill=(243, 219, 233))
    og.convert("RGB").save(os.path.join(IMG, "og-default.png"), optimize=True)
    print("assets ok", sorted(os.listdir(IMG)))


if __name__ == "__main__":
    main()
