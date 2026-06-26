#!/bin/bash

API_KEY="sk_29721598d00eb2fa4e9191416103825c15a7d848af8c2564"
VOICE_ID="ttwV3vM4gSmeC9ZeknPc"
MODEL="eleven_multilingual_v2"
OUTPUT_DIR="./audio_voiceovers"

mkdir -p "$OUTPUT_DIR"

declare -A TEXTS
TEXTS[V01]="Ich wollte das nie. Es war meine Frau, die es in mir gesehen hat — bevor ich es selbst sehen konnte."
TEXTS[V02]="Nicht jeder wird ein guter Makler. Ich stelle jedem drei Fragen — und die Antworten entscheiden mehr als jeder Kurs."
TEXTS[V03]="Du wartest auf Sicherheit. Die kommt nicht. Nicht-Entscheiden ist auch eine Entscheidung."
TEXTS[V04]="Die meisten starten mit Sichtbarkeit. Ich auch. Falsch. Fundament zuerst — dann Außenwirkung."
TEXTS[V05]="Ich lag falsch. Du begleitest Menschen in den emotionalsten Momenten ihres Lebens. Kein Verkaufsjob."
TEXTS[V06]="Er kam aus einem ehrlichen Gespräch. Kein Google. Kein Instagram. Nur Präsenz und echten Kontakt."
TEXTS[V07]="Allein das Wort lässt viele weglaufen. Dabei ist es simpel: Eigentümer wollen nicht akquiriert — sie wollen verstanden werden."
TEXTS[V08]="Und mir wurde klar: Der Verkäufer verlässt heute sein Zuhause. Der Käufer betritt seins. Ich stehe in der Mitte."
TEXTS[V09]="Er ist aus Vertrauen. In diesem Moment habe ich verstanden: Ich verkaufe keine Häuser. Ich helfe Menschen, neu anzufangen."
TEXTS[V10]="Ich wäre 12 Monate weiter. Genau deshalb begleite ich heute Menschen, die diesen Weg gehen wollen. Schreib mir CHANCE."

for KEY in $(echo "${!TEXTS[@]}" | tr ' ' '\n' | sort); do
  TEXT="${TEXTS[$KEY]}"
  OUTPUT_FILE="$OUTPUT_DIR/${KEY}_markus.mp3"
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
