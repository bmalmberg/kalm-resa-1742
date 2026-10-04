"""Bygger index.html från build/template.html och data/*.json."""
import json, re, pathlib

# Sidans adress på GitHub Pages (med / på slutet). Byt ANVANDARNAMN mot ditt GitHub-namn.
SITE_URL = "https://ANVANDARNAMN.github.io/kalm-resa-1742/"
R = pathlib.Path(__file__).resolve().parent.parent
t = (R/'build/template.html').read_text()
tx = json.loads((R/'data/text.json').read_text())['paras']
body = (t.replace('__BASE__', (R/'data/basemap.json').read_text())
         .replace('__DATA__', (R/'data/stops_and_places.json').read_text())
         .replace('__TEXT__', json.dumps(tx, ensure_ascii=False).replace('</', '<\\/')))
title = re.search(r'<title>.*?</title>', body).group(0)
body = body.replace(title, '', 1)
(R/'index.html').write_text(f'<!doctype html>\n<html lang="sv">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n{title}\n<meta name="description" content="Interaktiv karta över Pehr Kalms resa 1742 genom Västergötland och Bohuslän. Klicka på en ort och läs vad Kalm skrev där.">\n<meta property="og:type" content="website">\n<meta property="og:title" content="Pehr Kalms Wästgötha och Bahusländska resa 1742">\n<meta property="og:description" content="Interaktiv karta: 74 orter från Uppsala till Bohuslän och tillbaka, med citat ur Kalms reseskildring.">\n<meta property="og:url" content="{SITE_URL}">\n<meta property="og:image" content="{SITE_URL}og.png">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n<meta property="og:locale" content="sv_SE">\n<meta name="twitter:card" content="summary_large_image">\n<style>*,*::before,*::after{{box-sizing:border-box}}body{{margin:0}}[hidden]{{display:none!important}}</style>\n</head>\n<body>\n{body}\n</body>\n</html>\n')
print('index.html byggd')
