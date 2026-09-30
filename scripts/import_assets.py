"""Preserve artwork using fresh public image URLs from each original page."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import Request, build_opener, HTTPCookieProcessor
from http.cookiejar import CookieJar
from html.parser import HTMLParser
import json,re
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'site/assets.json').read_text())
bindings=json.loads((ROOT/'site/media-pages.json').read_text())
class Images(HTMLParser):
    def __init__(self):super().__init__();self.depth=0;self.urls=[]
    def handle_starttag(self,tag,attrs):
        if tag=='section':self.depth+=1
        if not self.depth:return
        attrs=dict(attrs)
        urls=([attrs.get('src','')] if tag=='img' else [])+re.findall(r'url\([\"\']?(https://[^\s\)\"\']+)',attrs.get('style',''))
        for u in urls:
            if ('sitesv-images' in u or 'googleusercontent.com' in u) and u not in self.urls:self.urls.append(u)
    def handle_endtag(self,tag):
        if tag=='section':self.depth-=1

def get(opener,url):
    with opener.open(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=45) as response:return response.read(),response.headers.get('Content-Type','')
def page_assets(page):
    targets=[ROOT/'docs'/x for x in page['assets']]
    if all(p.exists() and p.stat().st_size for p in targets):return
    opener=build_opener(HTTPCookieProcessor(CookieJar()))
    markup,_=get(opener,page['source'])
    parser=Images();parser.feed(markup.decode('utf-8'))
    if len(parser.urls)!=len(targets):raise ValueError(f"Image count changed for {page['source']}: expected {len(targets)}, got {len(parser.urls)}")
    for url,path in zip(parser.urls,targets):
        if path.exists() and path.stat().st_size:continue
        data,kind=get(opener,url)
        if not kind.startswith('image/') or not data:raise ValueError('Expected image: '+kind)
        path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
        print('Saved',path.name,len(data),'bytes',flush=True)
for item in manifest:
    if item['path'].endswith('.css'):
        target=ROOT/'docs'/item['path']
        target.parent.mkdir(parents=True,exist_ok=True)
        if not target.exists():target.write_bytes(get(build_opener(),item['url'])[0])
with ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(page_assets,bindings))
print('All original artwork is now stored locally.')
