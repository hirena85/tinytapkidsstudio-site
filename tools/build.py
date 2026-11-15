"""Builds every HTML page of tinytapkidsstudio.com.

    python tools/build.py

Edit the settings below, then re-run. Everything is plain static HTML in this folder.
- CONTACT: the public email shown on the site and in every privacy policy.
- GAMES: one entry per game. When a game goes live on Google Play, change its status to "live".
  The Play link is built from the package name, so nothing else needs to change.
- POLICY_SOURCES: the existing per-app privacy policies that get republished under /privacy/<slug>/.
  Any other email address or *.github.io link inside them is replaced with CONTACT / the domain.
"""
import html
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
GAMES_DIR = os.path.dirname(SITE)

DOMAIN = "tinytapkidsstudio.com"
STUDIO = "Tiny Tap Kids Studio"
# Public contact address. Placeholder until the studio mailbox/forwarding exists (see README.md).
CONTACT = "hello@tinytapkidsstudio.com"
YEAR = 2026

PLAY = "https://play.google.com/store/apps/details?id={}"

# status: live | testing | dev     audience: kids | teen | None
GAMES = [
    dict(slug="kaiju-rampage", name="Kaiju Rampage", pkg="com.tinytapkids.kaijurampage", status="live", audience="teen",
         tags=["Free with ads", "Optional purchases"],
         desc="Stomp the city, survive the army and beat giant bosses. Become the kaiju! A one-thumb monster roguelite with upgrades, new monsters and a Titan Mech to topple."),
    dict(slug="brick-blast-rocket", name="Brick Blast Rocket", pkg="com.tinytapkids.brickblast", status="live", audience="teen",
         tags=["Free with ads"],
         desc="Aim, shoot and smash candy bricks in space! A rocket-powered brick breaker with 4 worlds, 42 levels, boss battles, Endless mode and a Daily Challenge."),
    dict(slug="kids-fun-games", name="Kids Fun Games", pkg="com.tinytapkids.kidsgames", status="live", audience="kids",
         tags=["No ads", "Parent-locked unlock"],
         desc="13 fun games in one app for little ones: dig and build, wash things clean, play with 3D toy trains, feed the monster, splash in a bubble bath, build words, fill a UFO sticker book, draw and trace."),
    dict(slug="dino-smash-city", name="Dino Smash City", pkg="com.tinytapkids.dinosmash", status="live", audience="kids",
         tags=["No ads", "Parent-locked unlock"],
         desc="Go GIANT! Stomp around a toy city as a friendly dino: kick, grab, go bowling, pop barrels, dress up your dinos and collect stickers."),
    dict(slug="christmas-town-fun", name="Christmas Town Fun", pkg="com.tinytapkids.christmastownfun", status="testing", audience="kids",
         tags=["No ads", "Advent calendar"],
         desc="22 cozy Christmas games for kids in one snowy town: sleigh rides, snowball fun, gingerbread, cookies, tree decorating and an advent calendar to open every day."),
    dict(slug="deep-glow", name="Deep Glow", pkg="com.tinytapkids.deepglow", status="testing", audience="teen",
         tags=["Free with ads", "Leaderboards"],
         desc="Guide a glowing jellyfish into the abyss. Your light is your life: collect pearls, dodge the dark and dive deeper every time."),
    dict(slug="fudders-ngmi", name="Fudders NGMI", pkg="com.tinytapkids.fuddersngmi", status="testing", audience=None,
         tags=["3 games, 1 universe"],
         desc="Play as the Fudders, a crew of lovable losers, and survive the Hype Army across a bull-market city. Three games, one universe."),
    dict(slug="ink-heroes", name="Ink Heroes", pkg="com.tinytapkids.inkheroes", status="dev", audience=None,
         tags=["8 heroes", "300 pages", "Endless mode"],
         desc="Sketchbook heroes vs. the ink spill! Swap between eight doodled heroes on the fly to cross 300 notebook pages, then keep going in Endless mode."),
    dict(slug="stick-city-z", name="Stick City Z", pkg="com.tinytapkids.stickcityz", status="dev", audience=None,
         tags=["3D action"],
         desc="A stickman zombie town: climb buildings, leap across rooftops, drive through the horde and smash it with cartoon ink-splat action."),
]

