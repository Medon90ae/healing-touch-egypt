# -*- coding: utf-8 -*-
from pathlib import Path
p = Path(r'c:\followUPSHEET\healing_touch\github_seo_trend_engine.py')
code = p.read_text(encoding='utf-8')

target = 'def harvest_live_egypt_trends() -> dict:'
declaration = '''
LIVE_TRENDS_FILE = BASE_DIR / "media_assets" / "live_trends_registry.json"
_LIVE_TRENDS_CACHE = None

'''

if declaration not in code:
    code = code.replace(target, declaration + target)
    p.write_text(code, encoding='utf-8')
    print('[+] Added LIVE_TRENDS_FILE and _LIVE_TRENDS_CACHE declaration')
else:
    print('[=] Already present')
