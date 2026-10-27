# -*- coding: utf-8 -*-
import glob
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def inject_all():
    docs_dir = BASE_DIR / "docs"
    
    # 1. Main index.html
    index_html = docs_dir / "index.html"
    if index_html.exists():
        c = index_html.read_text(encoding="utf-8")
        if "whatsapp-triage.js" not in c:
            c = c.replace("</head>", '  <script src="assets/whatsapp-triage.js"></script>\n</head>')
            index_html.write_text(c, encoding="utf-8")
            print("[+] Injected into docs/index.html")
        else:
            print("[=] Already in docs/index.html")

    # 2. Subpages: docs/lp/*.html, docs/articles/*.html, docs/products/*.html
    subfolders = ["lp", "articles", "products"]
    for sub in subfolders:
        sub_dir = docs_dir / sub
        if not sub_dir.exists():
            continue
        for html_file in sub_dir.glob("*.html"):
            c = html_file.read_text(encoding="utf-8")
            if "whatsapp-triage.js" not in c:
                if "</head>" in c:
                    c = c.replace("</head>", '  <script src="../assets/whatsapp-triage.js"></script>\n</head>')
                elif "</body>" in c:
                    c = c.replace("</body>", '  <script src="../assets/whatsapp-triage.js"></script>\n</body>')
                html_file.write_text(c, encoding="utf-8")
                print(f"[+] Injected into {sub}/{html_file.name}")
            else:
                print(f"[=] Already in {sub}/{html_file.name}")

    # 3. docs/wa.html
    wa_html = docs_dir / "wa.html"
    if wa_html.exists():
        c = wa_html.read_text(encoding="utf-8")
        if "whatsapp-triage.js" not in c:
            c = c.replace("</head>", '  <script src="assets/whatsapp-triage.js"></script>\n</head>')
            wa_html.write_text(c, encoding="utf-8")
            print("[+] Injected into docs/wa.html")
        else:
            print("[=] Already in docs/wa.html")

if __name__ == "__main__":
    inject_all()