STATUS_LABEL = {"testing": "In testing", "dev": "In development"}
AUDIENCE_LABEL = {"kids": ("For kids", "kids"), "teen": ("Ages 13+", "teen")}

# Existing per-app policies (relative to the GPlay Games folder) -> republished at /privacy/<slug>/
POLICY_SOURCES = {
    "kaiju-rampage": "Kaiju-rampage-1.0.2 source/kaiju-rampage-1.0.2-source-art-store/store/privacy-policy.txt",
    "brick-blast-rocket": "Brick Blast/brick-blast-privacy-policy.txt",
    "kids-fun-games": "Kids Fun Games 1.9/privacy-1.9.txt",
    "dino-smash-city": "Source/dino-smash/web/privacy.html",
    "christmas-town-fun": "Christmas Town Fun/store/privacy/index.html",
    "deep-glow": "Deep Glow/store/deepglow-privacy/index.html",
}

PLAY_SVG = ('<svg viewBox="0 0 24 26" aria-hidden="true"><path fill="#00d7fe" d="M1 1.2 13.6 13 1 24.8c-.4-.3-.6-.8-.6-1.4V2.6c0-.6.2-1.1.6-1.4z"/>'
            '<path fill="#ffce00" d="m17.8 8.9-4.2 4.1 4.2 4.1 4.8-2.7c1.4-.8 1.4-2.1 0-2.9z"/>'
            '<path fill="#ff3a44" d="M17.8 17.1 13.6 13 1 24.8c.5.5 1.2.5 2.1.1z"/>'
            '<path fill="#00f076" d="M17.8 8.9 3.1 1.1C2.2.6 1.5.7 1 1.2L13.6 13z"/></svg>')


def esc(s):
    return html.escape(s, quote=True)


def page(title, desc, body, depth=0, canonical=""):
    root = "../" * depth
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="https://{DOMAIN}/{canonical}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://{DOMAIN}/{canonical}">
<meta property="og:image" content="https://{DOMAIN}/img/social.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0b1030">
<link rel="icon" type="image/png" sizes="32x32" href="{root}favicon-32.png">
<link rel="apple-touch-icon" href="{root}favicon-180.png">
<link rel="stylesheet" href="{root}css/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{root or './'}"><img src="{root}favicon-180.png" alt="" width="40" height="40">{STUDIO}</a>
    <nav class="nav" aria-label="Main">
      <a href="{root}#games">Games</a>
      <a href="{root}#about">About</a>
      <a href="{root}privacy/">Privacy</a>
      <a href="{root}#contact">Contact</a>
    </nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div>
      <p><strong style="color:#fff">{STUDIO}</strong> · Small taps, big adventures.</p>
      <p>© {YEAR} {STUDIO}. All rights reserved.</p>
    </div>
    <div>
      <p><a href="{root}privacy/">Privacy policy</a> · <a href="mailto:{CONTACT}">{CONTACT}</a></p>
      <p>Google Play and the Google Play logo are trademarks of Google LLC.</p>
    </div>
  </div>
