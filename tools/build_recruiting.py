"""Baut selbstständig-mit-plan.de aus den Team-Seiten von website/.
Aufruf: python3 tools/build_recruiting.py   (aus dem Repo-Hauptordner)
"""
import re, shutil, pathlib

SRC = pathlib.Path("website")
OUT = pathlib.Path("selbststaendig-mit-plan")
NEW = "https://www.xn--selbststndig-mit-plan-d2b.de"
MAIN = "https://www.markus-seitz.immobilien"
WA = "https://wa.me/4917615858511?text=Hallo%20Markus%2C%20ich%20interessiere%20mich%20f%C3%BCr%20dein%20Team."

if OUT.exists(): shutil.rmtree(OUT)
(OUT / "media").mkdir(parents=True)
shutil.copytree(SRC / "fonts", OUT / "fonts")
for m in ["iad-logo.png", "og-image.jpg", "apple-touch-icon.png", "ms-logo.png"]:
    shutil.copy(SRC / "media" / m, OUT / "media" / m)

# consent.js: eigene GA4-ID, bis dahin leer (dann lädt nichts von Google)
c = (SRC / "consent.js").read_text(encoding="utf-8")
c = c.replace('"ga4": "G-VQ73DJ6CFV"', '"ga4": ""')
c = c.replace("Google-Ads-ID und Conversion-Label", "GA4-ID (\"ga4\"), Google-Ads-ID und Conversion-Label")
(OUT / "consent.js").write_text(c, encoding="utf-8")

def meta(s, title, desc, path):
    url = NEW + "/" + path
    s = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", s, count=1, flags=re.S)
    s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', s, count=1)
    s = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', s, count=1)
    s = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">', s, count=1)
    s = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">', s, count=1)
    s = s.replace(MAIN + "/media/og-image.jpg", NEW + "/media/og-image.jpg")
    return s

def track_meetup(s):
    return s.replace("s.textContent='Dein E-Mail-Programm öffnet sich.",
                     "if(window.msTrack)msTrack('meetup');s.textContent='Dein E-Mail-Programm öffnet sich.")

OWN = {"index.html", "start.html", "wechsel.html", "impressum.html", "datenschutz.html", "agb.html", "widerruf.html"}
def fix_links(s):
    s = s.replace('href="team-start.html"', 'href="start.html"').replace('href="team-makler.html"', 'href="wechsel.html"')
    def absol(m):
        h = m.group(1)
        base = h.split("#")[0]
        if not base or "://" in h or h.startswith(("mailto:", "tel:", "#", "data:", "fonts/", "media/", "$")) or base in OWN:
            return m.group(0)
        return f'href="{MAIN}/{h}"'
    return re.sub(r'href="([^"]*)"', absol, s)


FIX_CSS = """<style>
.hero.wrap{padding-left:6%;padding-right:6%}
.bk.fw::before{display:none}
@media(max-width:800px){.cta,.mu,.hint{margin-left:16px!important;margin-right:16px!important;width:auto}}
</style>"""
def fix_css(s):
    return s.replace("</head>", FIX_CSS + "</head>", 1)

# --- Unterseiten -------------------------------------------------------------
pages = {
  "start.html": ("team-start.html", "Dein Start als Immobilienmakler | Selbstständig mit Plan",
                 "Ausbildung fast fertig? Starte als Immobilienmakler im Team von Markus Seitz: Mentor, Backoffice und ein klarer Plan für deine ersten sechs Monate."),
  "wechsel.html": ("team-makler.html", "Makler-Wechsel ehrlich durchrechnen | Selbstständig mit Plan",
                   "Rechne ehrlich: Dein erstes Jahr als Makler im Team von Markus Seitz mit 69 Prozent Provision im Vergleich zu deinem heutigen System."),
}
for out, (src, t, d) in pages.items():
    s = (SRC / src).read_text(encoding="utf-8")
    s = fix_css(fix_links(track_meetup(meta(s, t, d, out))))
    (OUT / out).write_text(s, encoding="utf-8")

# --- Startseite --------------------------------------------------------------
tpl = (SRC / "team-start.html").read_text(encoding="utf-8")
head = tpl[: tpl.index("</head>")]
head = meta(head, "Selbstständig als Immobilienmakler – mit Plan | Markus Seitz",
            "Selbstständig als Immobilienmakler, aber nicht allein: 69 Prozent ab dem ersten Euro, Mentor, Backoffice und ein klarer Plan. Lerne das Modell im Meetup kennen.", "")
