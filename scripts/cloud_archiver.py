#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
☁️ هيلينج تاتش مصر | الأرشفة السحابية على Google Drive وتفريغ مساحة الجهاز
Cloud Archiver — offload heavy media archives to Google Drive, then purge
local copies ONLY after the upload has been verified (name + byte size).
=============================================================================
Backends (auto-detected, in order):
  1. Google Drive for Desktop mount  (e.g. G:\\My Drive)  -> fully automatic,
     works from the Telegram bot and the 1-Click pipeline.
     Override with env var HT_GDRIVE_DESKTOP_ROOT.
  2. `gdrive` CLI on PATH (Antigravity Google Drive plugin) -> used when the
     archive sync is executed from an Antigravity agent session.
  3. none -> nothing is uploaded and NOTHING is deleted (safe no-op report).

Safety rules:
  * A local file is deleted only if the manifest records a verified upload
    with the same byte size.
  * The newest `keep_latest` entries of every archive root are always kept
    locally (the pipeline falls back to the latest archive / pack).
  * Backup-only roots (pomelli_library, branded_designs, research reports,
    client reviews, CRM db) are uploaded but never purged.

Usage:
  python scripts/cloud_archiver.py --status
  python scripts/cloud_archiver.py --sync            # upload + verify + purge
  python scripts/cloud_archiver.py --sync --no-purge # upload only
  python scripts/cloud_archiver.py --sync --dry-run
