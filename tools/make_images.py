"""Builds the site's web images (icons, banners, screenshots) as compressed WebP.

    python tools/make_images.py

Icons are saved at 512px, screenshots with a long edge of 1080px.
Studio logo, favicons and social.jpg are left alone unless --studio is passed.
"""
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
OUT = os.path.join(SITE, "img")
SHOTS = os.path.join(OUT, "shots")
os.makedirs(SHOTS, exist_ok=True)

ICON_SIZE = 512
BANNER = (1024, 500)
SHOT_LONG = 1080

# slug: (icon source, banner source)
ICONS_BANNERS = {
    "kaiju-rampage": (
        "/tmp/kaiju-store/icon-512.png",
        "/tmp/kaiju-store/feature-graphic-1024x500.png",
    ),
    "brick-blast-rocket": (
        "/workspace/brick-blast-rocket/store/graphics/icon-512.png",
        "/workspace/brick-blast-rocket/store/graphics/feature-graphic-1024x500.png",
    ),
    "kids-fun-games": (
        "/workspace/kids-games/store-listing/icon-512-play.png",
        "/workspace/kids-games/store-listing/feature-graphic-1024x500-v2.png",
    ),
    "dino-smash-city": (
        "/workspace/dino-smash/store-listing/v1.3/icon-512-play.png",
        "/workspace/dino-smash/store-listing/v1.3/feature-graphic-1024x500.png",
    ),
    "christmas-town-fun": (
        "/workspace/christmas-town-fun/assets/ui/icon.png",
        None,  # keep existing banner
    ),
    "deep-glow": (None, None),  # keep existing art (no local store kit on the box)
    "fudders-ngmi": (
        "/workspace/fudders-ngmi/store-listing/icon-512-play.png",
        "/workspace/fudders-ngmi/store-listing/1.0.0/feature-graphic-1024x500.png",
    ),
    "ink-heroes": (
        "/workspace/ink-heroes-icons-v2/icon-B-hero-squad-cobalt-1024.png",
        "/workspace/ink-heroes-store/graphics/feature-graphic-1024x500.png",
    ),
    "stick-city-z": (
        "/workspace/stick-city-z-store-kit/play-icon-512.png",
        "/workspace/stick-city-z-store-kit/feature-graphic-1024x500.png",
    ),
}

# slug: list of up to 3 screenshot source paths
SCREENSHOTS = {
    "kaiju-rampage": [
        "/tmp/kaiju-store/phone-1-become-the-kaiju.png",
        "/tmp/kaiju-store/phone-3-defeat-giant-bosses.png",
        "/tmp/kaiju-store/phone-6-smash-the-army.png",
    ],
    "brick-blast-rocket": [
        "/workspace/brick-blast-rocket/store/graphics/phone-1-aim-and-shoot.png",
        "/workspace/brick-blast-rocket/store/graphics/phone-3-wingman.png",
        "/workspace/brick-blast-rocket/store/graphics/phone-6-world-map.png",
    ],
    "kids-fun-games": [
        "/workspace/kids-fun-games-release-2.0/screenshots/01-home-no-locks.png",
        "/workspace/kids-games/store-listing/v1.9/graphics/phone/02-dig-build-big-world.png",
        "/workspace/kids-games/store-listing/v1.9/graphics/phone/04-toy-trains-3d.png",
    ],
    "dino-smash-city": [
        "/workspace/dino-smash/store-listing/v1.3/phone/01-kick.png",
        "/workspace/dino-smash/store-listing/v1.3/phone/02-giant.png",
        "/workspace/dino-smash/store-listing/v1.3/phone/06-dressup.png",
    ],
    "christmas-town-fun": [
        "/workspace/ctf-trailer-stills/01-title.png",
        "/workspace/ctf-trailer-stills/02-sleigh.png",
        "/workspace/ctf-trailer-stills/05-games-grid.png",
    ],
    "fudders-ngmi": [
        "/workspace/fudders-ngmi/store-listing/1.0.0/phone-screenshots/01-crybaby-hub.png",
        "/workspace/fudders-ngmi/store-listing/1.0.0/phone-screenshots/02-crybaby-tear-flood.png",
        "/workspace/fudders-ngmi/store-listing/1.0.0/phone-screenshots/08-boss-diamond-hands-colossus.png",
    ],
    "ink-heroes": [
        "/workspace/ink-heroes-store/screenshots/phone/03-menu-adventure-1920x1080.png",
        "/workspace/ink-heroes-store/screenshots/phone/05-katana-fight-1920x1080.png",
        "/workspace/ink-heroes-store/screenshots/phone/08-boss-homework-finisher-1920x1080.png",
    ],
    "stick-city-z": [
        "/workspace/stick-city-z-store-kit/phone-screenshots/01-heroes.png",
        "/workspace/stick-city-z-store-kit/phone-screenshots/02-combat.png",
        "/workspace/stick-city-z-store-kit/phone-screenshots/04-drive.png",
    ],
}


def cover(im, size):
    tw, th = size
    w, h = im.size
    s = max(tw / w, th / h)
    im = im.resize((round(w * s), round(h * s)), Image.LANCZOS)
    w, h = im.size
    l, t = (w - tw) // 2, (h - th) // 2
    return im.crop((l, t, l + tw, t + th))


def save_icon(src, dst):
    im = Image.open(src).convert("RGBA")
    # Flatten onto white if there is transparency, then cover to 512.
    bg = Image.new("RGB", im.size, (255, 255, 255))
    bg.paste(im, mask=im.split()[-1])
    cover(bg, (ICON_SIZE, ICON_SIZE)).save(dst, "WEBP", quality=88, method=6)


def save_banner(src, dst):
    im = Image.open(src).convert("RGB")
    cover(im, BANNER).save(dst, "WEBP", quality=82, method=6)


def save_shot(src, dst):
    im = Image.open(src).convert("RGB")
    w, h = im.size
    long_edge = max(w, h)
    if long_edge > SHOT_LONG:
        s = SHOT_LONG / long_edge
        im = im.resize((round(w * s), round(h * s)), Image.LANCZOS)
    im.save(dst, "WEBP", quality=80, method=6)
    return im.size


def main():
    for slug, (ic, bn) in ICONS_BANNERS.items():
        if ic:
            dst = os.path.join(OUT, f"{slug}-icon.webp")
            save_icon(ic, dst)
            print("icon ", slug, os.path.getsize(dst))
        if bn:
            dst = os.path.join(OUT, f"{slug}-banner.webp")
            save_banner(bn, dst)
            print("banner", slug, os.path.getsize(dst))
    for slug, paths in SCREENSHOTS.items():
        for i, src in enumerate(paths, 1):
            dst = os.path.join(SHOTS, f"{slug}-{i}.webp")
            size = save_shot(src, dst)
            print("shot ", f"{slug}-{i}", size, os.path.getsize(dst))


if __name__ == "__main__":
    main()
