# -*- coding: utf-8 -*-
with open('c:/followUPSHEET/healing_touch/github_seo_trend_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = '''            for st in ev_data.get("studies", []):
                pmid_k = f"PubMed {st.get('pmid')}"
                if pmid_k not in all_art_sources and (st.get("product_choice") in (art.get("product_id"), "6") or art.get("category") in st.get("product_name", "")):
                    all_art_sources.append(pmid_k)'''

replacement = '''            prod_id_map = {
                "1": "3m-tegaderm-plus-pad",
                "2": "bupy-silicone-scar-sheet",
                "3": "3m-micropore-tan-tape-1533-0",
                "4": "silicone-nostril-retainer",
                "5": "smith-nephew-opsite-spray",
                "6": "all"
            }
            for st in ev_data.get("studies", []):
                pmid_k = f"PubMed {st.get('pmid')}"
                target_pid = prod_id_map.get(str(st.get("product_choice")), "")
                if pmid_k not in all_art_sources and (target_pid == art.get("product_id") or target_pid == "all"):
                    all_art_sources.append(pmid_k)'''

if target in text:
    text = text.replace(target, replacement)
    with open('c:/followUPSHEET/healing_touch/github_seo_trend_engine.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Mapped product IDs accurately in github_seo_trend_engine.py")
else:
    print("Target block not found")
