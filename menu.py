# -*- coding: utf-8 -*-
"""
=============================================================================
🌿 هيلينج تاتش مصر | لوحة التحكم والمحرك الموحد الشامل (2026)
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
    print("        🌿 هيلينج تاتش مصر - لوحة التحكم والمحرك الموحد الشامل (2026)")
    print("=" * 70)
    print()
    print("  [1] التشغيل الشامل والنشر الفوري (استيعاب manual_inbox + بناء LPs + نشر GitHub وسوشيال)")
    print("  [2] تجهيز حملة اليوم والبرومبتات ومصادر البحث باختيار المنتج (Pomelli + Deep Research + PubMed)")
    print("  [3] معاينة وتجهيز الأصول واللاندنج بيدج بدون نشر (Dry Run)")
    print("  [4] فتح صندوق الاستقبال manual_inbox وملف البرومبتات")
    print("  [5] تحديث الموقع وتطبيق البوابة ونشر التغييرات مباشرة إلى GitHub Pages")
    print("  [6] استعراض وفحص سجل العملاء وحجوزات الاستشارات في Google Sheet")
    print("  [7] ربط وتفعيل حساب Reddit تلقائياً (لمرة واحدة فقط)")
    print("  [8] فتح أحدث منشور تم نشره على فيسبوك في المتصفح")
    print("  [9] 📋 فتح حزمة النشر الجاهزة الشاملة (YouTube + Blogger + Reddit)")
    print()
    print("=" * 70)


def run_option_1():
    print("\n[*] [1/5] جاري فحص manual_inbox واستيعاب الميديا وتوليد صفحات الهبوط (Multi-Angle LPs)...")
    subprocess.run([VENV_PYTHON, "antigravity_social_automation.py", "--mode", "auto-daily"], cwd=str(BASE_DIR))

    print("\n[*] [2/5] جاري إعادة بناء الموقع وخريطة السيو sitemap.xml والموسوعة الطبية...")
    subprocess.run([VENV_PYTHON, "github_seo_trend_engine.py", "--build-site"], cwd=str(BASE_DIR))

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
        subprocess.run(["git", "commit", "-m", "feat(deploy): update live clinical portal, landing pages, and ingested media"], cwd=str(BASE_DIR), check=False)
        subprocess.run(["git", "push", "origin", "main"], cwd=str(BASE_DIR), check=False)
        print("[+] 🚀 تم النشر بنجاح على GitHub Pages!")
    except Exception as e:
        print(f"[!] خطأ في رفع GitHub: {e}")

    print("\n[*] [5/5] جاري بث المنشورات والتوجيهات السريرية إلى منصات التواصل الاجتماعي (Facebook, Reddit, Blogger)...")
    subprocess.run([VENV_PYTHON, "antigravity_social_automation.py", "--mode", "publish"], cwd=str(BASE_DIR))

    # تجهيز حزمة النشر الجاهزة السريعة لريديت وبلوجر
    try:
        subprocess.run([VENV_PYTHON, "scripts/build_ready_to_publish_pack.py"], cwd=str(BASE_DIR), check=False)
    except Exception:
        pass

    print("\n" + "=" * 70)
    print("🎉 اكتمل النشر الشامل وتحديث كافة صفحات الموقع والأصول بنجاح!")
    print("👉 رابط البوابة الحية: https://medon90ae.github.io/healing-touch-egypt/portal/")
    print("👉 رابط الموقع الرئيسي: https://medon90ae.github.io/healing-touch-egypt/")
    print("=" * 70)


def run_option_2():
    print("\n[*] تجهيز حزمة البرومبتات والمصادر السريرية باختيار المنتج...")
    subprocess.run([VENV_PYTHON, "antigravity_social_automation.py", "--mode", "notebooklm"], cwd=str(BASE_DIR))
    prompts_txt = BASE_DIR / "media_assets" / "manual_inbox" / "PROMPTS_PACK_TODAY.txt"
    if prompts_txt.exists():
        try:
            os.startfile(str(prompts_txt))
        except Exception:
            pass


def run_option_3():
    print("\n[*] معاينة وتوليد الأصول واللاندنج بيدج بدون نشر فعلي (Dry Run)...")
    subprocess.run([VENV_PYTHON, "antigravity_social_automation.py", "--dry-run"], cwd=str(BASE_DIR))


def run_option_4():
    print("\n[*] فتح صندوق الاستقبال manual_inbox وملف البرومبتات...")
    inbox = BASE_DIR / "media_assets" / "manual_inbox"
    try:
        os.startfile(str(inbox))
    except Exception:
        pass
    prompts_txt = inbox / "PROMPTS_PACK_TODAY.txt"
    if prompts_txt.exists():
        try:
            os.startfile(str(prompts_txt))
        except Exception:
            pass


def run_option_5():
    print("\n[*] [1/3] جاري تحديث صفحات الموقع ومقالات السيو...")
    subprocess.run([VENV_PYTHON, "github_seo_trend_engine.py", "--build-site"], cwd=str(BASE_DIR))

    print("\n[*] [2/3] جاري بناء وتجميع تطبيق البوابة التفاعلية (Clinical Portal App)...")
    subprocess.run(["npm", "--prefix", "portal_app", "run", "build"], cwd=str(BASE_DIR), shell=True)
    portal_dist = BASE_DIR / "portal_app" / "dist"
    docs_portal = BASE_DIR / "docs" / "portal"
    if portal_dist.exists():
        import shutil
        shutil.copytree(str(portal_dist), str(docs_portal), dirs_exist_ok=True)

    print("\n[*] [3/3] جاري نشر التغييرات إلى GitHub Pages...")
    subprocess.run(["git", "add", "-A"], cwd=str(BASE_DIR), check=False)
    subprocess.run(["git", "commit", "-m", "feat(deploy): live site & portal sync to GitHub Pages"], cwd=str(BASE_DIR), check=False)
    subprocess.run(["git", "push", "origin", "main"], cwd=str(BASE_DIR), check=False)

    print("[OK] تم التحديث والنشر بنجاح على GitHub Pages!")
    print("👉 رابط البوابة المباشر: https://medon90ae.github.io/healing-touch-egypt/portal/")
    try:
        import webbrowser
        webbrowser.open("https://medon90ae.github.io/healing-touch-egypt/portal/")
    except Exception:
        pass


def run_option_6():
    print("\n[*] فحص الاتصال بسجل Google Sheet...")
    subprocess.run([VENV_PYTHON, "antigravity_social_automation.py", "--check-sheet"], cwd=str(BASE_DIR))
    import webbrowser
    webbrowser.open("https://docs.google.com/spreadsheets/d/12yAqzm-pSykfv7nRlvgocAHmwIYD_NPxqcNxrRKzA8k/edit?gid=513215731#gid=513215731")


def run_option_7():
    print("\n[*] ربط وتفويض حساب Reddit...")
    subprocess.run([VENV_PYTHON, "antigravity_social_automation.py", "--mode", "auth-reddit"], cwd=str(BASE_DIR))


def run_option_8():
    print("\n[*] فتح أحدث منشور تم نشره على فيسبوك...")
    subprocess.run([VENV_PYTHON, "antigravity_social_automation.py", "--mode", "open-latest"], cwd=str(BASE_DIR))


def run_option_9():
    print("\n[*] 📋 تجهيز وفتح حزمة النشر الشاملة (YouTube + Blogger + Reddit)...")
    ready_dir = BASE_DIR / "media_assets" / "ready_to_publish"
    ready_dir.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run([VENV_PYTHON, "scripts/build_ready_to_publish_pack.py"], cwd=str(BASE_DIR), check=False)
    except Exception:
        pass
    try:
        os.startfile(str(ready_dir))
    except Exception:
        pass
    # فتح روابط النشر في المتصفح تلقائياً لجميع المنصات
    import webbrowser
    webbrowser.open("https://studio.youtube.com/channel/UCcHqrSEET7IEhr9ueM8VELQ/videos/upload?d=ud")
    webbrowser.open("https://draft.blogger.com/blog/posts/6258225961862592152")
    webbrowser.open("https://www.reddit.com/r/u_Dull-Nectarine4963/submit")
    print("[+] تم فتح مجلد الأصول الجاهزة ونوافذ النشر المباشرة (YouTube + Blogger + Reddit) في المتصفح!")


def main():
    print_banner()
    try:
        choice = input("اختر رقم العملية المطلوبة (اضغط Enter لاختيار 1 للتشغيل والنشر الشامل): ").strip()
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
        "6": run_option_6,
        "7": run_option_7,
        "8": run_option_8,
        "9": run_option_9,
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
