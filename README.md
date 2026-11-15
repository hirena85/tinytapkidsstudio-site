# tinytapkidsstudio.com

The Tiny Tap Kids Studio website: plain static HTML with no build tools, cookies, analytics or trackers.

| Page | File |
|---|---|
| Home: hero, games grid (4 live + 5 coming soon), about, contact | `index.html` |
| Privacy hub (website + list of app policies) | `privacy/index.html` |
| Per-app privacy policies (for the Play Console) | `privacy/<game>/index.html` |
| Not-found page | `404.html` |
| Custom domain for GitHub Pages | `CNAME` |
| AdMob app-ads.txt (the studio's publisher line) | `app-ads.txt` |

## Editing

All pages are generated. Change `tools/build.py`, then run:

```
python tools/build.py index  # rebuild only the home page (leaves privacy pages alone)
python tools/build.py        # rebuild every HTML page, including privacy
python tools/make_images.py  # only if game art changed (re-reads the game folders)
```

Each game card on the home page shows the icon, two or three screenshots, a short description, a Google Play button (or a Coming soon label) and a link to that game's privacy page. Screenshot files live in `img/shots/`.

- **When a game goes live**, change its `status` from `"testing"`/`"dev"` to `"live"` in `GAMES`. The "Coming soon" badge becomes a real Google Play button (`https://play.google.com/store/apps/details?id=<package>`), and the card moves to "Out now".
- **New privacy policy** (e.g. Ink Heroes): add it to `POLICY_SOURCES`. Any email address or `*.github.io` link in the source is swapped automatically for `CONTACT` / the domain.
- **Contact email**: `CONTACT` at the top of `tools/build.py`. It is a placeholder (`hello@tinytapkidsstudio.com`) until you set up step 3 below.

Preview locally: `python -m http.server 8765` in this folder, then open http://localhost:8765.

---

## Going live: GitHub Pages + your Squarespace domain

GitHub Pages is free and you already use it for your current policy pages. Use a **new repository** for this site. Do not add the custom domain to your existing `<username>.github.io` repo: if that repo gets a custom domain, the old policy URLs your Play listings use today start redirecting.

### 1. Put the site on GitHub (≈5 min)
1. On github.com, click **New repository**. Name it `tinytapkidsstudio-site`, make it **Public**, and create it without a README.
2. Upload the contents of this folder. Either drag every file and folder except `tools/` and `README.md` onto the repo's **"uploading an existing file"** page (they don't hurt if included), or from a terminal in this folder:
   ```
   git init -b main
   git add .
   git commit -m "Tiny Tap Kids Studio website"
   git remote add origin https://github.com/<username>/tinytapkidsstudio-site.git
   git push -u origin main
   ```
3. In the repo, go to **Settings → Pages**. Set **Source: Deploy from a branch**, then **Branch: main / (root)**, and click **Save**.
4. On the same page, the **Custom domain** field should already show `tinytapkidsstudio.com` (from the `CNAME` file). If not, type it and save. Leave this page open.

### 2. Point the domain at GitHub (Squarespace, ≈5 min + DNS wait)
1. Sign in to Squarespace and go to **Domains → tinytapkidsstudio.com → DNS** (sometimes **DNS Settings**).
2. If you **don't** have a Squarespace website plan, delete the **Squarespace Defaults** record group. It points the domain at a Squarespace site. **Don't delete** any MX records from **Email forwarding** (step 3) or Google Workspace.
3. Under **Custom records**, add:

   | Host | Type | Data |
   |---|---|---|
   | @ | A | 185.199.108.153 |
   | @ | A | 185.199.109.153 |
   | @ | A | 185.199.110.153 |
   | @ | A | 185.199.111.153 |
   | @ | AAAA | 2606:50c0:8000::153 |
   | @ | AAAA | 2606:50c0:8001::153 |
   | @ | AAAA | 2606:50c0:8002::153 |
   | @ | AAAA | 2606:50c0:8003::153 |
   | www | CNAME | `<username>.github.io` |