"""

from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import json
import logging
import os
import re
import shutil
import string
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_DIR = BASE_DIR / "media_assets"
CONFIG_DIR = BASE_DIR / "config"
FOLDER_MAP_FILE = CONFIG_DIR / "gdrive_archive_map.json"
MANIFEST_FILE = CONFIG_DIR / "cloud_archive_manifest.json"

CLOUD_ROOT_NAME = "Healing_Touch_Egypt_Cloud_Archive"
CLOUD_ROOT_URL_TMPL = "https://drive.google.com/drive/folders/{}"

logger = logging.getLogger("CloudArchiver")
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%H:%M:%S")


@dataclass
class ArchiveSpec:
    local_rel: str            # path relative to BASE_DIR
    drive_path: str           # path under the cloud root folder
    purge: bool               # delete local copies after verified upload
    keep_latest: int = 0      # newest top-level entries always kept locally
    include: List[str] = field(default_factory=lambda: ["*"])   # top-level name patterns
    exclude: List[str] = field(default_factory=list)            # top-level name patterns
    recursive: bool = True


ARCHIVE_SPECS: List[ArchiveSpec] = [
    ArchiveSpec("media_assets/manual_inbox/archive", "01_Processed_Inbox_Archive", purge=True, keep_latest=0),
    ArchiveSpec("media_assets/ready_to_publish", "02_Ready_To_Publish_Packs", purge=True, keep_latest=1,
                include=["20*"]),
    ArchiveSpec("media_assets/notebooklm_hub/audio_inputs", "03_Clinical_Research_NotebookLM/audio_inputs",
                purge=True, keep_latest=1),
    ArchiveSpec("media_assets/notebooklm_hub/archive", "03_Clinical_Research_NotebookLM/archive",
                purge=True, keep_latest=0),
    ArchiveSpec("media_assets/notebooklm_hub/daily_sources_archive",
                "03_Clinical_Research_NotebookLM/daily_sources_archive", purge=True, keep_latest=2),
    ArchiveSpec("media_assets/notebooklm_hub", "03_Clinical_Research_NotebookLM/briefs", purge=True,
                keep_latest=1, include=["Healing_Touch_Brief_*.md"], recursive=False),
    ArchiveSpec("media_assets/notebooklm_hub/research_reports",
                "03_Clinical_Research_NotebookLM/research_reports", purge=False),
    ArchiveSpec("media_assets/notebooklm_hub/pic", "03_Clinical_Research_NotebookLM/pic", purge=False),
    ArchiveSpec("media_assets/pomelli_library", "04_Pomelli_Branded_Designs/pomelli_library", purge=False),
    ArchiveSpec("media_assets/branded_designs", "04_Pomelli_Branded_Designs/branded_designs", purge=False),
    ArchiveSpec("media_assets/client_reviews", "05_Client_Reviews_Proof", purge=False),
    ArchiveSpec("media_assets/crm_leads", "06_CRM_Leads_Backups", purge=False, include=["*.db", "*.csv", "*.json"],
                recursive=False),
    ArchiveSpec("media_assets/archive", "07_Media_Archive_Legacy", purge=True, keep_latest=0),
]

FLOW_INBOX_DRIVE_SUBFOLDER = "00_Flow_Inbox"

TOP_FOLDERS = sorted({s.drive_path.split("/")[0] for s in ARCHIVE_SPECS})

_lock = threading.Lock()


# -----------------------------------------------------------------------------
# JSON helpers
# -----------------------------------------------------------------------------
def _load_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)


def _rel(p: Path) -> str:
    return p.relative_to(BASE_DIR).as_posix()


# -----------------------------------------------------------------------------
# Backends
# -----------------------------------------------------------------------------
class DesktopBackend:
    """Google Drive for Desktop mounted folder (G:\\My Drive)."""
    name = "google_drive_desktop"

    def __init__(self, my_drive: Path):
        self.root = my_drive / CLOUD_ROOT_NAME
        self.root.mkdir(parents=True, exist_ok=True)
        (self.root / FLOW_INBOX_DRIVE_SUBFOLDER).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def detect() -> Optional["DesktopBackend"]:
        env = os.environ.get("HT_GDRIVE_DESKTOP_ROOT", "").strip()
        candidates: List[Path] = []
        if env:
            candidates.append(Path(env))
        for letter in string.ascii_uppercase:
            for sub in ("My Drive", "ملفاتي", "Mon Drive"):
                candidates.append(Path(f"{letter}:/{sub}"))
        for c in candidates:
            try:
                if c.is_dir():
                    return DesktopBackend(c)
            except OSError:
                continue
        return None

    def upload(self, local: Path, drive_rel_dir: str) -> Dict[str, str]:
        dest_dir = self.root / drive_rel_dir
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / local.name
        shutil.copy2(local, dest)
        if dest.stat().st_size != local.stat().st_size:
            raise IOError(f"size mismatch after copy: {dest}")
        return {"id": str(dest), "size": str(dest.stat().st_size)}

    def root_url(self, folder_map: Dict[str, str]) -> str:
        return folder_map.get("root") and CLOUD_ROOT_URL_TMPL.format(folder_map["root"]) or str(self.root)


class CliBackend:
    """Antigravity `gdrive` CLI (available inside agent sessions)."""
    name = "gdrive_cli"
    _ID_RE = re.compile(r"\(ID:\s*([A-Za-z0-9_\-]+)\)")

    def __init__(self, exe: str):
        self.exe = exe
        self.folder_map: Dict[str, str] = _load_json(FOLDER_MAP_FILE, {})

    @staticmethod
    def detect() -> Optional["CliBackend"]:
        exe = shutil.which("gdrive")
        if not exe:
            return None
        try:
            r = subprocess.run([exe, "readonly", "quota"], capture_output=True, text=True,
                               encoding="utf-8", errors="replace", timeout=60)
            if r.returncode != 0:
                return None
        except Exception:
            return None
        return CliBackend(exe)

    def _run(self, *args: str, timeout: int = 900) -> str:
        r = subprocess.run([self.exe, *args], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout)
        if r.returncode != 0:
            raise RuntimeError(f"gdrive {' '.join(args[:2])} failed: {(r.stderr or r.stdout).strip()[:300]}")
        return r.stdout

    def _find_child_folder(self, name: str, parent: str) -> Optional[str]:
        out = self._run("readonly", "search", "--name-exact", name, "--parent-id", parent, "--json", timeout=120)
        try:
            for item in json.loads(out or "[]"):
                if item.get("mimeType") == "application/vnd.google-apps.folder":
                    return item["id"]
        except json.JSONDecodeError:
            pass
        return None

    def ensure_root(self) -> str:
        with _lock:
            if self.folder_map.get("root"):
                return self.folder_map["root"]
            out = self._run("readonly", "search", "--name-exact", CLOUD_ROOT_NAME, "--json", timeout=120)
            items = [i for i in json.loads(out or "[]") if i.get("mimeType", "").endswith("folder")]
            if items:
                fid = items[0]["id"]
            else:
                m = self._ID_RE.search(self._run("mutate", "mkdir", CLOUD_ROOT_NAME))
                fid = m.group(1)
            self.folder_map["root"] = fid
            _save_json(FOLDER_MAP_FILE, self.folder_map)
            return fid

    def ensure_folder(self, drive_rel_dir: str) -> str:
        parent = self.ensure_root()
        acc = ""
        for part in [p for p in drive_rel_dir.split("/") if p]:
            acc = f"{acc}/{part}" if acc else part
            with _lock:
                cached = self.folder_map.get(acc)
            if cached:
                parent = cached
                continue
            fid = self._find_child_folder(part, parent)
            if not fid:
                m = self._ID_RE.search(self._run("mutate", "mkdir", part, "--parent", parent))
                if not m:
                    raise RuntimeError(f"could not create folder {acc}")
                fid = m.group(1)
            with _lock:
                self.folder_map[acc] = fid
                _save_json(FOLDER_MAP_FILE, self.folder_map)
            parent = fid
        return parent

    def upload(self, local: Path, drive_rel_dir: str) -> Dict[str, str]:
        parent = self.ensure_folder(drive_rel_dir)
        out = self._run("mutate", "upload", str(local), "--parent", parent)
        m = self._ID_RE.search(out)
        if not m:
            raise RuntimeError(f"upload returned no ID for {local.name}: {out[:200]}")
        fid = m.group(1)
        info = json.loads(self._run("readonly", "info", fid, "--json", timeout=120))
        remote_size = int(info.get("size", -1))
        if remote_size != local.stat().st_size:
            raise IOError(f"verify failed for {local.name}: remote={remote_size} local={local.stat().st_size}")
        return {"id": fid, "size": str(remote_size)}

    def root_url(self, folder_map: Optional[Dict[str, str]] = None) -> str:
        return CLOUD_ROOT_URL_TMPL.format(self.ensure_root())


def detect_backend():
    return DesktopBackend.detect() or CliBackend.detect()


# -----------------------------------------------------------------------------
# Planning
# -----------------------------------------------------------------------------
def _top_entries(spec: ArchiveSpec) -> List[Path]:
    root = BASE_DIR / spec.local_rel
    if not root.is_dir():
        return []
    entries = []
    for e in root.iterdir():
        if e.name.startswith(".") or e.name == "LATEST_PACK_PATH.txt":
            continue
        if not spec.recursive and e.is_dir():
            continue
        if not any(fnmatch.fnmatch(e.name, pat) for pat in spec.include):
            continue
        if any(fnmatch.fnmatch(e.name, pat) for pat in spec.exclude):
            continue
        # avoid double-handling nested roots that have their own spec
        if e.is_dir() and any((BASE_DIR / s.local_rel).resolve() == e.resolve() for s in ARCHIVE_SPECS):
            continue
        entries.append(e)
    entries.sort(key=lambda p: (p.stat().st_mtime, p.name), reverse=True)
    return entries


def _protected_paths() -> List[Path]:
    """Paths that must never be purged (e.g. the latest ready-to-publish pack)."""
    prot = []
    marker = MEDIA_DIR / "ready_to_publish" / "LATEST_PACK_PATH.txt"
    try:
        p = Path(marker.read_text(encoding="utf-8").strip())
        if p.exists():
            prot.append(p.resolve())
    except Exception:
        pass
    return prot


def _files_of(entry: Path) -> List[Path]:
    if entry.is_file():
        return [entry]
    return [f for f in entry.rglob("*") if f.is_file()]


def _dir_size(paths: List[Path]) -> int:
    total = 0
    for f in paths:
        try:
            total += f.stat().st_size
        except OSError:
            pass
    return total


def local_status() -> Dict[str, object]:
    manifest = _load_json(MANIFEST_FILE, {})
    rows = []
    total = purgeable = 0
    for spec in ARCHIVE_SPECS:
        files = [f for e in _top_entries(spec) for f in _files_of(e)]
        size = _dir_size(files)
        uploaded = sum(1 for f in files if _rel(f) in manifest)
        total += size
        if spec.purge:
            purgeable += size
        rows.append({"path": spec.local_rel, "drive": spec.drive_path, "files": len(files),
                     "uploaded": uploaded, "mb": round(size / 1048576, 1), "purge": spec.purge})
    dist = BASE_DIR / "portal_app" / "dist"
    dist_mb = round(_dir_size(_files_of(dist)) / 1048576, 1) if dist.exists() else 0.0
    free_gb = round(shutil.disk_usage(str(BASE_DIR)).free / 1073741824, 2)
    return {"rows": rows, "total_mb": round(total / 1048576, 1), "purgeable_mb": round(purgeable / 1048576, 1),
            "portal_dist_mb": dist_mb, "disk_free_gb": free_gb,
            "folder_map": _load_json(FOLDER_MAP_FILE, {})}


# -----------------------------------------------------------------------------
# Sync + purge
# -----------------------------------------------------------------------------
def sync_and_purge(purge: bool = True, dry_run: bool = False, workers: int = 6,
                   clean_portal_dist: bool = False, backend=None) -> Dict[str, object]:
    started = dt.datetime.now()
    free_before = shutil.disk_usage(str(BASE_DIR)).free
    backend = backend or detect_backend()
    manifest: Dict[str, Dict[str, str]] = _load_json(MANIFEST_FILE, {})
    result: Dict[str, object] = {"backend": getattr(backend, "name", "none"), "uploaded": 0, "skipped": 0,
                                 "failed": 0, "purged_files": 0, "purged_mb": 0.0, "errors": []}

    if backend is None:
        logger.warning("☁️ لا يوجد اتصال Google Drive متاح (Drive for Desktop أو gdrive CLI) — لن يتم رفع أو حذف أي ملف.")
        result["status"] = "no_backend"
        result.update(local_status())
        return result

    protected = _protected_paths()
    jobs = []  # (file, drive_dir)
    for spec in ARCHIVE_SPECS:
        root = BASE_DIR / spec.local_rel
        for entry in _top_entries(spec):
            for f in _files_of(entry):
                rel = _rel(f)
                st = f.stat()
                rec = manifest.get(rel)
                if rec and int(rec.get("size", -1)) == st.st_size:
                    result["skipped"] += 1
                    continue
                sub = f.parent.relative_to(root).as_posix()
                drive_dir = spec.drive_path if sub in ("", ".") else f"{spec.drive_path}/{sub}"
                jobs.append((f, drive_dir))

    logger.info(f"☁️ [{result['backend']}] ملفات جديدة للرفع: {len(jobs)} | مرفوعة سابقاً: {result['skipped']}")

    if not dry_run and jobs:
        # create folders sequentially first (CLI backend) to avoid duplicate folders
        if isinstance(backend, CliBackend):
            for d in sorted({d for _, d in jobs}):
                backend.ensure_folder(d)

        def _do(job):
            f, d = job
            return f, d, backend.upload(f, d)

        with ThreadPoolExecutor(max_workers=max(1, workers)) as ex:
            futs = [ex.submit(_do, j) for j in jobs]
            for i, fut in enumerate(as_completed(futs), 1):
                try:
                    f, d, info = fut.result()
                    with _lock:
                        manifest[_rel(f)] = {"id": info["id"], "size": info["size"], "drive_dir": d,
                                             "uploaded_at": dt.datetime.now().isoformat(timespec="seconds")}
                        result["uploaded"] += 1
                        if result["uploaded"] % 25 == 0:
                            _save_json(MANIFEST_FILE, manifest)
                except Exception as e:  # noqa: BLE001
                    result["failed"] += 1
                    result["errors"].append(str(e)[:300])
                    logger.warning(f"⚠️ فشل رفع ملف: {e}")
        _save_json(MANIFEST_FILE, manifest)

    # ---- purge (only verified uploads, never the newest keep_latest entries) ----
    purged_bytes = 0
    if purge and not dry_run:
        for spec in ARCHIVE_SPECS:
            if not spec.purge:
                continue
            entries = _top_entries(spec)
            for entry in entries[spec.keep_latest:]:
                if entry.resolve() in protected:
                    continue
                files = _files_of(entry)
                verified = [f for f in files
                            if _rel(f) in manifest and int(manifest[_rel(f)].get("size", -1)) == f.stat().st_size]
                for f in verified:
                    try:
                        sz = f.stat().st_size
                        f.unlink()
                        purged_bytes += sz
                        result["purged_files"] += 1
                        manifest[_rel(f)]["local_purged_at"] = dt.datetime.now().isoformat(timespec="seconds")
                    except OSError as e:
                        result["errors"].append(f"purge {f.name}: {e}")
                if entry.is_dir():
                    for d in sorted([p for p in entry.rglob("*") if p.is_dir()], key=lambda p: len(p.parts),
                                    reverse=True) + [entry]:
                        try:
                            d.rmdir()  # only removes when empty
                        except OSError:
                            pass
        _save_json(MANIFEST_FILE, manifest)

    if clean_portal_dist and not dry_run:
        dist = BASE_DIR / "portal_app" / "dist"
        portal_index = BASE_DIR / "docs" / "portal" / "index.html"
        if dist.exists() and portal_index.exists():  # only after it was synced to docs/portal
            sz = _dir_size(_files_of(dist))
            shutil.rmtree(dist, ignore_errors=True)
            purged_bytes += sz
            result["portal_dist_cleaned_mb"] = round(sz / 1048576, 1)

    result["purged_mb"] = round(purged_bytes / 1048576, 1)
    result["freed_gb_disk"] = round((shutil.disk_usage(str(BASE_DIR)).free - free_before) / 1073741824, 2)
    result["disk_free_gb"] = round(shutil.disk_usage(str(BASE_DIR)).free / 1073741824, 2)
    try:
        result["drive_url"] = backend.root_url(_load_json(FOLDER_MAP_FILE, {}))
    except Exception:
        result["drive_url"] = ""
    result["duration_s"] = round((dt.datetime.now() - started).total_seconds(), 1)
    result["status"] = "success" if result["failed"] == 0 else "partial"
    logger.info(f"☁️ اكتملت الأرشفة: رفع {result['uploaded']} | حذف محلي {result['purged_files']} "
                f"({result['purged_mb']} MB) | فشل {result['failed']} | المساحة الحرة الآن {result['disk_free_gb']} GB")
    return result


def format_report_ar(res: Dict[str, object]) -> str:
    """Telegram-friendly Arabic report."""
    if res.get("status") == "no_backend":
        return ("⚠️ <b>لم يتم العثور على اتصال Google Drive على هذا الجهاز.</b>\n\n"
                "لتفعيل الأرشفة التلقائية من البوت والمسار الشامل ثبّت <b>Google Drive for Desktop</b> "
                "(https://www.google.com/drive/download/) وسجّل بحساب medon90ae@gmail.com واختر وضع <b>Stream files</b>.\n"
                f"💾 المساحة الحرة حالياً: {res.get('disk_free_gb')} GB\n"
                "🔒 لم يتم حذف أي ملف محلي.")
    lines = [
        "☁️ <b>تقرير الأرشفة السحابية — Google Drive</b>",
        f"🔌 طريقة الاتصال: <code>{res.get('backend')}</code>",
        f"⬆️ ملفات تم رفعها الآن: {res.get('uploaded')}",
        f"✅ ملفات مؤرشفة مسبقاً: {res.get('skipped')}",
        f"🧹 ملفات حُذفت محلياً بعد التحقق: {res.get('purged_files')} ({res.get('purged_mb')} MB)",
        f"💾 المساحة الحرة على الجهاز الآن: {res.get('disk_free_gb')} GB",
    ]
    if res.get("failed"):
        lines.append(f"⚠️ ملفات فشل رفعها (لم تُحذف): {res.get('failed')}")
    if res.get("drive_url"):
        lines.append(f"📂 مجلد الأرشيف على درايف:\n👉 {res.get('drive_url')}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Healing Touch — Google Drive cloud archiver")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--sync", action="store_true")
    ap.add_argument("--no-purge", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--clean-portal-dist", action="store_true")
    ap.add_argument("--workers", type=int, default=6)
    a = ap.parse_args()
    if a.sync:
        res = sync_and_purge(purge=not a.no_purge, dry_run=a.dry_run, workers=a.workers,
                             clean_portal_dist=a.clean_portal_dist)
        print(json.dumps({k: v for k, v in res.items() if k != "rows"}, ensure_ascii=False, indent=2))
        return 0 if res.get("status") in ("success", "no_backend") else 2
    st = local_status()
    print(json.dumps(st, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
