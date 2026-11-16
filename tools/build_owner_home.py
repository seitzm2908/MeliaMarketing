"""Erzeugt website/index.html: die Eigentümer-Hälfte (Navy, Radar) der Doppelseite als eigene Startseite.
Quelle: quellen/doppelseite.html. Aufruf aus dem Repo-Hauptordner: python3 tools/build_owner_home.py
"""
import re, pathlib

src = pathlib.Path("quellen/doppelseite.html").read_text(encoding="utf-8")
RECRUIT = "https://www.xn--selbststndig-mit-plan-d2b.de/"

def cut(h, start, end_marker=None):
    i = h.index(start)
    if end_marker:
        j = h.index(end_marker, i) + len(end_marker)
    else:
        depth = 0
        for m in re.finditer(r"<(/?)div\b[^>]*>", h[i:]):
            depth += -1 if m.group(1) else 1
            if depth == 0:
                j = i + m.end(); break
    return h[:i] + h[j:]

head = src[: src.index("</head>")]
solo_css = """<style>
.hero.solo{--s:60;--p:72;cursor:default}
.hero.solo .owner{left:6%;width:44%}
.hero.solo .radar{left:72%;top:46%}
.hero.solo .obtns{display:flex;flex-wrap:wrap;gap:12px}
.dive.solo-welt{position:relative;inset:auto;clip-path:none!important;visibility:visible!important;overflow:visible;z-index:1;transition:none}
.solo-welt .in{min-height:0}
.solo-welt .in:first-of-type{padding-top:64px}
footer .own{margin-top:6px}
@media (max-width:800px){
 .hero.solo{--p:80;height:800px}
 .hero.solo .radar{left:50%;top:76%}
 .hero.solo .owner{left:6%;right:6%;width:auto}
 .hero.solo .owner p.t{display:block;font-size:15px}
}
</style>
"""
hs = src.index('<section class="hero"'); he = src.index("</section>", src.index('<div class="dive d-team"')) + 10
hero = src[hs:he]
hero = cut(hero, '<div class="layer world-team"')
hero = cut(hero, '<div class="seam"', "</div>")
hero = cut(hero, '<div class="spot"', "</div>")
hero = cut(hero, '<div class="col team"')
hero = cut(hero, '<div class="hint"', "</div>")
hero = cut(hero, "<!-- Eintauchen: Team-Welt -->", "-->")
hero = cut(hero, '<div class="dive d-team"')
oi = hero.index("<!-- Eintauchen: Eigentümer-Welt -->")
welt = hero[oi:hero.rindex("</section>")]
hero = hero[:oi] + "</section>\n"
welt = welt.replace("<!-- Eintauchen: Eigentümer-Welt -->", "", 1)
welt = welt.replace('<div class="dive d-owner" id="dvO" role="dialog" aria-label="Eigentümer-Welt" aria-hidden="true">',
                    '<section class="dive d-owner on solo-welt" id="dvO" aria-label="Bewertungen und Orte">', 1)
for dup in ['<button class="back" data-close>Zurück</button>', '<p class="lbl-o">Ich will verkaufen</p>',
            '<h2>Deine Immobilie <em>verdient eine Strategie.</em></h2>',
            '<p class="t">Ich kenne deinen Ort und seinen Markt. Wir starten mit einer realistischen Bewertung, nicht mit einem Inserat.</p>']:
    assert dup in welt, dup
    welt = welt.replace(dup, "", 1)
welt = welt[: welt.rindex("</div>")] + "</section>\n"
hero = hero.replace('<section class="hero" id="hero"', '<section class="hero solo" id="hero"', 1)
hero = hero.replace('<a class="brand" href="#">', '<a class="brand" href="/">')
hero = re.sub(r'<a class="btn-o fi" style="--d:1\.5s" href="#" data-dive="owner">([^<]*)</a>',
               r'<div class="obtns fi" style="--d:1.5s"><a class="btn-o" href="wert-radar.html">\1</a><a class="btn-o2" href="eigentuemer.html">Meine Strategie ansehen</a></div>', hero, count=1)
welt = re.sub(r'<div class="obtns">.*?</div>\s*', '', welt, count=1, flags=re.S)
welt = re.sub(r'<div class="in" style="min-height:0;padding-bottom:36px">\s*</div>\s*', '', welt, count=1)
assert 'padding-bottom:36px' not in welt
hero = hero.replace(' aria-label="Porträt von Markus Seitz, ziehen verschiebt die Naht"', ' aria-label="Porträt von Markus Seitz"')
assert "data-dive" not in hero and "world-team" not in hero and "col team" not in hero

fs = src.index("<footer"); fe = src.index("</footer>", fs) + 9
footer = src[fs:fe].replace("</footer>", f'<p class="own">Du bist Makler oder willst es werden? <a href="{RECRUIT}">Selbstständig mit Plan</a></p>\n</footer>')
tail = src[fe: src.index("</body>")]
tail = re.sub(r"<script>\s*\(function\(\)\{\s*var hero=document\.getElementById\('hero'\).*?\}\)\(\);\s*</script>", "", tail, flags=re.S)
assert "getElementById('hero')" not in tail
out = head + solo_css + "</head>" + src[src.index("</head>") + 7: hs] + hero + welt + footer + tail + "</body></html>\n"
pathlib.Path("website/index.html").write_text(out, encoding="utf-8")
print("website/index.html:", len(out) // 1024, "KB")
