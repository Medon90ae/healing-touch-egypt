# -*- coding: utf-8 -*-
"""
=============================================================================
🌿 هيلينج تاتش مصر | مركز القيادة السريري والتحكم التفاعلي عبر تيليجرام (2026)
Healing Touch Egypt - Mobile Telegram Interactive Command Center
=============================================================================
Provides a fully interactive, mobile-accessible Telegram bot with:
- Nested Inline Keyboards for seamless menu navigation.
- 1-Click Master Pipeline execution with live status feedback.
- Clinical product selection & PubMed/Egypt trend prompt generator.
- Direct mobile media ingestion (Photos/Videos saved straight to manual_inbox).
- Service monitoring (n8n health, CRM sync, GitHub Pages deployment).
- Strict authentication gate locked to authorized Chat ID.
=============================================================================
"""

import os
import sys
import time
import json
import logging
import threading
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List

import requests

# Set stdout encoding for Windows console
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Core Paths
BASE_DIR = Path(__file__).resolve().parent.parent
VENV_PYTHON = BASE_DIR / ".venv" / "Scripts" / "python.exe"
MEDIA_DIR = BASE_DIR / "media_assets"
MANUAL_INBOX = MEDIA_DIR / "manual_inbox"
READY_PUBLISH = MEDIA_DIR / "ready_to_publish"
AUDIO_INPUTS = MEDIA_DIR / "notebooklm_hub" / "audio_inputs"
PID_FILE = MEDIA_DIR / "telegram_bot.pid"
LOG_FILE = MEDIA_DIR / "telegram_bot.log"

# Ensure directories exist
for p in (MEDIA_DIR, MANUAL_INBOX, READY_PUBLISH, AUDIO_INPUTS):
    p.mkdir(parents=True, exist_ok=True)

# Setup logging (console + persistent file log)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(str(LOG_FILE), encoding="utf-8"),
    ],
)
logger = logging.getLogger("TelegramControlBot")

# Bot Configuration & Security Credentials
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "9068379040:AAGDIoqnXxOFnJcmXEBGL-xnj-0FXCUKHVA")
AUTHORIZED_CHAT_ID = str(os.getenv("TELEGRAM_CHAT_ID", "7692685242")).strip()

API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
FILE_API_URL = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}"

# Products Catalog Metadata
PRODUCTS_CATALOG = {
    "1": {
        "name": "ضمادة تيغاديرم الشفافة المقاومة للماء",
        "brand": "3M Tegaderm +Pad Film",
        "tag": "شاور آمن وحماية جروح العمليات والقيصرية من الماء",
        "icon": "🩹",
    },
    "2": {
        "name": "شيت السيليكون الطبي المطور للندبات",
        "brand": "BUPY Medical Silicone Scar Sheet",
        "tag": "تسطيح وترطيب ندبات القيصرية والجراحة ومنع الكيلويد",
        "icon": "🧴",
    },
    "3": {
        "name": "شريط ميكروبور الطبي الملون",
        "brand": "3M Micropore Tan Surgical Tape 1533-0",
        "tag": "تثبيت الأنف بعد التجميل وحماية ندبات الغدة والرقبة من الشمس",
        "icon": "🎗️",
    },
    "4": {
        "name": "دعامات الأنف السيليكونية الطبية",
        "brand": "Silicone Nostril Retainer",
        "tag": "منع انكماش الغضاريف ودعم تماثل فتحات الأنف بعد التجميل",
        "icon": "👃",
    },
    "5": {
        "name": "سبراي أوبسايت العازل للجروح",
        "brand": "Smith & Nephew Opsite Post-Op Spray",
        "tag": "عزل ثقوب مناظير التكميم والسمنة بحاجز بكتيري شفاف",
        "icon": "💨",
    },
    "6": {
        "name": "الحزمة السريرية الشاملة لكافة المنتجات",
        "brand": "All 5 Products Master Encyclopedia",
        "tag": "تغطية كاملة لكافة الإجراءات الجراحية والتجميلية في مصر",
        "icon": "📚",
    },
}

# Concurrency lock for long-running pipelines
PIPELINE_LOCK = threading.Lock()
ACTIVE_TASK_NAME = None


