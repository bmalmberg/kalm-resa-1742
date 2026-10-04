# Pehr Kalms Wästgötha och Bahusländska resa 1742

En interaktiv karta över Pehr Kalms resa 6 juli – 11 oktober 1742 från Uppsala genom Västmanland, Närke och Västergötland till Bohuslän och tillbaka. Klicka på en ort för att läsa vad Kalm skrev där, och läs vidare i hela texten.

Öppna `index.html` i en webbläsare, eller se den publicerade sidan via GitHub Pages.

## Innehåll

- `index.html` – färdig sida, allt inbakat (karta, data, text). Laddar d3 från cdnjs och typsnitt från Google Fonts.
- `data/stops_and_places.json` – orter (koordinater, Kalms stavning, `a: 1` = ungefärligt läge) och nedslag (datum, fas, citat, `a` = stycke i texten).
- `data/text.json` – reseskildringens text uppdelad i stycken (OCR, oredigerad).
- `data/basemap.json` – förprojicerade SVG-banor för land, sjöar och vattendrag.
- `build/` – mall och skript. Ändra i `build/template.html` eller i JSON-filerna och kör `python3 build/build.py` för att bygga om `index.html`.

## Om data

- **Koordinaterna** är satta ur minnet av Claude (AI) och inte uppslagna i någon ortnamnsdatabas. Kända orter ligger troligen rätt inom en kilometer eller så; orter med `a: 1` (streckad kant på kartan) är uppskattade utifrån Kalms beskrivningar och kan ligga flera kilometer fel. Rättelser välkomnas.
- **Citaten** är OCR-text ur trycket 1746 (Stockholm, Lars Salvius), varsamt rättad för uppenbara läsfel (t.ex. "fom" → "som") med bevarad 1700-talsstavning. Texten i läsfönstret är oredigerad.
- **Kartunderlag:** [geo-maps](https://github.com/simonepri/geo-maps) (MIT), baserat på OpenStreetMap (© OpenStreetMap-bidragsgivare, ODbL) och Natural Earth (public domain).
- Kalms text (1746) är fri från upphovsrätt.
