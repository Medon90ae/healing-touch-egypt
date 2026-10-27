# -*- coding: utf-8 -*-
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def patch_github_seo_trend_engine():
    seo_file = BASE_DIR / "github_seo_trend_engine.py"
    text = seo_file.read_text(encoding="utf-8")
    
    # 1. Fix the broken openPromoDrawer in get_shared_js
    old_target = """    /* تفعيل الـ Micro-Popup Drawer (R3) */
    function openPromoDrawer(contextTopic, preferredChannel, directWaUrl) {{
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
    }} else {{
        // في حالة عدم وجود المودال، يتم توجيهه إلى صفحة تأكيد الاستشارة wa.html لتسجيل البيانات أولاً
        const targetCase = "general";
        window.location.href = "wa.html?case=" + encodeURIComponent(targetCase) + "&topic=" + encodeURIComponent(contextTopic || document.title);
      }}
    }}"""

    new_replacement = """    /* تفعيل الـ Micro-Popup Drawer (R3) الموحد */
    function openPromoDrawer(contextTopic, preferredChannel, directWaUrl) {{
      const targetTopic = contextTopic || document.title;
      if (typeof window.HEALING_TOUCH_WHATSAPP !== 'undefined' && window.HEALING_TOUCH_WHATSAPP.showModal) {{
        window.HEALING_TOUCH_WHATSAPP.showModal(targetTopic);
        return false;
      }}
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
    }}"""

    if old_target in text:
        text = text.replace(old_target, new_replacement)
        print("[+] Fixed openPromoDrawer in github_seo_trend_engine.py")
    else:
        print("[!] Target openPromoDrawer not found verbatim, checking regex...")
        import re
        pat = re.compile(r'/\* تفعيل الـ Micro-Popup Drawer \(R3\) \*/.*?function closePromoModal', re.S)
        replacement_full = new_replacement + "\n\n    function closePromoModal"
        text, n = pat.subn(replacement_full, text)
        print(f"[+] Regex replaced openPromoDrawer: {n} match(es)")

    # 2. Inject <script src="assets/whatsapp-triage.js"></script> into index.html head
    if '<script src="assets/whatsapp-triage.js"></script>' not in text:
        text = text.replace(
            '<style>{get_shared_css()}</style>\n  <script>{get_shared_js(cfg)}</script>',
            '<style>{get_shared_css()}</style>\n  <script src="assets/whatsapp-triage.js"></script>\n  <script>{get_shared_js(cfg)}</script>'
        )
        print("[+] Injected whatsapp-triage.js in index.html generation")

    # 3. Inject <script src="../assets/whatsapp-triage.js"></script> into articles and products
    if '<script src="../assets/whatsapp-triage.js"></script>' not in text:
        # For articles and products subpages:
        text = text.replace(
            '<style>{get_shared_css()}</style>\n  <script>{get_shared_js(cfg)}</script>\n  <script type="application/ld+json">',
            '<style>{get_shared_css()}</style>\n  <script src="../assets/whatsapp-triage.js"></script>\n  <script>{get_shared_js(cfg)}</script>\n  <script type="application/ld+json">'
        )
        print("[+] Injected ../assets/whatsapp-triage.js in subpages generation")

    seo_file.write_text(text, encoding="utf-8")

def patch_campaign_landing_engine():
    lp_file = BASE_DIR / "campaign_landing_engine.py"
    text = lp_file.read_text(encoding="utf-8")

    # 1. Inject whatsapp-triage.js in head of generated LPs
    if '<script src="../assets/whatsapp-triage.js"></script>' not in text:
        text = text.replace(
            '<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap" rel="stylesheet">',
            '<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap" rel="stylesheet">\n  <script src="../assets/whatsapp-triage.js"></script>'
        )
        print("[+] Injected ../assets/whatsapp-triage.js into campaign_landing_engine.py head")

    # 2. Update _inject_gate_and_tracking_into_html so openPromoDrawer defers to window.HEALING_TOUCH_WHATSAPP
    old_gate_func = """      function openPromoDrawer(topic, channel) {{
        const m = document.getElementById('promo-lead-modal');
        if (m) {{ m.style.display = 'flex'; document.getElementById('consult-lead-name').focus(); }}
      }}"""
    
    new_gate_func = """      function openPromoDrawer(topic, channel) {{
        if (typeof window.HEALING_TOUCH_WHATSAPP !== 'undefined' && window.HEALING_TOUCH_WHATSAPP.showModal) {{
          window.HEALING_TOUCH_WHATSAPP.showModal(topic || '{title}');
          return;
        }}
        const m = document.getElementById('promo-lead-modal');
        if (m) {{ m.style.display = 'flex'; document.getElementById('consult-lead-name').focus(); }}
      }}"""

    if old_gate_func in text:
        text = text.replace(old_gate_func, new_gate_func)
        print("[+] Updated openPromoDrawer in campaign_landing_engine.py")

    lp_file.write_text(text, encoding="utf-8")

if __name__ == "__main__":
    patch_github_seo_trend_engine()
    patch_campaign_landing_engine()
