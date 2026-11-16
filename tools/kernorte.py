"""Reduziert die Orts-Seiten auf die Kernorte und ergänzt dort eigenen Inhalt.
Aufruf: python3 tools/kernorte.py website
"""
import re, sys, pathlib

root = pathlib.Path(sys.argv[1])
CORE = ["worms", "worms-pfeddersheim", "mannheim", "ludwigshafen", "alzey", "viernheim"]
RLP = ("Rheinland-Pfalz", "5,0", "BORISplus.rlp")
BW = ("Baden-Württemberg", "5,0", "BORIS-BW")
HE = ("Hessen", "6,0", "BORIS Hessen")

C = {
"worms": dict(ort="Worms", land=RLP, label="Worms im Detail",
  h2="Worms ist nicht gleich <em>Worms.</em>",
  lead="Zwischen Innenstadt und den Stadtteilen am Rand von Rheinhessen liegen in Worms große Unterschiede. Für den Preis zählt deshalb nicht nur die Stadt, sondern der Stadtteil, oft sogar die Straße.",
  cards=[("Innenstadt und innenstadtnahe Lagen","Kurze Wege, viele Wohnungen und Altbauten. Hier achten Käufer besonders auf Zustand, Energiewerte und Stellplatz."),
         ("Die westlichen Stadtteile","Pfeddersheim, Leiselheim, Horchheim, Weinsheim, Wiesoppenheim und Heppenheim: eher Einfamilien- und Reihenhäuser, gefragt bei Familien, die Ruhe und eine schnelle Anbindung an die A61 suchen."),
         ("Im Norden und am Rhein","Herrnsheim, Neuhausen, Hochheim, Pfiffligheim, Abenheim, Rheindürkheim und Ibersheim: von gewachsenen Ortskernen bis zu ländlich geprägten Lagen. Jede Lage hat ihre eigene Käufergruppe."),
         ("Käufer aus der ganzen Region","Über die S-Bahn Rhein-Neckar und die Nibelungenbrücke sind Mannheim, Ludwigshafen und das hessische Ried gut erreichbar. Viele Käufer vergleichen Worms deshalb direkt mit den teureren Städten am Rhein.")]),
"worms-pfeddersheim": dict(ort="Pfeddersheim", land=RLP, label="Pfeddersheim im Detail",
  h2="Pfeddersheim: <em>Kleinstadt-Charakter in Worms.</em>",
  lead="Pfeddersheim war lange eine eigenständige Stadt und gehört seit 1969 zu Worms. Altstadt, Reste der historischen Stadtmauer und die Weinberge prägen bis heute das Bild. Mein Büro liegt hier, in der Sankt-Georgen-Straße.",
  cards=[("Altstadt und Ortskern","Ältere Häuser mit Charakter. Ich prüfe früh, ob Denkmalschutz, Sanierungsbedarf oder enge Grundstücke den Käuferkreis verändern, damit der Preis von Anfang an stimmt."),
         ("Wohngebiete am Ortsrand","Einfamilien- und Doppelhäuser mit Garten sprechen vor allem Familien an, die ruhig wohnen und trotzdem schnell in der Stadt sein wollen."),
         ("Anbindung","Die A61 und die Wormser Innenstadt sind schnell erreicht. Das macht Pfeddersheim für Pendler Richtung Mannheim und Mainz interessant."),
         ("Kurze Wege zu mir","Mein Büro ist vor Ort. Besichtigungen, Rückfragen und Übergaben laufen ohne lange Anfahrt, und ich kenne die Straßen, über die wir sprechen.")]),
"mannheim": dict(ort="Mannheim", land=BW, label="Mannheim im Detail",
  h2="Mannheim verkauft sich <em>nach Lage.</em>",
  lead="Zwischen den Quadraten, dem Lindenhof und Stadtteilen wie Feudenheim oder Seckenheim liegen in Mannheim spürbare Preisunterschiede. Käufer vergleichen hier sehr genau, deshalb muss die Positionierung sitzen.",
  cards=[("Innenstadt und Quadrate","Vor allem Wohnungen, gesucht von Selbstnutzern und Kapitalanlegern. Käufer fragen früh nach Hausgeld, Rücklage und den Protokollen der Eigentümerversammlung. Ich bereite diese Unterlagen vorab auf."),
         ("Besonders gefragte Wohnlagen","Lindenhof, Oststadt, Neuostheim und Feudenheim gehören zu den gesuchten Adressen. Hier entscheidet oft die Präsentation darüber, ob der Preis am oberen Ende des Rahmens liegt."),
         ("Haus und Garten","In Stadtteilen wie Seckenheim, Käfertal, Neckarau, Rheinau oder Sandhofen suchen viele Familien Reihen- und Einfamilienhäuser."),
         ("Käufer von außerhalb","Mannheim ist ICE-Knoten, Frankfurt und Stuttgart sind schnell erreichbar. Das bringt Käufer, die beruflich in die Region ziehen und eine klare, gut vorbereitete Entscheidung treffen wollen.")]),
"ludwigshafen": dict(ort="Ludwigshafen", land=RLP, label="Ludwigshafen im Detail",
  h2="Ludwigshafen: <em>mehr Fläche fürs Geld.</em>",
  lead="Direkt gegenüber von Mannheim, aber spürbar günstiger: Das macht Ludwigshafen für viele Käufer interessant, die in der Metropolregion arbeiten und mehr Wohnfläche suchen.",
  cards=[("Ruhige Wohnlagen","Oggersheim, Ruchheim, Maudach, Gartenstadt und Rheingönheim sind bei Familien gefragt, die ein Haus mit Garten suchen."),
         ("Der Norden","Friesenheim, Oppau, Edigheim und Pfingstweide liegen nah an der BASF, dem größten Arbeitgeber der Stadt. Viele Käufer arbeiten direkt dort und schätzen kurze Wege."),
         ("Mitte und Süd","Hier geht es vor allem um Wohnungen. Bahnhofsnähe, S-Bahn und Zustand des Hauses entscheiden mit über den Preis."),
         ("Der Vergleich mit Mannheim","Käufer schauen oft auf beide Rheinseiten. Ich zeige, warum deine Immobilie in Ludwigshafen den Vergleich nicht scheuen muss.")]),
"alzey": dict(ort="Alzey", land=RLP, label="Alzey im Detail",
  h2="Alzey: <em>Kreisstadt mitten in Rheinhessen.</em>",
  lead="Als Kreisstadt des Landkreises Alzey-Worms verbindet Alzey Kleinstadtleben mit sehr guter Anbindung: Am Autobahnkreuz Alzey treffen sich A61 und A63.",
  cards=[("Kernstadt","Altstadt, Schulen, Einkaufen und Ärzte in kurzer Distanz. Wohnungen und Stadthäuser sind hier bei Paaren und Senioren gefragt."),
         ("Die Stadtteile","Dautenheim, Heimersheim, Schafhausen und Weinheim sind dörflich geprägt. Häuser mit Grundstück und Weinbau-Umfeld sprechen eine eigene Käufergruppe an."),
         ("Pendler Richtung Mainz und Worms","Viele Käufer arbeiten in Mainz, Worms oder im Rhein-Main-Gebiet und suchen bezahlbaren Wohnraum mit guter Verkehrsanbindung."),
         ("Hofreiten und ältere Häuser","Hofreiten sind typisch für Rheinhessen. Sie brauchen die richtige Zielgruppe und eine gute Geschichte im Exposé, nicht nur Quadratmeter.")]),
"viernheim": dict(ort="Viernheim", land=HE, label="Viernheim im Detail",
  h2="Viernheim: <em>Hessen, aber direkt an Mannheim.</em>",
  lead="Viernheim liegt im hessischen Kreis Bergstraße und grenzt direkt an Mannheim. Für viele Käufer ist das die ruhigere Alternative zur Großstadt, mit kurzen Wegen über die A6 und die A659.",
  cards=[("Gefragt bei Familien","Einfamilien- und Reihenhäuser sind hier besonders gesucht, oft von Familien, die in Mannheim oder Weinheim arbeiten."),
         ("Gute Versorgung","Mit dem Rhein-Neckar-Zentrum und der Innenstadt sind Einkaufen und Alltag schnell erledigt. Das zählt für Käufer mehr, als viele Eigentümer denken."),
         ("Anderes Bundesland, andere Kosten","Weil Viernheim in Hessen liegt, zahlen Käufer 6,0 Prozent Grunderwerbsteuer statt 5,0 Prozent wie in Mannheim. Das fließt in ihre Kalkulation ein, und ich berücksichtige es beim Preis."),
         ("Der Vergleich mit Mannheim","Käufer vergleichen Viernheim fast immer mit den Mannheimer Stadtteilen nebenan. Ich arbeite heraus, was für deine Immobilie hier spricht.")]),
}

