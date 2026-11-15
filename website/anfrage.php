<?php
// Bewertungsanfrage von der Startseite per E-Mail weiterleiten.
// Empfänger hier anpassen, falls nötig:
$empfaenger = 'markus.seitz@iaddeutschland.de';
$absender   = 'anfrage@markus-seitz.immobilien'; // Adresse der eigenen Domain (sonst landet die Mail im Spam)

if ($_SERVER['REQUEST_METHOD'] !== 'POST') { header('Location: /#bewertung'); exit; }

// Spam-Schutz: verstecktes Feld muss leer sein, Formular nicht in unter 3 Sekunden ausgefüllt
$t = (int)($_POST['t'] ?? 0);
if (!empty($_POST['firma']) || ($t > 0 && (microtime(true) * 1000 - $t) < 3000)) {
    header('Location: /danke.html'); exit;
}

function feld($k, $max = 200) {
    $v = trim((string)($_POST[$k] ?? ''));
    $v = str_replace(["\r", "\n"], ' ', $v);
    return mb_substr($v, 0, $max);
}
$d = [
    'Objektart'       => feld('objektart', 40),
    'PLZ / Ort'       => feld('ort', 80),
    'Wohnfläche (m²)' => feld('flaeche', 20),
    'Baujahr'         => feld('baujahr', 20),
    'Verkaufszeitraum'=> feld('zeitraum', 60),
    'Name'            => feld('name', 100),
    'Telefon'         => feld('telefon', 40),
    'E-Mail'          => feld('email', 120),
];
$email_ok = filter_var($d['E-Mail'], FILTER_VALIDATE_EMAIL);
if (!$d['Objektart'] || !$d['PLZ / Ort'] || !$d['Name'] || !$d['Telefon'] || !$email_ok || ($_POST['datenschutz'] ?? '') !== 'ja') {
    header('Location: /?fehler=1#bewertung'); exit;
}

$text = "Neue Bewertungsanfrage über markus-seitz.immobilien\n\n";
foreach ($d as $k => $v) { $text .= str_pad($k . ':', 18) . ($v !== '' ? $v : '–') . "\n"; }
$text .= "\nDatenschutz-Einwilligung: ja\nZeitpunkt: " . date('d.m.Y H:i') . "\n";

$betreff = '=?UTF-8?B?' . base64_encode('Neue Bewertungsanfrage: ' . $d['Objektart'] . ' in ' . $d['PLZ / Ort']) . '?=';
$header  = "From: Website Markus Seitz <{$absender}>\r\n"
         . "Reply-To: {$d['E-Mail']}\r\n"
         . "MIME-Version: 1.0\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: 8bit\r\n";

$ok = mail($empfaenger, $betreff, $text, $header, '-f' . $absender);
header('Location: ' . ($ok ? '/danke.html' : '/?fehler=2#bewertung'));
exit;
