# -*- coding: utf-8 -*-
with open('c:/followUPSHEET/healing_touch/antigravity_social_automation.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix cat_matched
text = text.replace(
    'if cat_matched.get("htmls"):\n        custom_stitch_html = cat_matched["htmls"][0].read_text(encoding="utf-8")\n        used_inbox_files.append(cat_matched["htmls"][0])',
    'if inbox_htmls:\n        custom_stitch_html = inbox_htmls[0].read_text(encoding="utf-8")\n        used_inbox_files.append(inbox_htmls[0])'
)

# Fix reddit_text
text = text.replace(
    '**استشارة مجانية عبر واتساب:** 01155803307 | **كود الخصم:** HT10 (شحن مجاني ومعاينة قبل الدفع)',
    '**للتوجيه السريري والاستشارة المجانية عبر واتساب:** 01155803307'
)

# Open lp_url in browser
text = text.replace(
    'open_tabs_in_default_windows_browser(fb_post_url=permalink, blogger_post_file=blogger_post[\'file_path\'])',
    'open_url_in_default_browser(lp_url)\n    open_tabs_in_default_windows_browser(fb_post_url=permalink, blogger_post_file=blogger_post[\'file_path\'])'
)

with open('c:/followUPSHEET/healing_touch/antigravity_social_automation.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("[+] Successfully patched cat_matched and reddit_text")
