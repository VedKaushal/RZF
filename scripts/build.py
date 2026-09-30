"""Build Zero's archive with Python's standard library; no package install needed."""
from pathlib import Path
import html
import json
import shutil
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
OUT = ROOT / 'docs'
OUT.mkdir(exist_ok=True)
pages = json.loads((SITE / 'pages.json').read_text())
config = json.loads((SITE / 'config.json').read_text())
by_slug = {p['slug']: p for p in pages}
children = {}
for p in pages:
    parent = p['slug'].rsplit('/', 1)[0] if '/' in p['slug'] else ''
    children.setdefault(parent, []).append(p)

def menu(parent, current, prefix, depth=0):
    result = '<ul class="zero-tree">'
    for p in children.get(parent, []):
        slug, title = p['slug'], html.escape(p['title'])
        active = ' aria-current="page"' if slug == current else ''
        link = f'<a href="{prefix}{slug}/"{active}>{title}</a>'
        if slug in children:
            expanded = current == slug or current.startswith(slug + '/') or slug == 'home'
            result += f'<li><div class="zero-row" style="--depth:{depth}"><button class="zero-toggle" aria-label="Toggle {html.escape(p["title"], quote=True)}" aria-expanded="{str(expanded).lower()}" aria-controls="nav-{slug.replace("/", "--")}"><span></span></button>{link}</div>'
            result += f'<div id="nav-{slug.replace("/", "--")}"'+('' if expanded else ' hidden')+'>'+menu(slug,current,prefix,depth+1)+'</div></li>'
        else:
            result += f'<li><div class="zero-row zero-leaf" style="--depth:{depth}">{link}</div></li>'
    return result + '</ul>'

def page_html(p, prefix, current):
    content = (SITE / 'content' / (p['slug']+'.html')).read_text().replace('{{ROOT}}',prefix)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(config['title'] if p['slug']=='home' else p['title']+' — '+config['title'])}</title>
<meta name="author" content="Zero"><meta name="description" content="Zero's personal archive of mathematics, medicine, history, art, and games.">
<link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Lato:300,300italic,400,400italic,700,700italic%7CSource+Code+Pro:400,600,700,800&display=swap">
<link rel="stylesheet" href="{prefix}{config['base_stylesheet']}">
<link rel="stylesheet" href="{prefix}themes/{p['theme']}">
<link rel="stylesheet" href="{prefix}assets/archive.css">
<script src="{prefix}assets/archive.js" defer></script></head>
<body class="EIlDfe" data-root="{prefix}"><a class="zero-skip" href="#zero-main">Skip to content</a>
<button id="zero-mobile" aria-label="Open navigation" aria-expanded="false" aria-controls="zero-sidebar"><span></span><span></span><span></span></button>
<button id="zero-shade" aria-label="Close navigation" hidden></button>
<nav id="zero-sidebar" aria-label="Archive"><a class="zero-brand" href="{prefix}">{html.escape(config['title'])}</a>{menu('',current,prefix)}</nav>
<button id="zero-search-open" aria-label="Search archive"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10" cy="10" r="6.5"/><path d="m15 15 6 6"/></svg></button>
<dialog id="zero-search"><form method="dialog"><label for="zero-query">Search the archive</label><button aria-label="Close search">×</button></form><input id="zero-query" type="search" placeholder="Search pages and writing…" autocomplete="off"><div id="zero-results" aria-live="polite"></div></dialog>
<main id="zero-main" tabindex="-1"><div class="QZ3zWd"><div class="fktJzd AKpWA vS6Uxe fOU46b Ly6Unf b2Iqye XeSM4 XxIgdb WwqPKb"><div class="UtePc RCETm yxgWrb">{content}</div></div></div></main>
</body></html>'''

for p in pages:
    destination=OUT/p['slug']/'index.html'
    destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_text(page_html(p,'../'*len(p['slug'].split('/')),p['slug']))
(OUT/'index.html').write_text(page_html(by_slug['home'],'./','home'))
(OUT/'themes').mkdir(exist_ok=True)
for file in (SITE/'themes').glob('*.css'):shutil.copyfile(file,OUT/'themes'/file.name)
(OUT/'assets').mkdir(exist_ok=True)
for file in (SITE/'shared').iterdir():shutil.copyfile(file,OUT/'assets'/file.name)
search=[]
for p in pages:
    raw=(SITE/'content'/(p['slug']+'.html')).read_text()
    text=html.unescape(re.sub('<[^>]+>',' ',raw))
    search.append({'title':p['title'],'slug':p['slug'],'text':re.sub(r'\s+',' ',text).strip()})
(OUT/'search.json').write_text(json.dumps(search,ensure_ascii=False))
(OUT/'.nojekyll').touch()
(OUT/'404.html').write_text('<!doctype html><meta charset="utf-8"><title>Page not found — Zero</title><body style="background:#000;color:#eee;font:20px sans-serif;padding:10vw"><h1>Page not found</h1><p>Find this page in <a style="color:#a2d4ce" href="/RZF/">Zero’s archive</a>.</p>')
print(f'Built {len(pages)} archive pages and the home entry point in docs/.')
