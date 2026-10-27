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
    promoCode: "HT10",
    defaultTopic: "general",
    leadWebhookUrl: "https://script.google.com/macros/s/AKfycbwDYeWbB9SjUqX1RXH7DaZ8yqG6V5Ay7yAiJ9L27Du1pJ8zb-NVgXzw6oz_0wJVp8Fr/exec",

    // أسماء التخصصات باللغة العربية
    topicLabels: {
      "c-section": "جرح القيصرية والشاور الآمن",
      "bariatric": "حماية ثقوب المنظار بعد جراحة السمنة والتكميم",
      "rhinoplasty": "تثبيت الأنف وتخفيف التورم ببلاستر 3M ودعامة السيليكون",
      "thyroid": "حماية ندبة الغدة الدرقية في الرقبة وتسطيحها",
      "keloid": "شيت السيليكون الطبي BUPY لعلاج وتسطيح الندبات والكلويد",
      "general": "بروتوكول التعافي بعد العمليات الجراحية"
    },
    
    // الرسائل الطبيعية المعتمدة المتضمنة كود HT10 للشحن والمعاينة المجانية
    messages: {
      "c-section": "أهلاً بحضرتك، محتاجة استشارة بخصوص جرح القيصرية والشاور الآمن، وتفعيل كود (HT10) للشحن المجاني وحق معاينة الشحنة قبل الاستلام.",
      "bariatric": "أهلاً بحضرتك، محتاج استشارة بخصوص حماية ثقوب المنظار بعد عملية التكميم، وتفعيل كود (HT10) للشحن المجاني وحق معاينة الشحنة قبل الاستلام.",
      "rhinoplasty": "أهلاً بحضرتك، محتاج استشارة بخصوص بلاستر 3M ودعامة الأنف لتثبيت النتيجة وتخفيف التورم، وتفعيل كود (HT10) للشحن المجاني وحق معاينة الشحنة قبل الاستلام.",
      "thyroid": "أهلاً بحضرتك، محتاجة استشارة بخصوص حماية ندبة الرقبة بعد استئصال الغدة الدرقية وتسطيحها، وتفعيل كود (HT10) للشحن المجاني وحق معاينة الشحنة قبل الاستلام.",
      "keloid": "أهلاً بحضرتك، محتاج استشارة بخصوص شيت السيليكون الطبي لتسطيح وتفتيح الندبة البارزة، وتفعيل كود (HT10) للشحن المجاني وحق معاينة الشحنة قبل الاستلام.",
      "general": "أهلاً بحضرتك في هيلينج تاتش مصر، محتاج استشارة بخصوص التعافي بعد عمليتي، وتفعيل كود (HT10) للشحن المجاني وحق معاينة الشحنة قبل الاستلام."
    },

    // تسجيل الليد فورياً في Google Sheet
    logLeadToGoogleSheet: function (data) {
      try {
        const payload = {
          patient_name: data.patient_name || "زائر استشارة سريعة",
          patient_phone: data.patient_phone || "تواصل مباشر",
          context_topic: data.context_topic || "استشارة عامة",
          channel: "whatsapp",
          promo_code: "HT10",
          page_url: data.page_url || window.location.href,
          source: data.source || window.location.pathname,
          notes: data.notes || "تفعيل كود HT10 للشحن المجاني والمعاينة قبل الاستلام",
          timestamp: new Date().toISOString()
        };

        if (navigator.sendBeacon) {
          const blob = new Blob([JSON.stringify(payload)], { type: "text/plain" });
          navigator.sendBeacon(this.leadWebhookUrl, blob);
        } else {
          fetch(this.leadWebhookUrl, {
            method: "POST",
            mode: "no-cors",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
          }).catch(function () {});
        }
      } catch (err) {
        console.warn("Lead tracking dispatch:", err);
      }
    },

    // توليد رابط wa.me المشفر والآمن
    getUrl: function (topic, customerName) {
      const cleanTopic = (topic || "general").toLowerCase();
      let text = "";
      const topicTitle = this.topicLabels[cleanTopic] || this.topicLabels["general"];

      if (customerName && customerName.trim().length >= 2) {
        text = "أهلاً بحضرتك، أنا (" + customerName.trim() + ") ومحتاج استشارة بخصوص (" + topicTitle + ")، مع تفعيل كود (HT10) للشحن المجاني وحق فتح ومعاينة الشحنة قبل الاستلام.";
      } else {
        text = this.messages[cleanTopic] || this.messages["general"];
      }

      return "https://wa.me/" + this.phone + "?text=" + encodeURIComponent(text);
    },

    // فتح نافذة المحادثة المباشرة مع تسجيل الليد في الشيت
    openTriage: function (topic) {
      const cleanTopic = (topic || "general").toLowerCase();
      const topicTitle = this.topicLabels[cleanTopic] || this.topicLabels["general"];

      // تسجيل فوري للنقرة في شيت الليدز
      this.logLeadToGoogleSheet({
        patient_name: "تواصل مباشر عبر واتساب",
        patient_phone: "تحويل مباشر",
        context_topic: topicTitle,
        source: "direct_button_click"
      });

      const url = this.getUrl(cleanTopic);
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
      const topicTitle = options.title || this.topicLabels[cleanTopic] || "الاستشارة السريرية المجانية";

      const modalHtml = `
        <div id="${modalId}" style="position:fixed; inset:0; z-index:999999; display:flex; align-items:center; justify-content:center; background:rgba(15, 23, 42, 0.75); backdrop-filter:blur(6px); padding:16px; font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; direction:rtl;">
          <div style="background:#ffffff; width:100%; max-width:440px; border-radius:24px; padding:28px 24px; box-shadow:0 25px 50px -12px rgba(0, 0, 0, 0.25); border:1px solid #E2E8F0; text-align:center; position:relative; animation:htFadeIn 0.25s ease-out;">
            <button id="ht-modal-close-btn" style="position:absolute; top:16px; left:16px; background:#F1F5F9; border:none; width:36px; height:36px; border-radius:50%; font-size:18px; color:#64748B; cursor:pointer; display:flex; align-items:center; justify-content:center;">&times;</button>
            
            <div style="width:56px; height:56px; border-radius:50%; background:#ECFDF5; color:#059669; display:flex; align-items:center; justify-content:center; margin:0 auto 16px auto; font-size:28px;">
              💬
            </div>

            <h3 style="margin:0 0 6px 0; color:#065F46; font-size:1.35rem; font-weight:700;">طلب استشارة سريرية مجانية</h3>
            <div style="background:#FEF3C7; color:#92400E; font-size:0.85rem; font-weight:700; padding:6px 12px; border-radius:20px; display:inline-block; margin-bottom:14px; border:1px dashed #F59E0B;">
              🎁 كود HT10: شحن مجاني + حق فتح ومعاينة الشحنة قبل الاستلام
            </div>

            <p style="margin:0 0 18px 0; color:#64748B; font-size:0.92rem; line-height:1.5;">
              تواصل مباشرة مع أخصائية التعافي لمتابعة بروتوكول: <strong>${topicTitle}</strong>
            </p>

            <form id="ht-modal-form" style="text-align:right;">
              <div style="margin-bottom:12px;">
                <label style="display:block; margin-bottom:5px; font-weight:600; color:#334155; font-size:0.88rem;">اسمك الكريم (اختياري):</label>
                <input id="ht-modal-name" type="text" placeholder="مثال: سارة أحمد" style="width:100%; padding:12px 14px; border-radius:12px; border:2px solid #E2E8F0; font-size:0.98rem; outline:none; box-sizing:border-box;" />
              </div>

              <div style="margin-bottom:16px;">
                <label style="display:block; margin-bottom:5px; font-weight:600; color:#334155; font-size:0.88rem;">رقم الموبايل / واتساب:</label>
                <input id="ht-modal-phone" type="tel" placeholder="مثال: 01012345678" style="width:100%; padding:12px 14px; border-radius:12px; border:2px solid #E2E8F0; font-size:1.02rem; outline:none; box-sizing:border-box;" required />
                <span id="ht-modal-error" style="display:none; color:#DC2626; font-size:0.8rem; margin-top:4px;">يرجى كتابة رقم موبايل مصري صحيح (11 رقماً يبدأ بـ 01).</span>
              </div>

              <button type="submit" id="ht-modal-submit-btn" style="width:100%; background:#25D366; color:#ffffff; font-weight:700; padding:14px; border-radius:12px; border:none; font-size:1.05rem; cursor:pointer; display:flex; align-items:center; justify-content:center; gap:8px; box-shadow:0 10px 15px -3px rgba(37, 211, 102, 0.3);">
                <span>تأكيد ونقل للمحادثة في واتساب</span>
                <span style="font-size:1.2rem;">←</span>
              </button>
            </form>

            <div style="margin-top:14px; padding-top:12px; border-top:1px solid #F1F5F9; font-size:0.78rem; color:#94A3B8; text-align:center;">
              🔒 بياناتك محمية بسرية سريرية تامة
            </div>
          </div>
        </div>
      `;

      const div = document.createElement("div");
      div.innerHTML = modalHtml;
      document.body.appendChild(div.firstElementChild);

      const modal = document.getElementById(modalId);
      const closeBtn = document.getElementById("ht-modal-close-btn");
      const form = document.getElementById("ht-modal-form");
      const nameInput = document.getElementById("ht-modal-name");
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

      const self = this;
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        const rawName = nameInput ? nameInput.value.trim() : "";
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
        submitBtn.innerHTML = "جاري التحويل وتثبيت كود HT10...";
        submitBtn.disabled = true;

        // تسجيل البيانات فوراً في Google Sheet
        self.logLeadToGoogleSheet({
          patient_name: rawName || "عميل واتساب",
          patient_phone: validPhone,
          context_topic: topicTitle,
          source: "modal_form_submission"
        });

        // توليد الرابط المخصص والتحويل الفوري للواتساب
        const targetUrl = self.getUrl(cleanTopic, rawName);
        setTimeout(function () {
          window.open(targetUrl, "_blank", "noopener,noreferrer");
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

  if (typeof MutationObserver !== "undefined") {
    const observer = new MutationObserver(function () {
      autoBindWhatsAppElements();
    });
    observer.observe(document.documentElement, { childList: true, subtree: true });
  }

})();