</footer>
</body>
</html>
"""


def play_button(g):
    if g["status"] == "live":
        return (f'<a class="play" href="{PLAY.format(g["pkg"])}" target="_blank" rel="noopener" '
                f'aria-label="Get {esc(g["name"])} on Google Play">{PLAY_SVG}'
                f'<span><small>Get it on</small><strong>Google Play</strong></span></a>')
    # PLACEHOLDER: when this game is live, set its status to "live" in GAMES; the link becomes
    # https://play.google.com/store/apps/details?id=<pkg>
    return (f'<span class="play soon" data-play-placeholder="{PLAY.format(g["pkg"])}">{PLAY_SVG}'
            f'<span><small>Coming soon to</small><strong>Google Play</strong></span></span>')


def card(g):
    tags = []
    if g["status"] != "live":
        tags.append(f'<span class="tag status">{STATUS_LABEL[g["status"]]}</span>')
    if g["audience"]:
        label, cls = AUDIENCE_LABEL[g["audience"]]
        tags.append(f'<span class="tag {cls}">{label}</span>')
    tags += [f'<span class="tag">{esc(t)}</span>' for t in g["tags"]]
    policy = (f'<a class="small" href="privacy/{g["slug"]}/">Privacy policy</a>'
              if g["slug"] in POLICY_SOURCES else '<span class="small">Privacy policy at launch</span>')
    return f"""      <article class="card" id="{g['slug']}">
        <img class="banner" src="img/{g['slug']}-banner.webp" alt="{esc(g['name'])} artwork" width="1024" height="500" loading="lazy">
        <div class="body">
          <div class="title-row">
            <img class="icon" src="img/{g['slug']}-icon.webp" alt="{esc(g['name'])} app icon" width="72" height="72" loading="lazy">
            <h3>{esc(g['name'])}</h3>
          </div>
          <div class="tags">{''.join(tags)}</div>
          <p>{esc(g['desc'])}</p>
          <div class="actions">{play_button(g)}{policy}</div>
        </div>
      </article>"""


def build_index():
    live = [g for g in GAMES if g["status"] == "live"]
    soon = [g for g in GAMES if g["status"] != "live"]
    body = f"""<section class="hero">
  <div class="wrap">
    <div>
      <p class="kicker" style="color:var(--yellow)">Indie game studio</p>
      <h1>Small taps.<br><span>Big adventures.</span></h1>
      <p class="lead">{STUDIO} makes bright, friendly mobile games for Android: gentle play boxes for little kids, and action games for older players.</p>
      <div class="cta">
        <a class="btn btn-yellow" href="#games">See our games</a>
        <a class="btn btn-ghost" href="privacy/">For parents</a>
      </div>
      <div class="hero-stats">
        <div><b>{len(live)}</b><span>On Google Play</span></div>
        <div><b>{len(soon)}</b><span>Coming soon</span></div>
      </div>
    </div>
    <img class="hero-logo" src="img/logo.webp" alt="Tiny Tap Kids Studio logo" width="640" height="640">
  </div>
</section>

<section id="games">
  <div class="wrap">
    <div class="section-head">
      <div>
        <p class="kicker">Our games</p>
        <h2>Play them on Android</h2>
        <p class="sub">Each card says who the game is made for. Our kids' games have no ads, and any purchase sits behind a parent check.</p>
      </div>
    </div>

    <h3 class="group-title"><span class="dot"></span>Out now on Google Play</h3>
    <div class="grid four">
{chr(10).join(card(g) for g in live)}
    </div>

    <h3 class="group-title"><span class="dot soon"></span>Coming soon</h3>
    <div class="grid">
{chr(10).join(card(g) for g in soon)}
    </div>
  </div>
</section>

