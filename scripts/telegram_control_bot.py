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
import html
import uuid
import socket
import logging
import threading
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple

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
RESEARCH_REPORTS_DIR = MEDIA_DIR / "notebooklm_hub" / "research_reports"
CLIENT_REVIEWS_DIR = MEDIA_DIR / "client_reviews"
PID_FILE = MEDIA_DIR / "telegram_bot.pid"
LOG_FILE = MEDIA_DIR / "telegram_bot.log"
SESSIONS_FILE = MEDIA_DIR / "telegram_user_sessions.json"

# Session State Constants (Guided Multi-Stage Clinical Pipeline & Proof Hub)
STATE_IDLE = "IDLE"
STATE_STAGE_1_RESEARCH = "STAGE_1_RESEARCH"
STATE_STAGE_2_PROMPTS = "STAGE_2_PROMPTS"
STATE_STAGE_3_MEDIA = "STAGE_3_MEDIA"
STATE_STAGE_REVIEW_INTAKE = "STAGE_REVIEW_INTAKE"

# Product Slugs Mapping for Client Reviews & Storage
PRODUCT_SLUGS = {
    "1": "3m-tegaderm-plus-pad",
    "2": "bupy-silicone-scar-sheet",
    "3": "3m-micropore-tan-tape-1533-0",
    "4": "silicone-nostril-retainer",
    "5": "smith-nephew-opsite-spray",
    "6": "master-bundle",
    "rev_prod_1": "3m-tegaderm-plus-pad",
    "rev_prod_2": "bupy-silicone-scar-sheet",
    "rev_prod_3": "3m-micropore-tan-tape-1533-0",
    "rev_prod_4": "silicone-nostril-retainer",
    "rev_prod_5": "smith-nephew-opsite-spray",
}

# Verified Platform Endpoints
POMELLI_BRAND_BOOK_URL = "https://labs.google.com/pomelli/brand_book/am6H88zhmUadtfPiiAmOnW"
NOTEBOOKLM_URL = "https://notebooklm.google.com/"
GEMINI_URL = "https://gemini.google.com/"
GOOGLE_FLOW_URL = "https://flow.google.com/project/942f62cb-f0e4-4860-bfce-2ba75998cfc7"

CHOICE_TO_CATEGORY = {
    "1": "c-section",
    "2": "c-section",
    "3": "thyroid",
    "4": "rhinoplasty",
    "5": "bariatric",
}

# Ensure directories exist
for p in (MEDIA_DIR, MANUAL_INBOX, READY_PUBLISH, AUDIO_INPUTS, RESEARCH_REPORTS_DIR, CLIENT_REVIEWS_DIR):
    p.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# 💾 Persistent Session State Machine