def section(d):
    land, satz, boris = d["land"]
    cards = "".join(f'<div class="card"><b>{t}</b><p>{p}</p></div>' for t, p in d["cards"])
    return (f'\n<section class="sec" id="lage" style="padding-top:0"><div class="wrap">\n'
            f'  <div class="label sr">{d["label"]}</div>\n'
            f'  <h2 class="sr" style="--i:1">{d["h2"]}</h2>\n'
            f'  <p class="lead sr" style="--i:2">{d["lead"]}</p>\n'
            f'  <div class="cards sr" style="--i:3">{cards}</div>\n'
            f'  <p class="lead sr" style="--i:4;font-size:15px;margin-top:22px"><strong>Gut zu wissen für {d["ort"]}:</strong> '
            f'In {land} beträgt die Grunderwerbsteuer {satz} Prozent, die in der Regel der Käufer zahlt. '
            f'Die amtlichen Bodenrichtwerte findest du kostenlos bei {boris}.</p>\n'
            f'</div></section>\n')

def faq(d):
    land, satz, boris = d["land"]
    return (f'<details><summary>Was sollte ich zu Grunderwerbsteuer und Bodenrichtwert in {d["ort"]} wissen?</summary>'
            f'<p>{d["ort"]} liegt in {land}. Dort beträgt die Grunderwerbsteuer {satz} Prozent des Kaufpreises, die in der Regel der Käufer trägt. '
            f'Den Bodenrichtwert deines Grundstücks kannst du kostenlos bei {boris} nachsehen. Er ist ein guter Startpunkt, ersetzt aber keine Bewertung des Gebäudes.</p></details>')