4. Wait. DNS usually updates in 15–60 minutes and can take up to 48 hours. Back on GitHub's **Settings → Pages**, the domain check turns green. Then tick **Enforce HTTPS** (it can take up to an hour to become clickable).
5. Check https://tinytapkidsstudio.com, https://www.tinytapkidsstudio.com and https://tinytapkidsstudio.com/app-ads.txt.

> Optional security step: in GitHub **Settings (your profile) → Pages → Add a verified domain**, verify `tinytapkidsstudio.com` with the TXT record GitHub shows. Then nobody else can claim the domain on GitHub.

### 3. Studio email: hello@tinytapkidsstudio.com (free)
Squarespace Domains includes free email forwarding: mail sent to hello@ lands in an inbox you choose.

**Tip, to keep your personal address private when you reply:** forwarding only *receives*. If you reply from your personal Gmail, the sender sees that address. So forward to a separate, free studio Gmail (e.g. a new `tinytapkidsstudio…@gmail.com`) and answer from there. If you later want replies to show hello@ itself, that needs Google Workspace (paid, about $7/month).

1. Sign in at squarespace.com → profile menu → **Domains** → click **tinytapkidsstudio.com**.
2. In the domain's left menu, open **Email** → **Email forwarding**.
3. Click **Add rule**. Set **Alias** to `hello` (full address hello@tinytapkidsstudio.com) and **Forward to** to your studio Gmail (or personal inbox). Then **Save**.
4. Squarespace adds the MX records itself. In **DNS**, an "Email forwarding" record group (MX records) appears. **Don't delete it** when you remove the Squarespace Defaults group in step 2 of the hosting steps above.
5. If Squarespace emails the destination inbox a confirmation link, click it.
6. Wait about 15–60 minutes. Then, from a *different* email account, send a test to hello@tinytapkidsstudio.com. Check spam the first time. If it's there, mark it **Not spam**, or add a Gmail filter: *To: hello@tinytapkidsstudio.com → Never send to spam*, label "Studio".
7. Optional: add more aliases the same way (e.g. `support`, `privacy`). They all forward to the same inbox.

If test mail doesn't arrive after a few hours, check that **DNS** shows the forwarding MX records and that no other MX records (old Google Workspace or another provider) are still listed.

To use a different contact address, change `CONTACT` in `tools/build.py` and rebuild.

### 4. Update Google Play Console (once the site is live)
For each live app, go to **Policy and programs → App content → Privacy policy**:

| App | Privacy policy URL |
|---|---|
| Kaiju Rampage | https://tinytapkidsstudio.com/privacy/kaiju-rampage/ |
| Brick Blast Rocket | https://tinytapkidsstudio.com/privacy/brick-blast-rocket/ |
| Kids Fun Games | https://tinytapkidsstudio.com/privacy/kids-fun-games/ |
| Dino Smash City | https://tinytapkidsstudio.com/privacy/dino-smash-city/ |
| Christmas Town Fun | https://tinytapkidsstudio.com/privacy/christmas-town-fun/ |
| Deep Glow | https://tinytapkidsstudio.com/privacy/deep-glow/ |

Also do these:
- **Store presence → Store settings → Store listing contact details → Website**: `https://tinytapkidsstudio.com`, and **Email** if you switched to hello@.
- **AdMob → Apps → app-ads.txt**: AdMob crawls `app-ads.txt` on the website listed in Play. The file here already holds your publisher line, so verification carries over after you change the website. Recheck it after a day.
- **Developer page** (optional): set its website to the new domain too.
- Keep the old `github.io` policy pages online until every app points at the new URLs.

---

## Before each new game launch
1. Write its privacy policy (copy the closest existing one) and add it to `POLICY_SOURCES`.
2. Set the game's `status` to `"live"` in `GAMES`.
3. `python tools/build.py`, then upload or push the changed files.
