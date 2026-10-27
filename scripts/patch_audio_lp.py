# -*- coding: utf-8 -*-
with open('c:/followUPSHEET/healing_touch/campaign_landing_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Add audio check and audio_block
target_video_block = '''    video_block = ""
    if video_rel_path:
        video_block = f"""
        <div class="video-container-card">
          <div class="video-header-tag">🎬 فيديو الشرح السريري العملي التفاعلي</div>
          <video controls autoplay muted loop playsinline class="lp-video-player">
            <source src="{video_rel_path}" type="video/mp4">
            متصفحك لا يدعم تشغيل الفيديو المباشر.
          </video>
          <p class="video-caption">شرح تفاعلي لبيولوجيا التعافي، مراحل تنظيم الكولاجين، وطريقة استخدام المستلزمات الطبية المعتمدة للوقاية من تضخم الندبات.</p>
        </div>
        """'''

replacement_video_and_audio = '''    # فحص وجود فيديو
    video_block = ""
    if not video_rel_path:
        for ext in [".mp4", ".mov", ".webm"]:
            cand_v = DOCS_DIR / "assets" / f"campaign_{cat}_video{ext}"
            if cand_v.exists():
                video_rel_path = f"../assets/{cand_v.name}"
                break

    if video_rel_path:
        video_block = f"""
        <div class="video-container-card">
          <div class="video-header-tag">🎬 فيديو الشرح السريري العملي التفاعلي</div>
          <video controls autoplay muted loop playsinline class="lp-video-player">
            <source src="{video_rel_path}" type="video/mp4">
            متصفحك لا يدعم تشغيل الفيديو المباشر.
          </video>
          <p class="video-caption">شرح تفاعلي لبيولوجيا التعافي، مراحل تنظيم الكولاجين، وطريقة استخدام المستلزمات الطبية المعتمدة للوقاية من تضخم الندبات.</p>
        </div>
        """

    # فحص وجود تعليق صوتي وبودكاست سريري
    audio_rel_path = ""
    for ext in [".m4a", ".mp3", ".wav"]:
        cand_a = DOCS_DIR / "assets" / f"campaign_{cat}_audio{ext}"
        if cand_a.exists():
            audio_rel_path = f"../assets/{cand_a.name}"
            break

    audio_block = ""
    if audio_rel_path:
        audio_block = f"""
        <div class="audio-container-card" style="background:#F0FDF4; border:1px solid #A7F3D0; border-radius:14px; padding:20px; margin:24px 0;">
          <div style="font-weight:800; color:#065F46; margin-bottom:10px; font-size:1.05rem;">🎙️ استمع إلى الشرح والبودكاست السريري لحالة اليوم (Audio Overview):</div>
          <audio controls style="width:100%; border-radius:30px;">
            <source src="{audio_rel_path}" type="audio/mp4">
            متصفحك لا يدعم تشغيل الصوت المباشر.
          </audio>
          <p style="font-size:0.88rem; color:#475569; margin-top:8px;">حوار سريري توضيحي حول فيزيولوجيا التئام الأنسجة، ترطيب الكولاجين، وطريقة الوقاية من تضخم الندبات والكلويد.</p>
        </div>
        """'''

if target_video_block in text:
    text = text.replace(target_video_block, replacement_video_and_audio)
    print("[+] Added audio detection and player block")

# Add audio_block after video_block in the HTML container
text = text.replace(
    '{video_block}',
    '{video_block}\n    {audio_block}'
)

# Sanitize remaining FAQ
text = text.replace(
    '("ما هي مميزات كود HT10 وكيف أحصل على الاستشارة السريرية؟", "كود HT10 يمنحك أولوية المتابعة السريرية المجانية مع أخصائية العناية بالتعافي عبر واتساب، بالإضافة لحق فتح ومعاينة الشحنة الطبية قبل الاستلام للتأكد من أصلية العبوات وتاريخ الصلاحية.")',
    '("كيف أحصل على التوجيه والاستشارة السريرية المجانية لمرحلة تعافي جرحي؟", "يمكنك التواصل المباشر مع استشاري العناية بالتعافي عبر واتساب من خلال الرابط أو الزر المباشر بالصفحة؛ لتحصل على إرشادات علمية دقيقة تناسب نوع عمليتك وتاريخ إجرائها ومعدل التئام الأنسجة لديك.")'
)

with open('c:/followUPSHEET/healing_touch/campaign_landing_engine.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("[+] Successfully updated campaign_landing_engine.py with audio player and clean FAQ")
