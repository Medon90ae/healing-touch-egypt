# -*- coding: utf-8 -*-
"""
=============================================================================
🌿 هيلينج تاتش مصر | محرك الفيديو والبودكاست السريري فائق السرعة (2026)
FFmpeg Pure-Pomelli High-Speed Video & Audio Engine (Zero Stock Photos)
=============================================================================
"""

import sys
import os
import shutil
import subprocess
from pathlib import Path
from PIL import Image

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def run_ffmpeg(cmd: list) -> bool:
    """تشغيل أمر ffmpeg بأمان مع دعم المسارات وبدون تعارض الترميز."""
    try:
        p = subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False
        )
        return p.returncode == 0
    except Exception as e:
        print(f"[!] استثناء ffmpeg: {e}")
        return False


def build_audio_visual_videos(audio_path: Path, hero_image_path: Path, out_dir_16x9: Path, out_dir_9x16: Path) -> dict:
    """
    تحويل الملف الصوتي / البودكاست المرفوع إلى فيديوهات مرئية جاهزة للمنصات (16:9 و 9:16)
    تعتمد حصرياً على جلسة تصوير Pomelli الحقيقية بدون أي شاشة سوداء أو صور ستوك.
    """
    results = {"video_16x9": None, "video_9x16": None}
    if not audio_path.exists() or not hero_image_path.exists():
        return results

    out_16x9 = out_dir_16x9 / "فيديو_بودكاست_صوتي_كامل_16x9.mp4"
    out_9x16 = out_dir_9x16 / "فيديو_بودكاست_صوتي_شورتس_9x16.mp4"

    # 1. فيديو 16:9 لليوتيوب (صوت + صورة Pomelli مع لون سريري عميق فائق السرعة)
    cmd_16x9 = [
        "ffmpeg", "-y",
        "-loop", "1", "-r", "1", "-i", str(hero_image_path),
        "-i", str(audio_path),
        "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0x0D4A4D",
        "-c:v", "libx264", "-preset", "ultrafast",
        "-c:a", "copy",
        "-pix_fmt", "yuv420p", "-shortest",
        str(out_16x9)
    ]
    if run_ffmpeg(cmd_16x9) and out_16x9.exists():
        results["video_16x9"] = out_16x9
        print(f"[+] 🎙️ تم إنتاج فيديو البودكاست الصوتي الكامل لليوتيوب (16:9): {out_16x9.name}")

    # 2. فيديو 9:16 رأسي للشورتس والتيك توك والريلز (محدد بـ 59 ثانية لمنصات الشورتس)
    cmd_9x16 = [
        "ffmpeg", "-y",
        "-loop", "1", "-r", "1", "-i", str(hero_image_path),
        "-i", str(audio_path), "-t", "59",
        "-vf", "split[orig][bg];[bg]scale=270:480:force_original_aspect_ratio=increase,crop=270:480,boxblur=5:2,scale=1080:1920[b];[orig]scale=1080:1920:force_original_aspect_ratio=decrease[fg];[b][fg]overlay=(W-w)/2:(H-h)/2",
        "-c:v", "libx264", "-preset", "ultrafast",
        "-c:a", "copy",
        "-pix_fmt", "yuv420p", "-shortest",
        str(out_9x16)
    ]
    if run_ffmpeg(cmd_9x16) and out_9x16.exists():
        results["video_9x16"] = out_9x16
        print(f"[+] 📱 تم إنتاج فيديو البودكاست الصوتي الرأسي للشورتس وتيك توك (9:16): {out_9x16.name}")

    return results


def build_uploaded_video_variants(video_path: Path, out_dir_16x9: Path, out_dir_9x16: Path) -> dict:
    """
    تجهيز نسختي الفيديو المرفوع:
    1. نسخة كاملة 16:9 لليوتيوب.
    2. نسخة رأسية 9:16 للشورتس وتيك توك (59 ثانية) مع خلفية ضبابية من نفس الفيديو.
    """
    results = {"video_16x9": None, "video_9x16": None}
    if not video_path.exists():
        return results

    out_16x9 = out_dir_16x9 / "فيديو_يوتيوب_كامل_16x9.mp4"
    out_9x16 = out_dir_9x16 / "فيديو_شورتس_وريلز_9x16.mp4"

    # النسخة الكاملة
    try:
        shutil.copy2(str(video_path), str(out_16x9))
        results["video_16x9"] = out_16x9
        print(f"[+] 🎬 تم اعتماد وتجهيز الفيديو الكامل لليوتيوب: {out_16x9.name}")
    except Exception:
        pass

    # النسخة الرأسية 9:16 (59 ثانية للشورتس، مع بلور سريع فائق الجودة من نفس الفيديو)
    cmd_vertical = [
        "ffmpeg", "-y",
        "-i", str(video_path), "-t", "59",
        "-filter_complex", "[0:v]split[orig][bg];[bg]scale=270:480:force_original_aspect_ratio=increase,crop=270:480,boxblur=5:2,scale=1080:1920[blurred];[orig]scale=1080:1920:force_original_aspect_ratio=decrease[centered];[blurred][centered]overlay=(W-w)/2:(H-h)/2",
        "-c:v", "libx264", "-preset", "ultrafast",
        "-c:a", "copy",
        "-pix_fmt", "yuv420p",
        str(out_9x16)
    ]
    if run_ffmpeg(cmd_vertical) and out_9x16.exists():
        results["video_9x16"] = out_9x16
        print(f"[+] 📱 تم إنتاج فيديو الشورتس والريلز الرأسي الخالي من الستوك (9:16): {out_9x16.name}")

    return results


def generate_clean_youtube_thumbnail(image_path: Path, output_path: Path):
    """توليد صورة مصغرة 1280x720 احترافية لليوتيوب من صور Pomelli."""
    if not image_path.exists():
        return
    try:
        img = Image.open(image_path)
        w, h = img.size
        target_ratio = 16 / 9
        current_ratio = w / h
        if current_ratio > target_ratio:
            new_w = int(h * target_ratio)
            left = (w - new_w) // 2
            img_cropped = img.crop((left, 0, left + new_w, h))
        else:
            new_h = int(w / target_ratio)
            top = (h - new_h) // 2
            img_cropped = img.crop((0, top, w, top + new_h))
        thumb = img_cropped.resize((1280, 720), Image.Resampling.LANCZOS)
        thumb.save(str(output_path))
        print(f"[+] 🖼️ تم توليد الصورة المصغرة لليوتيوب بنجاح: {output_path.name}")
    except Exception as e:
        print(f"[!] خطأ في توليد الصورة المصغرة: {e}")