core_files = {f"immobilie-verkaufen-{c}.html" for c in CORE}
link_li = re.compile(r'<li><a href="(immobilie-verkaufen-[a-z-]+\.html)">[^<]*</a></li>')
link_a = re.compile(r'<a href="(immobilie-verkaufen-[a-z-]+\.html)">[^<]*</a>')
keep = lambda m: m.group(0) if m.group(1) in core_files else ""

for f in sorted(root.glob("*.html")):
    s = f.read_text(encoding="utf-8"); o = s
    s = link_li.sub(keep, s)
    s = link_a.sub(keep, s)
    name = f.name
    if name.startswith("immobilie-verkaufen-") and name not in core_files:
        s = re.sub(r'<meta name="robots" content="[^"]*">', '<meta name="robots" content="noindex,follow">', s, count=1)
    if name in core_files:
        d = C[name[len("immobilie-verkaufen-"):-5]]
        if 'id="lage"' not in s:
            anchor = "\n<style>\n.rvb"
            assert s.count(anchor) == 1, name
            s = s.replace(anchor, section(d) + anchor, 1)
            i = s.index('class="faq'); j = s.index("</details></div>", i) + len("</details>")
            s = s[:j] + faq(d) + s[j:]
    if s != o:
        f.write_text(s, encoding="utf-8"); print("geändert:", name)

sm = root / "sitemap.xml"; x = sm.read_text(encoding="utf-8")
x = re.sub(r'\s*<url>\s*<loc>[^<]*/(immobilie-verkaufen-[a-z-]+\.html)</loc>.*?</url>',
           lambda m: m.group(0) if m.group(1) in core_files else "", x, flags=re.S)
sm.write_text(x, encoding="utf-8")
print("sitemap URLs:", x.count("<loc>"))