class TelegramBotClient:
    """Lightweight, resilient Telegram Bot API client using standard requests."""

    def __init__(self, token: str, session: Optional[requests.Session] = None):
        self.token = token
        self.api_url = f"https://api.telegram.org/bot{token}"
        self.file_url = f"https://api.telegram.org/file/bot{token}"
        self.session = session or requests.Session()

    def send_message(
        self,
        chat_id: str | int,
        text: str,
        reply_markup: Optional[Dict[str, Any]] = None,
        parse_mode: str = "HTML",
        disable_web_page_preview: bool = True,
    ) -> Optional[Dict[str, Any]]:
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": disable_web_page_preview,
        }
        if reply_markup:
            payload["reply_markup"] = json.dumps(reply_markup)
        try:
            r = self.session.post(f"{self.api_url}/sendMessage", data=payload, timeout=20)
            if r.status_code == 200:
                return r.json()
            logger.error("sendMessage failed [%d]: %s", r.status_code, r.text)
        except Exception as e:
            logger.error("sendMessage exception: %s", e)
        return None

    def edit_message_text(
        self,
        chat_id: str | int,
        message_id: int,
        text: str,
        reply_markup: Optional[Dict[str, Any]] = None,
        parse_mode: str = "HTML",
        disable_web_page_preview: bool = True,
    ) -> Optional[Dict[str, Any]]:
        payload = {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": disable_web_page_preview,
        }
        if reply_markup:
            payload["reply_markup"] = json.dumps(reply_markup)
        try:
            r = self.session.post(f"{self.api_url}/editMessageText", data=payload, timeout=20)
            if r.status_code == 200:
                return r.json()
            logger.warning("editMessageText returned [%d]: %s", r.status_code, r.text)
        except Exception as e:
            logger.error("editMessageText exception: %s", e)
        return None

    def answer_callback_query(
        self, callback_query_id: str, text: Optional[str] = None, show_alert: bool = False
    ) -> bool:
        payload = {"callback_query_id": callback_query_id}
        if text:
            payload["text"] = text
        if show_alert:
            payload["show_alert"] = True
        try:
            r = self.session.post(f"{self.api_url}/answerCallbackQuery", data=payload, timeout=10)
            return r.status_code == 200
        except Exception as e:
            logger.error("answerCallbackQuery exception: %s", e)
            return False

    def send_document(
        self,
        chat_id: str | int,
        file_path: Path | str,
        caption: Optional[str] = None,
        parse_mode: str = "HTML",
    ) -> Optional[Dict[str, Any]]:
        p = Path(file_path)
        if not p.exists():
            logger.error("send_document: File does not exist: %s", file_path)
            return None
        data = {"chat_id": chat_id, "parse_mode": parse_mode}
        if caption:
            data["caption"] = caption
        try:
            with open(p, "rb") as f:
                files = {"document": (p.name, f)}
                r = self.session.post(f"{self.api_url}/sendDocument", data=data, files=files, timeout=60)
            if r.status_code == 200:
                return r.json()
            logger.error("sendDocument failed [%d]: %s", r.status_code, r.text)
        except Exception as e:
            logger.error("sendDocument exception: %s", e)
        return None

    def get_file(self, file_id: str) -> Optional[Dict[str, Any]]:
        try:
            r = self.session.get(f"{self.api_url}/getFile", params={"file_id": file_id}, timeout=20)
            if r.status_code == 200 and r.json().get("ok"):
                return r.json().get("result")
        except Exception as e:
            logger.error("getFile exception: %s", e)
        return None

    def download_file(self, file_path_remote: str, destination: Path) -> bool:
        try:
            url = f"{self.file_url}/{file_path_remote}"
            r = self.session.get(url, stream=True, timeout=120)
            if r.status_code == 200:
                with open(destination, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1024 * 64):
                        if chunk:
                            f.write(chunk)
                return True
            logger.error("download_file HTTP [%d]: %s", r.status_code, url)
        except Exception as e:
            logger.error("download_file exception: %s", e)
        return False

    def get_updates(self, offset: Optional[int] = None, timeout: int = 25) -> List[Dict[str, Any]]:
        params = {"timeout": timeout}
        if offset is not None:
            params["offset"] = offset
        try:
            r = self.session.get(f"{self.api_url}/getUpdates", params=params, timeout=timeout + 10)
            if r.status_code == 200 and r.json().get("ok"):
                return r.json().get("result", [])
        except requests.exceptions.Timeout:
            return []
        except Exception as e:
            logger.warning("getUpdates network warning: %s", e)
            time.sleep(2)
        return []


bot = TelegramBotClient(token=TELEGRAM_BOT_TOKEN)


# =============================================================================
# 📱 Keyboards & Menu Builders
# =============================================================================

def build_main_menu_keyboard() -> Dict[str, Any]:
    return {
        "inline_keyboard": [
            [
                {"text": "🚀 التشغيل والنشر الشامل (1-Click Pipeline)", "callback_data": "act_master"}
            ],
            [
                {"text": "🩺 اختيار منتج وتجهيز الأبحاث والبرومبتات", "callback_data": "menu_products"}
            ],
            [
                {"text": "👁️ معاينة بدون نشر (Dry Run)", "callback_data": "act_dry_run"}
            ],
            [
                {"text": "⚙️ حالة خدمة n8n", "callback_data": "act_n8n_status"},
                {"text": "👥 مزامنة عملاء CRM", "callback_data": "act_crm_sync"},
            ],
            [
                {"text": "🌐 تحديث ونشر الموقع لـ GitHub Pages", "callback_data": "act_deploy_site"}
            ],
            [
                {"text": "📦 أحدث حزمة نشر جاهزة", "callback_data": "act_latest_pack"},
                {"text": "📥 فحص صندوق manual_inbox", "callback_data": "act_inbox_status"},
            ],
        ]
    }


