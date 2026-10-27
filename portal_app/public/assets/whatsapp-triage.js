/**
 * =============================================================================
 * 🌿 هيلينج تاتش مصر | المحرك والوسيط المركزي الموحد للاستشارات والتوجيه عبر واتساب (2026)
 * Unified WhatsApp Clinical Triage & Lead Orchestration Engine (Global Form & Router)
 * =============================================================================
 */

(function () {
  "use strict";

  // المتغير العالمي الموحد لجميع صفحات ومكونات المشروع
  const WHATSAPP_CONFIG = {
    phone: "201155803307",
    displayPhone: "01155803307",
    defaultTopic: "general",
    leadWebhookUrl: "https://script.google.com/macros/s/AKfycbwDYeWbB9SjUqX1RXH7DaZ8yqG6V5Ay7yAiJ9L27Du1pJ8zb-NVgXzw6oz_0wJVp8Fr/exec",
    
    // الرسائل السريرية المعتمدة لكل تخصص (خالية 100% من الألفاظ التجارية والترويج التجاري)
    messages: {
      "general": "أهلاً بكم في منصة هيلينج تاتش مصر، أود الحصول على توجيه سريري مجاني حول مرحلة تعافي جرحي والمنتج الأنسب لحالتي.",
      "c-section": "أهلاً بكم، أود استشارة سريرية مجانية حول بروتوكول تعافي جرح القيصرية والشاور الآمن والوقاية من تضخم الندبة.",
      "bariatric": "أهلاً بكم، أود استشارة سريرية مجانية حول حماية ثقوب المنظار بعد جراحة السمنة (التكميم/تحويل المسار) وتأمين الاستحمام.",
      "rhinoplasty": "أهلاً بكم، أود استشارة سريرية مجانية حول بلاستر 3M ودعامة الأنف السيليكون لتثبيت النتيجة وتخفيف التورم.",
      "thyroid": "أهلاً بكم، أود استشارة سريرية مجانية حول حماية ووقاية جرح الغدة الدرقية في الرقبة من أشعة الشمس وتسطيح الندبة.",
      "keloid": "أهلاً بكم، أود استشارة سريرية مجانية حول شيت السيليكون الطبي BUPY لعلاج وتسطيح الندبات البارزة والكلويد."
    },

    // توليد رابط wa.me المشفر والآمن
    getUrl: function (topic) {
      const cleanTopic = (topic || "general").toLowerCase();
      const text = this.messages[cleanTopic] || this.messages["general"];
      return "https://wa.me/" + this.phone + "?text=" + encodeURIComponent(text);
    },

    // فتح نافذة المحادثة المباشرة
    openTriage: function (topic) {
      const url = this.getUrl(topic);
      window.open(url, "_blank", "noopener,noreferrer");
    },

    // فتح النموذج السريري الموحد (Unified Clinical Modal)
    showModal: function (topic, options) {
      options = options || {};
      const modalId = "ht-clinical-triage-modal";
      let existingModal = document.getElementById(modalId);
      if (existingModal) {
        existingModal.remove();
      }

      const cleanTopic = (topic || "general").toLowerCase();
      const topicTitles = {
        "c-section": "جراحة القيصرية والشاور",
        "bariatric": "جراحة السمنة وثقوب المنظار",
        "rhinoplasty": "جراحة وتجميل الأنف",
        "thyroid": "جراحة الغدة الدرقية",
        "keloid": "علاج وتسطيح الندبات البارزة",
        "general": "الاستشارة والتعافي الجراحي"
      };
      const title = options.title || topicTitles[cleanTopic] || "الاستشارة السريرية المجانية";

      const modalHtml = `
        <div id="${modalId}" style="position:fixed; inset:0; z-index:999999; display:flex; align-items:center; justify-content:center; background:rgba(15, 23, 42, 0.75); backdrop-filter:blur(6px); padding:16px; font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; direction:rtl;">
          <div style="background:#ffffff; width:100%; max-width:440px; border-radius:24px; padding:28px 24px; box-shadow:0 25px 50px -12px rgba(0, 0, 0, 0.25); border:1px solid #E2E8F0; text-align:center; position:relative; animation:htFadeIn 0.25s ease-out;">
            <button id="ht-modal-close-btn" style="position:absolute; top:16px; left:16px; background:#F1F5F9; border:none; width:36px; height:36px; border-radius:50%; font-size:18px; color:#64748B; cursor:pointer; display:flex; align-items:center; justify-content:center;">&times;</button>
            
            <div style="width:56px; height:56px; border-radius:50%; background:#ECFDF5; color:#059669; display:flex; align-items:center; justify-content:center; margin:0 auto 16px auto; font-size:28px;">
              💬
            </div>

            <h3 style="margin:0 0 8px 0; color:#065F46; font-size:1.35rem; font-weight:700;">طلب توجيه سريري مجاني</h3>
            <p style="margin:0 0 20px 0; color:#64748B; font-size:0.95rem; line-height:1.6;">
              تواصل مباشرة مع أخصائية الرعاية الصحية لمتابعة بروتوكول <strong>${title}</strong>
            </p>

            <form id="ht-modal-form" style="text-align:right;">
              <div style="margin-bottom:16px;">
                <label style="display:block; margin-bottom:6px; font-weight:600; color:#334155; font-size:0.9rem;">رقم هاتفك أو واتساب:</label>
                <input id="ht-modal-phone" type="tel" placeholder="مثال: 01012345678" style="width:100%; padding:14px 16px; border-radius:12px; border:2px solid #E2E8F0; font-size:1.05rem; outline:none; box-sizing:border-box; transition:border-color 0.2s;" required />
                <span id="ht-modal-error" style="display:none; color:#DC2626; font-size:0.8rem; margin-top:4px;">يرجى كتابة رقم هاتف مصري صحيح (11 رقماً يبدأ بـ 01).</span>
              </div>

              <button type="submit" id="ht-modal-submit-btn" style="width:100%; background:#25D366; color:#ffffff; font-weight:700; padding:15px; border-radius:12px; border:none; font-size:1.05rem; cursor:pointer; display:flex; align-items:center; justify-content:center; gap:8px; box-shadow:0 10px 15px -3px rgba(37, 211, 102, 0.3);">
                <span>الانتقال للمحادثة في واتساب فوراً</span>
                <span style="font-size:1.2rem;">←</span>
              </button>
            </form>

            <div style="margin-top:16px; padding-top:14px; border-top:1px solid #F1F5F9; font-size:0.8rem; color:#94A3B8; text-align:center;">
              🔒 خصوصية بياناتك مؤمنة بالكامل وفق المعايير السريرية
            </div>
          </div>
        </div>
      `;

      const div = document.createElement("div");
      div.innerHTML = modalHtml;
      document.body.appendChild(div.firstElementChild);

      // ربط أحداث الإغلاق والتقديم
      const modal = document.getElementById(modalId);
      const closeBtn = document.getElementById("ht-modal-close-btn");
      const form = document.getElementById("ht-modal-form");
      const phoneInput = document.getElementById("ht-modal-phone");
      const errorMsg = document.getElementById("ht-modal-error");
      const submitBtn = document.getElementById("ht-modal-submit-btn");

      phoneInput.focus();

      closeBtn.addEventListener("click", function () {
        modal.remove();
      });

      modal.addEventListener("click", function (e) {
        if (e.target === modal) {
          modal.remove();
        }
      });

      form.addEventListener("submit", function (e) {
        e.preventDefault();
        const rawPhone = phoneInput.value.trim().replace(/[\s\-\(\)]/g, "");
        
        // التحقق من صحة رقم الموبايل المصري
        const cleanPhoneMatch = rawPhone.match(/(?:(?:\+?20)|0)?(1[0125]\d{8})$/);
        if (!cleanPhoneMatch) {
          errorMsg.style.display = "block";
          phoneInput.style.borderColor = "#DC2626";
          return;
        }

        const validPhone = "0" + cleanPhoneMatch[1];
        errorMsg.style.display = "none";
        phoneInput.style.borderColor = "#10B981";
        submitBtn.innerHTML = "جاري التحويل الآمن...";
        submitBtn.disabled = true;

        // إرسال البيانات للـ Google Sheet
        try {
          fetch(WHATSAPP_CONFIG.leadWebhookUrl, {
            method: "POST",
            mode: "no-cors",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              action: "record_consultation_lead",
              phone: validPhone,
              topic: cleanTopic,
              source: window.location.pathname,
              timestamp: new Date().toISOString()
            })
          }).catch(function () {});
        } catch (err) {}

        // التوجيه الفوري للواتساب بعد 100 ميلي ثانية
        setTimeout(function () {
          WHATSAPP_CONFIG.openTriage(cleanTopic);
          modal.remove();
        }, 150);
      });
    }
  };

  // تسجيل الكائن كمتغير عالمي للمشروع
  window.HEALING_TOUCH_WHATSAPP = WHATSAPP_CONFIG;
  window.openClinicalConsultation = function (topic) {
    WHATSAPP_CONFIG.showModal(topic);
  };
  window.openDirectWhatsApp = function (topic) {
    WHATSAPP_CONFIG.openTriage(topic);
  };

  // ربط تلقائي لجميع الأزرار والروابط في الصفحة بمجرد تحميل DOM
  function autoBindWhatsAppElements() {
    // 1. فحص أي رابط يحتوي على wa.me
    const waLinks = document.querySelectorAll('a[href*="wa.me"], a[href*="whatsapp.com"], a[href*="wa.html"]');
    waLinks.forEach(function (link) {
      if (!link.getAttribute("data-wa-bound")) {
        link.setAttribute("data-wa-bound", "true");
        link.addEventListener("click", function (e) {
          e.preventDefault();
          const topic = link.getAttribute("data-wa-topic") || "general";
          WHATSAPP_CONFIG.showModal(topic);
        });
      }
    });

    // 2. فحص أي زر يحتوي على data-wa-topic أو كلاس btn-whatsapp
    const waButtons = document.querySelectorAll('[data-wa-topic], .btn-whatsapp, .btn-wa-triage');
    waButtons.forEach(function (btn) {
      if (!btn.getAttribute("data-wa-bound")) {
        btn.setAttribute("data-wa-bound", "true");
        btn.addEventListener("click", function (e) {
          e.preventDefault();
          const topic = btn.getAttribute("data-wa-topic") || "general";
          WHATSAPP_CONFIG.showModal(topic);
        });
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", autoBindWhatsAppElements);
  } else {
    autoBindWhatsAppElements();
  }

  // إعادة الفحص عند أي تغيير ديناميكي في الصفحة
  if (typeof MutationObserver !== "undefined") {
    const observer = new MutationObserver(function () {
      autoBindWhatsAppElements();
    });
    observer.observe(document.documentElement, { childList: true, subtree: true });
  }

})();
