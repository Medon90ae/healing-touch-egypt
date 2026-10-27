# -*- coding: utf-8 -*-
with open('c:/followUPSHEET/healing_touch/github_seo_trend_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    '🛡️ موثق بـ {len(art.get("sources", []))} مراجع سريرية من PubMed وNCBI',
    '🛡️ موثق بـ {len(all_art_sources)} مراجع سريرية من PubMed وNCBI'
)

text = text.replace(
    '📚 المراجع والأبحاث الطبية المعتمدة في هذا الدليل ({len(art.get("sources", []))} مراجع موثقة):',
    '📚 المراجع والأبحاث الطبية المعتمدة في هذا الدليل ({len(all_art_sources)} مراجع موثقة):'
)

with open('c:/followUPSHEET/healing_touch/github_seo_trend_engine.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated reference count in article generator.")
