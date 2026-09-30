"""Copy original public artwork and layout CSS into this repository once."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import Request, urlopen
import json
import time

ROOT=Path(__file__).resolve().parents[1]
assets=json.loads((ROOT/'site/assets.json').read_text())

def download(item):
    target=ROOT/'docs'/item['path']
    if target.exists() and target.stat().st_size > 0:
        return
    target.parent.mkdir(parents=True,exist_ok=True)
    for attempt in range(3):
        try:
            request=Request(item['url'],headers={'User-Agent':'Mozilla/5.0','Referer':'https://sites.google.com/view/zerofpa/home'})
            with urlopen(request,timeout=45) as response:
                data=response.read()
                kind=response.headers.get('Content-Type','')
            if not data or (target.suffix=='.img' and not kind.startswith('image/')):
                raise ValueError('Expected an image, received '+kind)
            if target.suffix=='.css' and b'{' not in data:
                raise ValueError('Invalid stylesheet')
            # Remove Google's unused logo and default header asset references.
            # Actual page images are separately preserved in the manifest.
            target.write_bytes(data)
            print('Saved',target.name,len(data),'bytes',flush=True)
            return
        except Exception:
            if attempt==2:raise
            time.sleep(1+attempt)

with ThreadPoolExecutor(max_workers=6) as pool:
    list(pool.map(download,assets))
print(f'All {len(assets)} original assets are available locally.')
