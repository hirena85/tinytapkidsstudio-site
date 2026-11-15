"""Builds the site's images (webp) from the game folders.
Run from anywhere:  python tools/make_images.py
Source paths are relative to the GPlay Games folder (two levels up)."""
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
GAMES = os.path.dirname(SITE)
OUT = os.path.join(SITE, "img")
os.makedirs(OUT, exist_ok=True)

BANNER = (1024, 500)

# slug: (icon source, banner source, optional banner crop box)
SOURCES = {
    "kaiju-rampage": ("Kaiju Rampage/Kaiju Rampage 512 icon.png", "Kaiju Rampage/Kaiju Rampage feature graphic.png", None),
    "brick-blast-rocket": ("Brick Blast/icon-512.png", "Brick Blast/Feature graphic.png", None),
    "kids-fun-games": ("Kids Fun Games 1.9/icon-512-play.png", "Kids Fun Games 1.9/kids-fun-games-1.9-store-graphics/graphics/feature-graphic-1024x500.png", None),
    "dino-smash-city": ("Dino Smash City/App icon.png", "Dino Smash City/Feature graphic.png", None),
    "christmas-town-fun": ("Christmas Town Fun/store/icon-512.png", "Christmas Town Fun/store/feature-graphic-1024x500.png", None),
    "deep-glow": ("Deep Glow/store/icon-512.png", "Deep Glow/store/feature-graphic-1024x500.png", None),
    "fudders-ngmi": ("fudders-ngmi-1.0.0-source/fudders-ngmi/android/app/src/main/res/mipmap-xxxhdpi/ic_launcher.png",
                     "fudders-ngmi-1.0.0-source/fudders-ngmi/store-listing/1.2.0/feature-graphic-1024x500.png", None),
    "ink-heroes": ("Ink Heroes/assets/icon/icon_1024.png", "Ink Heroes/art-src/intro/heroes_notebook.png", (0, 71, 1920, 1008)),
    "stick-city-z": ("Stick City Z/assets/icon/icon_foreground.png", "Stick City Z/real_city_rooftops.png", (100, 150, 1180, 677)),
}


def cover(im, size):
    """Scale + centre-crop to fill size exactly."""
    tw, th = size
    w, h = im.size
    s = max(tw / w, th / h)
    im = im.resize((round(w * s), round(h * s)), Image.LANCZOS)
    w, h = im.size
    l, t = (w - tw) // 2, (h - th) // 2
    return im.crop((l, t, l + tw, t + th))


def icon(src, dst):
    im = Image.open(src).convert("RGBA")
    if "mipmap" in src:  # launcher icon has rounded transparent corners: trim to the art
        bbox = im.getchannel("A").getbbox()
        im = im.crop(bbox)
        w, h = im.size
        inset = round(w * 0.025)  # drop the rounded corners
        im = im.crop((inset, inset, w - inset, h - inset))
    im = cover(im.convert("RGB"), (256, 256))
    im.save(dst, "WEBP", quality=88, method=6)


def banner(src, dst, box):
    im = Image.open(src).convert("RGB")
    if box:
        im = im.crop(box)
    cover(im, BANNER).save(dst, "WEBP", quality=82, method=6)


for slug, (ic, bn, box) in SOURCES.items():
    icon(os.path.join(GAMES, ic), os.path.join(OUT, f"{slug}-icon.webp"))
    banner(os.path.join(GAMES, bn), os.path.join(OUT, f"{slug}-banner.webp"), box)
    print("ok", slug)

# Studio logo + social preview + favicons
logo = Image.open(os.path.join(GAMES, "_Studio Assets/Tiny Tap Kids Intro/ttk-logo-intro/logo_final_transparent.png")).convert("RGBA")
logo = logo.crop(logo.getchannel("A").getbbox())
l = logo.copy(); l.thumbnail((640, 640), Image.LANCZOS); l.save(os.path.join(OUT, "logo.webp"), "WEBP", quality=90, method=6)
l = logo.copy(); l.thumbnail((640, 640), Image.LANCZOS); l.save(os.path.join(OUT, "logo.png"), optimize=True)

dev = Image.open(os.path.join(GAMES, "_Studio Assets/Play Developer Profile/developer_icon_512.png")).convert("RGB")
for s in (32, 180, 512):
    dev.resize((s, s), Image.LANCZOS).save(os.path.join(SITE, f"favicon-{s}.png"), optimize=True)

hdr = Image.open(os.path.join(GAMES, "_Studio Assets/Play Developer Profile/header_4096x2304.jpg")).convert("RGB")
cover(hdr, (1200, 630)).save(os.path.join(OUT, "social.jpg"), quality=85, optimize=True)
print("ok studio")
