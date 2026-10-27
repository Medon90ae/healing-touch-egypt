# -*- coding: utf-8 -*-
from pathlib import Path
p = Path(r'c:\followUPSHEET\healing_touch\github_seo_trend_engine.py')
code = p.read_text(encoding='utf-8')

new_chunk = '''    # مقالات ذات صلة سريرياً فقط (بدون حشو أو تكرار ميكانيكي)
    related_articles = [
        other for other in all_articles 
        if other["slug"] != art["slug"] and (other.get("category") == art.get("category") or other.get("product_id") == art.get("product_id"))
    ][:2]
    if len(related_articles) < 2:
        related_articles = [other for other in all_articles if other["slug"] != art["slug"]][:2]

    other_cards = []
    for other in related_articles:
        other_wa = build_whatsapp_link(cfg, other["title"], is_article=True)
        other_cards.append(f"""
        <div class="article-card" data-category="{other.get('category', 'c-section')}">
          <div>
            <div class="art-meta-top">
              <span class="art-cat-tag">{other.get("category_label", "دليل سريري")}</span>
              <span class="art-Evidence-tag">✅ {len(other.get("sources", []))} مراجع معتمدة</span>
            </div>
            <h3><a href="{other['slug']}.html">{other["title"]}</a></h3>
            <p class="art-hook-text" style="font-size:0.92rem; color:var(--text-muted); line-height:1.6; margin-top:8px;">{other.get("hook_summary", "")[:130]}...</p>
          </div>
          <div class="art-card-actions" style="margin-top:14px;">
            <a href="{other['slug']}.html" class="btn-read-guide" style="flex:1; text-align:center;">📖 قراءة الدليل السريري</a>
            <a href="{other_wa}" target="_blank" rel="noopener" class="btn-ask-doc-mini" style="text-decoration:none;">💬 استشارة</a>
          </div>
        </div>
        """)
    other_html = "\\n".join(other_cards)'''

idx = code.find('other_cards = []')
if idx != -1:
    end_idx = code.find('other_html = "\\n".join(other_cards[:6])', idx)
    if end_idx != -1:
        end_idx += len('other_html = "\\n".join(other_cards[:6])')
        code = code[:idx] + new_chunk.strip() + code[end_idx:]
        p.write_text(code, encoding='utf-8')
        print('[+] Successfully replaced other_cards block!')
    else:
        print('[-] end_idx not found')
else:
    print('[-] other_cards not found')
