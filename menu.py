# -*- coding: utf-8 -*-
"""
=============================================================================
🌿 هيلينج تاتش مصر | محرك التشغيل والنشر السريري الموحد (2026)
Interactive Terminal Control Center & Unified Orchestration Suite
=============================================================================
"""

import sys
import os
import subprocess
from pathlib import Path

# ضبط ترميز UTF-8 لطرفية ويندوز لمنع تشوه النصوص العربية
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent
VENV_PYTHON = str(BASE_DIR / ".venv" / "Scripts" / "python.exe")


def print_banner():
    print("=" * 70)
    print("        🌿 هيلينج تاتش مصر - محرك التشغيل والنشر السريري الموحد (2026)")
    print("=" * 70)
    print()
    print("  [1] التشغيل الشامل واستيعاب manual_inbox وبناء LPs وتجهيز المنصات")
    print("  [2] تجهيز برومبتات اليوم ومصادر الأبحاث الطبية المعتمدة (PubMed + Deep Research)")
    print("  [3] تحديث ونشر الموقع والموسوعة ورفع التحديثات مباشرة إلى GitHub Pages")
    print("  [4] فتح أحدث حزمة نشر جاهزة للمنصات (أحدث مجلد مؤرخ)")
    print("  [5] استعراض روابط صفحات الهبوط الـ 12 الحية المباشرة")
    print()
    print("=" * 70)


def run_option_1():
    print("\n[*] [1/5] جاري فحص manual_inbox واستيعاب الميديا وتوليد صفحات الهبوط (Multi-Angle LPs)...")
    manual_inbox = BASE_DIR / "media_assets" / "manual_inbox"
    user_files = [f for f in manual_inbox.iterdir() if f.is_file() and not f.name.startswith(".") and f.name not in ["PROMPTS_PACK_TODAY.txt", "PROMPTS_PACK_TODAY.md"]]
    if not user_files:
        archive_dir = manual_inbox / "archive"
        if archive_dir.exists():
            recent_dirs = sorted([d for d in archive_dir.iterdir() if d.is_dir()], key=lambda x: x.name, reverse=True)
            if recent_dirs:
                latest = recent_dirs[0]
                latest_files = [f for f in latest.iterdir() if f.is_file()]
                if latest_files:
                    print(f"[*] ℹ️ صندوق manual_inbox فارغ — جاري تلقائياً استعادة ملفات آخر حملة من الأرشيف ({latest.name})...")
                    import shutil
                    for lf in latest_files:
                        shutil.copy2(str(lf), str(manual_inbox / lf.name))
                    print(f"[+] ✅ تم استعادة {len(latest_files)} ملفات إلى manual_inbox لضمان اعتماد محتواك المرفوع.")

    subprocess.run([VENV_PYTHON, "antigravity_social_automation.py", "--mode", "auto-daily"], cwd=str(BASE_DIR))

    print("\n[*] [2/5] جاري إعادة بناء الموقع وخريطة السيو sitemap.xml والموسوعة الطبية...")
    subprocess.run([VENV_PYTHON, "github_seo_trend_engine.py", "--build-site"], cwd=str(BASE_DIR))
    subprocess.run([VENV_PYTHON, "scripts/inject_triage_all_pages.py"], cwd=str(BASE_DIR), check=False)

    print("\n[*] [3/5] جاري بناء وتجميع تطبيق البوابة التفاعلية (Clinical Portal App)...")
    try:
        subprocess.run(["npm", "--prefix", "portal_app", "run", "build"], cwd=str(BASE_DIR), shell=True)
        portal_dist = BASE_DIR / "portal_app" / "dist"
        docs_portal = BASE_DIR / "docs" / "portal"
        if portal_dist.exists():
            import shutil
            shutil.copytree(str(portal_dist), str(docs_portal), dirs_exist_ok=True)
    except Exception as e:
        print(f"[!] تنبيه تجميع البوابة: {e}")

    print("\n[*] [4/5] جاري رفع ونشر كافة التحديثات والصفحات الحية إلى GitHub Pages...")
    try:
        subprocess.run(["git", "add", "-A"], cwd=str(BASE_DIR), check=False)
        subprocess.run(["git", "commit", "-m", "feat(deploy): live portal and multi-angle landing pages sync"], cwd=str(BASE_DIR), check=False)
        subprocess.run(["git", "push", "origin", "main"], cwd=str(BASE_DIR), check=False)
        print("[+] 🚀 تم النشر بنجاح على GitHub Pages!")
    except Exception as e:
        print(f"[!] خطأ في رفع GitHub: {e}")

    print("\n[*] [5/5] جاري تجهيز حزمة النشر الشاملة بالمجلدات المؤرخة وتحديث فهرس الصفحات...")
    try:
        subprocess.run([VENV_PYTHON, "scripts/build_ready_to_publish_pack.py"], cwd=str(BASE_DIR), check=False)
        subprocess.run([VENV_PYTHON, "scripts/build_landing_pages_directory.py"], cwd=str(BASE_DIR), check=False)
    except Exception:
        pass

    # فتح أحدث حزمة مؤرخة تلقائياً
    run_option_4()

    print("\n" + "=" * 70)
    print("🎉 اكتمل النشر الشامل وتحديث كافة صفحات الموقع والأصول بنجاح!")
    print("👉 رابط البوابة الحية: https://medon90ae.github.io/healing-touch-egypt/portal/")
    print("👉 رابط الموقع الرئيسي: https://medon90ae.github.io/healing-touch-egypt/")
    print("=" * 70)


