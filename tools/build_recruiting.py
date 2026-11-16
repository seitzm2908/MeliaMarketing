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

# --- Startseite: Team-Hälfte der bisherigen Startseite ------------------------
src = (SRC / "index.html").read_text(encoding="utf-8")
head = src[: src.index("</head>")]
head = re.sub(r'<script type="application/ld\+json">.*?</script>', "", head, flags=re.S)
head = meta(head, "Selbstständig als Immobilienmakler – mit Plan | Markus Seitz",
            "Selbstständig als Immobilienmakler, aber nicht allein: 69 Prozent ab dem ersten Euro, Mentor, Backoffice und ein klarer Plan. Lerne das Modell im Meetup kennen.", "")
solo_css = """<style>
.hero.solo{--s:0;--p:29;background:#fff;cursor:default}
.hero.solo .world-team{-webkit-mask-image:none!important;mask-image:none!important}
.hero.solo .brand span{color:var(--navy,#0E2339)}
.hero.solo .pt{cursor:default}
.hero.solo .team{right:5%;width:42%}
.hero.solo .team h1 em{font-style:italic;color:var(--coral)}
.dive.solo-welt{position:relative;inset:auto;clip-path:none!important;visibility:visible!important;overflow:visible;z-index:1;transition:none}
.solo-welt .in{padding-top:72px;min-height:0}
.mtp{margin:46px 0 10px;padding:34px 30px;border-radius:30px;background:linear-gradient(160deg,#F3FBFF,#DFF3FB)}
.mtp h3{margin:0 0 10px;font:italic 700 clamp(24px,2.6vw,34px)/1.2 Montserrat;color:var(--blue)}
.mtp p{margin:0 0 20px;max-width:56ch}
.mtp .row{display:flex;flex-wrap:wrap;gap:12px}
.mtp .pill.o{background:#fff;color:#000;border:2px solid var(--blue)}
footer .own{margin-top:6px}
@media (max-width:800px){
 .hero.solo{--p:29;height:900px}
 .hero.solo .team{left:6%;right:6%;width:auto;bottom:60px}
 .mtp{padding:26px 22px}
}
</style>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"WebSite","name":"Selbstständig mit Plan","url":"__NEW__/","publisher":{"@type":"Person","name":"Markus Seitz","jobTitle":"Immobilienmakler, Teamleader iad Deutschland","url":"__NEW__/","sameAs":["__MAIN__/"]}}</script>
""".replace("__NEW__", NEW).replace("__MAIN__", MAIN)

hs = src.index('<section class="hero"'); he = src.index("</section>", src.index('<div class="dive d-team"')) + 10
hero = src[hs:he]
def cut(h, start, end_marker=None):
    i = h.index(start)
    if end_marker:
        j = h.index(end_marker, i) + len(end_marker)
    else:  # balanced <div>
        depth = 0
        for m in re.finditer(r"<(/?)div\b[^>]*>", h[i:]):
            depth += -1 if m.group(1) else 1
            if depth == 0:
                j = i + m.end(); break
    return h[:i] + h[j:]
hero = cut(hero, '<div class="layer world-owner"')
hero = cut(hero, '<div class="seam"', "</div>")
hero = cut(hero, '<div class="spot"', "</div>")
hero = cut(hero, '<div class="col owner"')
hero = cut(hero, '<div class="hint"', "</div>")
hero = cut(hero, "<!-- Eintauchen: Eigentümer-Welt -->", "-->")
hero = cut(hero, '<div class="dive d-owner"')
# Team-Welt aus dem Overlay lösen und als eigenen Abschnitt hinter den Hero stellen
ti = hero.index("<!-- Eintauchen: Team-Welt -->")
welt = hero[ti:hero.rindex("</section>")]
hero = hero[:ti] + "</section>\n"
welt = welt.replace('<div class="dive d-team" id="dvT" role="dialog" aria-label="Team-Welt" aria-hidden="true">',
                    '<section class="dive d-team solo-welt" id="dvT" aria-label="Team-Welt">', 1)
welt = welt.replace('<button class="back" data-close>Zurück</button>', "", 1)
for dup in ['<p class="lbl-t">Ich will einsteigen</p>', '<h2>Komm in mein <em>Team.</em></h2>', '<p class="claim">Klarer Rahmen, persönliche Begleitung, offene Zahlen.</p>']:
    assert dup in welt, dup
    welt = welt.replace(dup, "", 1)