<section class="about" id="about">
  <div class="wrap about-grid">
    <div>
      <p class="kicker">About us</p>
      <h2>A tiny studio with a big toy box</h2>
      <p class="sub">{STUDIO} is a small independent studio. We build every game ourselves: the art, the sounds and the code. Some games are for little hands, others are for older players, and every one of them is tested on real phones before it ships.</p>
      <div class="values" style="margin-top:24px">
        <div class="value"><span class="emoji" aria-hidden="true">🧸</span><div><h3>Made for little hands</h3><p>Big buttons, no reading needed and nothing punishing. In our kids' games you can't really lose.</p></div></div>
        <div class="value"><span class="emoji" aria-hidden="true">🛡️</span><div><h3>Parents first</h3><p>Our kids' games have no ads and no tracking. Purchases and tips sit behind a grown-up check.</p></div></div>
        <div class="value"><span class="emoji" aria-hidden="true">🎮</span><div><h3>Real games for older players</h3><p>Monsters, brick breakers and deep-sea dives for teens and grown-ups, free to play with fair ads.</p></div></div>
      </div>
    </div>
    <img class="heroes-art" src="img/ink-heroes-banner.webp" alt="The eight doodled heroes of Ink Heroes, drawn on notebook paper" width="1024" height="500" loading="lazy">
  </div>
</section>

<section id="contact">
  <div class="wrap">
    <div class="contact-box">
      <div>
        <p class="kicker" style="color:#fff">Contact</p>
        <h2>Say hello!</h2>
        <p>Questions about a game, a bug to report, an idea for a new level or a privacy request? Email us. Parents are always welcome.</p>
      </div>
      <div><a class="mail" href="mailto:{CONTACT}">{CONTACT}</a></div>
    </div>
  </div>
</section>"""
    return page(f"{STUDIO}: kid-friendly mobile games",
                f"{STUDIO} makes bright, friendly Android games: Kids Fun Games, Dino Smash City, Kaiju Rampage, Brick Blast Rocket and more.",
                body)


# ---------- privacy policies ----------

URL_RE = re.compile(r'(https?://[^\s<>)"]+[^\s<>)".,;:])')
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+\w")
OLD_SITE_RE = re.compile(r"(https?://)?[\w-]+\.github\.io")
LINK_PHRASES = {  # phrases in the text policies that lost their links
    "How Google uses information from sites or apps that use its services": "https://policies.google.com/technologies/partner-sites",
    "Google Mobile Ads SDK data disclosure": "https://developers.google.com/admob/android/privacy/play-data-disclosure",
}


def scrub(s):
    """Swap any personal email / old github.io site for the studio's public details."""
    s = EMAIL_RE.sub(CONTACT, s)
    return OLD_SITE_RE.sub(f"https://{DOMAIN}", s)


def linkify(s):
    s = URL_RE.sub(lambda m: f'<a href="{m.group(1)}">{m.group(1)}</a>', s)
    return s.replace(CONTACT, f'<a href="mailto:{CONTACT}">{CONTACT}</a>')


