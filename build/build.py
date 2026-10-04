"""Bygger index.html från build/template.html och data/*.json."""
import json, re, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
t = (R/'build/template.html').read_text()
tx = json.loads((R/'data/text.json').read_text())['paras']
body = (t.replace('__BASE__', (R/'data/basemap.json').read_text())
         .replace('__DATA__', (R/'data/stops_and_places.json').read_text())
         .replace('__TEXT__', json.dumps(tx, ensure_ascii=False).replace('</', '<\\/')))
title = re.search(r'<title>.*?</title>', body).group(0)
body = body.replace(title, '', 1)
(R/'index.html').write_text(f'<!doctype html>\n<html lang="sv">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n{title}\n<style>*,*::before,*::after{{box-sizing:border-box}}body{{margin:0}}[hidden]{{display:none!important}}</style>\n</head>\n<body>\n{body}\n</body>\n</html>\n')
print('index.html byggd')