welt = welt[: welt.rindex("</div>")] + "</section>\n"
hero = hero.replace('<section class="hero" id="hero"', '<section class="hero solo" id="hero"', 1)
hero = hero.replace('aria-label="Startseite Markus Seitz Immobilien"', 'aria-label="Selbstständig mit Plan"')
hero = hero.replace('<div class="chip">Markus Seitz Immobilien. Mit iad.</div>', '<div class="chip">Selbstständig mit Plan. Mit iad.</div>')
hero = hero.replace('<a class="brand" href="#">', '<a class="brand" href="index.html">')
hero = hero.replace('<h2><span class="w"><i style="--d:.8s">Komm', '<h1 style="margin:0 0 14px;font:800 clamp(40px,4vw,66px)/.98 Montserrat;letter-spacing:-.025em;color:var(--blue)"><span class="w"><i style="--d:.8s">Komm', 1)
hero = re.sub(r'(<i style="--d:1\.08s">Team\.</i></span></em>)</h2>', r"\1</h1>", hero, count=1)
hero = hero.replace('<button class="zug fi" style="--d:1.45s" data-dive="team"><strong>Du bist Makler und überlegst zu wechseln?</strong><span class="pill">Ehrlich durchrechnen</span></button>',
                    '<a class="zug fi" style="--d:1.45s;text-decoration:none" href="wechsel.html"><strong>Du bist Makler und überlegst zu wechseln?</strong><span class="pill">Ehrlich durchrechnen</span></a>')
hero = hero.replace('<button class="zug fi" style="--d:1.6s" data-dive="team"><strong>Deine Ausbildung ist fast fertig? Und jetzt?</strong><span class="pill">Meinen Start planen</span></button>',
                    '<a class="zug fi" style="--d:1.6s;text-decoration:none" href="start.html"><strong>Deine Ausbildung ist fast fertig? Und jetzt?</strong><span class="pill">Meinen Start planen</span></a>')
assert 'data-dive' not in hero and "world-owner" not in hero, "Hero nicht sauber getrennt"
mtp = f"""   <div class="mtp"><h3>Lerne das Modell im Meetup kennen.</h3><p>Alle zwei Wochen donnerstags um 18 Uhr, online per Google Meet. Unverbindlich, mit deinen Fragen.</p><div class="row"><a class="pill" style="text-decoration:none" href="start.html#meetup-anmeldung">Zum Meetup anmelden</a><a class="pill o" style="text-decoration:none" href="{WA}" target="_blank" rel="noopener">Per WhatsApp schreiben</a></div></div>
   <p class="fine">"""
welt = welt.replace('   <p class="fine">', mtp, 1)

fs = src.index("<footer"); fe = src.index("</footer>", fs) + 9
footer = re.sub(r'<nav class="allorte".*?</nav>\s*', "", src[fs:fe], flags=re.S)
footer = footer.replace("</footer>", f'<p class="own">Du willst eine Immobilie verkaufen? <a href="{MAIN}/">markus-seitz.immobilien</a></p>\n</footer>')

script = """<script>
(function(){
var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
var w=document.getElementById('dvT'),n69=document.getElementById('n69');
document.querySelectorAll('.dive .in').forEach(function(x){Array.prototype.forEach.call(x.children,function(c,i){c.style.setProperty('--i',i)})});
function count(){if(!n69)return;if(reduce){n69.textContent='69';return}var st=performance.now()+600,dur=1500;n69.textContent='0';
(function step(now){var k=Math.min(1,Math.max(0,(now-st)/dur));k=1-Math.pow(1-k,4);n69.textContent=Math.round(69*k);if(k<1)requestAnimationFrame(step)})(performance.now());}
var els=w.querySelectorAll('.rv');
if(reduce||!('IntersectionObserver' in window)){w.classList.add('on');els.forEach(function(e){e.classList.add('vis')});return}
new IntersectionObserver(function(en,o){if(en[0].isIntersecting){w.classList.add('on');count();o.disconnect()}},{threshold:.05}).observe(w);
var io=new IntersectionObserver(function(en){en.forEach(function(x){if(x.isIntersecting){x.target.classList.add('vis');io.unobserve(x.target)}})},{threshold:.2});
els.forEach(function(e){io.observe(e)});
})();
</script>"""
idx = head + solo_css + "</head><body>\n" + hero + welt + footer + "\n" + script + "\n</body></html>"
idx = fix_links(track_meetup(idx))
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
