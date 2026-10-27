# -*- coding: utf-8 -*-
from pathlib import Path
p = Path(r'c:\followUPSHEET\healing_touch\github_seo_trend_engine.py')
code = p.read_text(encoding='utf-8')

# The function openPromoDrawer inside get_shared_js f-string must use {{ and }}
old_js = '''function openPromoDrawer(contextTopic, preferredChannel, directWaUrl) {
      const targetTopic = contextTopic || document.title;
      const targetWaUrl = directWaUrl || buildDynamicWaUrl(targetTopic);
      if (preferredChannel === 'whatsapp' || !preferredChannel) {
        try {
          if (navigator.sendBeacon) {
            navigator.sendBeacon(TRACKING_ENDPOINT, JSON.stringify({
              channel: 'whatsapp',
              topic: targetTopic,
              lead_type: 'direct_whatsapp_click',
              timestamp: new Date().toISOString()
            }));
          }
        } catch(e) {}
        window.open(targetWaUrl, '_blank');
        return false;
      }
      window.open(directWaUrl || IG_URL, '_blank');
      return false;
    }'''

new_js = '''function openPromoDrawer(contextTopic, preferredChannel, directWaUrl) {{
      const targetTopic = contextTopic || document.title;
      const targetWaUrl = directWaUrl || buildDynamicWaUrl(targetTopic);
      if (preferredChannel === 'whatsapp' || !preferredChannel) {{
        try {{
          if (navigator.sendBeacon) {{
            navigator.sendBeacon(TRACKING_ENDPOINT, JSON.stringify({{
              channel: 'whatsapp',
              topic: targetTopic,
              lead_type: 'direct_whatsapp_click',
              timestamp: new Date().toISOString()
            }}));
          }}
        }} catch(e) {{}}
        window.open(targetWaUrl, '_blank');
        return false;
      }}
      window.open(directWaUrl || IG_URL, '_blank');
      return false;
    }}'''

if old_js in code:
    code = code.replace(old_js, new_js)
    p.write_text(code, encoding='utf-8')
    print('[+] Successfully patched escaped braces in openPromoDrawer!')
else:
    print('[-] old_js not found in code')