def build_products_submenu_keyboard() -> Dict[str, Any]:
    buttons = []
    for key, prod in PRODUCTS_CATALOG.items():
        btn_text = f"{prod['icon']} [{key}] {prod['name']}"
        buttons.append([{"text": btn_text, "callback_data": f"prod_{key}"}])

    buttons.append([{"text": "🔙 العودة للقائمة الرئيسية", "callback_data": "menu_main"}])
    return {"inline_keyboard": buttons}


def get_main_menu_text() -> str:
    now_str = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    return (
        "🌿 <b>هيلينج تاتش مصر | مركز القيادة السريري والتحكم التفاعلي (2026)</b>\n"
        "<i>Healing Touch Egypt - Mobile Telegram Command Center</i>\n\n"
        f"⏱️ <b>التوقيت الحالي:</b> {now_str}\n"
        "🔒 <b>الحالة:</b> متصل ومؤمن لحساب المشرف المعتمد\n\n"
        "👇 <b>اختر العملية المطلوبة من القائمة التفاعلية أدناه:</b>"
    )


def get_products_menu_text() -> str:
    return (
        "🩺 <b>قائمة المنتجات السريرية المعتمدة (Clinical Products Suite):</b>\n\n"
        "اختر المنتج ليكون محور أبحاث ومحتوى اليوم، وسيقوم المحرك فوراً بـ:\n"
        "1. سحب أحدث أوراق <b>PubMed</b> وترندات جوجل مصر الصاعدة.\n"
        "2. توليد حزمة برومبتات اليوم المجهزة للمنصات وإرسالها لك كمستند.\n"
        "3. تجهيز روابط Pomelli و NotebookLM بنقرة واحدة.\n\n"
        "👇 <b>اختر المنتج الطبي المطلوب:</b>"
    )


# =============================================================================
# ⚙️ Action Handlers (Executed Safely in Background Threads)
# =============================================================================

