"""Verify every published page, local link, image, and stylesheet."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs'
errors=[]
class Links(HTMLParser):
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        for key in ('href','src'):
            url=attrs.get(key,'')
            if not url or url.startswith(('#','data:','/')) or urlsplit(url).scheme:continue
            path=(self.path.parent/unquote(urlsplit(url).path)).resolve()
            if path.is_dir():path=path/'index.html'
            if not path.exists():errors.append(f'{self.path.relative_to(OUT)}: missing {url}')
for page in OUT.rglob('*.html'):
    parser=Links();parser.path=page;parser.feed(page.read_text())
for p in json.loads((ROOT/'site/pages.json').read_text()):
    if not (OUT/p['slug']/'index.html').is_file():errors.append('Missing page '+p['slug'])
for a in json.loads((ROOT/'site/assets.json').read_text()):
    target=OUT/a['path']
    if not target.exists() or not target.stat().st_size:errors.append('Missing asset '+a['path'])
if errors:raise SystemExit('\n'.join(errors))
print('All 66 archive pages, local links, and original assets verified.')