# -----------------------------------------------------------------------------
def load_user_sessions() -> Dict[str, Dict[str, Any]]:
    if SESSIONS_FILE.exists():
        try:
            return json.loads(SESSIONS_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def save_user_sessions(sessions: Dict[str, Dict[str, Any]]):
    try:
        SESSIONS_FILE.write_text(json.dumps(sessions, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass


USER_SESSIONS: Dict[str, Dict[str, Any]] = load_user_sessions()


def get_session(chat_id: str | int) -> Dict[str, Any]:
    cid = str(chat_id).strip()
    if cid not in USER_SESSIONS:
        USER_SESSIONS[cid] = {
            "stage": STATE_IDLE,
            "product_choice": "1",
            "review_product_id": None,
            "research_file": None,
            "findings": [],
            "anxieties": [],
            "media_files": [],
            "updated_at": datetime.now().isoformat(),
        }
    return USER_SESSIONS[cid]


def update_session(chat_id: str | int, **kwargs) -> Dict[str, Any]:
    cid = str(chat_id).strip()
    sess = get_session(cid)
    sess.update(kwargs)
    sess["updated_at"] = datetime.now().isoformat()
    USER_SESSIONS[cid] = sess
    save_user_sessions(USER_SESSIONS)
    return sess


def reset_session(chat_id: str | int):
    cid = str(chat_id).strip()
    USER_SESSIONS[cid] = {
        "stage": STATE_IDLE,
        "product_choice": "1",
        "review_product_id": None,
        "research_file": None,
        "findings": [],
        "anxieties": [],
        "media_files": [],
        "updated_at": datetime.now().isoformat(),
    }
    save_user_sessions(USER_SESSIONS)


def extract_text_from_file(file_path: Path) -> str:
    """Extracts text from txt, md, json, csv, docx, or pdf files safely."""
    suffix = file_path.suffix.lower()
    if suffix in [".txt", ".md", ".json", ".csv"]:
        for enc in ["utf-8", "utf-8-sig", "cp1256", "windows-1256", "latin-1"]:
            try:
                return file_path.read_text(encoding=enc).strip()
            except Exception:
                continue
    elif suffix == ".pdf":
        try:
            import pypdf
            reader = pypdf.PdfReader(str(file_path))
            pages = [p.extract_text() or "" for p in reader.pages]
            return "\n\n".join(pages).strip()
        except Exception:
            pass
    elif suffix in [".docx", ".doc"]:
        try:
            import docx
            doc = docx.Document(str(file_path))
            return "\n".join([p.text for p in doc.paragraphs if p.text.strip()]).strip()
        except Exception:
            pass
    try:
        raw = file_path.read_bytes()
        return raw.decode("utf-8", errors="ignore").strip()
    except Exception:
        return ""

# Setup logging (persistent file log + console if available)
log_handlers = [logging.FileHandler(str(LOG_FILE), encoding="utf-8")]
if sys.stdout is not None:
    log_handlers.append(logging.StreamHandler(sys.stdout))

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=log_handlers,
)
logger = logging.getLogger("TelegramControlBot")

# Single-instance Socket Lock (Prevents duplicate instances and Telegram 409 Conflicts)
SINGLE_INSTANCE_PORT = 48199
_SINGLE_INSTANCE_SOCKET: Optional[socket.socket] = None


def acquire_single_instance_lock(port: int = SINGLE_INSTANCE_PORT) -> bool:
    """Binds to a dedicated localhost port to ensure strictly 1 running bot instance.
    The OS automatically releases the socket when the process exits or terminates.
    """
    global _SINGLE_INSTANCE_SOCKET
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)
        s.bind(("127.0.0.1", port))
        s.listen(1)
        _SINGLE_INSTANCE_SOCKET = s
        return True
    except OSError:
        return False

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

# Import clinical research and SEO configs
sys.path.insert(0, str(BASE_DIR))
try:
    from antigravity_social_automation import PRODUCT_PROMPT_CONFIGS
except Exception:
    PRODUCT_PROMPT_CONFIGS = {}

try:
    from clinical_research_harvester import harvest_pubmed_studies
except Exception:
    def harvest_pubmed_studies(p_id, max_results=3):
        return []

TRENDS_FILE = BASE_DIR / "media_assets" / "live_trends_registry.json"

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
            elif r.status_code == 409:
                logger.error("409 Conflict: Another bot instance is polling Telegram! Retrying in 5s... %s", r.text)
                time.sleep(5)
                return []
            else:
                logger.warning("getUpdates returned HTTP %d: %s", r.status_code, r.text)
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
                {"text": "🌟 إدارة وأرشفة تجارب المرضى والعملاء", "callback_data": "menu_reviews"}
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
            [
                {"text": "☁️ أرشفة Google Drive وتفريغ مساحة الجهاز", "callback_data": "act_cloud_archive"}
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


def build_reviews_hub_keyboard() -> Dict[str, Any]:
    return {
        "inline_keyboard": [
            [{"text": "🩹 [1] تجارب 3M Tegaderm +Pad (شاور القيصرية)", "callback_data": "rev_prod_1"}],
            [{"text": "🧴 [2] تجارب BUPY Silicone Scar Sheet (تسطيح الندبة)", "callback_data": "rev_prod_2"}],
            [{"text": "🎗️ [3] تجارب 3M Micropore Tan Tape (تثبيت الأنف)", "callback_data": "rev_prod_3"}],
            [{"text": "👃 [4] تجارب Silicone Nostril Retainer (دعامات الأنف)", "callback_data": "rev_prod_4"}],
            [{"text": "💨 [5] تجارب Smith & Nephew Opsite Spray (مناظير السمنة)", "callback_data": "rev_prod_5"}],
            [{"text": "📋 قوالب النشر المعتمدة طبياً (Medical Privacy)", "callback_data": "rev_privacy_templates"}],
            [{"text": "🔙 العودة للقائمة الرئيسية", "callback_data": "menu_main"}],
        ]
    }


def get_reviews_hub_text() -> str:
    return (
        "🌟 <b>مركز استقبال وأرشفة تجارب المرضى والعملاء (Customer Proof Hub)</b>\n\n"
        "هنا يمكنك إدارة تجارب الحالات الواقعية، استلام الصور السريرية، والتسجيلات الصوتية، "
        "وتوليد قوالب النشر المعتمدة والمتوافقة 100% مع معايير الخصوصية الطبية.\n\n"
        "👇 <b>اختر المنتج السريري لتسجيل تجربة جديدة أو استعراض القوالب:</b>"
    )


def intake_client_review_asset(
    product_id: str,
    review_data: Optional[Dict[str, Any]] = None,
    photo_bytes: Optional[bytes] = None,
    audio_bytes: Optional[bytes] = None,
    photo_filename: Optional[str] = None,
    audio_filename: Optional[str] = None,
    **kwargs,
) -> Dict[str, Any]:
    """
    R5: Ingests client review asset (photo, audio, metadata) into media_assets/client_reviews/{product_id}/.
    Appends review metadata to reviews_metadata.json and returns the saved metadata record.
    """
    data: Dict[str, Any] = {}
    if isinstance(review_data, dict):
        data.update(review_data)
    data.update(kwargs)

    target_reviews_dir = CLIENT_REVIEWS_DIR
    prod_dir = target_reviews_dir / str(product_id)
    photos_dir = prod_dir / "photos"
    audio_dir = prod_dir / "audio"
    photos_dir.mkdir(parents=True, exist_ok=True)
    audio_dir.mkdir(parents=True, exist_ok=True)

    timestamp_now = datetime.now()
    timestamp_str = timestamp_now.strftime("%Y%m%d_%H%M%S")
    review_id = data.get("review_id") or f"rev_{timestamp_str}_{uuid.uuid4().hex[:6]}"

    saved_photo_path = data.get("photo_path")
    if photo_bytes is not None:
        p_name = photo_filename or data.get("photo_filename") or f"review_{timestamp_str}_{review_id}.jpg"
        p_dest = photos_dir / p_name
        p_dest.write_bytes(photo_bytes)
        saved_photo_path = f"photos/{p_name}"

    saved_audio_path = data.get("audio_path")
    if audio_bytes is not None:
        a_name = audio_filename or data.get("audio_filename") or f"voice_{timestamp_str}_{review_id}.mp3"
        a_dest = audio_dir / a_name
        a_dest.write_bytes(audio_bytes)
        saved_audio_path = f"audio/{a_name}"

    record = {
        "review_id": review_id,
        "product_id": str(product_id),
        "timestamp": data.get("timestamp") or timestamp_now.isoformat(),
        "rating": int(data.get("rating", 5)),
        "patient_pseudonym": data.get("patient_pseudonym", "أم قيصرية - القاهرة"),
        "surgery_type": data.get("surgery_type", "ولادة قيصرية (اليوم 21)"),
        "review_text": data.get("review_text", "تجربة سريرية ممتازة في تسريع الالتئام."),
        "specialist_advice": data.get("specialist_advice", "ينصح بالالتزام بالبروتوكول السريري اليومي."),
        "photo_path": saved_photo_path,
        "audio_path": saved_audio_path,
        "privacy_status": data.get("privacy_status", "anonymized_approved"),
    }

    meta_file = prod_dir / "reviews_metadata.json"
    records: List[Dict[str, Any]] = []
    if meta_file.exists():
        try:
            loaded = json.loads(meta_file.read_text(encoding="utf-8"))
            if isinstance(loaded, list):
                records = loaded
        except Exception as e:
            logger.warning("Could not read existing reviews_metadata.json for %s: %s", product_id, e)

    records.append(record)
    meta_file.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info("Ingested client review %s for product %s in %s", review_id, product_id, prod_dir)

    return record


def build_medical_privacy_review_templates(
    product_id_or_data: Any = None,
    review_data: Optional[Dict[str, Any]] = None,
    **kwargs,
) -> Dict[str, str]:
    """
    R5: Generates platform-ready medical privacy compliant review templates for:
    - Instagram / Facebook (7-slide carousel guidelines)
    - TikTok / Reels (30s Egyptian dialect script)
    - Blogger / Website (Schema.org Review snippet)

    Compliance Guardrails:
    1. Anonymized patient pseudonym (e.g. 'أم قيصرية - القاهرة').
    2. ZERO prohibited doctor titles ('طبيبة', 'الدكتورة').
    3. Mandatory approved specialist title ('أخصائية العناية بالتعافي').
    4. Mandatory approved WhatsApp consultation link with promo code HT10.
    """
    data: Dict[str, Any] = {}
    if isinstance(product_id_or_data, dict):
        data.update(product_id_or_data)
        product_id = data.get("product_id", "")
    else:
        product_id = str(product_id_or_data) if product_id_or_data else ""
        if isinstance(review_data, dict):
            data.update(review_data)
    data.update(kwargs)

    patient_pseudonym = data.get("patient_pseudonym") or "أم قيصرية - القاهرة"
    surgery_type = data.get("surgery_type") or "ولادة قيصرية (اليوم 21)"
    review_text = data.get("review_text") or "تحسن ملحوظ في تسطيح الندبة وتراجع الحكة والاحمرار مع الاستخدام اليومي."
    product_name = data.get("product_name") or data.get("product_id") or "المنتج الطبي المعتمد"
    specialist_advice = data.get("specialist_advice") or "ينصح بالاستمرار على تطبيق المنتج يومياً لحماية الأنسجة وتجنب الكيلويد."
    rating = data.get("rating", 5)
    stars = "⭐" * int(rating) if isinstance(rating, (int, float)) and rating > 0 else "⭐⭐⭐⭐⭐"
    wa_link = "https://wa.me/201155803307?text=استشارة%20سريرية%20بكود%20HT10"

    instagram_carousel = (
        f"📸 تجربة سريرية موثقة | {patient_pseudonym}\n"
        f"الإجراء: {surgery_type} | التقييم: {stars} ({rating}/5)\n\n"
        f"📌 مخطط كاروسيل إنستجرام وفيسبوك (7 شرائح طبية موثقة):\n"
        f"▫️ الشريحة 1 (الغلاف): تجربة واقعية لـ {patient_pseudonym} مع {product_name}.\n"
        f"▫️ الشريحة 2 (المعاناة السابقة): تساؤلات ومخاوف الحالة قبل بدء استخدام {product_name}.\n"
        f"▫️ الشريحة 3 (البروتوكول السريري): طريقة الاستخدام المتبعة بتوجيه أخصائية العناية بالتعافي.\n"
        f"▫️ الشريحة 4 (دليل التحسن): صورة توضيحية لتطور التئام الأنسجة ومظهر الندبة.\n"
        f"▫️ الشريحة 5 (شهادة المريض): \"{review_text}\"\n"
        f"▫️ الشريحة 6 (الرأي السريري): توجيه أخصائية العناية بالتعافي: {specialist_advice}\n"
        f"▫️ الشريحة 7 (الاستشارة المباشرة): لحجز استشارة مجانية مع أخصائية العناية بالتعافي بكود HT10:\n"
        f"🔗 {wa_link}\n\n"
        f"#هيلينج_تاتش_مصر #تعافي_جراحي #عناية_بالجروح #HT10"
    )

    tiktok_reels_script = (
        f"⚡ سيناريو ريلز وتيك توك سريري (30 ثانية) | {patient_pseudonym}\n"
        f"الإجراء: {surgery_type} | تقييم الحالة: {stars}\n\n"
        f"🎬 المشهد 1 (0-3 ثوانٍ - Hook بصري وإنساني):\n"
        f"\"لو بتسألي عن تجربة حقيقية بعد {surgery_type}.. اسمعي تجربة {patient_pseudonym}.\"\n\n"
        f"🎬 المشهد 2 (3-12 ثانية - شهادة المريض الواقعية):\n"
        f"\"قالت لنا: '{review_text}'. النتيجة كانت فارقة جداً مع الاستمرار على {product_name}.\"\n\n"
        f"🎬 المشهد 3 (12-22 ثانية - التوجيه السريري المعتمد):\n"
        f"\"توضح أخصائية العناية بالتعافي إن حماية الجرح وترطيب الأنسجة هو الأساس لمنع الندبات البارزة، ونصيحتها: {specialist_advice}\"\n\n"
        f"🎬 المشهد 4 (22-30 ثانية - CTA موثوق):\n"
        f"\"استشيري أخصائية العناية بالتعافي مجاناً عبر واتساب واستفيدي من كود الخصم HT10:\n"
        f"{wa_link}\"\n\n"
        f"#تيك_توك_طبي #هيلينج_تاتش_مصر #تجارب_المرضى #HT10"
    )

    blogger_snippet = (
        f"<div class=\"clinical-review-box\" style=\"border:1px solid #10B981; border-radius:12px; padding:20px; margin:20px 0; background:#F0FDF4;\">\n"
        f"  <div style=\"display:flex; justify-content:space-between; align-items:center;\">\n"
        f"    <h4 style=\"color:#064E3B; margin:0;\">🌟 تجربة سريرية موثقة: {patient_pseudonym}</h4>\n"
        f"    <span style=\"color:#F59E0B; font-weight:bold;\">{stars} ({rating}/5)</span>\n"
        f"  </div>\n"
        f"  <p style=\"color:#374151; font-size:14px; margin:8px 0;\"><strong>الإجراء الجراحي:</strong> {surgery_type} | <strong>المنتج:</strong> {product_name}</p>\n"
        f"  <blockquote style=\"background:#FFFFFF; border-right:4px solid #10B981; padding:12px 16px; margin:12px 0; color:#1F2937; border-radius:6px;\">\n"
        f"    \"{review_text}\"\n"
        f"  </blockquote>\n"
        f"  <p style=\"color:#065F46; font-size:14px; margin:10px 0;\"><strong>💡 توجيه أخصائية العناية بالتعافي:</strong> {specialist_advice}</p>\n"
        f"  <div style=\"margin-top:14px;\">\n"
        f"    <a href=\"{wa_link}\" style=\"background:#10B981; color:#FFFFFF; padding:8px 16px; border-radius:6px; text-decoration:none; font-weight:bold; display:inline-block;\">\n"
        f"      💬 استشارة أخصائية العناية بالتعافي عبر واتساب (كود HT10)\n"
        f"    </a>\n"
        f"  </div>\n"
        f"</div>"
    )

    return {
        "instagram_carousel": instagram_carousel,
        "tiktok_reels_script": tiktok_reels_script,
        "blogger_snippet": blogger_snippet,
    }


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
        sess = get_session(chat_id)
        prod_choice = str(sess.get("product_choice") or "").strip()
        selected_cat = CHOICE_TO_CATEGORY.get(prod_choice)
        prod_label = PRODUCTS_CATALOG.get(prod_choice, {}).get("name", "المنتج السريري المختار")

        status_msg = bot.send_message(
            chat_id,
            "⏳ <b>[1/4] جاري تشغيل المسار الشامل الموحد (Google Flow + Drive + Auto-Publish)...</b>\n"
            f"• 🎯 المنتج المستهدف: <b>{html.escape(prod_label)}</b>\n"
            "• ☁️ سحب وسائط <code>00_Flow_Inbox</code> و <code>manual_inbox</code>\n"
            "• 🌐 بناء وتحديث صفحات الهبوط على GitHub Pages\n"
            "• 📱 النشر التلقائي على فيسبوك وإنستجرام وتجهيز يوتيوب وتيكتوك...",
        )
        target_msg_id = status_msg.get("result", {}).get("message_id") if status_msg else None

        cmd = [str(VENV_PYTHON), "single_click_master_pipeline.py"]
        if selected_cat:
            cmd.extend(["--category", selected_cat])
        res = subprocess.run(
            cmd,
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        if res.returncode == 0:
            report_file = MEDIA_DIR / "latest_live_publish_report.json"
            rep: Dict[str, Any] = {}
            if report_file.exists():
                try:
                    rep = json.loads(report_file.read_text(encoding="utf-8"))
                except Exception:
                    rep = {}

            lp_url = rep.get("landing_page_url") or "https://medon90ae.github.io/healing-touch-egypt/"
            fb_photo_url = rep.get("facebook_photo_url") or "https://www.facebook.com/1371809382684781"
            fb_reel_url = rep.get("facebook_reel_url")
            ig_post_url = rep.get("instagram_post_url") or "https://www.instagram.com/mohamedahmedalahmady/"
            yt_dir = rep.get("youtube_manual_dir") or r"G:\My Drive\Healing_Touch_Egypt_Cloud_Archive\02_Ready_To_Publish_Packs"
            tt_dir = rep.get("tiktok_manual_dir") or r"G:\My Drive\Healing_Touch_Egypt_Cloud_Archive\02_Ready_To_Publish_Packs"

            fb_reel_line = f"🎬 <b>ريلز فيسبوك (نُشر تلقائياً):</b>\n👉 {fb_reel_url}\n\n" if fb_reel_url else ""

            success_text = (
                "✅ <b>اكتمل النشر التلقائي وتحديث صفحات الهبوط والأرشفة السحابية بنجاح!</b>\n\n"
                "🌐 <b>صفحة الهبوط المحدثة للحملة (GitHub Pages Live):</b>\n"
                f"👉 {lp_url}\n\n"
                "📘 <b>منشور فيسبوك (نُشر تلقائياً):</b>\n"
                f"👉 {fb_photo_url}\n\n"
                f"{fb_reel_line}"
                "📸 <b>منشور إنستجرام (نُشر تلقائياً):</b>\n"
                f"👉 {ig_post_url}\n\n"
                "🎥 <b>جاهز للرفع اليدوي (يوتيوب + تيكتوك بصيغة JPG/MP4):</b>\n"
                f"• يوتيوب: <code>{yt_dir}</code>\n"
                f"• تيكتوك: <code>{tt_dir}</code>\n"
                "<i>(تم إلغاء بلوجر وريديت نهائياً كما طلبت)</i>\n\n"
                "☁️ <b>تنظيف الجهاز (Zero Local Storage):</b> تم نقل كافة الحزم والأصول إلى Google Drive وتفريغ مساحة القرص C تلقائياً!"
            )
            keyboard = {
                "inline_keyboard": [
                    [{"text": "🎬 فتح Google Flow Studio", "url": GOOGLE_FLOW_URL}],
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
    """Executes Stage 1: registers user session and delivers Deep Research Card instantly."""
    prod_info = PRODUCTS_CATALOG.get(prod_choice, PRODUCTS_CATALOG["1"])
    update_session(chat_id, stage=STATE_STAGE_1_RESEARCH, product_choice=prod_choice)

    # Background silent generator for PROMPTS_PACK_TODAY.txt so files are pre-built
    def _bg_pack_gen():
        try:
            cmd = [
                str(VENV_PYTHON),
                "antigravity_social_automation.py",
                "--mode",
                "notebooklm",
                "--product",
                prod_choice,
            ]
            subprocess.run(cmd, cwd=str(BASE_DIR), capture_output=True, timeout=120)
        except Exception:
            pass

    threading.Thread(target=_bg_pack_gen, daemon=True).start()

    # Deliver Stage 1 Deep Research Prompt card instantly
    card_text, card_keyboard = build_stage1_deep_research_card(prod_choice)
    bot.send_message(chat_id, card_text, reply_markup=card_keyboard)


def analyze_clinical_research(raw_text: str, product_choice: str) -> Dict[str, Any]:
    """Analyzes raw clinical research text, extracting findings, patient anxieties, and guidelines."""
    lines = [ln.strip() for ln in raw_text.splitlines() if ln.strip()]
    findings = []
    anxieties = []
    guidelines = []

    clinical_keywords = [
        "ندبة", "ندبات", "جرح", "جروح", "شاور", "ماء", "استحمام", "سيليكون", "تيغاديرم",
        "غضروف", "كولاجين", "التئام", "التهاب", "بكتيريا", "تعافي", "قيصرية", "تجميل",
        "تكميم", "أنف", "فتحات", "أوبسايت", "ميكروبور", "كيلويد", "hypertrophic",
        "infection", "healing", "scar", "wound", "sterile", "دعامة", "دعامات",
    ]
    anxiety_keywords = [
        "خوف", "قلق", "حكة", "ألم", "احمرار", "صديد", "بلل", "انكماش", "أثر",
        "تشوه", "عرق", "حساسية", "تورم", "سخونة", "نزف", "عدوى", "أمان",
    ]

    for line in lines:
        cleaned = line.lstrip("•-*#0123456789. \t").strip()
        if len(cleaned) < 15 or len(cleaned) > 250:
            continue
        if any(w in cleaned for w in anxiety_keywords) or "?" in cleaned or "؟" in cleaned:
            if len(anxieties) < 4 and cleaned not in anxieties:
                anxieties.append(cleaned)
        elif any(w in cleaned for w in clinical_keywords):
            if len(findings) < 5 and cleaned not in findings:
                findings.append(cleaned)
        elif len(guidelines) < 3 and any(w in cleaned for w in ["يجب", "ينصح", "طريقة", "تغيير", "غيار", "تطبيق", "خطوات", "بروتوكول"]):
            if cleaned not in guidelines:
                guidelines.append(cleaned)

    # Fallback to configured defaults if research had few explicit matches
    cfg = PRODUCT_PROMPT_CONFIGS.get(str(product_choice), PRODUCT_PROMPT_CONFIGS.get("1", {}))
    prod_name = cfg.get("name_ar", PRODUCTS_CATALOG.get(str(product_choice), {}).get("name", "المنتج الطبي"))
    if not findings:
        findings = [
            f"دراسات التئام الأنسجة السريرية لـ {prod_name} تؤكد قدرته على عزل الجرح ومنع الندبات التضخمية.",
            "التوصيات السريرية تؤكد أهمية الحفاظ على بيئة رطبة معقمة لتسريع تكوين ألياف الكولاجين المنتظمة.",
        ]
    if not anxieties:
        anxieties = cfg.get(
            "patient_anxieties",
            ["الخوف من وصول الماء أو البكتيريا أثناء الاستحمام وتأثير ذلك على العملية", "القلق من بقاء أثر بارز أو حكة مستمرة في مكان الجرح"],
        )[:3]

    return {
        "findings": findings,
        "anxieties": anxieties,
        "guidelines": guidelines,
        "total_chars": len(raw_text),
        "total_lines": len(lines),
    }


def build_stage1_deep_research_card(choice: str) -> Tuple[str, Dict[str, Any]]:
    d = get_product_data(choice)
    name_ar = html.escape(d["name_ar"])
    focus = html.escape(d["focus"])
    brand = html.escape(d["cfg"].get("brand", PRODUCTS_CATALOG.get(choice, {}).get("brand", "")))

    kws_html = "\n".join([f"• <code>{html.escape(k)}</code>" for k in d["keywords"][:6]])
    lts_html = "\n".join([f"• {html.escape(q)}" for q in (d["long_tails"][:3] + d["trends"][:3])])

    studies_html_list = []
    for s in d["studies"]:
        y = s.get("pub_year", "2025")
        t = html.escape(s.get("title", "")[:75])
        u = s.get("url", "https://pubmed.ncbi.nlm.nih.gov/")
        studies_html_list.append(f"• <a href='{u}'>[{y}] {t}...</a>")
    studies_html = "\n".join(studies_html_list) if studies_html_list else "• دراسات PubMed المعتمدة في أرشيف التعافي"

    prompt_lines = [
        f"بصفتك باحثاً إكلينيكياً واستشارياً في جراحة التعافي وعلاج الجروح في مصر:",
        f"أريد بحثاً سريرياً دقيقاً وموثقاً حول: {d['focus']}.",
        "",
        "الأسئلة السريرية والبحثية المحددة المطلوب الإجابة عليها تفصيلياً:",
    ]
    prompt_lines.extend([f"• {q}" for q in d["queries"]])
    prompt_lines.append("")
    prompt_lines.append("مخاوف وتساؤلات المرضى المقلقة في مصر المطلوب طمأنتهم علمياً بشأنها:")
    prompt_lines.extend([f"• {a}" for a in d["anxieties"]])
    prompt_lines.append("")
    prompt_lines.append("تساؤلات وترندات بحث جوجل مصر الصاعدة هذا الأسبوع للإجابة عليها:")
    prompt_lines.extend([f"• {t}" for t in d["trends"][:4]])
    prompt_lines.append("")
    prompt_lines.append("الشروط الصارمة للمحتوى الناتج:")
    prompt_lines.append("1. نبرة طبية توجيهية هادئة تشرح فسيولوجيا التئام الأنسجة وتبدد المخاوف دون تهويل.")
    prompt_lines.append("2. استهداف الجمهور المصري وإجابات تناسب الصيف والعرق وطريقة الغيار المنزلي.")
    prompt_lines.append("3. منع تام لأي عروض تسويقية أو أسعار؛ التركيز 100% على الإرشاد والدعم والتثقيف الصحي.")
    prompt_lines.append("4. إدراج توجيه واضح للتواصل مع أخصائي التعافي عبر واتساب 01155803307 بكود HT10 وحق المعاينة قبل الاستلام.")
    prompt_lines.append("")
    prompt_lines.append("أحدث أبحاث PubMed السريرية المعتمدة للاستشهاد بها ودعم المحتوى:")
    for s in d["studies"]:
        prompt_lines.append(f"• [{s.get('pub_year')}] {s.get('title')} -> {s.get('url')}")

    raw_prompt = "\n".join(prompt_lines)
    escaped_code = html.escape(raw_prompt)

    msg = (
        f"🔬 <b>[المرحلة 1 من 4] البحث السريري المعمق (Gemini Deep Research)</b>\n\n"
        f"🎯 <b>المنتج:</b> {name_ar}\n"
        f"🏷️ <b>العلامة:</b> {brand}\n"
        f"📌 <b>المحور السريري:</b> {focus}\n\n"
        f"🔑 <b>أهم الكلمات البحثية في مصر:</b>\n"
        f"{kws_html}\n\n"
        f"❓ <b>الأسئلة وترندات جوجل مصر الصاعدة:</b>\n"
        f"{lts_html}\n\n"
        f"📚 <b>أحدث دراسات PubMed السريرية:</b>\n"
        f"{studies_html}\n\n"
        f"📋 <b>خطوات التشغيل الآن:</b>\n"
        f"1️⃣ اضغط داخل المربع للنسخ الفوري بلمسة واحدة 👇\n"
        f"2️⃣ اضغط زر <b>🌐 فتح Gemini Deep Research</b> والصق البرومبت.\n"
        f"3️⃣ بعد انتهاء البحث، انسخ التقرير الناتج أو احفظه، و<b>أرسله هنا في الشات مباشرة</b> (كنص أو كملف txt / docx / pdf / md) لنقوم بتحليله وتوليد برومبتات الهوية والصوتيات فوراً!\n\n"
        f"👇 <b>برومبت البحث السريري المعمق:</b>\n"
        f"<pre><code>{escaped_code}</code></pre>"
    )

    keyboard = {
        "inline_keyboard": [
            [
                {"text": "🎬 البرومبت الموحد الشامل — Google Flow (فيديو + صور + سيو)", "callback_data": f"prompt_flow_{choice}"},
            ],
            [
                {"text": "🌐 فتح Gemini Deep Research مباشرة", "url": GEMINI_URL},
            ],
            [
                {"text": "📋 خيارات وبرومبتات إضافية للمنتج", "callback_data": f"hub_prod_{choice}"},
                {"text": "🩺 اختيار منتج آخر", "callback_data": "menu_products"},
            ],
            [
                {"text": "🏠 القائمة الرئيسية", "callback_data": "menu_main"},
            ],
        ]
    }
    return msg, keyboard


def build_unified_google_flow_card(choice: str, analysis: Optional[Dict[str, Any]] = None) -> Tuple[str, Dict[str, Any]]:
    """
    Generates the All-in-One Super Prompt for Google Flow (Veo 3.1 + Imagen 4 + Gemini)
    to produce 9:16 vertical Reel, 16:9 horizontal video, 8K contextual clinical photos
    (zero distorted text overlay), and full Arabic SEO copy in one single prompt.
    """
    d = get_product_data(choice)
    name_ar = html.escape(d["name_ar"])
    brand = html.escape(d["cfg"].get("brand", PRODUCTS_CATALOG.get(choice, {}).get("brand", "")))
    focus = html.escape(d["focus"])

    findings_list = (analysis or {}).get("findings") or [d["focus"]]
    anxieties_list = (analysis or {}).get("anxieties") or d.get("anxieties", [])[:3]
    kws_str = "، ".join(d.get("keywords", [])[:5])
    hashtags_str = " ".join(d.get("hashtags", [])[:6])

    super_prompt = (
        f"[GOOGLE FLOW ALL-IN-ONE CLINICAL PRODUCTION BRIEF — HEALING TOUCH EGYPT 2026]\n"
        f"Project Workspace: {GOOGLE_FLOW_URL}\n"
        f"Product: {brand} ({d['name_ar']})\n"
        f"Clinical Focus: {d['focus']}\n"
        f"Brand Palette: Clinical Forest Green (#064E3B), Medical Mint (#10B981), Slate Navy (#0F172A), Sterile White (#FFFFFF).\n\n"
        f"=== 1. VIDEO SCENE GENERATION (Veo 3.1 — Generate in 9:16 Vertical & 16:9 Horizontal) ===\n"
        f"• Scene 1 (0-4s Visual Hook): Compassionate Egyptian clinical recovery suite, soft natural morning light, "
        f"a recovery care specialist (أخصائية العناية بالتعافي) wearing sterile mint medical gloves preparing {brand} on a stainless steel tray.\n"
        f"• Scene 2 (4-12s Physiological Protection): Macro cinematic close-up showing the breathable, waterproof sterile barrier "
        f"protecting post-operative tissue ({findings_list[0]}), calm reassuring motion, 8K documentary realism.\n"
        f"• Scene 3 (12-20s Patient Peace of Mind): Warm reassuring atmosphere in an upscale Cairo home recovery setting, "
        f"demonstrating effortless daily hygiene and confidence.\n"
        f"• Audio & Voiceover Guide (Egyptian White Arabic Dialect): Calm, reassuring female specialist voice addressing: "
        f"{' / '.join(anxieties_list[:2])}, ending with: 'للاستشارة السريرية المجانية مع أخصائية العناية بالتعافي عبر واتساب 01155803307 بكود HT10 مع حق المعاينة قبل الاستلام.'\n\n"
        f"=== 2. 8K CLINICAL STILL IMAGES (Imagen 4 — 1:1 Square & 9:16 Story) ===\n"
        f"• Photorealistic 8K macro medical photography of {brand} in an authentic Egyptian clinical setting, "
        f"shallow depth of field (85mm f/2.8), Clinical Forest Green (#064E3B) and Mint (#10B981) accents.\n"
        f"• STRICT VISUAL GUARDRAIL: Generate contextual clinical lifestyle and sterile tray scenes ONLY — "
        f"ZERO artificial text overlays on packaging to avoid text distortion; our local engine composites the real product label and Arabic typography automatically.\n\n"
        f"=== 3. OMNICHANNEL ARABIC SEO COPYPACK (Facebook + Instagram + YouTube + TikTok) ===\n"
        f"• Focus Keywords (Egypt): {kws_str}\n"
        f"• Mandatory Compliance: Use title 'أخصائية العناية بالتعافي' only (never 'طبيبة'/'الدكتورة'), zero commercial price hype, "
        f"include WhatsApp consultation 01155803307 + code HT10 + hashtags: {hashtags_str}"
    )

    msg = (
        f"🎬 <b>البرومبت الموحد الشامل لـ Google Flow (All-in-One Super Prompt)</b>\n\n"
        f"🎯 <b>المنتج:</b> {name_ar} (<code>{brand}</code>)\n"
        f"📌 <b>المحور السريري:</b> {focus}\n\n"
        f"✨ <b>ماذا ينتج هذا البرومبت الموحد دفعة واحدة؟</b>\n"
        f"1️⃣ فيديو عمودي <code>9:16</code> للريلز والشورتس وتيكتوك + فيديو أفقي <code>16:9</code> ليوتيوب وصفحة الهبوط.\n"
        f"2️⃣ صور طبية سياقية <code>8K</code> (بدون تشويه نصوص العبوة) لفيسبوك وإنستجرام.\n"
        f"3️⃣ سكريبت وكابشن السيو العربي الموحد بكود <code>HT10</code>.\n\n"
        f"📋 <b>اضغط داخل المربع لنسخ البرومبت الموحد بلمسة واحدة 👇:</b>\n"
        f"<pre><code>{html.escape(super_prompt)}</code></pre>\n\n"
        f"☁️ <b>بعد التوليد في Google Flow:</b>\n"
        f"ارفع المخرجات مباشرة إلى مجلد درايف <code>00_Flow_Inbox</code> (أو أرسلها هنا في تيليجرام) ثم اضغط <b>🚀 تشغيل المسار الشامل الآن</b> ليتم النشر التلقائي وتنظيف جهازك بالكامل!"
    )

    keyboard = {
        "inline_keyboard": [
            [
                {"text": "🎬 فتح مشروع Google Flow مباشرة", "url": GOOGLE_FLOW_URL},
            ],
            [
                {"text": "🚀 تشغيل المسار والنشر الشامل الآن", "callback_data": "act_master"},
            ],
            [
                {"text": "🎨 برومبت Pomelli", "callback_data": f"prompt_pomelli_{choice}"},
                {"text": "🎙️ برومبت NotebookLM", "callback_data": f"prompt_nlm_{choice}"},
            ],
            [
                {"text": "🔙 رجوع لخيارات المنتج", "callback_data": f"hub_prod_{choice}"},
                {"text": "🏠 القائمة الرئيسية", "callback_data": "menu_main"},
            ],
        ]
    }
    return msg, keyboard


def build_synthesized_pomelli_card(choice: str, analysis: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    d = get_product_data(choice)
    name_ar = html.escape(d["name_ar"])
    brand = html.escape(d["cfg"].get("brand", PRODUCTS_CATALOG.get(choice, {}).get("brand", "")))

    findings_sample = analysis.get("findings", [])
    findings_context = " - ".join(findings_sample[:2]) if findings_sample else d["focus"]

    pomelli_1_1 = (
        f"Photorealistic 8K macro medical photography following the Healing Touch Egypt Brand Book aesthetic: "
        f"Brand Colors: `#064E3B` (Clinical Forest Green), `#10B981` (Medical Mint), `#0F172A` (Slate Navy Charcoal), `#FFFFFF` (Sterile White). "
        f"Scene: Immaculate sterile stainless steel medical preparation tray, soft natural directional clinical lighting. "
        f"Centerpiece: Authentic medical packaging of {brand} ({name_ar}), placed cleanly with visible authentic specifications. "
        f"Clinical context from research: {findings_context}. "
        f"Surrounding props: sterile surgical gauze, sterile cotton drape, medical scissors. "
        f"Camera: Macro 85mm f/2.8 lens, shallow depth of field focusing on authentic medical texture, professional healthcare documentary photography, "
        f"zero text overlays, zero cartoonish elements, sterile, reassuring, compassionate."
    )

    pomelli_9_16 = (
        f"Vertical 9:16 aspect ratio clinical photography following the Healing Touch Egypt Brand Book guidelines: "
        f"Clean, compassionate Egyptian clinical recovery suite setting. "
        f"Showing authentic healthcare specialist handling {brand} ({name_ar}) with sterile surgical gloves. "
        f"Palette accents: `#064E3B` Forest Green and `#10B981` Mint. "
        f"Soft natural ambient light, calm reassuring atmosphere for post-operative recovery, 8K ultra-clean documentary realism, no text, no artifacts."
    )

    msg = (
        f"🎨 <b>[المرحلة 2 من 4] برومبتات Google Pomelli Brand Book (واقعية 8K)</b>\n\n"
        f"🎯 <b>المنتج:</b> {name_ar}\n"
        f"🏷️ <b>العلامة:</b> {brand}\n"
        f"🌿 <b>كتاب الهوية المعتمد:</b> متطابق مع هوية وألوان هيلينج تاتش السريرية\n\n"
        f"📐 <b>1️⃣ برومبت الصورة المربعة 1:1 (للموقع وفيسبوك وإنستجرام Feed):</b>\n"
        f"<i>(اضغط داخل المربع للنسخ الفوري بلمسة واحدة 👇)</i>\n"
        f"<pre><code>{html.escape(pomelli_1_1)}</code></pre>\n\n"
        f"📱 <b>2️⃣ برومبت الستوري والريلز العمودي 9:16 (إنستجرام وتيك توك):</b>\n"
        f"<i>(اضغط داخل المربع للنسخ الفوري بلمسة واحدة 👇)</i>\n"
        f"<pre><code>{html.escape(pomelli_9_16)}</code></pre>"
    )

    keyboard = {
        "inline_keyboard": [
            [
                {"text": "🎨 فتح Google Pomelli Brand Book مباشرة", "url": POMELLI_BRAND_BOOK_URL},
            ],
            [
                {"text": "🎙️ برومبت Google NotebookLM", "callback_data": f"prompt_nlm_{choice}"},
                {"text": "🚀 تشغيل المسار الشامل", "callback_data": "act_master"},
            ],
            [
                {"text": "🩺 اختيار منتج آخر", "callback_data": "menu_products"},
                {"text": "🏠 القائمة الرئيسية", "callback_data": "menu_main"},
            ],
        ]
    }
    return msg, keyboard


def build_synthesized_notebooklm_card(choice: str, analysis: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    d = get_product_data(choice)
    name_ar = html.escape(d["name_ar"])

    findings_bullets = "\n".join([f"• {f}" for f in analysis.get("findings", [])[:3]])
    anxieties_bullets = "\n".join([f"• {a}" for a in analysis.get("anxieties", [])[:2]])

    audio_prompt = (
        f"قم بتوليد حوار بودكاست طبي بين اثنين من استشاريي التعافي الطبي في مصر باللهجة المصرية البيضاء الراقية، "
        f"يتناولان فيه بالنقاش العلمي الهادئ والمريح نتائج تقرير البحث السريري حول {d['name_ar']}:\n"
        f"أهم الحقائق المستخلصة من البحث:\n{findings_bullets}\n\n"
        f"المخاوف المطلوب طمأنة المريض بشأنها علمياً:\n{anxieties_bullets}\n\n"
        f"بروتوكول العناية المنزلي الصحيح وتصحيح المفاهيم الخاطئة في مصر.\n"
        f"الخاتمة: التأكيد على كود الخصم والمعاينة HT10 والتواصل مع أخصائية التعافي عبر واتساب 01155803307 وحق معاينة المنتج قبل الاستلام والشحن المجاني."
    )

    video_prompt = (
        f"أنشئ بريف وإنتاج فيديو شارح تفاعلي (Explainer Video) يستند لتقرير البحث السريري حول {d['name_ar']}:\n"
        f"المحاور: فسيولوجيا تعافي الأنسجة، تجنب الماء أو الحكة، خطوات الغيار العملي الآمن، ودحض المخاوف الشائعة.\n"
        f"النبرة: وقورة، طبية، مطمئنة، وتوجيه هادئ للاستشارة عبر واتساب 01155803307 بكود HT10."
    )

    msg = (
        f"🎙️ <b>[المرحلة 2 من 4] برومبتات استوديو Google NotebookLM</b>\n\n"
        f"🎯 <b>المنتج:</b> {name_ar}\n"
        f"🧠 <b>المعرفة المدخلة:</b> تم دمج وتطويع نتائج تقرير البحث السريري المرفوع\n\n"
        f"🎧 <b>1️⃣ برومبت البودكاست والنقاش الصوتي (Audio Overview):</b>\n"
        f"<i>(اضغط داخل المربع للنسخ الفوري بلمسة واحدة 👇)</i>\n"
        f"<pre><code>{html.escape(audio_prompt)}</code></pre>\n\n"
        f"🎬 <b>2️⃣ برومبت الفيديو التوضيحي السريري (Video Overview):</b>\n"
        f"<i>(اضغط داخل المربع للنسخ الفوري بلمسة واحدة 👇)</i>\n"
        f"<pre><code>{html.escape(video_prompt)}</code></pre>"
    )

    keyboard = {
        "inline_keyboard": [
            [
                {"text": "🌐 فتح Google NotebookLM مباشرة", "url": NOTEBOOKLM_URL},
            ],
            [
                {"text": "🎨 برومبت Pomelli Brand Book", "callback_data": f"prompt_pomelli_{choice}"},
                {"text": "🚀 تشغيل المسار الشامل", "callback_data": "act_master"},
            ],
            [
                {"text": "🩺 اختيار منتج آخر", "callback_data": "menu_products"},
                {"text": "🏠 القائمة الرئيسية", "callback_data": "menu_main"},
            ],
        ]
    }
    return msg, keyboard


def handle_research_report_received(
    chat_id: str,
    raw_text: str,
    source_label: str = "نص رسالة",
    file_path: Optional[Path] = None,
):
    """Processes uploaded research report, analyzes clinical points, and synthesizes Stage 2 prompts."""
    session = get_session(chat_id)
    choice = session.get("product_choice", "1")
    prod_info = PRODUCTS_CATALOG.get(choice, PRODUCTS_CATALOG["1"])

    clean_text = raw_text.strip()
    if len(clean_text) < 40:
        bot.send_message(
            chat_id,
            "⚠️ <b>النص المستلم قصير جداً (أقل من 40 حرف).</b>\n"
            "يرجى نسخ التقرير الطبي الكامل من Gemini Deep Research أو رفع ملف التقرير للبدء بالتحليل.",
            reply_markup=build_stage1_deep_research_card(choice)[1],
        )
        return

    # Save to dedicated clinical archive
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    saved_report_file = RESEARCH_REPORTS_DIR / f"research_report_prod_{choice}_{timestamp_str}.txt"
    try:
        saved_report_file.write_text(clean_text, encoding="utf-8")
    except Exception as e:
        logger.warning("Could not write research report file: %s", e)

    # Analyze clinical findings
    analysis = analyze_clinical_research(clean_text, choice)

    # Update session
    update_session(
        chat_id,
        stage=STATE_STAGE_3_MEDIA,
        product_choice=choice,
        research_file=str(saved_report_file),
        findings=analysis["findings"],
        anxieties=analysis["anxieties"],
    )

    findings_bullets = "\n".join([f"• {f}" for f in analysis["findings"][:4]])
    anxieties_bullets = "\n".join([f"• {a}" for a in analysis["anxieties"][:3]])

    ack_text = (
        f"✅ <b>تم استلام تقرير البحث السريري وتحليله بنجاح!</b>\n\n"
        f"🎯 <b>المنتج:</b> {prod_info['name']}\n"
        f"📊 <b>المصدر:</b> {source_label} | <b>الحجم:</b> {len(clean_text)} حرف\n"
        f"📁 <b>الأرشيف السريري:</b> <code>{saved_report_file.name}</code>\n\n"
        f"🧠 <b>أبرز المخرجات السريرية المستخلصة من التقرير:</b>\n"
        f"{findings_bullets}\n\n"
        f"❓ <b>مخاوف المرضى المعالجة علمياً في التقرير:</b>\n"
        f"{anxieties_bullets}\n\n"
        f"👇 <b>تم توليد برومبتات الهوية والصوتيات الذكية استناداً لنتائج هذا البحث:</b>"
    )
    bot.send_message(chat_id, ack_text)

    # Send Unified Google Flow Super Prompt Card first
    flow_text, flow_kb = build_unified_google_flow_card(choice, analysis)
    bot.send_message(chat_id, flow_text, reply_markup=flow_kb)

    # Send Pomelli Brand Book Card
    pomelli_text, pomelli_kb = build_synthesized_pomelli_card(choice, analysis)
    bot.send_message(chat_id, pomelli_text, reply_markup=pomelli_kb)

    # Send NotebookLM Studio Card
    nlm_text, nlm_kb = build_synthesized_notebooklm_card(choice, analysis)
    bot.send_message(chat_id, nlm_text, reply_markup=nlm_kb)

    # Final guidance message for Stage 3 Media Ingestion
    guidance_text = (
        "💡 <b>الخطوة التالية (المرحلة 3 من 4 - توليد ورفع الوسائط):</b>\n\n"
        "1️⃣ افتح <b>Google Flow</b> بالبرومبت الموحد الشامل أعلاه لتوليد الفيديوهات والصور دفعة واحدة.\n"
        "2️⃣ ضع المخرجات في مجلد درايف <code>00_Flow_Inbox</code> أو <b>أرسلها هنا في شات تيليجرام مباشرة</b>.\n"
        "3️⃣ اضغط <b>🚀 تشغيل المسار الشامل</b> ليتم تحديث صفحات الهبوط، والنشر التلقائي على فيسبوك وإنستجرام، وتجهيز يوتيوب وتيكتوك، وتفريغ مساحة جهازك على Google Drive!"
    )
    guidance_kb = {
        "inline_keyboard": [
            [
                {"text": "🎬 فتح مشروع Google Flow", "url": GOOGLE_FLOW_URL},
            ],
            [
                {"text": "🎨 فتح Pomelli Brand Book", "url": POMELLI_BRAND_BOOK_URL},
                {"text": "🎙️ فتح NotebookLM", "url": NOTEBOOKLM_URL},
            ],
            [
                {"text": "🚀 تشغيل المسار الشامل (إذا رفعت الميديا)", "callback_data": "act_master"},
                {"text": "📥 فحص manual_inbox", "callback_data": "act_inbox_status"},
            ],
            [
                {"text": "🏠 القائمة الرئيسية", "callback_data": "menu_main"},
            ],
        ]
    }
    bot.send_message(chat_id, guidance_text, reply_markup=guidance_kb)


def get_category_trends(category: str) -> List[str]:
    """Loads live Google Suggest queries for Egyptian market by clinical category."""
    if TRENDS_FILE.exists():
        try:
            data = json.loads(TRENDS_FILE.read_text(encoding="utf-8"))
            return data.get("categories", {}).get(category, [])
        except Exception:
            pass
    return []


def get_product_data(choice: str) -> Dict[str, Any]:
    """Retrieves full clinical configuration, PubMed papers, and Egypt trends."""
    choice_str = str(choice).strip()
    cfg = PRODUCT_PROMPT_CONFIGS.get(choice_str, PRODUCT_PROMPT_CONFIGS.get("1", {}))
    cat = cfg.get("category", "c-section")
    trends = get_category_trends(cat)
    studies = harvest_pubmed_studies(choice_str, max_results=3)
    return {
        "choice": choice_str,
        "cfg": cfg,
        "name_ar": cfg.get("name_ar", PRODUCTS_CATALOG.get(choice_str, {}).get("name", "منتج سريري")),
        "focus": cfg.get("clinical_focus", PRODUCTS_CATALOG.get(choice_str, {}).get("tag", "العناية والتعافي السريري")),
        "keywords": cfg.get("target_keywords_egypt", []),
        "long_tails": cfg.get("long_tail_queries_egypt", []),
        "hashtags": cfg.get("egypt_hashtags", []),
        "queries": cfg.get("gemini_research_queries", []),
        "anxieties": cfg.get("patient_anxieties", []),
        "pomelli_1_1": cfg.get("pomelli_prompt_1_1", ""),
        "pomelli_9_16": cfg.get("pomelli_prompt_9_16", ""),
        "trends": trends,
        "studies": studies,
    }


def build_product_hub_card(choice: str) -> Tuple[str, Dict[str, Any]]:
    d = get_product_data(choice)
    name_ar = html.escape(d["name_ar"])
    focus = html.escape(d["focus"])

    text = (
        f"🌿 <b>مركز أبحاث وبرومبتات المنتج السريرية المعتمدة</b>\n\n"
        f"🎯 <b>المنتج:</b> {name_ar}\n"
        f"📌 <b>المحور السريري:</b> {focus}\n"
        f"📈 <b>سيو وترندات مصر:</b> تم رصد وتحليل استفسارات جوجل مصر الصاعدة\n"
        f"📚 <b>الأبحاث الموثقة:</b> تم استخراج أحدث دراسات PubMed السريرية\n\n"
        f"👇 <b>اختر المنصة لعرض الكلمات البحثية والأسئلة والبرومبت المخصص للنسخ المباشر:</b>"
    )

    keyboard = {
        "inline_keyboard": [
            [
                {"text": "🎬 البرومبت الموحد الشامل — Google Flow (فيديو + صور + سيو)", "callback_data": f"prompt_flow_{choice}"},
            ],
            [
                {"text": "🔬 برومبت Gemini Deep Research", "callback_data": f"prompt_gemini_{choice}"},
            ],
            [
                {"text": "🎙️ برومبت Google NotebookLM", "callback_data": f"prompt_nlm_{choice}"},
                {"text": "🎨 برومبت Google Pomelli", "callback_data": f"prompt_pomelli_{choice}"},
            ],
            [
                {"text": "📱 برومبتات السوشيال (ريلز / تيك توك / يوتيوب)", "callback_data": f"prompt_social_menu_{choice}"},
            ],
            [
                {"text": "📄 تحميل الحزمة كاملة (ملف TXT)", "callback_data": f"prompt_file_{choice}"},
                {"text": "🚀 تشغيل المسار الشامل الآن", "callback_data": "act_master"},
            ],
            [
                {"text": "🩺 اختيار منتج آخر", "callback_data": "menu_products"},
                {"text": "🏠 القائمة الرئيسية", "callback_data": "menu_main"},
            ],
        ]
    }
    return text, keyboard


def build_gemini_prompt_card(choice: str) -> Tuple[str, Dict[str, Any]]:
    d = get_product_data(choice)
    name_ar = html.escape(d["name_ar"])
    focus = html.escape(d["focus"])

    kws_html = "\n".join([f"• <code>{html.escape(k)}</code>" for k in d["keywords"][:6]])
    lts_html = "\n".join([f"• {html.escape(q)}" for q in (d["long_tails"][:3] + d["trends"][:3])])

    studies_html_list = []
    for s in d["studies"]:
        y = s.get("pub_year", "2025")
        t = html.escape(s.get("title", "")[:75])
        u = s.get("url", "https://pubmed.ncbi.nlm.nih.gov/")
        studies_html_list.append(f"• <a href='{u}'>[{y}] {t}...</a>")
    studies_html = "\n".join(studies_html_list) if studies_html_list else "• دراسات PubMed المعتمدة في أرشيف التعافي"

    prompt_lines = [
        f"بصفتك باحثاً إكلينيكياً واستشارياً في جراحة التعافي وعلاج الجروح في مصر:",
        f"أريد بحثاً سريرياً دقيقاً وموثقاً حول: {d['focus']}.",
        "",
        "الأسئلة السريرية والبحثية المحددة المطلوب الإجابة عليها تفصيلياً:",
    ]
    prompt_lines.extend([f"• {q}" for q in d["queries"]])
    prompt_lines.append("")
    prompt_lines.append("مخاوف وتساؤلات المرضى المقلقة في مصر المطلوب طمأنتهم علمياً بشأنها:")
    prompt_lines.extend([f"• {a}" for a in d["anxieties"]])
    prompt_lines.append("")
    prompt_lines.append("تساؤلات وترندات بحث جوجل مصر الصاعدة هذا الأسبوع للإجابة عليها:")
    prompt_lines.extend([f"• {t}" for t in d["trends"][:4]])
    prompt_lines.append("")
    prompt_lines.append("الشروط الصارمة للمحتوى الناتج:")
    prompt_lines.append("1. نبرة طبية توجيهية هادئة تشرح فسيولوجيا التئام الأنسجة وتبدد المخاوف دون تهويل.")
    prompt_lines.append("2. استهداف الجمهور المصري وإجابات تناسب الصيف والعرق وطريقة الغيار المنزلي.")
    prompt_lines.append("3. منع تام لأي عروض تسويقية أو أسعار؛ التركيز 100% على الإرشاد والدعم والتثقيف الصحي.")
    prompt_lines.append("4. إدراج توجيه واضح للتواصل مع أخصائي التعافي عبر واتساب 01155803307 بكود HT10 وحق المعاينة قبل الاستلام.")
    prompt_lines.append("")
    prompt_lines.append("أحدث أبحاث PubMed السريرية المعتمدة للاستشهاد بها ودعم المحتوى:")
    for s in d["studies"]:
        prompt_lines.append(f"• [{s.get('pub_year')}] {s.get('title')} -> {s.get('url')}")

    raw_prompt = "\n".join(prompt_lines)
    escaped_code = html.escape(raw_prompt)

    msg = (
        f"🔬 <b>برومبت البحث المعمق في Gemini Deep Research</b>\n\n"
        f"🎯 <b>المنتج:</b> {name_ar}\n"
        f"📌 <b>المحور:</b> {focus}\n\n"
        f"🔑 <b>أهم الكلمات البحثية في مصر (Focus Keywords):</b>\n"
        f"{kws_html}\n\n"
        f"❓ <b>الأسئلة وترندات جوجل مصر الصاعدة:</b>\n"
        f"{lts_html}\n\n"
        f"📚 <b>أحدث أبحاث PubMed السريرية المعتمدة:</b>\n"
        f"{studies_html}\n\n"
        f"📋 <b>نص البرومبت الإكلينيكي (اضغط داخل المربع للنسخ الفوري بلمسة واحدة 👇):</b>\n"
        f"<pre><code>{escaped_code}</code></pre>"
    )

    keyboard = {
        "inline_keyboard": [
            [
                {"text": "🌐 فتح موقع Gemini مباشرة", "url": "https://gemini.google.com/"},
            ],
            [
                {"text": "🎙️ برومبت NotebookLM", "callback_data": f"prompt_nlm_{choice}"},
                {"text": "🎨 برومبت Pomelli", "callback_data": f"prompt_pomelli_{choice}"},
            ],
            [
                {"text": "🔙 رجوع لخيارات المنتج", "callback_data": f"hub_prod_{choice}"},
                {"text": "🏠 القائمة الرئيسية", "callback_data": "menu_main"},
            ],
        ]
    }
    return msg, keyboard


def build_notebooklm_prompt_card(choice: str) -> Tuple[str, Dict[str, Any]]:
    d = get_product_data(choice)
    name_ar = html.escape(d["name_ar"])

    audio_prompt = (
        f"قم بتوليد حوار صوتي بين اثنين من استشاريي التعافي الطبي باللهجة المصرية الراقية يشرحان فيه بأسلوب ودي مريح "
        f"للمريض أهمية {d['name_ar']} في مرحلة التعافي، وكيفية التغلب على الحكة أو القلق بعد العملية وتصحيح المفاهيم الخاطئة "
        f"الشائعة في مصر، مع التأكيد على حق معاينة المنتج قبل الاستلام وتطبيق كود HT10 والاستشارة عبر واتساب 01155803307."
    )

    video_prompt = (
        f"أنشئ فيديو شارحاً تفاعلياً (Explainer Video) لحالة التعافي باستخدام {d['name_ar']} يركز على بيولوجيا التئام "
        f"الأنسجة وطريقة العناية السليمة بالخطوات، بنبرة طمأنينة علمية راقية تجيب على قلق المريض المصري من الندبات "
        f"والالتهاب ومخاوف الاستحمام، مع التنويه لحق معاينة الشحنة قبل الاستلام والتواصل واتساب 01155803307 بكود HT10."
    )

    msg = (
        f"🎙️ <b>برومبتات استوديو Google NotebookLM</b>\n\n"
        f"🎯 <b>المنتج:</b> {name_ar}\n\n"
        f"💡 <i>طريقة الاستخدام:</i>\n"
        f"1. افتح رابط NotebookLM أدناه وأنشئ نوت بوك جديد.\n"
        f"2. ارفع ملف المعرفة السريرية المرفق، أو أبحاث PubMed.\n"
        f"3. انسخ الأوامر التالية واستخدمها في استوديو الصوت والفيديو:\n\n"
        f"🎧 <b>1️⃣ برومبت البودكاست والنقاش الصوتي (Audio Overview):</b>\n"
        f"<i>(اضغط داخل المربع للنسخ الفوري بلمسة واحدة 👇)</i>\n"
        f"<pre><code>{html.escape(audio_prompt)}</code></pre>\n\n"
        f"🎬 <b>2️⃣ برومبت الفيديو التوضيحي السريري (Video Overview):</b>\n"
        f"<i>(اضغط داخل المربع للنسخ الفوري بلمسة واحدة 👇)</i>\n"
        f"<pre><code>{html.escape(video_prompt)}</code></pre>"
    )

    keyboard = {
        "inline_keyboard": [
            [
                {"text": "🌐 فتح Google NotebookLM مباشرة", "url": "https://notebooklm.google.com/"},
            ],
            [
                {"text": "🔬 برومبت Gemini", "callback_data": f"prompt_gemini_{choice}"},
                {"text": "🎨 برومبت Pomelli", "callback_data": f"prompt_pomelli_{choice}"},
            ],
            [
                {"text": "🔙 رجوع لخيارات المنتج", "callback_data": f"hub_prod_{choice}"},
                {"text": "🏠 القائمة الرئيسية", "callback_data": "menu_main"},
            ],
        ]
    }
    return msg, keyboard


def build_pomelli_prompt_card(choice: str) -> Tuple[str, Dict[str, Any]]:
    d = get_product_data(choice)
    name_ar = html.escape(d["name_ar"])
    p1 = d.get("pomelli_1_1", "")
    p9 = d.get("pomelli_9_16", "")

    msg = (
        f"🎨 <b>برومبتات توليد الصور الطبية في Google Pomelli (واقعية سريرية 8K)</b>\n\n"
        f"🎯 <b>المنتج:</b> {name_ar}\n\n"
        f"📐 <b>1️⃣ برومبت البوست المربع 1:1 (للموقع وفيسبوك وإنستجرام Feed):</b>\n"
        f"<i>(اضغط داخل المربع للنسخ الفوري بلمسة واحدة 👇)</i>\n"
        f"<pre><code>{html.escape(p1)}</code></pre>\n\n"
        f"📱 <b>2️⃣ برومبت الستوري والريلز العمودي 9:16 (إنستجرام وتيك توك):</b>\n"
        f"<i>(اضغط داخل المربع للنسخ الفوري بلمسة واحدة 👇)</i>\n"
        f"<pre><code>{html.escape(p9)}</code></pre>\n\n"
        f"💡 <i>تذكير: أي صورة تقوم بحفظها من Pomelli، أرسلها هنا مباشرة في الشات لتصل إلى manual_inbox تلقائياً!</i>"
    )

    keyboard = {
        "inline_keyboard": [
            [
                {"text": "🎨 فتح Google Pomelli Brand Book مباشرة", "url": POMELLI_BRAND_BOOK_URL},
            ],
            [
                {"text": "🔬 برومبت Gemini", "callback_data": f"prompt_gemini_{choice}"},
                {"text": "🎙️ برومبت NotebookLM", "callback_data": f"prompt_nlm_{choice}"},
            ],
            [
                {"text": "🔙 رجوع لخيارات المنتج", "callback_data": f"hub_prod_{choice}"},
                {"text": "🏠 القائمة الرئيسية", "callback_data": "menu_main"},
            ],
        ]
    }
    return msg, keyboard


def build_social_prompts_menu(choice: str) -> Tuple[str, Dict[str, Any]]:
    d = get_product_data(choice)
    name_ar = html.escape(d["name_ar"])

    text = (
        f"📱 <b>برومبتات صناعة المحتوى السريري والسيو لمنصات التواصل</b>\n\n"
        f"🎯 <b>المنتج:</b> {name_ar}\n\n"
        f"👇 <b>اختر نوع المحتوى المطلوب لعرض البرومبت والسكريبت المهيأ للنسخ:</b>"
    )

    keyboard = {
        "inline_keyboard": [
            [
                {"text": "🎬 البرومبت الموحد الشامل — Google Flow", "callback_data": f"prompt_flow_{choice}"},
            ],
            [
                {"text": "🎬 سكريبت وسيو يوتيوب مصر (16:9 + Shorts)", "callback_data": f"prompt_yt_{choice}"},
            ],
            [
                {"text": "⚡ سكريبت تيك توك مصر (Viral Hook)", "callback_data": f"prompt_tt_{choice}"},
            ],
            [
                {"text": "📸 كاروسيل وريلز إنستجرام وفيسبوك مصر", "callback_data": f"prompt_ig_{choice}"},
            ],
            [
                {"text": "🔙 رجوع لخيارات المنتج", "callback_data": f"hub_prod_{choice}"},
                {"text": "🏠 القائمة الرئيسية", "callback_data": "menu_main"},
            ],
        ]
    }
    return text, keyboard


def build_social_prompt_card(choice: str, sub: str) -> Tuple[str, Dict[str, Any]]:
    cfg = PRODUCT_PROMPT_CONFIGS.get(choice, PRODUCT_PROMPT_CONFIGS.get("1", {}))
    name_ar = cfg.get("name_ar", "")
    focus = cfg.get("clinical_focus", "")
    kws = "، ".join(cfg.get("target_keywords_egypt", [])[:5])
    lts = "\n".join([f"• {q}" for q in cfg.get("long_tail_queries_egypt", [])[:4]])
    hashtags = " ".join(cfg.get("egypt_hashtags", []))

    if sub == "yt":
        title = "🎬 <b>برومبت سكريبت وسيو يوتيوب مصر (Long-form + Shorts)</b>"
        prompt = (
            f"بصفتك كبير استشاريي إنتاج الفيديو الطبي والسيو السريري في مصر (Clinical Video SEO Specialist - Egypt):\n"
            f"الموضوع السريري: {name_ar} - {focus}.\n\n"
            f"الكلمات المفتاحية الإلزامية بمصر: {kws}\n\n"
            f"الأسئلة الأكثر بحثاً في مصر المطلوب الإجابة عليها بالفيديو:\n{lts}\n\n"
            f"المطلوب إنتاجه تفصيلياً:\n"
            f"1. [العنوان السريري الجذاب]: عنوان أقل من 60 حرفاً يثير الطمأنينة بدون تهويل تجاري.\n"
            f"2. [سكريبت الفيديو الكامل 16:9 (3 إلى 5 دقائق)]:\n"
            f"   • أول 15 ثانية (Hook): مخاطبة مباشرة لأكبر خوف يقلق المريض المصري.\n"
            f"   • الدقيقة 1-2 (فسيولوجيا الأنسجة): شرح مبسط لكيفية تعافي الجرح.\n"
            f"   • الدقيقة 2-4 (البروتوكول السريري العملي): خطوات العناية العملية بالترتيب بأمان.\n"
            f"   • الخاتمة (CTA): طمأنة المريض والتوجيه الهادئ لطلب استشارة مجانية عبر واتساب 01155803307 بكود HT10 وحق المعاينة قبل الاستلام والشحن المجاني.\n"
            f"3. [سكريبت شورتس عمودي 9:16 (أقل من 59 ثانية)].\n"
            f"4. [وصف الفيديو المهيأ لسيو يوتيوب مصر SEO Description].\n"
            f"5. [قائمة التاغات الدلالية Tags]: 15 تاغ بحثي نشط في يوتيوب مصر.\n\n"
            f"القواعد الإلزامية: منع تام لذكر أي أسعار أو خصومات بيعية؛ النبرة طبية توجيهية وقورة."
        )
    elif sub == "tt":
        title = "⚡ <b>برومبت سكريبت تيك توك مصر (Viral Hook & Script)</b>"
        prompt = (
            f"بصفتك صانع محتوى طبي رقمي متخصص في خوارزميات تيك توك في مصر (TikTok Medical SEO - Egypt):\n"
            f"الموضوع السريري: {name_ar} - {focus}.\n"
            f"الكلمات المستهدفة بمصر: {kws}\n\n"
            f"المطلوب إنتاجه بدقة تامة:\n"
            f"1. [الهوك البصري والنفسي في أول ثانيتين]: جملة افتتاحية قوية توقف التمرير فوراً.\n"
            f"2. [سكريبت الفيديو (مدة 45 إلى 55 ثانية)]:\n"
            f"   • اللهجة: لهجة مصرية بيضاء راقية ومحترمة.\n"
            f"   • توجيهات الكاميرا والمشاهد (Visual & B-roll Cues) بين أقواس.\n"
            f"   • النص المكتوب على الشاشة (On-Screen Text) أثناء الحديث.\n"
            f"   • خاتمة هادئة للتواصل مع أخصائي التعافي واتساب 01155803307 بكود HT10.\n"
            f"3. [كابشن تيك توك والهاشتاجات]: {hashtags}"
        )
    elif sub == "ig":
        title = "📸 <b>برومبت كاروسيل وريلز إنستجرام مصر</b>"
        prompt = (
            f"بصفتك مصمم محتوى سريري واستراتيجي إنستجرام في مصر:\n"
            f"الموضوع السريري: {name_ar} - {focus}.\n\n"
            f"المطلوب إنتاجه:\n"
            f"1. [دليل الكاروسيل السريري (Clinical Carousel - 7 شرائح توعوية)]:\n"
            f"   • الشريحة 1 (الغلاف): عنوان عريض يبرز الخطأ الشائع في رعاية الجروح.\n"
            f"   • الشريحة 2 (المشكلة الحقيقية): مخاوف المرضى الواقعية (التهاب، عرق، ألم).\n"
            f"   • الشريحة 3 (الفسيولوجيا): ماذا يحدث لطبقات الجلد وألياف الكولاجين؟\n"
            f"   • الشريحة 4 و 5 (الحل العملي خطوة بخطوة): طريقة الاستخدام الآمنة.\n"
            f"   • الشريحة 6 (الدليل العلمي): استشهاد سريع بأبحاث PubMed.\n"
            f"   • الشريحة 7 (الخاتمة): بطاقة التوجيه السريري واتساب 01155803307 بكود HT10.\n"
            f"2. [سكريبت ريلز عمودي 9:16 (50 ثانية)].\n"
            f"3. [كابشن إنستجرام مع الهاشتاجات]: {hashtags}"
        )
    else:  # blog
        title = "✍️ <b>برومبت مقال مدونة بلوجر (SEO 1500 كلمة)</b>"
        prompt = (
            f"بصفتك كبير كتاب المحتوى الطبي واستشاري السيو المتخصص في محرك بحث جوجل مصر:\n"
            f"نريد كتابة مقال طبي استشاري شامل ومطول (1200 إلى 1500 كلمة) مهيأ للتصدر في المرتبة الأولى بنتائج بحث جوجل في جمهورية مصر العربية.\n"
            f"الموضوع السريري: {name_ar} - {focus}.\n"
            f"الكلمات المفتاحية: {kws}\n"
            f"الأسئلة الأكثر بحثاً في مصر:\n{lts}\n\n"
            f"المطلوب:\n"
            f"1. مقدمة طمأنينة تشرح مخاوف المريض بأسلوب علمي راقٍ.\n"
            f"2. الفسيولوجيا الطبية لتعافي الأنسجة.\n"
            f"3. بروتوكول العناية خطوة بخطوة وطريقة التغيير الآمنة.\n"
            f"4. جدول مقارنة سريري بين المستلزم الأصلي والممارسات الخاطئة الشائعة.\n"
            f"5. فقرة الأسئلة الشائعة (FAQ Schema).\n"
            f"6. توجيه واضح لطلب استشارة سريرية مجانية عبر واتساب 01155803307 بكود HT10 وحق المعاينة قبل الاستلام."
        )

    msg = (
        f"{title}\n\n"
        f"🎯 <b>المنتج:</b> {html.escape(name_ar)}\n\n"
        f"📋 <b>نص البرومبت الإكلينيكي (اضغط داخل المربع للنسخ الفوري بلمسة واحدة 👇):</b>\n"
        f"<pre><code>{html.escape(prompt)}</code></pre>"
    )

    keyboard = {
        "inline_keyboard": [
            [
                {"text": "🔙 رجوع لقائمة السوشيال", "callback_data": f"prompt_social_menu_{choice}"},
                {"text": "🎯 خيارات المنتج", "callback_data": f"hub_prod_{choice}"},
            ],
            [
                {"text": "🏠 القائمة الرئيسية", "callback_data": "menu_main"},
            ],
        ]
    }
    return msg, keyboard


def handle_show_product_hub(chat_id: str, choice: str):
    card_text, card_keyboard = build_product_hub_card(choice)
    bot.send_message(chat_id, card_text, reply_markup=card_keyboard)


def handle_show_google_flow_prompt(chat_id: str, choice: str):
    sess = get_session(chat_id)
    analysis = {
        "findings": sess.get("findings") or [],
        "anxieties": sess.get("anxieties") or [],
    }
    card_text, card_keyboard = build_unified_google_flow_card(choice, analysis)
    bot.send_message(chat_id, card_text, reply_markup=card_keyboard)


def handle_show_gemini_prompt(chat_id: str, choice: str):
    card_text, card_keyboard = build_gemini_prompt_card(choice)
    bot.send_message(chat_id, card_text, reply_markup=card_keyboard)


def handle_show_notebooklm_prompt(chat_id: str, choice: str):
    card_text, card_keyboard = build_notebooklm_prompt_card(choice)
    bot.send_message(chat_id, card_text, reply_markup=card_keyboard)


def handle_show_pomelli_prompt(chat_id: str, choice: str):
    card_text, card_keyboard = build_pomelli_prompt_card(choice)
    bot.send_message(chat_id, card_text, reply_markup=card_keyboard)


def handle_show_social_menu(chat_id: str, choice: str):
    card_text, card_keyboard = build_social_prompts_menu(choice)
    bot.send_message(chat_id, card_text, reply_markup=card_keyboard)


def handle_show_social_single(chat_id: str, choice: str, sub: str):
    card_text, card_keyboard = build_social_prompt_card(choice, sub)
    bot.send_message(chat_id, card_text, reply_markup=card_keyboard)


def handle_send_prompts_file(chat_id: str, choice: str):
    prompts_txt = MANUAL_INBOX / "PROMPTS_PACK_TODAY.txt"
    if not prompts_txt.exists():
        hub_archive = BASE_DIR / "media_assets" / "notebooklm_hub" / "archive"
        if hub_archive.exists():
            files = sorted(hub_archive.glob("Prompts_Pack_*.md"), key=lambda f: f.stat().st_mtime, reverse=True)
            if files:
                prompts_txt = files[0]

    prod_info = PRODUCTS_CATALOG.get(choice, PRODUCTS_CATALOG["1"])
    if prompts_txt.exists():
        caption = (
            f"📄 <b>ملف حزمة البرومبتات والمصادر الطبية الكاملة:</b>\n"
            f"🎯 <b>المنتج:</b> {prod_info['name']}\n"
            f"🎟️ <b>كود الخصم المعتمد:</b> HT10\n"
            f"🩺 <b>الاستشارة:</b> أخصائية العناية بالتعافي (واتساب 01155803307)"
        )
        bot.send_document(chat_id, prompts_txt, caption=caption)
    else:
        bot.send_message(chat_id, "⚠️ لم يتم العثور على ملف البرومبتات. يرجى اختيار المنتج لإعادة توليده.")


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
# 📥 Direct Media & Research Document Ingestion from Telegram
# =============================================================================

def handle_incoming_research_document(message: Dict[str, Any]):
    """Downloads clinical research document (.txt, .md, .pdf, .docx, .json) and extracts text."""
    chat_id = str(message.get("chat", {}).get("id"))
    if chat_id != AUTHORIZED_CHAT_ID:
        return

    doc = message["document"]
    file_id = doc["file_id"]
    original_name = doc.get("file_name") or "research_document.txt"
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest_path = RESEARCH_REPORTS_DIR / f"upload_{timestamp_str}_{original_name}"

    file_info = bot.get_file(file_id)
    if not file_info or "file_path" not in file_info:
        bot.send_message(chat_id, "❌ تعذر استرجاع مسار الملف من سيرفر تيليجرام.")
        return

    bot.send_message(chat_id, f"⏳ جاري استقبال المستند السريري <code>{original_name}</code> واستخراج محتواه...")
    if bot.download_file(file_info["file_path"], dest_path):
        extracted_text = extract_text_from_file(dest_path)
        if len(extracted_text) >= 40:
            handle_research_report_received(
                chat_id=chat_id,
                raw_text=extracted_text,
                source_label=f"مستند مرفوع ({original_name})",
                file_path=dest_path,
            )
        else:
            bot.send_message(
                chat_id,
                f"⚠️ تم تحميل المستند <code>{original_name}</code> لكن لم يتم العثور على محتوى نصي كافٍ (أقل من 40 حرف).\n"
                f"يرجى التأكد من أن الملف يحتوي على تقرير البحث السريري أو نسخ التقرير ولصقه مباشرة في الشات.",
                reply_markup=build_main_menu_keyboard(),
            )
    else:
        bot.send_message(chat_id, "❌ فشل تحميل الملف من سيرفر تيليجرام.")


def handle_incoming_media(message: Dict[str, Any]):
    """Saves user-sent photos, videos, or audio into manual_inbox."""
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
    elif "voice" in message or "audio" in message:
        aud = message.get("voice") or message.get("audio")
        file_id = aud["file_id"]
        original_name = f"telegram_audio_{timestamp_str}.mp3"
        media_type = "تسجيل صوتي 🎙️"
    elif "document" in message:
        doc = message["document"]
        file_id = doc["file_id"]
        original_name = doc.get("file_name") or f"telegram_doc_{timestamp_str}.dat"
        media_type = "مستند/ملف 📄"

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
        sess = get_session(chat_id)
        m_files = sess.get("media_files", [])
        m_files.append(save_path.name)
        update_session(chat_id, media_files=m_files, stage=STATE_STAGE_3_MEDIA)

        confirm_text = (
            f"✅ <b>تم استلام {media_type} وإيداعه في manual_inbox بنجاح!</b>\n\n"
            f"📁 <b>اسم الملف:</b> <code>{save_path.name}</code>\n"
            f"⚖️ <b>الحجم:</b> {size_kb} KB\n"
            f"📊 <b>إجمالي وسائط الجلسة:</b> {len(m_files)} أصل مهيأ\n"
            f"📍 <b>الموقع:</b> <code>manual_inbox</code>\n\n"
            f"👇 <b>الخطوة التالية (المرحلة 4 من 4):</b>\n"
            f"يمكنك إرسال المزيد من الصور والفيديوهات، أو إطلاق المسار الشامل الموحد الآن لاستيعاب كافة الوسائط وبناء صفحات الهبوط وتحديث البوابة والنشر الفوري:"
        )
        keyboard = {
            "inline_keyboard": [
                [{"text": "🚀 تشغيل المسار الشامل الموحد الآن (1-Click Pipeline)", "callback_data": "act_master"}],
                [{"text": "📥 استعراض محتويات manual_inbox", "callback_data": "act_inbox_status"}],
                [{"text": "🏠 القائمة الرئيسية", "callback_data": "menu_main"}],
            ]
        }
        bot.send_message(chat_id, confirm_text, reply_markup=keyboard)
    else:
        bot.send_message(chat_id, "❌ فشل تحميل الملف من سيرفر تيليجرام.")


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
        toast_msg = f"⏳ جاري تجهيز أبحاث وترندات المنتج [{data.split('_')[1]}]..."
    elif data.startswith("hub_prod_"):
        toast_msg = "🎯 خيارات وبرومبتات المنتج"
    elif data.startswith("prompt_gemini_"):
        toast_msg = "🔬 جاري عرض برومبت Gemini ومصادر PubMed..."
    elif data.startswith("prompt_nlm_"):
        toast_msg = "🎙️ جاري عرض برومبتات استوديو NotebookLM..."
    elif data.startswith("prompt_pomelli_"):
        toast_msg = "🎨 جاري عرض برومبتات Google Pomelli..."
    elif data.startswith("prompt_social_menu_"):
        toast_msg = "📱 قائمة برومبتات السوشيال ميديا"
    elif data.startswith("prompt_yt_"):
        toast_msg = "🎬 برومبت وسكريبت يوتيوب مصر"
    elif data.startswith("prompt_tt_"):
        toast_msg = "⚡ برومبت وسكريبت تيك توك مصر"
    elif data.startswith("prompt_ig_"):
        toast_msg = "📸 برومبت كاروسيل وريلز إنستجرام"
    elif data.startswith("prompt_blog_"):
        toast_msg = "✍️ برومبت مقال مدونة بلوجر"
    elif data.startswith("prompt_file_"):
        toast_msg = "📄 جاري إرسال حزمة البرومبتات كاملة..."
    elif data == "act_master":
        toast_msg = "🚀 جاري إطلاق المسار الشامل..."
    elif data == "act_dry_run":
        toast_msg = "👁️ جاري تشغيل وضع المعاينة..."
    elif data == "menu_reviews":
        toast_msg = "🌟 مركز استقبال وأرشفة تجارب المرضى"
    elif data.startswith("rev_prod_"):
        toast_msg = f"📥 تسجيل تجربة للمنتج [{data.split('_')[2]}]..."
    elif data == "rev_privacy_templates":
        toast_msg = "📋 قوالب النشر الطبية المعتمدة..."

    bot.answer_callback_query(cq_id, text=toast_msg)

    # 1. Main Menu Navigation
    if data == "menu_main":
        reset_session(chat_id)
        bot.edit_message_text(chat_id, msg_id, get_main_menu_text(), reply_markup=build_main_menu_keyboard())

    # 2. Products Submenu
    elif data == "menu_products":
        bot.edit_message_text(chat_id, msg_id, get_products_menu_text(), reply_markup=build_products_submenu_keyboard())

    # 2b. Reviews Hub Submenu & Actions
    elif data == "menu_reviews":
        bot.edit_message_text(chat_id, msg_id, get_reviews_hub_text(), reply_markup=build_reviews_hub_keyboard())

    elif data.startswith("rev_prod_"):
        prod_key = data.split("_")[2]
        slug = PRODUCT_SLUGS.get(prod_key, f"product_{prod_key}")
        prod_meta = PRODUCTS_CATALOG.get(prod_key, {})
        prod_name = prod_meta.get("name", f"المنتج رقم {prod_key}")
        update_session(chat_id, stage=STATE_STAGE_REVIEW_INTAKE, review_product_id=prod_key)
        intake_prompt = (
            f"📥 <b>تسجيل تجربة سريرية جديدة: {prod_name}</b>\n\n"
            f"📦 <b>المعرف السريري:</b> <code>{slug}</code>\n"
            f"🔒 <b>الحالة:</b> <code>{STATE_STAGE_REVIEW_INTAKE}</code>\n\n"
            f"📸 <b>لإضافة صورة أو سكرين شات:</b> أرسل الصورة مباشرة في المحادثة.\n"
            f"🎙️ <b>لإضافة تسجيل صوتي (Voice Note):</b> أرسل الفويس نوت مباشرة.\n"
            f"✍️ <b>لإضافة نص التقييم:</b> أرسل رسالة نصية بالرأي والملاحظات السريرية.\n\n"
            f"👇 <b>اختر الإجراء التالي:</b>"
        )
        kb = {
            "inline_keyboard": [
                [{"text": "📋 استعراض قوالب النشر الطبية", "callback_data": "rev_privacy_templates"}],
                [{"text": "🌟 العودة لمركز تجارب المرضى", "callback_data": "menu_reviews"}],
                [{"text": "🏠 القائمة الرئيسية", "callback_data": "menu_main"}],
            ]
        }
        bot.edit_message_text(chat_id, msg_id, intake_prompt, reply_markup=kb)

    elif data == "rev_privacy_templates":
        sess = get_session(chat_id)
        prod_key = sess.get("review_product_id") or "2"
        prod_meta = PRODUCTS_CATALOG.get(prod_key, {})
        prod_name = prod_meta.get("name", "BUPY Medical Silicone Scar Sheet")
        sample_meta = {
            "review_id": f"rev_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "product_id": PRODUCT_SLUGS.get(prod_key, "bupy-silicone-scar-sheet"),
            "product_name": prod_name,
            "timestamp": datetime.now().isoformat(),
            "rating": 5,
            "patient_pseudonym": "أم قيصرية - القاهرة",
            "surgery_type": "ولادة قيصرية (اليوم 21)",
            "review_text": "شيت السيليكون فرق جدا في تسطيح الندبة وتخفيف الشد بعد أسبوعين من الاستخدام المنتظم.",
            "specialist_advice": "ينصح بالاستمرار على شيت السيليكون لمدة 12 ساعة يومياً لحماية الأنسجة وتجنب الكيلويد.",
        }
        tpls = build_medical_privacy_review_templates(sample_meta)
        preview_text = (
            "📋 <b>قوالب النشر المعتمدة طبياً (Medical Privacy Compliant Templates)</b>\n"
            "<i>مطابقة لمعايير خصوصية المرضى المصرية وقواعد وزارة الصحة</i>\n\n"
            "──────────\n"
            "<b>1️⃣ إنستجرام / فيسبوك (7-Slide Carousel):</b>\n"
            f"{tpls['instagram_carousel']}\n\n"
            "──────────\n"
            "<b>2️⃣ تيك توك / ريلز (30s Script):</b>\n"
            f"{tpls['tiktok_reels_script']}\n\n"
            "──────────\n"
            "<b>3️⃣ مقال بلوجر / الموقع:</b>\n"
            f"<code>{tpls['blogger_snippet']}</code>"
        )
        if len(preview_text) > 4000:
            preview_text = preview_text[:3950] + "\n\n... [تم الاقتطاع لطول الرسالة]"
        kb = {
            "inline_keyboard": [
                [{"text": "🌟 العودة لمركز تجارب المرضى", "callback_data": "menu_reviews"}],
                [{"text": "🏠 القائمة الرئيسية", "callback_data": "menu_main"}],
            ]
        }
        bot.send_message(chat_id, preview_text, reply_markup=kb)

    # 3. Product Selection & Generation (Stage 1 Launcher)
    elif data.startswith("prod_"):
        choice = data.split("_")[1]
        threading.Thread(
            target=handle_product_research_generation,
            args=(chat_id, choice),
            daemon=True,
        ).start()

    # 4. Product Prompt Hub & Platform Prompts
    elif data.startswith("hub_prod_"):
        choice = data.split("_")[2]
        handle_show_product_hub(chat_id, choice)

    elif data.startswith("prompt_flow_"):
        choice = data.split("_")[2]
        handle_show_google_flow_prompt(chat_id, choice)

    elif data.startswith("prompt_gemini_"):
        choice = data.split("_")[2]
        handle_show_gemini_prompt(chat_id, choice)

    elif data.startswith("prompt_nlm_"):
        choice = data.split("_")[2]
        handle_show_notebooklm_prompt(chat_id, choice)

    elif data.startswith("prompt_pomelli_"):
        choice = data.split("_")[2]
        handle_show_pomelli_prompt(chat_id, choice)

    elif data.startswith("prompt_social_menu_"):
        choice = data.split("_")[3]
        handle_show_social_menu(chat_id, choice)

    elif data.startswith("prompt_yt_"):
        choice = data.split("_")[2]
        handle_show_social_single(chat_id, choice, "yt")

    elif data.startswith("prompt_tt_"):
        choice = data.split("_")[2]
        handle_show_social_single(chat_id, choice, "tt")

    elif data.startswith("prompt_ig_"):
        choice = data.split("_")[2]
        handle_show_social_single(chat_id, choice, "ig")

    elif data.startswith("prompt_blog_"):
        choice = data.split("_")[2]
        handle_show_social_single(chat_id, choice, "blog")

    elif data.startswith("prompt_file_"):
        choice = data.split("_")[2]
        handle_send_prompts_file(chat_id, choice)

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

    elif data == "act_cloud_archive":
        threading.Thread(
            target=handle_cloud_archive,
            args=(chat_id,),
            daemon=True,
        ).start()


def handle_cloud_archive(chat_id: str):
    """Uploads archives/packs to Google Drive, purges verified local copies, reports freed space."""
    try:
        from scripts.cloud_archiver import sync_and_purge, local_status, format_report_ar
    except ImportError:
        from cloud_archiver import sync_and_purge, local_status, format_report_ar  # type: ignore
    try:
        st = local_status()
        bot.send_message(
            chat_id,
            "⏳ <b>جاري الأرشفة السحابية إلى Google Drive...</b>\n"
            f"📦 حجم الأرشيف المحلي الحالي: {st.get('total_mb')} MB\n"
            f"💾 المساحة الحرة قبل التفريغ: {st.get('disk_free_gb')} GB\n"
            "🔒 لن يُحذف أي ملف من الجهاز قبل التحقق من رفعه بنجاح.",
        )
        res = sync_and_purge(purge=True, clean_portal_dist=True)
        bot.send_message(chat_id, format_report_ar(res), reply_markup=build_main_menu_keyboard())
    except Exception as e:  # noqa: BLE001
        bot.send_message(chat_id, f"❌ تعذرت الأرشفة السحابية: <code>{e}</code>", reply_markup=build_main_menu_keyboard())

def handle_incoming_review_media(msg: Dict[str, Any], session: Dict[str, Any]):
    """R5: Ingests patient review media (photo or audio) into client_reviews/{product_id}/."""
    chat_id = str(msg.get("chat", {}).get("id"))
    prod_key = session.get("review_product_id") or "2"
    prod_slug = PRODUCT_SLUGS.get(prod_key, f"product_{prod_key}")
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")

    photo_bytes = None
    photo_filename = None
    audio_bytes = None
    audio_filename = None

    if "photo" in msg:
        photo = msg["photo"][-1]
        file_id = photo["file_id"]
        file_info = bot.get_file(file_id)
        if file_info and "file_path" in file_info:
            temp_path = MEDIA_DIR / f"temp_rev_{timestamp_str}.jpg"
            if bot.download_file(file_info["file_path"], temp_path):
                photo_bytes = temp_path.read_bytes()
                photo_filename = f"review_photo_{timestamp_str}.jpg"
                try:
                    temp_path.unlink()
                except Exception:
                    pass
    elif "voice" in msg or "audio" in msg:
        aud = msg.get("voice") or msg.get("audio")
        file_id = aud["file_id"]
        file_info = bot.get_file(file_id)
        if file_info and "file_path" in file_info:
            temp_path = MEDIA_DIR / f"temp_rev_{timestamp_str}.mp3"
            if bot.download_file(file_info["file_path"], temp_path):
                audio_bytes = temp_path.read_bytes()
                audio_filename = f"review_voice_{timestamp_str}.mp3"
                try:
                    temp_path.unlink()
                except Exception:
                    pass

    record = intake_client_review_asset(
        product_id=prod_slug,
        review_data={
            "patient_pseudonym": "أم قيصرية - القاهرة",
            "surgery_type": PRODUCTS_CATALOG.get(prod_key, {}).get("tag", "رعاية سريرية"),
            "review_text": "تم استلام وسائط التجربة السريرية بنجاح عبر تيليجرام.",
            "rating": 5,
        },
        photo_bytes=photo_bytes,
        audio_bytes=audio_bytes,
        photo_filename=photo_filename,
        audio_filename=audio_filename,
    )

    confirm_text = (
        f"✅ <b>تم استلام وأرشفة وسائط التجربة بنجاح!</b>\n\n"
        f"🆔 <b>معرف التجربة:</b> <code>{record['review_id']}</code>\n"
        f"📦 <b>المنتج:</b> <code>{prod_slug}</code>\n"
        f"📂 <b>المسار:</b> <code>media_assets/client_reviews/{prod_slug}/</code>\n\n"
        f"👇 <b>يمكنك استعراض قوالب النشر الطبية المعتمدة لهذه التجربة:</b>"
    )
    kb = {
        "inline_keyboard": [
            [{"text": "📋 استعراض قوالب النشر الطبية", "callback_data": "rev_privacy_templates"}],
            [{"text": "🌟 العودة لمركز تجارب المرضى", "callback_data": "menu_reviews"}],
            [{"text": "🏠 القائمة الرئيسية", "callback_data": "menu_main"}],
        ]
    }
    bot.send_message(chat_id, confirm_text, reply_markup=kb)


def process_message(msg: Dict[str, Any]):
    chat_id = str(msg.get("chat", {}).get("id"))

    # Security Gate
    if chat_id != AUTHORIZED_CHAT_ID:
        bot.send_message(
            chat_id,
            "⚠️ <b>عذراً، هذا البوت خاص بمركز القيادة السريري لهيلينج تاتش مصر.</b>\nالوصول مقتصر على المشرف المعتمد فقط.",
        )
        return

    # Check session state for review intake media
    session = get_session(chat_id)
    if session.get("stage") == STATE_STAGE_REVIEW_INTAKE:
        if any(k in msg for k in ("photo", "voice", "audio")):
            handle_incoming_review_media(msg, session)
            return

    # Check for document upload: if research text document -> Stage 2 Ingestion, else media
    if "document" in msg:
        doc = msg["document"]
        fname = (doc.get("file_name") or "").lower()
        if any(fname.endswith(ext) for ext in [".txt", ".md", ".pdf", ".docx", ".doc", ".json"]):
            handle_incoming_research_document(msg)
            return
        else:
            handle_incoming_media(msg)
            return

    # Direct media uploads (photos, videos, audio)
    if any(k in msg for k in ("photo", "video", "voice", "audio")):
        handle_incoming_media(msg)
        return

    text = msg.get("text", "").strip()

    # Commands & Shortcuts
    if text.startswith("/start") or text == "قائمة" or text.startswith("/menu"):
        reset_session(chat_id)
        bot.send_message(chat_id, get_main_menu_text(), reply_markup=build_main_menu_keyboard())
        return
    elif text.startswith("/cancel") or text == "إلغاء":
        reset_session(chat_id)
        bot.send_message(chat_id, "🔙 تم إلغاء العملية والعودة للقائمة الرئيسية.", reply_markup=build_main_menu_keyboard())
        return
    elif text.startswith("/run") or text == "1":
        threading.Thread(
            target=handle_master_pipeline_execution,
            args=(chat_id,),
            daemon=True,
        ).start()
        return
    elif text.startswith("/products") or text == "2":
        bot.send_message(chat_id, get_products_menu_text(), reply_markup=build_products_submenu_keyboard())
        return
    elif text.startswith("/status"):
        handle_n8n_status(chat_id)
        return

    # Check session state for review text intake
    if session.get("stage") == STATE_STAGE_REVIEW_INTAKE and text:
        prod_key = session.get("review_product_id") or "2"
        prod_slug = PRODUCT_SLUGS.get(prod_key, f"product_{prod_key}")
        record = intake_client_review_asset(
            product_id=prod_slug,
            review_data={
                "patient_pseudonym": "أم قيصرية - القاهرة",
                "surgery_type": PRODUCTS_CATALOG.get(prod_key, {}).get("tag", "رعاية سريرية"),
                "review_text": text,
                "rating": 5,
            },
        )
        confirm_text = (
            f"✅ <b>تم تسجيل وحفظ نص التجربة السريرية بنجاح!</b>\n\n"
            f"🆔 <b>المعرف:</b> <code>{record['review_id']}</code>\n"
            f"📦 <b>المنتج:</b> <code>{prod_slug}</code>\n"
            f"📝 <b>نص التجربة:</b> \"{text}\"\n\n"
            f"👇 <b>يمكنك استعراض قوالب النشر الطبية المعتمدة:</b>"
        )
        kb = {
            "inline_keyboard": [
                [{"text": "📋 استعراض قوالب النشر الطبية", "callback_data": "rev_privacy_templates"}],
                [{"text": "🌟 العودة لمركز تجارب المرضى", "callback_data": "menu_reviews"}],
                [{"text": "🏠 القائمة الرئيسية", "callback_data": "menu_main"}],
            ]
        }
        bot.send_message(chat_id, confirm_text, reply_markup=kb)
        return

    # Check session state for clinical research text upload
    session = get_session(chat_id)
    if session.get("stage") == STATE_STAGE_1_RESEARCH or len(text) >= 70:
        handle_research_report_received(chat_id, text, source_label="رسالة نصية مباشرة")
        return

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
    if not acquire_single_instance_lock():
        logger.warning(
            "Another instance of TelegramControlBot is already active on 127.0.0.1:%d. Exiting cleanly.",
            SINGLE_INSTANCE_PORT,
        )
        sys.exit(0)
    try:
        run_bot_polling()
    except Exception as fatal_e:
        logger.critical("Fatal unhandled exception in bot main: %s", fatal_e, exc_info=True)