def run_option_2():
    print("\n[*] تجهيز حزمة البرومبتات ومصادر الأبحاث السريرية المعتمدة (PubMed + Deep Research)...")
    subprocess.run([VENV_PYTHON, "antigravity_social_automation.py", "--mode", "notebooklm"], cwd=str(BASE_DIR))
    prompts_txt = BASE_DIR / "media_assets" / "manual_inbox" / "PROMPTS_PACK_TODAY.txt"
    if prompts_txt.exists():
        try:
            os.startfile(str(prompts_txt))
        except Exception:
            pass


def run_option_3():
    print("\n[*] [1/3] جاري تحديث صفحات الموقع ومقالات السيو والموسوعة...")
    subprocess.run([VENV_PYTHON, "github_seo_trend_engine.py", "--build-site"], cwd=str(BASE_DIR))

    print("\n[*] [2/3] جاري بناء وتجميع تطبيق البوابة التفاعلية (Clinical Portal App)...")
    subprocess.run(["npm", "--prefix", "portal_app", "run", "build"], cwd=str(BASE_DIR), shell=True)
    portal_dist = BASE_DIR / "portal_app" / "dist"
    docs_portal = BASE_DIR / "docs" / "portal"
    if portal_dist.exists():
        import shutil
        shutil.copytree(str(portal_dist), str(docs_portal), dirs_exist_ok=True)

    print("\n[*] [3/3] جاري نشر التغييرات مباشرة إلى GitHub Pages...")
    subprocess.run(["git", "add", "-A"], cwd=str(BASE_DIR), check=False)
    subprocess.run(["git", "commit", "-m", "feat(deploy): live site & portal sync to GitHub Pages"], cwd=str(BASE_DIR), check=False)
    subprocess.run(["git", "push", "origin", "main"], cwd=str(BASE_DIR), check=False)

    print("[OK] تم التحديث والنشر بنجاح على GitHub Pages!")
    print("👉 رابط البوابة المباشر: https://medon90ae.github.io/healing-touch-egypt/portal/")


def run_option_4():
    print("\n[*] 📂 جاري فتح أحدث حزمة نشر جاهزة ومفرزة للمنصات...")
    ready_dir = BASE_DIR / "media_assets" / "ready_to_publish"
    latest_marker = ready_dir / "LATEST_PACK_PATH.txt"
    target_pack = None

    if latest_marker.exists():
        try:
            p_text = latest_marker.read_text(encoding="utf-8").strip()
            if p_text and Path(p_text).exists():
                target_pack = Path(p_text)
        except Exception:
            pass

    if not target_pack and ready_dir.exists():
        recent_packs = sorted([d for d in ready_dir.iterdir() if d.is_dir() and d.name.startswith("202")], key=lambda x: x.name, reverse=True)
        if recent_packs:
            target_pack = recent_packs[0]

    if target_pack and target_pack.exists():
        print(f"[+] تم تحديد أحدث مجلد مؤرخ: {target_pack.name}")
        try:
            os.startfile(str(target_pack))
        except Exception:
            pass
    elif ready_dir.exists():
        try:
            os.startfile(str(ready_dir))
        except Exception:
            pass


def run_option_5():
    print("\n[*] 🌐 جاري فحص واستعراض كافة صفحات الهبوط (Landing Pages Directory)...")
    try:
        subprocess.run([VENV_PYTHON, "scripts/build_landing_pages_directory.py"], cwd=str(BASE_DIR))
    except Exception:
        pass
    md_file = BASE_DIR / "media_assets" / "LANDING_PAGES_DIRECTORY.md"
    if md_file.exists():
        try:
            os.startfile(str(md_file))
        except Exception:
            pass


def main():
    print_banner()
    try:
        choice = input("اختر رقم العملية المطلوبة (اضغط Enter لاختيار 1 للتشغيل الشامل): ").strip()
    except (EOFError, KeyboardInterrupt):
        return

    if not choice:
        choice = "1"

    actions = {
        "1": run_option_1,
        "2": run_option_2,
        "3": run_option_3,
        "4": run_option_4,
        "5": run_option_5,
    }

    action = actions.get(choice, run_option_1)
    action()
    print("\nاضغط Enter للخروج...")
    try:
        input()
    except Exception:
        pass


if __name__ == "__main__":
    main()