head = head.replace(f'href="{NEW}/"', f'href="{NEW}/"')
extra_css = """<style>
.cards5{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}
.chips{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 26px}.chips span{display:inline-flex;align-items:center;min-height:40px;padding:0 16px;border-radius:999px;border:2px solid #CDEFFB;font:600 14px/1 Montserrat;color:#003A55;background:#F5FBFE}.chips span.rab{border-color:#F6C9C3;background:#FFF6F5}
h3.sub{margin:0 0 12px;font:italic 700 18px/1.3 Montserrat;color:var(--blue)}
.paths{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}
.pth{padding:30px 28px;border-radius:30px;border:2px solid #CDEFFB;display:flex;flex-direction:column;gap:12px;align-items:flex-start}
.pth .no{font:800 15px/1 Montserrat;color:var(--coral)}.pth h3{margin:0;font:italic 700 22px/1.25 Montserrat;color:var(--blue)}.pth p{margin:0 0 6px}
.from{font-size:14px;margin:26px 0 0}.from a{color:#006390;font-weight:600}
@media(max-width:800px){.cards5,.paths{grid-template-columns:1fr}}
</style>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"WebSite","name":"Selbstständig mit Plan","url":"%s/","publisher":{"@type":"Person","name":"Markus Seitz","jobTitle":"Immobilienmakler, Teamleader iad Deutschland","url":"%s/","sameAs":["%s/"]}}</script>
""" % (NEW, NEW, MAIN)
body_start = tpl.index("<body>")
header = tpl[body_start: tpl.index("</header>") + 9]
header = header.replace('<a class="bk" href="index.html">Startseite</a>', '<a class="bk fw" href="#meetup-anmeldung">Zum Meetup</a>')
cta_block = tpl[tpl.index('<section class="cta rv">'): tpl.index("<footer")]
footer = tpl[tpl.index("<footer"): tpl.index("</footer>") + 9]
reveal = re.search(r"<script>\s*\(function\(\)\{var reduce=.*?\}\)\(\);", tpl, re.S).group(0) + "\n</script>"

ICONS = [
 '<path d="M8 30 L32 10 L56 30"/><path d="M15 27 V53 H49 V27"/><path class="cx" d="M10 56 L54 12"/>',
 '<path d="M32 14 L58 26 L32 38 L6 26 Z"/><path d="M16 32 V44 C24 51 40 51 48 44 V32"/><path class="cx" d="M58 26 V42"/>',
 '<path d="M12 36 V30 C12 18 21 10 32 10 C43 10 52 18 52 30 V36"/><rect x="8" y="34" width="10" height="16" rx="5"/><rect x="46" y="34" width="10" height="16" rx="5"/><path class="cx" d="M52 50 C52 56 46 58 38 58"/>',
 '<path d="M32 8 V58"/><path d="M32 16 H50 L56 22 L50 28 H32"/><path d="M32 34 H14 L8 40 L14 46 H32"/><path class="cx" d="M24 58 H40"/>',
 '<rect x="8" y="12" width="48" height="32" rx="5"/><path d="M24 54 H40 M32 44 V54"/><path class="cx" d="M19 29 L27 37 L44 20"/>',
]
CARDS = [("Keine Geschäftsstelle", "Kein Büro, keine Büro- und IT-Pauschale. Du arbeitest dort, wo deine Kunden sind."),
         ("Eigene iad Universität", "Fachwissen aufbauen mit Certified Trainern und einem nationalen Trainerteam."),
         ("Dein Backoffice", "Eine fest zugeordnete Innendienstkraft unterstützt dich ab dem ersten Tag."),
         ("Mentor und Marschroute", "Ich begleite dich mit einem klaren Plan für deine ersten sechs Monate."),
         ("Dein Werkzeugkasten", "CRM, Bewertung, Video und Foto. Alles in einem Paket.")]
cards = "".join(f'<div class="wc rv" style="--n:{i}"><div class="bdg"><svg viewBox="0 0 64 64" aria-hidden="true">{ICONS[i]}</svg></div><h3>{t}</h3><p>{p}</p></div>' for i, (t, p) in enumerate(CARDS))
tools = "".join(f"<span>{x}</span>" for x in ["onOffice", "PriceHubble", "Momenzo", "Google Workspace", "Casafari", "DocuSign", "CARD.PM"])
rab = "".join(f'<span class="rab">{x}</span>' for x in ["Finanzierung", "Versicherungen", "Immobilienmarktbeobachtung"])

