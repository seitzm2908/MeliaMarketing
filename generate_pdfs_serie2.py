#!/usr/bin/env python3
"""
PDF-Generator fuer alle 16 Serie-2-Videos.
Ausfuehren: python3 generate_pdfs_serie2.py
Ausgabe:    ./pdfs_serie2/V01_Serie2_Produktionsblatt.pdf ... V16_...pdf
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white

DUNKEL    = HexColor("#1A1A2E")
GOLD      = HexColor("#C9A84C")
GRAU      = HexColor("#666666")
HELLGRAU  = HexColor("#DDDDDD")

VIDEOS = [
    {
        "num": "V01",
        "titel": "Die Frage, die sich jeder Profi stellen sollte",
        "hook": "Wie viel Prozent deiner Provision behältst du wirklich?",
        "einsprech": (
            "Ich habe diese Frage lange nicht gestellt. Bis ich gemerkt habe, "
            "dass ich jeden Monat einen erheblichen Teil meiner Arbeit einfach "
            "abgebe. Heute nicht mehr."
        ),
        "caption": [
            "Als Immobilienprofi weißt du, was ein Abschluss wert ist.",
            " ",
            "Die Frage ist: Wie viel davon landet wirklich bei dir?",
            " ",
            "Bei iad behalten unsere Berater 69 % der Provision — einer der "
            "höchsten Sätze am Markt. Dazu ein internationales Netzwerk mit "
            "über 20.000 Beratern und 525 Mio. € Jahresumsatz im Rücken.",
            " ",
            "Kein Bürozwang. Kein Dach, das dir 30–40 % abnimmt.",
            " ",
            "Wenn dich das interessiert: Kein Pitch — ein ehrliches Gespräch.",
        ],
        "cta": "Schreib mir PROVISION in die DMs.",
        "keyword": "PROVISION",
    },
    {
        "num": "V02",
        "titel": "Was 20.000 Berater fuer dich bedeuten",
        "hook": "Stell dir vor, du hast 20.000 Kollegen — weltweit.",
        "einsprech": (
            "Nicht Konkurrenten. Kollegen. Ein Netzwerk, das für dich arbeitet "
            "— bei Referenzen, bei grenzüberschreitenden Deals, bei Wissen. "
            "Das ist iad."
        ),
        "caption": [
            "Allein als Makler zu arbeiten bedeutet: alle Verbindungen selbst aufbauen.",
            " ",
            "Bei iad gehörst du vom ersten Tag an einem internationalen Netzwerk "
            "mit über 20.000 Beratern an. In Deutschland, Frankreich, Spanien, "
            "Portugal, Belgien und weiteren Ländern.",
            " ",
            "Das bedeutet: Internationale Kunden. Grenzüberschreitende Deals. "
            "Und Wissen, das kein Einzelkämpfer je allein aufbauen könnte.",
            " ",
            "Wenn du erfahrener Makler bist und weißt, was ein starkes "
            "Netzwerk wert ist:",
        ],
        "cta": "Schreib mir NETZWERK in die DMs.",
        "keyword": "NETZWERK",
    },
    {
        "num": "V03",
        "titel": "Warum erfahrene Makler wechseln",
        "hook": "Ich frage jeden erfahrenen Makler, der zu mir kommt, dasselbe.",
        "einsprech": (
            "Was hat dich aufgehalten, früher zu wechseln? Die Antwort ist fast "
            "immer gleich: Ich wusste nicht, dass es diese Alternative gibt."
        ),
        "caption": [
            "Die meisten Makler, die zu iad wechseln, sagen danach dasselbe:",
            " ",
            "\"Hätte ich das früher gewusst.\"",
            " ",
            "69 % Provision. Kein Bürozwang. Internationales Netzwerk. "
            "Volle unternehmerische Freiheit — mit einem der größten "
            "Immobilienunternehmen weltweit im Rücken.",
            " ",
            "Du bringst die Erfahrung. Wir bringen die Struktur, die dich weiterbringt.",
            " ",
            "Kein Druck — aber ein offenes Gespräch.",
        ],
        "cta": "Schreib mir WECHSEL in die DMs.",
        "keyword": "WECHSEL",
    },
    {
        "num": "V04",
        "titel": "525 Millionen Euro — was das fuer dich bedeutet",
        "hook": "525 Millionen Euro Jahresumsatz. Was hat das mit dir zu tun?",
        "einsprech": (
            "Stabilität. Glaubwürdigkeit. Und ein Unternehmen, das wächst — "
            "nicht trotz der Marktlage, sondern wegen seiner Struktur. "
            "Daran kannst du teilhaben."
        ),
        "caption": [
            "iad ist eines der größten Immobilienunternehmen weltweit.",
            " ",
            "525 Mio. € Kartenumsatz jährlich. Über 20.000 Berater. "
            "Mehrere europäische Märkte.",
            " ",
            "Das bedeutet für dich als Berater: Du arbeitest selbstständig "
            "— aber nie allein. Mit einer Marke im Rücken, der Eigentümer "
            "und Käufer vertrauen.",
            " ",
            "Wenn du weißt, was solide Unternehmensstruktur im Vertrieb wert ist:",
        ],
        "cta": "Schreib mir IAD in die DMs.",
        "keyword": "IAD",
    },
    {
        "num": "V05",
        "titel": "Wie Innovation im Immobilienmarkt wirklich aussieht",
        "hook": "Die meisten Immobilienunternehmen reden von Innovation. Wir leben sie.",
        "einsprech": (
            "Digitale Tools, KI-gestützte Prozesse, internationale Plattform "
            "— das sind keine Versprechen bei iad. Das ist der Alltag. Und "
            "das gibt dir als Berater einen echten Vorsprung."
        ),
        "caption": [
            "In einer Branche, die sich gerade stärker verändert als je zuvor, "
            "entscheidet die Infrastruktur, mit der du arbeitest.",
            " ",
            "iad setzt konsequent auf digitale Prozesse, KI-gestützte Tools "
            "und internationale Vernetzung — damit du als Berater weniger Zeit "
            "mit Administration und mehr Zeit mit echten Mandaten verbringst.",
            " ",
            "Du bist Profi. Dann arbeit auch mit den Tools eines Profis.",
        ],
        "cta": "Schreib mir INNOVATION in die DMs.",
        "keyword": "INNOVATION",
    },
    {
        "num": "V06",
        "titel": "Freiheit und Struktur — kein Widerspruch",
        "hook": "Selbstständig. Aber nicht allein.",
        "einsprech": (
            "Du arbeitest eigenverantwortlich — mit deinen Kunden, in deiner "
            "Region, nach deinen Regeln. Aber mit einem globalen Unternehmen "
            "im Rücken. Das ist der Kern von iad."
        ),
        "caption": [
            "Die meisten Makler müssen wählen: Freiheit oder Struktur.",
            " ",
            "Bei iad brauchst du das nicht.",
            " ",
            "Du bist vollständig selbstständig — kein Bürozwang, keine fixen "
            "Arbeitszeiten, keine fremden Vorgaben. Gleichzeitig arbeitest du "
            "mit der Infrastruktur, dem Netzwerk und der Marke eines der "
            "größten Immobilienunternehmen weltweit.",
            " ",
            "69 % Provision. Vollständige Freiheit. Globaler Rückhalt.",
            " ",
            "Wir reden ehrlich darüber, ob das zu dir passt.",
        ],
        "cta": "Schreib mir FREIHEIT in die DMs.",
        "keyword": "FREIHEIT",
    },
    {
        "num": "V07",
        "titel": "Was passiert, wenn du dein eigenes Team aufbaust",
        "hook": "Was wäre, wenn dein Einkommen nicht nur von deiner eigenen Arbeit abhängt?",
        "einsprech": (
            "Bei iad hast du die Möglichkeit, dein eigenes Team aufzubauen "
            "und an deren Umsatz beteiligt zu sein. Das ist die zweite "
            "Einkommenssäule, die die meisten Makler nie haben."
        ),
        "caption": [
            "Als Einzelmakler hängt alles an dir.",
            " ",
            "Bei iad hast du zusätzlich die Möglichkeit, andere Berater zu "
            "entwickeln und aufzunehmen — und an deren Umsatz beteiligt zu sein.",
            " ",
            "Das ist kein MLM. Das ist ein legitimes Partnerschaftsmodell, "
            "das dir langfristig eine zweite Einkommenssäule aufbaut — "
            "neben deinen eigenen Abschlüssen.",
            " ",
            "Wenn du bereits daran denkst, zu skalieren:",
        ],
        "cta": "Schreib mir TEAM in die DMs.",
        "keyword": "TEAM",
    },
    {
        "num": "V08",
        "titel": "Mein erstes Gespräch mit einem Makler, der gewechselt hat",
        "hook": "Er hat 12 Jahre bei einem klassischen Immobilienunternehmen gearbeitet.",
        "einsprech": (
            "Als er mir gesagt hat, wie viel Provision er vorher behalten hat, "
            "war ich ehrlich überrascht. Nicht, weil es wenig war. Sondern "
            "weil er es für normal gehalten hatte."
        ),
        "caption": [
            "Viele Makler akzeptieren Konditionen, weil sie nichts anderes kennen.",
            " ",
            "Dieser Berater hat 12 Jahre lang einen erheblichen Teil seiner "
            "Provision abgegeben — und erst bei unserem Gespräch gemerkt, "
            "wie viel das über die Jahre bedeutet hat.",
            " ",
            "Heute ist er bei iad. Mit 69 % Provision, vollem Netzwerkzugang "
            "und der Freiheit, sein Business selbst zu gestalten.",
            " ",
            "Was gibst du gerade jeden Monat ab?",
        ],
        "cta": "Schreib mir PROVISION in die DMs.",
        "keyword": "PROVISION",
    },
    {
        "num": "V09",
        "titel": "International arbeiten als Makler — wie das geht",
        "hook": "Dein nächster Käufer kommt vielleicht aus Frankreich.",
        "einsprech": (
            "Mit iad bist du von Tag eins Teil eines internationalen Netzwerks. "
            "Grenzüberschreitende Deals, internationale Käufer, europäische "
            "Referenzen — das ist kein Versprechen, das ist Realität."
        ),
        "caption": [
            "Wer nur lokal denkt, lässt Potenzial liegen.",
            " ",
            "iad ist in mehreren europäischen Ländern aktiv — Deutschland, "
            "Frankreich, Spanien, Portugal, Belgien und weiteren Märkten.",
            " ",
            "Als Berater profitierst du vom internationalen Netzwerk, von "
            "Referenzen aus anderen Ländern und von internationalen Käufern.",
            " ",
            "Für erfahrene Makler mit dem richtigen Netzwerk ist das ein "
            "echter Wettbewerbsvorteil.",
        ],
        "cta": "Schreib mir INTERNATIONAL in die DMs.",
        "keyword": "INTERNATIONAL",
    },
    {
        "num": "V10",
        "titel": "Das Gespräch, das alles veraendert",
        "hook": "Ich führe dieses Gespräch gerne. Aber nur mit den Richtigen.",
        "einsprech": (
            "Ich suche keine Einsteiger. Ich suche erfahrene Makler, die "
            "wissen, was sie können — und die bereit sind, mit den richtigen "
            "Rahmenbedingungen das nächste Level zu erreichen."
        ),
        "caption": [
            "Ich bin Immobilienberater bei iad — einem der größten "
            "Immobilienunternehmen weltweit.",
            " ",
            "Ich baue gerade mein Team mit erfahrenen Maklern auf, die mehr "
            "aus ihrer Arbeit machen wollen:",
            " ",
            "69 % Provision — einer der höchsten Sätze am Markt",
            "Internationales Netzwerk mit 20.000+ Beratern",
            "525 Mio. € Jahresumsatz — Stabilität und Glaubwürdigkeit",
            "Volle Selbstständigkeit — kein Bürozwang, keine Vorgaben",
            "Optional: eigenes Team aufbauen und skalieren",
            " ",
            "Kein Standardpitch. Ein offenes Gespräch darüber, ob das zu "
            "dir und deiner Situation passt.",
            " ",
            "Ich melde mich persönlich. → selbstständig-mit-plan.de",
        ],
        "cta": "Schreib mir PROFI in die DMs.",
        "keyword": "PROFI",
    },
    {
        "num": "V11",
        "titel": "Dein erster Tag bei iad — was wirklich passiert",
        "hook": "Dein erster Tag bei iad. Was erwartet dich wirklich?",
        "einsprech": (
            "Kein Sprung ins kalte Wasser. Persönlicher Mentor, alle Tools "
            "direkt verfügbar, strukturiertes Onboarding. Du bist von Tag "
            "eins produktiv — nicht allein."
        ),
        "caption": [
            "Viele Makler fragen mich: Wie läuft der Wechsel zu iad ab?",
            " ",
            "Hier die ehrliche Antwort:",
            " ",
            "Du bekommst einen persönlichen Mentor — jemanden, der selbst "
            "den Weg gegangen ist. Alle digitalen Tools sind von Tag eins "
            "zugänglich. Ein strukturierter Onboarding-Prozess führt dich "
            "durch die ersten Wochen.",
            " ",
            "Kein \"Sink or swim\". Kein Alleingang.",
            " ",
            "Wenn du verstehen willst, wie ein Einstieg konkret aussieht:",
        ],
        "cta": "Schreib mir START in die DMs.",
        "keyword": "START",
    },
    {
        "num": "V12",
        "titel": "Nicht Vorgesetzter. Mentor.",
        "hook": "Bei iad hast du vom ersten Tag einen persönlichen Mentor.",
        "einsprech": (
            "Ich begleite neue Berater persönlich — nicht mit Frontaltraining, "
            "sondern mit echtem Erfahrungstransfer. Weil ich selbst genau "
            "diesen Weg gegangen bin."
        ),
        "caption": [
            "Bei klassischen Immobilienunternehmen gibt es Vorgesetzte.",
            " ",
            "Bei iad gibt es Mentoren.",
            " ",
            "Ich begleite erfahrene Makler, die zu meinem Team stoßen, "
            "persönlich. Kein Standard-Training — echter Erfahrungsaustausch, "
            "echte Gespräche, echte Unterstützung.",
            " ",
            "Denn ich kenne die Fragen, die du hast. Ich hatte sie selbst.",
            " ",
            "Wenn du wissen willst, wie das konkret aussieht:",
        ],
        "cta": "Schreib mir MENTOR in die DMs.",
        "keyword": "MENTOR",
    },
    {
        "num": "V13",
        "titel": "Ich kenne deinen Einwand",
        "hook": "Klingt zu gut, um wahr zu sein — oder?",
        "einsprech": (
            "Das höre ich oft. Deshalb kein Versprechen, kein Pitch, kein "
            "Druck. Nur ein offenes Gespräch — mit Zahlen, Fakten und echten "
            "Antworten auf echte Fragen."
        ),
        "caption": [
            "Ich verstehe den Gedanken.",
            " ",
            "69 % Provision. 20.000 Berater. 525 Mio. € Umsatz. "
            "Klingt nach einem zu guten Pitch.",
            " ",
            "Deshalb sage ich: Ruf mich einfach an. Oder schreib mir. "
            "Ich beantworte jede Frage, die du hast — offen und ohne Druck.",
            " ",
            "Wer nichts zu verbergen hat, führt das Gespräch.",
        ],
        "cta": "Schreib mir FRAGE in die DMs.",
        "keyword": "FRAGE",
    },
    {
        "num": "V14",
        "titel": "Deine Zeit gehört dir",
        "hook": "Wann hast du zum letzten Mal selbst entschieden, wann du arbeitest?",
        "einsprech": (
            "Kein Bürozwang. Keine fixen Arbeitszeiten. Du entscheidest, "
            "wann, wo und wie du arbeitest. Das ist nicht Theorie "
            "— das ist mein Alltag."
        ),
        "caption": [
            "Als angestellter oder gebundener Makler kennst du das:",
            " ",
            "Büropflicht. Kernzeiten. Termine nach fremden Vorgaben.",
            " ",
            "Bei iad gibt es das nicht. Kein Bürozwang — du arbeitest, wo "
            "du willst. Keine Kernzeiten — du strukturierst deinen Tag selbst. "
            "Keine Vorgaben — außer den Ergebnissen, die du dir selbst setzt.",
            " ",
            "Das ist vollständige unternehmerische Freiheit. Mit dem globalen "
            "Netzwerk von iad als Rückhalt.",
        ],
        "cta": "Schreib mir FREIZEIT in die DMs.",
        "keyword": "FREIZEIT",
    },
    {
        "num": "V15",
        "titel": "Dein Name. Deine Marke. Dein Business.",
        "hook": "Du hast jahrelang eine Marke aufgebaut. Deine eigene.",
        "einsprech": (
            "Bei iad gehört dein Name dir. Deine Kunden, dein Netzwerk, "
            "dein Ruf — das nimmst du mit. Und bekommst den Rückenwind "
            "eines globalen Unternehmens dazu."
        ),
        "caption": [
            "Als erfahrener Makler hast du etwas aufgebaut, das man nicht "
            "kaufen kann: Vertrauen. Reputation. Ein Netzwerk.",
            " ",
            "Bei iad gibst du das nicht auf.",
            " ",
            "Du arbeitest weiterhin unter deinem eigenen Namen. Deine "
            "Kundenbeziehungen gehören dir. Dein Netzwerk bleibt deins.",
            " ",
            "Was hinzukommt: die Marke, Infrastruktur und globale Reichweite "
            "von iad — eines der größten Immobilienunternehmen weltweit.",
            " ",
            "Mehr, nicht weniger.",
        ],
        "cta": "Schreib mir MARKE in die DMs.",
        "keyword": "MARKE",
    },
    {
        "num": "V17",
        "titel": "Was dich dein aktuelles Modell wirklich kostet",
        "hook": "Rechne mal kurz mit mir.",
        "einsprech": (
            "5 Abschlüsse im Monat. 40 % Provisionsabgabe. Auf 10 Jahre gerechnet "
            "— weißt du, was diese Zahl bedeutet? Die meisten Makler haben sie "
            "noch nie ausgerechnet."
        ),
        "caption": [
            "Mach diese Rechnung einmal.",
            " ",
            "5 Abschlüsse im Monat. Durchschnittliche Provision pro Deal. "
            "Wie viel gibst du davon ab — jeden Monat, jedes Jahr?",
            " ",
            "Bei klassischen Modellen sind das oft 30–40 %, die du nicht siehst. "
            "Über 10 Jahre ist das eine Summe, bei der die meisten Makler still werden.",
            " ",
            "Bei iad behältst du 69 % — einer der höchsten Sätze am Markt.",
            " ",
            "Ich zeige dir, was die Zahl bei dir konkret bedeutet.",
        ],
        "cta": "Schreib mir RECHNER in die DMs.",
        "keyword": "RECHNER",
    },
    {
        "num": "V18",
        "titel": "So sieht mein Alltag als iad-Berater wirklich aus",
        "hook": "7:30 Uhr. Homeoffice. Kein Chef. Kein Büro. Kein Muss.",
        "einsprech": (
            "Morgens Akquise nach eigenem Rhythmus, mittags Besichtigung, abends "
            "Abschluss. Das ist kein Lifestyle-Marketing. Das ist mein Donnerstag "
            "— und der von jedem iad-Berater."
        ),
        "caption": [
            "Kein Standardtag. Kein Bürozwang. Keine Rechenschaft.",
            " ",
            "Das ist nicht das Versprechen von iad — das ist die Realität, die "
            "ich und andere Berater täglich leben.",
            " ",
            "Ich entscheide, wann ich arbeite, wo ich Termine mache und welche "
            "Kunden ich betreue. Volle unternehmerische Verantwortung — mit dem "
            "Netzwerk und der Infrastruktur eines der größten Immobilienunternehmen weltweit.",
            " ",
            "Willst du wissen, wie dein Alltag aussehen könnte?",
        ],
        "cta": "Schreib mir ALLTAG in die DMs.",
        "keyword": "ALLTAG",
    },
    {
        "num": "V19",
        "titel": "Was mir ein Makler nach 3 Monaten geschrieben hat",
        "hook": "Er hat mir nach 3 Monaten eine Nachricht geschickt.",
        "einsprech": (
            "Nicht um sich zu bedanken. Sondern weil er gemerkt hat, dass er in "
            "drei Monaten mehr behalten hat als im ganzen letzten Halbjahr. "
            "Das hatte er selbst nicht erwartet."
        ),
        "caption": [
            "Ich erinnere mich genau an diese Nachricht.",
            " ",
            "Er war 9 Jahre bei einem klassischen Immobilienunternehmen. Hatte "
            "Erfahrung, Netzwerk, gute Abschlüsse — aber nie das Gefühl, wirklich "
            "für sich zu arbeiten.",
            " ",
            "Nach 3 Monaten bei iad: mehr Provision behalten als im gesamten "
            "letzten Halbjahr. Gleiche Abschlüsse. Andere Konditionen.",
            " ",
            "Das ist kein Einzelfall.",
            " ",
            "Ich erzähle dir mehr.",
        ],
        "cta": "Schreib mir ERFAHRUNG in die DMs.",
        "keyword": "ERFAHRUNG",
    },
    {
        "num": "V20",
        "titel": "Als Einzelmakler arbeitest du, bis du aufhörst",
        "hook": "Als Einzelmakler arbeitest du, bis du aufhörst zu arbeiten.",
        "einsprech": (
            "Kein Urlaub ohne Umsatzverlust. Kein Ausfall ohne Folgen. Bei iad "
            "kannst du ein Team aufbauen, das auch dann Abschlüsse macht, wenn "
            "du nicht vor Ort bist. Das ist der Unterschied."
        ),
        "caption": [
            "Das ist die Wahrheit, über die viele Makler nicht sprechen wollen.",
            " ",
            "Als Einzelkämpfer hängt alles an dir — dein Umsatz, deine Kunden, "
            "deine Abschlüsse. Fällst du aus, fällt alles aus.",
            " ",
            "Bei iad hast du die Möglichkeit, ein eigenes Team aufzubauen und "
            "an deren Umsatz beteiligt zu sein. Das ist keine Theorie — das ist "
            "das Modell, das aus Maklern Unternehmer macht.",
            " ",
            "69 % Provision aus eigenen Abschlüssen. Plus Beteiligung am Team. "
            "Das ist skalierbar.",
        ],
        "cta": "Schreib mir SKALIERUNG in die DMs.",
        "keyword": "SKALIERUNG",
    },
    {
        "num": "V21",
        "titel": "Der Unterschied zwischen gut und gut aufgestellt",
        "hook": "Du bist ein guter Makler. Aber arbeitest du auch mit den richtigen Rahmenbedingungen?",
        "einsprech": (
            "Können und Konditionen — beides zählt. Viele exzellente Makler "
            "arbeiten mit Strukturen, die ihre Ergebnisse deckeln. Das ist kein "
            "Versagen. Das ist das falsche System."
        ),
        "caption": [
            "Es gibt Makler, die hervorragend sind — und trotzdem nicht das "
            "rausholen, was sie könnten.",
            " ",
            "Nicht weil sie nicht gut genug arbeiten. Sondern weil die Strukturen, "
            "in denen sie arbeiten, ihr Potenzial begrenzen.",
            " ",
            "69 % Provision statt 40–50 %. Internationales Netzwerk statt "
            "Einzelkämpfer. Eigenes Team statt alles allein.",
            " ",
            "Du bringst das Können. Ich zeige dir das System, das dazu passt.",
        ],
        "cta": "Schreib mir SYSTEM in die DMs.",
        "keyword": "SYSTEM",
    },
    {
        "num": "V22",
        "titel": "Warum jetzt der richtige Zeitpunkt ist",
        "hook": "Der Markt verändert sich. Dein Einstiegsfenster auch.",
        "einsprech": (
            "Makler, die jetzt die Weichen stellen, werden in zwei Jahren mit "
            "aufgebautem Team, stabilem Netzwerk und klarer Positionierung "
            "dastehen. Wer wartet, wartet länger als geplant."
        ),
        "caption": [
            "Es gibt nie den perfekten Zeitpunkt. Aber es gibt bessere und schlechtere.",
            " ",
            "Der Immobilienmarkt ist im Wandel. Digitalisierung, internationale "
            "Käufer, veränderte Käuferprofile — wer jetzt die richtigen Strukturen "
            "aufbaut, ist in zwei Jahren anders aufgestellt als alle, die "
            "abgewartet haben.",
            " ",
            "Bei iad bist du Teil eines der größten Immobilienunternehmen weltweit "
            "— mit 69 % Provision, internationalem Netzwerk und der Möglichkeit, "
            "ein eigenes Team aufzubauen.",
            " ",
            "Der Zeitpunkt ist jetzt. Nicht irgendwann.",
        ],
        "cta": "Schreib mir JETZT in die DMs.",
        "keyword": "JETZT",
    },
    {
        "num": "V23",
        "titel": "Immobilienberuf und Familie — wie das wirklich funktioniert",
        "hook": "Wie machst du das eigentlich — mit Familie?",
        "einsprech": (
            "Ich kenne die Frage. Kein fixer Bürostart, keine Pflichtzeiten, "
            "keine Anwesenheitspflicht. Mein Job passt sich meinem Leben an "
            "— nicht andersherum. Das ist bei iad kein Versprechen, das ist der Alltag."
        ),
        "caption": [
            "Die ehrliche Antwort auf eine Frage, die viele stellen, aber "
            "kaum jemand offen beantwortet.",
            " ",
            "Als iad-Berater gibt es keinen Bürozwang, keine Pflichtzeiten, "
            "keine Anwesenheitspflicht. Du entscheidest, wann du arbeitest "
            "— und wann nicht.",
            " ",
            "Kinderarzttermin am Dienstagvormittag? Schulaufführung am Donnerstag? "
            "Das bestimmst du.",
            " ",
            "Das macht vollständige Selbstständigkeit erst wirklich wertvoll "
            "— nicht die Provision allein.",
            " ",
            "Wenn dich das anspricht:",
        ],
        "cta": "Schreib mir FAMILIE in die DMs.",
        "keyword": "FAMILIE",
    },
    {
        "num": "V24",
        "titel": "Wie kommen deine Leads — oder gehst du jedem hinterher?",
        "hook": "Wie kommen deine Leads zu dir — oder gehst du noch jedem einzeln hinterher?",
        "einsprech": (
            "Bei iad hast du Zugang zu digitalen Tools und KI-gestützten Prozessen, "
            "die dir Akquise-Arbeit abnehmen. Mehr Zeit für echte Gespräche. "
            "Weniger Zeit für manuelle Kaltakquise."
        ),
        "caption": [
            "Viele Makler verbringen einen Großteil ihrer Zeit mit Akquise, "
            "die kaum Ergebnisse bringt.",
            " ",
            "Bei iad hast du Zugang zu einer digitalen Plattform und "
            "KI-gestützten Tools, die Leads generieren, qualifizieren und "
            "vorbereiten — bevor du das erste Gespräch führst.",
            " ",
            "Das bedeutet: Du sprichst mit Menschen, die bereits Interesse haben. "
            "Nicht mit Fremden, die du kalt anrufst.",
            " ",
            "Weniger Reibung. Mehr Abschlüsse.",
            " ",
            "Ich zeige dir, wie das konkret aussieht.",
        ],
        "cta": "Schreib mir LEADS in die DMs.",
        "keyword": "LEADS",
    },
    {
        "num": "V25",
        "titel": "Von Franchise zu iad — was sich wirklich ändert",
        "hook": "Du zahlst Franchisegebühren. Weißt du genau, was du dafür bekommst?",
        "einsprech": (
            "Viele Makler kommen von Franchise-Systemen zu iad. Nicht weil das "
            "System schlecht war — sondern weil sie gemerkt haben, dass sie "
            "dasselbe, oder mehr, für deutlich weniger Kosten bekommen können."
        ),
        "caption": [
            "Franchise-Systeme haben ihren Wert. Aber sie haben auch ihren Preis.",
            " ",
            "Viele erfahrene Makler, die von großen Franchise-Marken zu iad "
            "wechseln, stellen fest: Sie bekommen Netzwerk, Marke, Tools und "
            "Support — ohne die laufenden Franchisegebühren und "
            "Umsatzbeteiligungen nach oben.",
            " ",
            "69 % Provision. Internationales Netzwerk mit 20.000+ Beratern. "
            "Vollständige Selbstständigkeit.",
            " ",
            "Kein Franchise-Vertrag, der dir Vorschriften macht.",
            " ",
            "Wenn du aus einem Franchise-System kommst und wissen willst, "
            "was der Unterschied konkret bedeutet:",
        ],
        "cta": "Schreib mir FRANCHISE in die DMs.",
        "keyword": "FRANCHISE",
    },
    {
        "num": "V26",
        "titel": "Was iad dir an Weiterbildung wirklich mitgibt",
        "hook": "Was bringt dir iad — außer der höheren Provision?",
        "einsprech": (
            "Zugang zu Trainings, internationalen Best Practices, internen "
            "Wissensnetzwerken — und ein Mentor, der selbst aktiver Berater ist. "
            "Das ist Weiterbildung, die echten Unterschied macht. Kein Pflichtprogramm."
        ),
        "caption": [
            "Die Provision ist ein Argument. Aber nicht das einzige.",
            " ",
            "Als iad-Berater hast du Zugang zu einem internationalen "
            "Wissensnetzwerk — Best Practices aus Deutschland, Frankreich, "
            "Spanien, Portugal und weiteren Märkten. Du lernst, was in anderen "
            "Ländern bereits funktioniert, bevor es in deinem Markt ankommt.",
            " ",
            "Dazu kommt ein persönlicher Mentor — kein Trainer, der Kurse abhält, "
            "sondern jemand, der selbst aktiv vermittelt und weiß, wie der Markt "
            "gerade wirklich aussieht.",
            " ",
            "Das ist der Unterschied zwischen Weiterbildung auf dem Papier "
            "und Weiterbildung, die zählt.",
        ],
        "cta": "Schreib mir TRAINING in die DMs.",
        "keyword": "TRAINING",
    },
    {
        "num": "V27",
        "titel": "69 % vs. was du gerade behältst",
        "hook": "69 % Provision. Wie viel behältst du gerade?",
        "einsprech": (
            "Das ist keine Marketing-Aussage. Das sind konkrete Zahlen. "
            "Wenn du bei 50 % bist und 10 Deals im Monat machst, weißt du "
            "was 19 % mehr bedeuten. Ich rechne das gerne mit dir durch."
        ),
        "caption": [
            "Mach die Rechnung.",
            " ",
            "Angenommen du machst 10 Deals im Monat. Durchschnittliche Provision "
            "pro Deal: 8.000 EUR. Du behältst aktuell 50 %.",
            " ",
            "Das sind 40.000 EUR monatlich bei dir.",
            " ",
            "Bei iad mit 69 %: 55.200 EUR — also 15.200 EUR mehr im Monat. "
            "Aus denselben Abschlüssen.",
            " ",
            "Das ist kein Versprechen. Das ist Mathematik.",
            " ",
            "Ich rechne das mit deinen echten Zahlen durch.",
        ],
        "cta": "Schreib mir VERGLEICH in die DMs.",
        "keyword": "VERGLEICH",
    },
    {
        "num": "V28",
        "titel": "Was ich Maklerinnen sage, die fragen",
        "hook": "Ich bekomme zunehmend Anfragen von Maklerinnen. Das sind ihre Fragen.",
        "einsprech": (
            "Wie vereinbare ich Kunden mit Familie? Wie baue ich als Frau in "
            "dieser Branche Vertrauen auf? Und was bedeutet vollständige "
            "Selbstständigkeit konkret? Diese Gespräche führe ich gerne "
            "— offen und ohne Floskeln."
        ),
        "caption": [
            "In den letzten Monaten kommen zunehmend Anfragen von erfahrenen Maklerinnen.",
            " ",
            "Ihre Fragen unterscheiden sich manchmal — aber die Konditionen nicht.",
            " ",
            "69 % Provision. Vollständige Selbstständigkeit. Internationales "
            "Netzwerk. Eigenes Team aufbauen. Das gilt für jeden Berater bei iad.",
            " ",
            "Was ich in diesen Gesprächen erlebe: Maklerinnen mit Erfahrung "
            "wissen genau, was sie können. Sie brauchen keine Überzeugungsarbeit "
            "— sie brauchen die richtigen Rahmenbedingungen.",
            " ",
            "Wenn du diese Fragen hast:",
        ],
        "cta": "Schreib mir MAKLERIN in die DMs.",
        "keyword": "MAKLERIN",
    },
    {
        "num": "V16",
        "titel": "Was willst du in 3 Jahren anders machen?",
        "hook": "Was willst du in 3 Jahren anders machen als heute?",
        "einsprech": (
            "Die Makler, die heute wechseln, sind in 3 Jahren mit eigenem "
            "Team, stabiler Provision und internationalem Netzwerk aufgestellt. "
            "Der richtige Zeitpunkt ist jetzt — nicht irgendwann."
        ),
        "caption": [
            "In 3 Jahren wirst du heute eine Entscheidung getroffen haben.",
            " ",
            "Die Makler, die jetzt zu iad wechseln, bauen gerade auf:",
            " ",
            "Eigenes Team mit Umsatzbeteiligung",
            "69 % Provision — stabil und planbar",
            "Internationales Netzwerk aus 20.000+ Beratern",
            "Vollständige unternehmerische Freiheit",
            " ",
            "Oder du machst in 3 Jahren genau das, was du heute machst.",
            " ",
            "Ich zeige dir, wie der Weg konkret aussieht.",
        ],
        "cta": "Schreib mir ZUKUNFT in die DMs.",
        "keyword": "ZUKUNFT",
    },
]


def make_badge(label):
    cell = Paragraph(label, ParagraphStyle("badge", fontName="Helvetica-Bold",
                     fontSize=8, textColor=white, leading=10))
    t = Table([[cell]], colWidths=[4.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DUNKEL),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def build_pdf(video, out_dir):
    filename = f"{video['num']}_Serie2_Produktionsblatt.pdf"
    path = os.path.join(out_dir, filename)

    doc = SimpleDocTemplate(path, pagesize=A4,
                            rightMargin=2.5*cm, leftMargin=2.5*cm,
                            topMargin=2.5*cm, bottomMargin=2.5*cm)

    s_meta   = ParagraphStyle("meta",   fontName="Helvetica",       fontSize=9,  textColor=GRAU,   leading=12)
    s_num    = ParagraphStyle("num",    fontName="Helvetica-Bold",  fontSize=22, textColor=DUNKEL, leading=26)
    s_titel  = ParagraphStyle("titel",  fontName="Helvetica",       fontSize=12, textColor=GRAU,   leading=16)
    s_hook   = ParagraphStyle("hook",   fontName="Helvetica-BoldOblique", fontSize=14, textColor=DUNKEL, leading=21)
    s_note   = ParagraphStyle("note",   fontName="Helvetica",       fontSize=8,  textColor=GRAU,   leading=11)
    s_body   = ParagraphStyle("body",   fontName="Helvetica",       fontSize=12, textColor=DUNKEL, leading=19)
    s_cta    = ParagraphStyle("cta",    fontName="Helvetica-Bold",  fontSize=12, textColor=GOLD,   leading=19)
    s_footer = ParagraphStyle("footer", fontName="Helvetica",       fontSize=8,  textColor=GRAU,   leading=11)
    s_kw     = ParagraphStyle("kw",     fontName="Helvetica-Bold",  fontSize=9,  textColor=DUNKEL, leading=12)

    story = []

    story.append(Paragraph("SERIE 2 — Vom Immobilienprofi zum Immobilienprofi", s_meta))
    story.append(Paragraph(f"VIDEO {video['num'][1:]}", s_num))
    story.append(Paragraph(video["titel"], s_titel))
    story.append(Spacer(1, 0.35*cm))
    story.append(HRFlowable(width="100%", thickness=2, color=GOLD, spaceAfter=0.5*cm))

    # HOOK
    story.append(make_badge("HOOK"))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(f"„{video['hook']}“", s_hook))
    story.append(Spacer(1, 0.1*cm))
    story.append(Paragraph("Text-Overlay · Frame 1 · BOLD WEISS · groß", s_note))
    story.append(Spacer(1, 0.45*cm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=HELLGRAU, spaceAfter=0.45*cm))

    # EINSPRECHTEXT
    story.append(make_badge("EINSPRECHTEXT (ca. 10 Sek.)"))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(video["einsprech"], s_body))
    story.append(Spacer(1, 0.45*cm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=HELLGRAU, spaceAfter=0.45*cm))

    # CAPTION
    story.append(make_badge("CAPTION"))
    story.append(Spacer(1, 0.2*cm))
    for line in video["caption"]:
        story.append(Paragraph(line, s_body))
    story.append(Spacer(1, 0.15*cm))
    story.append(Paragraph(video["cta"], s_cta))

    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width="100%", thickness=2, color=GOLD, spaceAfter=0.35*cm))
    story.append(Paragraph(
        f"Markus Seitz Immobilien iad · Serie 2 · {video['num']} · KI generiert", s_footer))
    story.append(Paragraph(f"DM-Keyword: {video['keyword']}", s_kw))

    doc.build(story)
    return path


if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "pdfs_serie2")
    os.makedirs(out_dir, exist_ok=True)

    for v in VIDEOS:
        path = build_pdf(v, out_dir)
        print(f"  Erstellt: {path}")

    print(f"\nFertig! Alle {len(VIDEOS)} PDFs liegen in: {out_dir}/")
