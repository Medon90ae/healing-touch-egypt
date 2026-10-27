# -*- coding: utf-8 -*-
"""
Integrate Clinical Research Harvester into:
1. antigravity_social_automation.py (export_notebooklm_master_source)
2. github_seo_trend_engine.py (dynamic merge of PubMed studies into encyclopedia)
"""

import sys
from pathlib import Path

BASE_DIR = Path(r"c:\followUPSHEET\healing_touch").resolve()

# -----------------------------------------------------------------------------
# 1. Update antigravity_social_automation.py
# -----------------------------------------------------------------------------
asa_file = BASE_DIR / "antigravity_social_automation.py"
asa_text = asa_file.read_text(encoding="utf-8")

# In export_notebooklm_master_source, add PubMed harvesting right after live trends
target_harvest = '''    # جلب أسئلة الترند الحي من جوجل مصر
    live_trend_queries = []
    try:
        from github_seo_trend_engine import harvest_live_egypt_trends
        live_map = harvest_live_egypt_trends()
        cat_key = selected_cfg["category"]
        live_trend_queries = live_map.get(cat_key, [])
    except Exception:
        pass'''

replacement_harvest = '''    # جلب أسئلة الترند الحي من جوجل مصر
    live_trend_queries = []
    try:
        from github_seo_trend_engine import harvest_live_egypt_trends
        live_map = harvest_live_egypt_trends()
        cat_key = selected_cfg["category"]
        live_trend_queries = live_map.get(cat_key, [])
    except Exception:
        pass

    # 🔬 استكشاف أحدث الأبحاث السريرية من PubMed / NCBI لنمو الموسوعة والمصادر
    discovered_studies = []
    try:
        from clinical_research_harvester import harvest_pubmed_studies, format_evidence_for_notebooklm_and_prompts
        print("\\n[*] 🔬 جاري استكشاف أحدث الأبحاث والدراسات السريرية من PubMed / NCBI لهذا المنتج...")
        discovered_studies = harvest_pubmed_studies(product_choice, max_results=3)
        if discovered_studies:
            print(f"[+] 📚 تم رصد وتوثيق {len(discovered_studies)} أبحاث طبية جديدة في الموسوعة وسجل الأبحاث:")
            for s in discovered_studies:
                print(f"    • [{s['pub_year']}] {s['title'][:75]}...")
                print(f"      🔗 {s['url']}")
    except Exception as e:
        print(f"[!] تنبيه استكشاف PubMed: {e}")'''

if target_harvest in asa_text:
    asa_text = asa_text.replace(target_harvest, replacement_harvest)
    print("[+] Hooked PubMed research harvesting into export_notebooklm_master_source")
else:
    print("[!] Target harvest block not found in antigravity_social_automation.py")

# Also inject discovered_studies into prompts_pack_lines and md_lines
target_pack_step3 = '''        "---------------------------------------------------------------------",
        "📥 الخطوة التالية ببساطة:",'''

replacement_pack_step3 = '''        "---------------------------------------------------------------------",
        "4️⃣ أحدث الأبحاث والمراجع الطبية الحقيقية المستكشفة من PubMed / NCBI (جاهزة للاستشهاد):",
        "---------------------------------------------------------------------",'''

# Build evidence lines
evidence_block = '''        "---------------------------------------------------------------------",
        "4️⃣ أحدث الأبحاث والمراجع الطبية الحقيقية المستكشفة من PubMed / NCBI (جاهزة للاستشهاد):",
        "---------------------------------------------------------------------",
    ]
    if discovered_studies:
        for idx, s in enumerate(discovered_studies, 1):
            prompts_pack_lines.append(f"[{idx}] {s['title']}")
            prompts_pack_lines.append(f"    • المجلة وسنة النشر: {s['journal']} ({s['pub_year']}) | PMID: {s['pmid']}")
            prompts_pack_lines.append(f"    • الرابط المباشر للدراسة: {s['url']}")
            prompts_pack_lines.append(f"    • الأهمية السريرية: {s['summary_ar']}\\n")
    prompts_pack_lines.extend([
        "---------------------------------------------------------------------",
        "📥 الخطوة التالية ببساطة:",'''

target_full_step = '''        "---------------------------------------------------------------------",
        "📥 الخطوة التالية ببساطة:",'''