def txt_to_html(text):
    text = scrub(text).replace("\r\n", "\n")
    blocks = [b for b in re.split(r"\n\s*\n", text.strip()) if b.strip()]
    title = blocks.pop(0).strip()
    out = []
    for b in blocks:
        lines = [l.rstrip() for l in b.split("\n") if l.strip()]
        first = lines[0].strip()
        if len(lines) == 1 and re.match(r"^[A-Z][\w ]{1,20}:\s", first) and not re.match(r"^\d", first):
            out.append(f'<p class="meta">{linkify(esc(first))}</p>')  # "Developer: ...", "Effective date: ..."
            continue
        if len(lines) == 1 and (re.match(r"^\d+\.\s", first) or (len(first) < 50 and not first.endswith((".", ":")))):
            out.append(f"<h2>{esc(first)}</h2>")
            continue
        if first.startswith("•"):
            items = []
            for l in lines:
                if l.strip().startswith("•"):
                    items.append(l.strip()[1:].strip())
                else:
                    items[-1] += " " + l.strip()
            if all(i.count(" | ") >= 2 for i in items):  # "a | b | c" rows -> table
                rows = [[c.strip() for c in i.split(" | ")] for i in items]
                head = "".join(f"<th>{esc(c)}</th>" for c in rows[0])
                trs = "".join("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in r) + "</tr>" for r in rows[1:])
                out.append(f"<table><thead><tr>{head}</tr></thead><tbody>{trs}</tbody></table>")
            else:
                out.append("<ul>" + "".join(f"<li>{linkify(esc(i))}</li>" for i in items) + "</ul>")
            continue
        if len(lines) > 1 and all(re.match(r"^[A-Z][\w ]{1,20}:\s", l.strip()) for l in lines):
            out.append('<p class="meta">' + "<br>".join(linkify(esc(l.strip())) for l in lines) + "</p>")
            continue
        parts = []
        for l in lines:
            if l.startswith("  ") and parts:
                parts.append("<br>" + linkify(esc(l.strip())))
            else:
                parts.append(linkify(esc(l.strip())))
        para = " ".join(parts).replace(" <br>", "<br>")
        for phrase, url in LINK_PHRASES.items():
            if phrase in para and url not in para:
                para = para.replace(phrase, f'<a href="{url}">{phrase}</a>', 1)
        out.append(f"<p>{para}</p>")
    return title, "\n".join(out)


def html_to_html(src):
    src = scrub(src)
    title = re.sub(r"<[^>]+>", "", re.search(r"<h1[^>]*>(.*?)</h1>", src, re.S).group(1)).strip()
    body = re.search(r"<body[^>]*>(.*)</body>", src, re.S).group(1)
    body = re.sub(r"<(style|script)\b.*?</\1>", "", body, flags=re.S)
    body = re.sub(r"<h1[^>]*>.*?</h1>", "", body, count=1, flags=re.S)
    # unwrap a <main>/<article>/<div class=wrap> container so our layout applies
    body = re.sub(r"</?(main|article)[^>]*>", "", body)
    # plain-text emails -> mailto links (leave ones that are already links)
    parts = re.split(r"(<a\b.*?</a>)", body, flags=re.S)
    body = "".join(p if p.startswith("<a") else p.replace(CONTACT, f'<a href="mailto:{CONTACT}">{CONTACT}</a>') for p in parts)
    return title, body.strip()


def build_policies():
    os.makedirs(os.path.join(SITE, "privacy"), exist_ok=True)
    by_slug = {g["slug"]: g for g in GAMES}
    for slug, rel in POLICY_SOURCES.items():
        g = by_slug[slug]
        with open(os.path.join(GAMES_DIR, rel), encoding="utf-8") as f:
            src = f.read()
        title, content = (html_to_html(src) if rel.endswith(".html") else txt_to_html(src))
        leftover = set(EMAIL_RE.findall(content)) - {CONTACT}
        assert not leftover and ".github.io" not in content, (slug, leftover)
        body = f"""<article class="doc">
  <p class="crumbs"><a href="../">← All privacy policies</a></p>
  <h1>{esc(g['name'])} privacy policy</h1>
{content}
</article>"""
        d = os.path.join(SITE, "privacy", slug)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8", newline="\n") as f:
            f.write(page(f"{g['name']} privacy policy · {STUDIO}", f"Privacy policy for the {g['name']} Android app by {STUDIO}.",
                         body, depth=2, canonical=f"privacy/{slug}/"))
        print("policy", slug, "<-", title)

    items = []
    for g in GAMES:
        if g["slug"] in POLICY_SOURCES:
            items.append(f'<li><a href="{g["slug"]}/"><img src="../img/{g["slug"]}-icon.webp" alt="" width="44" height="44">'
                         f'<div>{esc(g["name"])}<span>{g["pkg"]}</span></div></a></li>')
    upcoming = ", ".join(g["name"] for g in GAMES if g["slug"] not in POLICY_SOURCES)
    body = f"""<article class="doc">
  <p class="kicker">For parents and players</p>
  <h1>Privacy at {STUDIO}</h1>
  <p class="meta">Effective date: November 14, 2026 · Contact: <a href="mailto:{CONTACT}">{CONTACT}</a></p>

  <p>We make games, not profiles. Most of our games keep everything they save on your device, and our games for children collect no personal information at all. Each app has its own privacy policy below, because each one does slightly different things (for example, some general-audience games show ads from Google AdMob).</p>

  <h2>App privacy policies</h2>
  <ul class="policy-list">
    {chr(10).join(items)}
  </ul>
  <p class="note">Privacy policies for {esc(upcoming)} will be published here before each game is released.</p>

  <h2>Our games for children</h2>
  <p>Kids Fun Games, Dino Smash City and Christmas Town Fun are made for young children and follow the Google Play Families Policy. They have no ads, no analytics, no accounts and no tracking, and they do not collect personal information from anyone. Optional purchases or tips are processed by Google Play and sit behind a parent check that young children cannot complete.</p>

  <h2>This website</h2>
  <p>This website ({DOMAIN}) is a simple information page. It does not use cookies, analytics, ads, tracking pixels, embedded videos or social media widgets, and it has no forms or accounts. Like every website, the hosting provider that serves these pages may keep standard technical logs (such as IP address, browser type and the page requested) for security and to keep the site running. We do not use those logs to identify visitors.</p>
  <p>The "Get it on Google Play" buttons are ordinary links. When you follow one, you leave this site and Google's own privacy policy applies.</p>

  <h2>Children's privacy</h2>
  <p>We do not knowingly collect personal information from children. If you believe a child has sent us personal information, for example by email, contact us and we will delete it.</p>

  <h2>Your questions and requests</h2>
  <p>If you have a question about any of our games or want us to delete an email you sent us, write to <a href="mailto:{CONTACT}">{CONTACT}</a>.</p>

  <h2>Changes</h2>
  <p>If this page or an app's policy changes, we will update it here and change its effective date.</p>
</article>"""
    with open(os.path.join(SITE, "privacy", "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(page(f"Privacy · {STUDIO}", f"Privacy policies for {STUDIO} games and website.", body, depth=1, canonical="privacy/"))


def build_misc():
    body = """<article class="doc" style="text-align:center;padding-bottom:40px">
  <p class="kicker">404</p>
  <h1>Oops, this page wandered off!</h1>
  <p class="sub" style="margin:12px auto 24px">Maybe a dino stomped on it. Let's head back home.</p>
  <p><a class="btn btn-yellow" href="/">Back to the games</a></p>
</article>"""
    # 404 is served at any URL depth, so it uses root-absolute paths.
    html404 = page(f"Page not found · {STUDIO}", "Page not found.", body)
    for a, b in [('href="css/', 'href="/css/'), ('href="favicon', 'href="/favicon'), ('src="favicon', 'src="/favicon'),
                 ('href="#', 'href="/#'), ('href="privacy/', 'href="/privacy/'), ('href="./"', 'href="/"')]:
        html404 = html404.replace(a, b)
    files = {
        "404.html": html404,
        "CNAME": DOMAIN + "\n",
        "robots.txt": f"User-agent: *\nAllow: /\nSitemap: https://{DOMAIN}/sitemap.xml\n",
        "sitemap.xml": '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                       + "".join(f"  <url><loc>https://{DOMAIN}/{p}</loc></url>\n"
                                 for p in ["", "privacy/"] + [f"privacy/{s}/" for s in POLICY_SOURCES])
                       + "</urlset>\n",
        ".nojekyll": "",
    }
    # AdMob app-ads.txt: the studio's AdMob publisher line (same for every AdMob app).
    with open(os.path.join(GAMES_DIR, "Brick Blast", "app-ads.txt"), encoding="utf-8") as f:
        files["app-ads.txt"] = f.read().strip() + "\n"
    for name, text in files.items():
        with open(os.path.join(SITE, name), "w", encoding="utf-8", newline="\n") as f:
            f.write(text)


if __name__ == "__main__":
    with open(os.path.join(SITE, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(build_index())
    build_policies()
    build_misc()
    print("built index, privacy, 404, CNAME, robots, sitemap, app-ads.txt")