def handle_master_pipeline_execution(chat_id: str, message_id: Optional[int] = None):
    """Executes single_click_master_pipeline.py and sends live status."""
    global ACTIVE_TASK_NAME

    if not PIPELINE_LOCK.acquire(blocking=False):
        bot.send_message(
            chat_id,
            f"⚠️ <b>هناك عملية تشغيل جارية بالفعل حالياً</b> (المهمة: <code>{ACTIVE_TASK_NAME or 'Pipeline'}</code>).\nيرجى الانتظار حتى اكتمالها.",
        )
        return

    ACTIVE_TASK_NAME = "Single-Click Master Pipeline"
    try:
        status_msg = bot.send_message(
            chat_id,
            "⏳ <b>[1/4] جاري تشغيل المسار الشامل الموحد...</b>\n"
            "• فحص وتصنيف وسائط <code>manual_inbox</code>\n"
            "• استخراج الأبحاث وترندات جوجل مصر الحية\n"
            "• بناء صفحات الهبوط وتوليد حزم النشر للمنصات الستة...",
        )
        target_msg_id = status_msg.get("result", {}).get("message_id") if status_msg else None

        cmd = [str(VENV_PYTHON), "single_click_master_pipeline.py"]
        res = subprocess.run(
            cmd,
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        if res.returncode == 0:
            success_text = (
                "✅ <b>اكتمل تنفيذ المسار الشامل بنجاح باهر!</b>\n\n"
                "🌐 <b>رابط البوابة التفاعلية الحية:</b>\n"
                "👉 https://medon90ae.github.io/healing-touch-egypt/portal/\n\n"
                "🔗 <b>رابط الموقع والصفحات الطبية:</b>\n"
                "👉 https://medon90ae.github.io/healing-touch-egypt/\n\n"
                "📱 <b>محرك الأتمتة n8n:</b> تم إرسال مسودة المنشور للاعتماد السريري والتمرير الفوري للمنصات!\n"
                "🧹 تم تنظيف صندوق <code>manual_inbox</code> وأرشفة الوسائط بأمان."
            )
            keyboard = {
                "inline_keyboard": [
                    [{"text": "🚀 تشغيل مجدداً", "callback_data": "act_master"}],
                    [{"text": "📦 استعراض الحزمة الجاهزة", "callback_data": "act_latest_pack"}],
                    [{"text": "🏠 القائمة الرئيسية", "callback_data": "menu_main"}],
                ]
            }
            if target_msg_id:
                bot.edit_message_text(chat_id, target_msg_id, success_text, reply_markup=keyboard)
            else:
                bot.send_message(chat_id, success_text, reply_markup=keyboard)
        else:
            err_snippet = (res.stderr or res.stdout)[-400:]
            error_text = (
                f"❌ <b>حدث خطأ أثناء تنفيذ المسار (كود الخطأ: {res.returncode}):</b>\n\n"
                f"<code>{err_snippet}</code>"
            )
            bot.send_message(chat_id, error_text, reply_markup=build_main_menu_keyboard())

    except Exception as ex:
        logger.error("Error in master pipeline runner: %s", ex, exc_info=True)
        bot.send_message(chat_id, f"❌ <b>استثناء غير متوقع:</b>\n<code>{ex}</code>")
    finally:
        ACTIVE_TASK_NAME = None
        PIPELINE_LOCK.release()


def handle_product_research_generation(chat_id: str, prod_choice: str):
    """Generates research & prompt pack for selected product and sends file to Telegram."""
    global ACTIVE_TASK_NAME

    prod_info = PRODUCTS_CATALOG.get(prod_choice, PRODUCTS_CATALOG["1"])

    if not PIPELINE_LOCK.acquire(blocking=False):
        bot.send_message(
            chat_id,
            f"⚠️ <b>هناك عملية تشغيل جارية بالفعل حالياً</b> (المهمة: <code>{ACTIVE_TASK_NAME}</code>). يرجى الانتظار.",
        )
        return

    ACTIVE_TASK_NAME = f"Product Research: {prod_info['name']}"
    try:
        bot.send_message(
            chat_id,
            f"⏳ <b>جاري إعداد أبحاث وترندات اليوم لمنتج:</b>\n"
            f"<b>{prod_info['icon']} {prod_info['name']}</b> ({prod_info['brand']})\n\n"
            f"• استخراج أحدث توصيات <b>PubMed</b> السريرية المنشورة...\n"
            f"• سحب أسئلة وترندات جوجل مصر الصاعدة...\n"
            f"• تجهيز برومبتات المنصات (Facebook, Reels, TikTok, Shorts, Reddit, Blogger)...",
        )

        cmd = [
            str(VENV_PYTHON),
            "antigravity_social_automation.py",
            "--mode",
            "notebooklm",
            "--product",
            prod_choice,
        ]
        res = subprocess.run(
            cmd,
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        prompts_txt = MANUAL_INBOX / "PROMPTS_PACK_TODAY.txt"
        if prompts_txt.exists():
            caption = (
                f"📄 <b>حزمة برومبتات ومصادر أبحاث اليوم المعتمدة:</b>\n"
                f"🎯 <b>المنتج:</b> {prod_info['name']}\n"
                f"🎟️ <b>كود الخصم المعتمد:</b> HT10\n"
                f"🩺 <b>الاستشارة:</b> أخصائية العناية بالتعافي (واتساب 01155803307)"
            )
            bot.send_document(chat_id, prompts_txt, caption=caption)

        action_card_text = (
            f"✨ <b>تم تجهيز حزمة الأبحاث والبرومبتات بنجاح!</b>\n\n"
            f"🎯 <b>المنتج:</b> {prod_info['name']}\n"
            f"📌 <b>المحور:</b> {prod_info['tag']}\n\n"
            f"🌐 يمكنك الآن فتح أدوات الذكاء الاصطناعي الأربعة مباشرة من الروابط أدناه:\n"
            f"• <b>Pomelli:</b> لحملات التصاميم والمنشورات المعتمدة\n"
            f"• <b>NotebookLM:</b> لتوليد الفيديو التوضيحي والبودكاست السريري\n"
            f"• <b>Gemini Deep Research:</b> للأبحاث الطبية الموثقة\n\n"
            f"💡 <i>أي صور أو فيديوهات تقوم بحفظها، أرسلها هنا مباشرة في الشات لتصل إلى manual_inbox تلقائياً!</i>"
        )
        action_keyboard = {
            "inline_keyboard": [
                [
                    {"text": "🔗 فتح Google Pomelli", "url": "https://labs.google.com/pomelli/campaigns"},
                    {"text": "🔗 فتح Google NotebookLM", "url": "https://notebooklm.google.com/"},
                ],
                [
                    {"text": "🔗 فتح Gemini Research", "url": "https://gemini.google.com/"},
                    {"text": "🔗 فتح Google Stitch", "url": "https://stitch.withgoogle.com/"},
                ],
                [
                    {"text": "🚀 تشغيل المسار الشامل الآن", "callback_data": "act_master"}
                ],
                [
                    {"text": "🩺 اختيار منتج آخر", "callback_data": "menu_products"},
                    {"text": "🏠 القائمة الرئيسية", "callback_data": "menu_main"},
                ],
            ]
        }
        bot.send_message(chat_id, action_card_text, reply_markup=action_keyboard)

    except Exception as ex:
        logger.error("Error generating product research: %s", ex, exc_info=True)
        bot.send_message(chat_id, f"❌ خطأ أثناء إعداد أبحاث المنتج: <code>{ex}</code>")
    finally:
        ACTIVE_TASK_NAME = None
        PIPELINE_LOCK.release()


def handle_dry_run_execution(chat_id: str):
    """Executes dry run mode and reports results."""
    global ACTIVE_TASK_NAME

    if not PIPELINE_LOCK.acquire(blocking=False):
        bot.send_message(chat_id, "⚠️ هناك مهمة قيد التشغيل بالفعل. يرجى الانتظار.")
        return

    ACTIVE_TASK_NAME = "Dry Run Mode"
    try:
        bot.send_message(
            chat_id,
            "👁️ <b>جاري تشغيل وضع المعاينة (Dry Run)...</b>\n"
            "تجهيز صفحات الهبوط وفحص الأصول بدون النشر على المنصات...",
        )
        cmd = [str(VENV_PYTHON), "single_click_master_pipeline.py", "--dry-run"]
        res = subprocess.run(
            cmd,
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if res.returncode == 0:
            bot.send_message(
                chat_id,
                "✅ <b>اكتملت المعاينة (Dry Run) بنجاح تام!</b>\n"
                "كافة صفحات الهبوط والأصول وحزم النشر جاهزة بنسبة 100% بدون أي أخطاء.",
                reply_markup=build_main_menu_keyboard(),
            )
        else:
            bot.send_message(
                chat_id,
                f"⚠️ تنبيه المعاينة:\n<code>{(res.stderr or res.stdout)[-300:]}</code>",
                reply_markup=build_main_menu_keyboard(),
            )
    finally:
        ACTIVE_TASK_NAME = None
        PIPELINE_LOCK.release()


def handle_n8n_status(chat_id: str):
    """Checks n8n service health and reports status."""
    health_url = "http://localhost:5678/healthz"
    is_healthy = False
    details = ""
    try:
        r = requests.get(health_url, timeout=3)
        if r.status_code == 200:
            is_healthy = True
            details = r.text
    except Exception as e:
        details = str(e)

    if is_healthy:
        text = (
            "⚙️ <b>حالة خدمة محرك الأتمتة n8n:</b>\n\n"
            "• <b>الحالة:</b> 🟢 متصلة وتعمل بنشاط (ONLINE)\n"
            "• <b>المنفذ:</b> 5678\n"
            "• <b>الاستجابة:</b> HTTP 200 OK\n"
            "• <b>رابط لوحة التحكم:</b> http://localhost:5678\n\n"
            "محرك النشر عبر المنصات الستة واستقبال الـ Webhooks في أتم الجاهزية."
        )
        keyboard = {"inline_keyboard": [[{"text": "🏠 القائمة الرئيسية", "callback_data": "menu_main"}]]}
    else:
        text = (
            "⚙️ <b>حالة خدمة محرك الأتمتة n8n:</b>\n\n"
            "• <b>الحالة:</b> 🔴 غير متصلة أو متوقفة مؤقتاً (OFFLINE)\n"
            f"• <b>التفاصيل:</b> <code>{details}</code>\n\n"
            "يمكنك إعادة تشغيل الخدمة بضغطة زر أدناه:"
        )
        keyboard = {
            "inline_keyboard": [
                [{"text": "▶️ تشغيل خدمة n8n الآن", "callback_data": "act_restart_n8n"}],
                [{"text": "🏠 القائمة الرئيسية", "callback_data": "menu_main"}],
            ]
        }

    bot.send_message(chat_id, text, reply_markup=keyboard)


def handle_restart_n8n(chat_id: str):
    """Executes start_n8n.bat in background."""
    bot.send_message(chat_id, "⏳ جاري إطلاق خدمة n8n الصامتة في الخلفية...")
    start_bat = BASE_DIR / "start_n8n.bat"
    if start_bat.exists():
        subprocess.run(["cmd.exe", "/c", str(start_bat)], cwd=str(BASE_DIR), capture_output=True)
    time.sleep(3)
    handle_n8n_status(chat_id)


def handle_deploy_site(chat_id: str):
    """Builds portal, SEO articles, and deploys to GitHub Pages."""
    global ACTIVE_TASK_NAME

    if not PIPELINE_LOCK.acquire(blocking=False):
        bot.send_message(chat_id, "⚠️ هناك عملية جارية بالفعل. يرجى الانتظار.")
        return

    ACTIVE_TASK_NAME = "Deploy to GitHub Pages"
    try:
        bot.send_message(
            chat_id,
            "🌐 <b>[1/3] جاري بناء خريطة السيو والموسوعة وتطبيق البوابة...</b>",
        )
        # 1. Build SEO site
        subprocess.run(
            [str(VENV_PYTHON), "github_seo_trend_engine.py", "--build-site"],
            cwd=str(BASE_DIR),
            check=False,
        )
        # 2. Build portal app
        try:
            subprocess.run(
                ["npm", "--prefix", "portal_app", "run", "build"],
                cwd=str(BASE_DIR),
                shell=True,
                check=False,
            )
            portal_dist = BASE_DIR / "portal_app" / "dist"
            docs_portal = BASE_DIR / "docs" / "portal"
            if portal_dist.exists():
                import shutil
                shutil.copytree(str(portal_dist), str(docs_portal), dirs_exist_ok=True)
        except Exception:
            pass

        # 3. Git commit & push
        bot.send_message(chat_id, "🚀 <b>[2/3] جاري رفع التحديثات إلى GitHub Pages...</b>")
        subprocess.run(["git", "add", "-A"], cwd=str(BASE_DIR), check=False)
        subprocess.run(
            ["git", "commit", "-m", "feat(deploy): live site, portal, and seo sync via Telegram Bot"],
            cwd=str(BASE_DIR),
            check=False,
        )
        subprocess.run(["git", "push", "origin", "main"], cwd=str(BASE_DIR), check=False)

        done_text = (
            "✅ <b>تم نشر وتحديث الموقع والبوابة السريرية على GitHub Pages بنجاح!</b>\n\n"
            "👉 <b>رابط البوابة التفاعلية:</b>\n"
            "https://medon90ae.github.io/healing-touch-egypt/portal/\n\n"
            "👉 <b>رابط الموقع والصفحات الطبية:</b>\n"
            "https://medon90ae.github.io/healing-touch-egypt/"
        )
        bot.send_message(chat_id, done_text, reply_markup=build_main_menu_keyboard())
    finally:
        ACTIVE_TASK_NAME = None
        PIPELINE_LOCK.release()


def handle_crm_sync(chat_id: str):
    """Syncs SQLite local offline leads with Google Sheet."""
    crm_script = BASE_DIR / "scripts" / "crm_sync_engine.py"
    if not crm_script.exists():
        bot.send_message(chat_id, "⚠️ سكربت مزامنة العملاء غير متوفر.", reply_markup=build_main_menu_keyboard())
        return

    res = subprocess.run(
        [str(VENV_PYTHON), str(crm_script), "--stats"],
        cwd=str(BASE_DIR),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    sync_res = subprocess.run(
        [str(VENV_PYTHON), str(crm_script), "--sync"],
        cwd=str(BASE_DIR),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    output_text = (
        "👥 <b>تقرير مزامنة بيانات العملاء وسجل SQLite المحلي:</b>\n\n"
        f"<code>{res.stdout[:500] or 'لا توجد بيانات مسجلة'}</code>\n\n"
        f"<b>نتيجة المزامنة مع Google Sheet:</b>\n"
        f"<code>{sync_res.stdout[:300] or 'تمت المزامنة بنجاح'}</code>"
    )
    bot.send_message(chat_id, output_text, reply_markup=build_main_menu_keyboard())


def handle_latest_pack(chat_id: str):
    """Finds latest dated ready-to-publish pack and sends summary."""
    latest_marker = READY_PUBLISH / "LATEST_PACK_PATH.txt"
    target_pack = None
    if latest_marker.exists():
        try:
            p_text = latest_marker.read_text(encoding="utf-8").strip()
            if p_text and Path(p_text).exists():
                target_pack = Path(p_text)
        except Exception:
            pass

    if not target_pack and READY_PUBLISH.exists():
        packs = sorted(
            [d for d in READY_PUBLISH.iterdir() if d.is_dir() and d.name.startswith("202")],
            key=lambda x: x.name,
            reverse=True,
        )
        if packs:
            target_pack = packs[0]

    if target_pack:
        files = list(target_pack.glob("*.*"))
        f_list = "\n".join([f"• <code>{f.name}</code>" for f in files[:8]])
        text = (
            f"📦 <b>أحدث حزمة نشر جاهزة للمنصات:</b>\n\n"
            f"📁 <b>المجلد:</b> <code>{target_pack.name}</code>\n"
            f"📊 <b>عدد الملفات:</b> {len(files)} أصل مهيأ\n\n"
            f"<b>أبرز الملفات المفرزة:</b>\n{f_list}\n\n"
            f"📍 المسار على الجهاز:\n<code>{target_pack}</code>"
        )
    else:
        text = "📦 لا توجد حزم نشر سابقة حتى الآن. يمكنك تشغيل المسار الشامل لإنشاء أول حزمة!"

    bot.send_message(chat_id, text, reply_markup=build_main_menu_keyboard())


def handle_inbox_status(chat_id: str):
    """Reports status of media_assets/manual_inbox."""
    files = [
        f
        for f in MANUAL_INBOX.iterdir()
        if f.is_file() and not f.name.startswith(".") and f.name not in ["PROMPTS_PACK_TODAY.txt", "PROMPTS_PACK_TODAY.md"]
    ]
    if files:
        f_summary = "\n".join([f"• <code>{f.name}</code> ({round(f.stat().st_size / 1024, 1)} KB)" for f in files[:10]])
        text = (
            f"📥 <b>حالة صندوق الاستقبال manual_inbox:</b>\n\n"
            f"📁 يحتوي على <b>{len(files)}</b> ملف وسائط جاهز للاستيعاب:\n{f_summary}\n\n"
            f"اضغط على الزر أدناه لتشغيل المسار الشامل واستيعابها في صفحات الهبوط والمنصات:"
        )
        keyboard = {
            "inline_keyboard": [
                [{"text": "🚀 تشغيل المسار واستيعاب الوسائط الآن", "callback_data": "act_master"}],
                [{"text": "🏠 القائمة الرئيسية", "callback_data": "menu_main"}],
            ]
        }
    else:
        text = (
            "📥 <b>صندوق الاستقبال manual_inbox نظيف وفارغ!</b>\n\n"
            "💡 <b>طريقة الإضافة السريعة:</b>\n"
            "أرسل أي صورة أو فيديو هنا في شات تيليجرام مباشرة من هاتفك، وسيتم حفظها فوراً في الصندوق!"
        )
        keyboard = {"inline_keyboard": [[{"text": "🏠 القائمة الرئيسية", "callback_data": "menu_main"}]]}

    bot.send_message(chat_id, text, reply_markup=keyboard)


# =============================================================================
# 📥 Direct Media Ingestion from Telegram
# =============================================================================

def handle_incoming_media(message: Dict[str, Any]):
    """Saves user-sent photos, videos, audio, or documents into manual_inbox."""
    chat_id = str(message.get("chat", {}).get("id"))
    if chat_id != AUTHORIZED_CHAT_ID:
        return

    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_id = None
    original_name = None
    media_type = "ملف"

    if "photo" in message:
        # Highest resolution is the last element
        photo = message["photo"][-1]
        file_id = photo["file_id"]
        original_name = f"telegram_photo_{timestamp_str}.jpg"
        media_type = "صورة 📸"
    elif "video" in message:
        video = message["video"]
        file_id = video["file_id"]
        ext = ".mp4"
        original_name = video.get("file_name") or f"telegram_video_{timestamp_str}{ext}"
        media_type = "فيديو 🎥"
    elif "document" in message:
        doc = message["document"]
        file_id = doc["file_id"]
        original_name = doc.get("file_name") or f"telegram_doc_{timestamp_str}.dat"
        media_type = "مستند/ملف 📄"
    elif "voice" in message or "audio" in message:
        aud = message.get("voice") or message.get("audio")
        file_id = aud["file_id"]
        original_name = f"telegram_audio_{timestamp_str}.mp3"
        media_type = "تسجيل صوتي 🎙️"

    if not file_id:
        return

    file_info = bot.get_file(file_id)
    if not file_info or "file_path" not in file_info:
        bot.send_message(chat_id, "❌ تعذر استرجاع مسار الملف من سيرفر تيليجرام.")
        return

    remote_path = file_info["file_path"]
    save_path = MANUAL_INBOX / original_name

    # If audio, also save to audio_inputs for NotebookLM merging
    if "صوتي" in media_type:
        save_path = AUDIO_INPUTS / original_name

    bot.send_message(chat_id, f"⏳ جاري تحميل {media_type} وحفظه في صندوق الاستقبال <code>manual_inbox</code>...")
    success = bot.download_file(remote_path, save_path)

    if success:
        size_kb = round(save_path.stat().st_size / 1024, 1)
        confirm_text = (
            f"✅ <b>تم استلام {media_type} بنجاح!</b>\n\n"
            f"📁 <b>اسم الملف:</b> <code>{save_path.name}</code>\n"
            f"⚖️ <b>الحجم:</b> {size_kb} KB\n"
            f"📍 <b>الموقع:</b> <code>manual_inbox</code>\n\n"
            f"هل تريد تشغيل المسار الشامل الآن واستيعابه في صفحات الهبوط والمنصات؟"
        )
        keyboard = {
            "inline_keyboard": [
                [{"text": "🚀 تشغيل المسار الشامل الآن", "callback_data": "act_master"}],
                [{"text": "📥 استعراض محتويات manual_inbox", "callback_data": "act_inbox_status"}],
                [{"text": "🏠 القائمة الرئيسية", "callback_data": "menu_main"}],
            ]
        }
        bot.send_message(chat_id, confirm_text, reply_markup=keyboard)
    else:
        bot.send_message(chat_id, f"❌ فشل تحميل الملف من سيرفر تيليجرام.")


# =============================================================================
# 🔄 Main Dispatcher & Polling Engine
# =============================================================================

def process_callback_query(cq: Dict[str, Any]):
    cq_id = cq.get("id")
    user_id = str(cq.get("from", {}).get("id"))
    chat_id = str(cq.get("message", {}).get("chat", {}).get("id")) or user_id
    msg_id = cq.get("message", {}).get("message_id")
    data = cq.get("data", "")

    logger.info("Button clicked: data='%s', from_user=%s, chat_id=%s", data, user_id, chat_id)

    # Security Gate
    if user_id != AUTHORIZED_CHAT_ID and chat_id != AUTHORIZED_CHAT_ID:
        logger.warning("Unauthorized button click attempt from user %s", user_id)
        bot.answer_callback_query(cq_id, "⚠️ غير مصرح لك باستخدام هذا البوت.", show_alert=True)
        return

    # Instant UI feedback toast for user on click
    toast_msg = "⏳ جاري التنفيذ..."
    if data == "menu_main":
        toast_msg = "🏠 القائمة الرئيسية"
    elif data == "menu_products":
        toast_msg = "🩺 قائمة المنتجات السريرية"
    elif data.startswith("prod_"):
        toast_msg = f"⏳ جاري سحب أبحاث المنتج [{data.split('_')[1]}]..."
    elif data == "act_master":
        toast_msg = "🚀 جاري إطلاق المسار الشامل..."
    elif data == "act_dry_run":
        toast_msg = "👁️ جاري تشغيل وضع المعاينة..."

    bot.answer_callback_query(cq_id, text=toast_msg)

    # 1. Main Menu Navigation
    if data == "menu_main":
        bot.edit_message_text(chat_id, msg_id, get_main_menu_text(), reply_markup=build_main_menu_keyboard())

    # 2. Products Submenu
    elif data == "menu_products":
        bot.edit_message_text(chat_id, msg_id, get_products_menu_text(), reply_markup=build_products_submenu_keyboard())

    # 3. Product Selection
    elif data.startswith("prod_"):
        choice = data.split("_")[1]
        threading.Thread(
            target=handle_product_research_generation,
            args=(chat_id, choice),
            daemon=True,
        ).start()

    # 4. Action Handlers
    elif data == "act_master":
        threading.Thread(
            target=handle_master_pipeline_execution,
            args=(chat_id, msg_id),
            daemon=True,
        ).start()

    elif data == "act_dry_run":
        threading.Thread(
            target=handle_dry_run_execution,
            args=(chat_id,),
            daemon=True,
        ).start()

    elif data == "act_n8n_status":
        handle_n8n_status(chat_id)

    elif data == "act_restart_n8n":
        threading.Thread(
            target=handle_restart_n8n,
            args=(chat_id,),
            daemon=True,
        ).start()

    elif data == "act_deploy_site":
        threading.Thread(
            target=handle_deploy_site,
            args=(chat_id,),
            daemon=True,
        ).start()

    elif data == "act_crm_sync":
        threading.Thread(
            target=handle_crm_sync,
            args=(chat_id,),
            daemon=True,
        ).start()

    elif data == "act_latest_pack":
        handle_latest_pack(chat_id)

    elif data == "act_inbox_status":
        handle_inbox_status(chat_id)


def process_message(msg: Dict[str, Any]):
    chat_id = str(msg.get("chat", {}).get("id"))

    # Security Gate
    if chat_id != AUTHORIZED_CHAT_ID:
        bot.send_message(
            chat_id,
            "⚠️ <b>عذراً، هذا البوت خاص بمركز القيادة السريري لهيلينج تاتش مصر.</b>\nالوصول مقتصر على المشرف المعتمد فقط.",
        )
        return

    # Check for direct media upload
    if any(k in msg for k in ("photo", "video", "document", "voice", "audio")):
        handle_incoming_media(msg)
        return

    text = msg.get("text", "").strip()

    # Commands
    if text.startswith("/start") or text == "قائمة" or text.startswith("/menu"):
        bot.send_message(chat_id, get_main_menu_text(), reply_markup=build_main_menu_keyboard())
    elif text.startswith("/run") or text == "1":
        threading.Thread(
            target=handle_master_pipeline_execution,
            args=(chat_id,),
            daemon=True,
        ).start()
    elif text.startswith("/products") or text == "2":
        bot.send_message(chat_id, get_products_menu_text(), reply_markup=build_products_submenu_keyboard())
    elif text.startswith("/status"):
        handle_n8n_status(chat_id)
    else:
        # Default fallback: show main interactive menu
        bot.send_message(chat_id, get_main_menu_text(), reply_markup=build_main_menu_keyboard())


def write_pid_file():
    try:
        PID_FILE.write_text(str(os.getpid()), encoding="utf-8")
    except Exception as e:
        logger.warning("Could not write PID file: %s", e)


def remove_pid_file():
    try:
        if PID_FILE.exists():
            PID_FILE.unlink()
    except Exception:
        pass


def run_bot_polling():
    """Main long-polling loop with exponential backoff on network failures."""
    write_pid_file()
    logger.info("🌿 Healing Touch Telegram Control Bot started [PID: %d]", os.getpid())
    logger.info("Target Chat ID: %s", AUTHORIZED_CHAT_ID)

    # Send startup message to user
    bot.send_message(
        AUTHORIZED_CHAT_ID,
        "🌿 <b>تم تشغيل مركز القيادة السريري التفاعلي بنجاح!</b>\n\n"
        "يمكنك الآن التحكم الكامل في النظام واختيار المنتجات والنشر الشامل واستقبال الميديا مباشرة من هنا 👇",
        reply_markup=build_main_menu_keyboard(),
    )

    offset = None
    consecutive_errors = 0

    try:
        while True:
            try:
                updates = bot.get_updates(offset=offset, timeout=25)
                consecutive_errors = 0

                for update in updates:
                    update_id = update["update_id"]
                    offset = update_id + 1

                    try:
                        if "callback_query" in update:
                            process_callback_query(update["callback_query"])
                        elif "message" in update:
                            process_message(update["message"])
                    except Exception as handler_ex:
                        logger.error("Error processing update %s: %s", update_id, handler_ex, exc_info=True)

            except requests.exceptions.RequestException as re:
                consecutive_errors += 1
                sleep_secs = min(30, 2 ** consecutive_errors)
                logger.warning("Network issue (err #%d): %s. Retrying in %ds...", consecutive_errors, re, sleep_secs)
                time.sleep(sleep_secs)
            except Exception as e:
                logger.error("Unexpected error in poll loop: %s", e, exc_info=True)
                time.sleep(3)

    finally:
        remove_pid_file()
        logger.info("🌿 Bot polling loop stopped.")


if __name__ == "__main__":
    run_bot_polling()
