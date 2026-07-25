#!/bin/bash

API_KEY="sk_29721598d00eb2fa4e9191416103825c15a7d848af8c2564"
VOICE_ID="ttwV3vM4gSmeC9ZeknPc"
MODEL="eleven_multilingual_v2"
OUTPUT_DIR="./audio_voiceovers_serie2"

mkdir -p "$OUTPUT_DIR"

declare -A TEXTS
TEXTS[V01]="Ich habe diese Frage lange nicht gestellt. Bis ich gemerkt habe, dass ich jeden Monat einen erheblichen Teil meiner Arbeit einfach abgebe. Heute nicht mehr."
TEXTS[V02]="Nicht Konkurrenten. Kollegen. Ein Netzwerk, das für dich arbeitet — bei Referenzen, bei grenzüberschreitenden Deals, bei Wissen. Das ist iad."
TEXTS[V03]="Was hat dich aufgehalten, früher zu wechseln? Die Antwort ist fast immer gleich: Ich wusste nicht, dass es diese Alternative gibt."
TEXTS[V04]="Stabilität. Glaubwürdigkeit. Und ein Unternehmen, das wächst — nicht trotz der Marktlage, sondern wegen seiner Struktur. Daran kannst du teilhaben."
TEXTS[V05]="Digitale Tools, KI-gestützte Prozesse, internationale Plattform — das sind keine Versprechen bei iad. Das ist der Alltag. Und das gibt dir als Berater einen echten Vorsprung."
TEXTS[V06]="Du arbeitest eigenverantwortlich — mit deinen Kunden, in deiner Region, nach deinen Regeln. Aber mit einem globalen Unternehmen im Rücken. Das ist der Kern von iad."
TEXTS[V07]="Bei iad hast du die Möglichkeit, dein eigenes Team aufzubauen und an deren Umsatz beteiligt zu sein. Das ist die zweite Einkommenssäule, die die meisten Makler nie haben."
TEXTS[V08]="Als er mir gesagt hat, wie viel Provision er vorher behalten hat, war ich ehrlich überrascht. Nicht, weil es wenig war. Sondern weil er es für normal gehalten hatte."
TEXTS[V09]="Mit iad bist du von Tag eins Teil eines internationalen Netzwerks. Grenzüberschreitende Deals, internationale Käufer, europäische Referenzen — das ist Realität."
TEXTS[V10]="Ich suche keine Einsteiger. Ich suche erfahrene Makler, die wissen, was sie können — und die bereit sind, mit den richtigen Rahmenbedingungen das nächste Level zu erreichen."
TEXTS[V11]="Kein Sprung ins kalte Wasser. Persönlicher Mentor, alle Tools direkt verfügbar, strukturiertes Onboarding. Du bist von Tag eins produktiv — nicht allein."
TEXTS[V12]="Ich begleite neue Berater persönlich — nicht mit Frontaltraining, sondern mit echtem Erfahrungstransfer. Weil ich selbst genau diesen Weg gegangen bin."
TEXTS[V13]="Das höre ich oft. Deshalb kein Versprechen, kein Pitch, kein Druck. Nur ein offenes Gespräch — mit Zahlen, Fakten und echten Antworten auf echte Fragen."
TEXTS[V14]="Kein Bürozwang. Keine fixen Arbeitszeiten. Du entscheidest, wann, wo und wie du arbeitest. Das ist nicht Theorie — das ist mein Alltag."
TEXTS[V15]="Bei iad gehört dein Name dir. Deine Kunden, dein Netzwerk, dein Ruf — das nimmst du mit. Und bekommst den Rückenwind eines globalen Unternehmens dazu."
TEXTS[V16]="Die Makler, die heute wechseln, sind in 3 Jahren mit eigenem Team, stabiler Provision und internationalem Netzwerk aufgestellt. Der richtige Zeitpunkt ist jetzt — nicht irgendwann."

for KEY in $(echo "${!TEXTS[@]}" | tr ' ' '\n' | sort); do
  TEXT="${TEXTS[$KEY]}"
  OUTPUT_FILE="$OUTPUT_DIR/${KEY}_markus_serie2.mp3"
  echo "Generiere $KEY ..."

  curl -s -X POST "https://api.elevenlabs.io/v1/text-to-speech/${VOICE_ID}" \
    -H "xi-api-key: ${API_KEY}" \
    -H "Content-Type: application/json" \
    -d "{
      \"text\": \"${TEXT}\",
      \"model_id\": \"${MODEL}\",
      \"voice_settings\": {
        \"stability\": 0.5,
        \"similarity_boost\": 0.85,
        \"style\": 0.2,
        \"use_speaker_boost\": true
      }
    }" \
    --output "$OUTPUT_FILE"

  if [ -s "$OUTPUT_FILE" ]; then
    echo "  ✓ Gespeichert: $OUTPUT_FILE"
  else
    echo "  ✗ Fehler bei $KEY"
    rm -f "$OUTPUT_FILE"
  fi
done

echo ""
echo "Fertig! Dateien liegen in: $OUTPUT_DIR"