main = f"""
<section class="hero wrap"><div class="caps" aria-hidden="true"><i></i><i></i><i></i></div>
<p class="lbl">Für Makler und alle, die es werden wollen</p>
<h1>Selbstständig.<br><em>Mit Plan.</em></h1>
<p class="claim">Klarer Rahmen, persönliche Begleitung, offene Zahlen.</p>
<div class="btns" style="margin-top:28px"><a class="pill" href="#meetup-anmeldung">Zum Meetup anmelden</a><a class="pill o" href="#wege">Welcher Weg passt zu mir?</a></div>
</section>
<section class="wrap">
<div class="price rv"><div class="num">69<sup>%</sup></div><p>ab dem ersten Euro. Vom ersten Tag an, so wie iad es in Deutschland vergütet.</p></div>
<div class="sep"></div>
<h2 class="rv">Das bekommst du bei mir.</h2>
<div class="cards5">{cards}</div>
<div class="sep"></div>
<h3 class="sub rv">Im Beitrag enthalten</h3><div class="chips rv">{tools}</div>
<h3 class="sub rv">Mit Mengenrabatt über das Netzwerk</h3><div class="chips rv">{rab}</div>
<div class="sep"></div>
<h2 class="rv">Von Worms aus deutschlandweit.</h2>
<p class="rv" style="max-width:60ch">Mein Team wächst über Regionen und Bundesländer hinweg. Dein Standort kann der nächste sein. Dein Ort fehlt noch? Schreib mir, wo du starten willst.</p>
<div class="btns rv"><a class="pill o" href="https://wa.me/4917615858511?text=Hallo%20Markus%2C%20ich%20m%C3%B6chte%20in%20deinem%20Team%20starten.%20Mein%20Ort%3A%20" target="_blank" rel="noopener">Schreib mir</a></div>
<div class="sep"></div>
<h2 class="rv" id="wege">Welcher Weg passt zu dir?</h2>
<div class="paths">
 <div class="pth rv" style="--n:0"><span class="no">01</span><h3>Du bist Makler und überlegst zu wechseln?</h3><p>Rechne mit deinen Zahlen. Im Meetup gemeinsam, ohne Verpflichtung.</p><a class="pill" href="wechsel.html">Ehrlich durchrechnen</a></div>
 <div class="pth rv" style="--n:1"><span class="no">02</span><h3>Deine Ausbildung ist fast fertig? Und jetzt?</h3><p>Selbstständig heißt nicht allein. Du startest in einem Team mit 14 Menschen.</p><a class="pill" href="start.html">Meinen Start planen</a></div>
</div>
<p class="fine">Selbstständige Tätigkeit auf Provisionsbasis, ohne Fixgehalt. Der Einstieg erfolgt über einen Handelsvertretervertrag mit der I@D Deutschland GmbH, Markus Seitz Immobilien ist dabei nicht Vertragspartner. Alle Angaben sind unverbindliche Informationen.</p>
<p class="from">Du willst eine Immobilie verkaufen? Dann bist du hier richtig: <a href="{MAIN}/">markus-seitz.immobilien</a></p>
<div class="sep"></div>
</section>
"""
idx = head + extra_css + "</head>" + header + main + cta_block + footer + "\n" + reveal + "</body></html>"
idx = fix_css(fix_links(track_meetup(idx)))
(OUT / "index.html").write_text(idx, encoding="utf-8")

# --- Rechtliches -------------------------------------------------------------
for f in ["impressum.html", "datenschutz.html", "agb.html", "widerruf.html"]:
    s = (SRC / f).read_text(encoding="utf-8")
    s = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{NEW}/{f}">', s)
    s = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{NEW}/{f}">', s)
    s = re.sub(r'<meta name="robots" content="[^"]*">', '<meta name="robots" content="noindex,follow">', s)
    s = s.replace('"ga4": "G-VQ73DJ6CFV"', '"ga4": ""')
    (OUT / f).write_text(fix_links(s), encoding="utf-8")

# --- Technik -----------------------------------------------------------------
(OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {NEW}/sitemap.xml\n", encoding="utf-8")
urls = "".join(f"  <url><loc>{NEW}/{p}</loc></url>\n" for p in ["", "wechsel.html", "start.html"])
(OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n', encoding="utf-8")
(OUT / ".htaccess").write_text("""# Eine Adresse für Google: alles auf https://www. umleiten (301)
RewriteEngine On
RewriteCond %{HTTPS} off [OR]
RewriteCond %{HTTP_HOST} !^www\\. [NC]
RewriteRule ^(.*)$ https://www.xn--selbststndig-mit-plan-d2b.de/$1 [R=301,L]
""", encoding="utf-8")
print("fertig:", sorted(p.name for p in OUT.iterdir()))