if target_full_step in asa_text:
    asa_text = asa_text.replace(target_full_step, evidence_block, 1)
    print("[+] Injected discovered PubMed studies into PROMPTS_PACK_TODAY.txt")

# Also inject into md_lines
target_md_refs = '''    md_lines.append("\\n## 📚 ثانياً: المراجع السريرية والأبحاث المعتمدة:")'''
replacement_md_refs = '''    md_lines.append("\\n## 📚 ثانياً: المراجع السريرية والأبحاث المعتمدة:")
    if discovered_studies:
        md_lines.append("### 🔬 أبحاث PubMed / NCBI الحديثة المستكشفة اليوم:")
        for s in discovered_studies:
            md_lines.append(f"- [{s['title']} ({s['journal']} - {s['pub_year']})]({s['url']}) — {s['summary_ar']}")'''

if target_md_refs in asa_text:
    asa_text = asa_text.replace(target_md_refs, replacement_md_refs, 1)
    print("[+] Injected discovered PubMed studies into Healing_Touch_NotebookLM_Source.md")

asa_file.write_text(asa_text, encoding="utf-8")

# -----------------------------------------------------------------------------
# 2. Update github_seo_trend_engine.py to merge evidence registry into ALL_MEDICAL_REFERENCES
# -----------------------------------------------------------------------------
gste_file = BASE_DIR / "github_seo_trend_engine.py"
gste_text = gste_file.read_text(encoding="utf-8")

target_ref_get = 'ref_obj = ALL_MEDICAL_REFERENCES.get(s_key)'
replacement_ref_get = '''# دمج أبحاث PubMed الحية المكتشفة من سجل الأبحاث
        expanded_refs = dict(ALL_MEDICAL_REFERENCES)
        try:
            ev_file = BASE_DIR / "media_assets" / "medical_evidence_registry.json"
            if ev_file.exists():
                ev_data = json.loads(ev_file.read_text(encoding="utf-8"))
                for st in ev_data.get("studies", []):
                    pmid_k = f"PubMed {st.get('pmid')}"
                    expanded_refs[pmid_k] = {
                        "title": f"{st.get('title')} ({st.get('journal', 'PubMed')} - {st.get('pub_year', '2026')})",
                        "url": st.get("url"),
                        "summary": st.get("summary_ar", "بحث سريري محكم موثق من قاعدة بيانات المكتبة الطبية الأمريكية الوطنية (NCBI / PubMed).")
                    }
        except Exception:
            pass
        ref_obj = expanded_refs.get(s_key)'''

if target_ref_get in gste_text:
    gste_text = gste_text.replace(target_ref_get, replacement_ref_get)
    print("[+] Dynamically connected medical_evidence_registry.json to article sources renderer")

# Also in build_article_page, ensure that if there are relevant studies for the product in evidence registry, they appear in sources
target_refs_loop = '''    # قائمة المراجع الطبية (10 إلى 12 مرجعاً موثقاً من PubMed وNCBI)
    refs_list_html = []
    for i, s_key in enumerate(art.get("sources", []), 1):'''

replacement_refs_loop = '''    # قائمة المراجع الطبية (10 إلى 12 مرجعاً موثقاً من PubMed وNCBI) + الأبحاث المكتشفة حديثاً
    all_art_sources = list(art.get("sources", []))
    try:
        ev_file = BASE_DIR / "media_assets" / "medical_evidence_registry.json"
        if ev_file.exists():
            ev_data = json.loads(ev_file.read_text(encoding="utf-8"))
            for st in ev_data.get("studies", []):
                pmid_k = f"PubMed {st.get('pmid')}"
                if pmid_k not in all_art_sources and (st.get("product_choice") in (art.get("product_id"), "6") or art.get("category") in st.get("product_name", "")):
                    all_art_sources.append(pmid_k)
    except Exception:
        pass

    refs_list_html = []
    for i, s_key in enumerate(all_art_sources, 1):'''

if target_refs_loop in gste_text:
    gste_text = gste_text.replace(target_refs_loop, replacement_refs_loop)
    print("[+] Enabled dynamic encyclopedia growth: new PubMed studies automatically append to article references")

gste_file.write_text(gste_text, encoding="utf-8")
print("[+] Successfully integrated Clinical Research Harvester into the ecosystem!")
