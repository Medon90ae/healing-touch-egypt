# Complete Hybrid Architecture Design: Python Engine & n8n Orchestrator
## التصميم المعماري الهجين المتكامل: محرك بايثون ومنصة n8n للأتمتة

- **Project**: Healing Touch Egypt (هيلينج تاتش مصر)
- **Target Environment**: Windows Production & Hybrid Cloud
- **Document ID**: `HT-ARCH-HYBRID-2026-R3`
- **Date**: 2026-10-28
- **Classification**: Master Architectural Specification & Interface Contracts

---

## 1. System Vision & Architectural Philosophy

The **Healing Touch Egypt Hybrid Automation Architecture** achieves high operational performance by combining the strengths of two distinct execution paradigms:
1. **The Python Local Heavy Engine (Computational Muscle)**: Executes offline, resource-intensive, deterministic data processing—such as multi-threaded FFmpeg video synthesis, Playwright Chromium typography rendering, static clinical website compilation, and deep NCBI PubMed medical research scraping.
2. **The n8n Workflow Automation Engine (Network Orchestrator & Nervous System)**: Manages continuous, stateful, event-driven network communication—such as webhook intake, resilient social media API publishing with exponential backoff, interactive Telegram Human-in-the-Loop (HITL) review gates, and real-time patient lead synchronization into Google Sheets and WhatsApp staff channels.

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 THE HYBRID BEST-OF-BOTH-WORLDS                                  │
│                                                                                                 │
│    ┌─────────────────────────────────┐                 ┌─────────────────────────────────┐      │
│    │       PYTHON LOCAL ENGINE       │                 │      N8N WORKFLOW ENGINE        │      │
│    │     (High-Speed Computation)    │                 │    (Network & Orchestration)    │      │
│    ├─────────────────────────────────┤                 ├─────────────────────────────────┤      │
│    │ • FFmpeg 4K Video Compilation   │                 │ • Visual Schedule / Cron        │      │
│    │ • Playwright Typography Cards   │  HTTP Webhook   │ • Meta Graph API Resilient Pub  │      │
│    │ • Static Clinical SEO Engine    ├────────────────►│ • Telegram HITL Review Gate     │      │
│    │ • Manual Inbox File Ingestion   │   JSON Payload  │ • Lead Ingestion & Sheet Sync   │      │
│    │ • Constant O(1) Memory Footprint│                 │ • Automatic Exponential Backoff │      │
│    └─────────────────────────────────┘                 └─────────────────────────────────┘      │
│                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Definitive Demarcation Matrix

The division of system responsibilities is strictly enforced across all modules:

| Architectural Domain | Sub-Component | Responsible Engine | Implementation Details |
| :--- | :--- | :--- | :--- |
| **Media Processing** | FFmpeg 16:9 & 9:16 Video Rendering | **Python (100%)** | `scripts/media_video_engine.py`: Direct OS subprocess, `-preset ultrafast`, disk-to-disk streaming. Prevents Node.js V8 heap crashes. |
| **Media Processing** | Playwright Cairo Typography Cards | **Python (100%)** | `antigravity_social_automation.py` (`_render_image_playwright`): Headless Chromium rendering 1080x1080 and 1080x1920 high-DPI cards. |
| **Data Ingestion** | Manual Asset Intake Triage | **Python (100%)** | `smart_intake_classifier.py`: File-based monitoring of `media_assets/manual_inbox/`, encoding normalization (`cp1256`/`utf-8`), and archiving. |
| **Medical Evidence** | PubMed Clinical Research Harvester | **Python (100%)** | `clinical_research_harvester.py`: Querying NCBI E-utilities, PMID citation formatting, and medical brief assembly. |
| **Static Site & App** | Static SEO Hub & React Portal App | **Python & Vite (100%)** | `github_seo_trend_engine.py` & `portal_app`: Building 15 clinical cluster articles, 5 product profiles, and pushing to GitHub Pages. |
| **Scheduling** | Automated Daily & Hourly Triggers | **n8n (100%)** | `n8n-nodes-base.scheduleTrigger`: Visual cron triggers, timezone coordination (Africa/Cairo), holiday calendar overrides. |
| **Social Publishing** | Facebook & Instagram Graph API | **n8n (100%)** | `n8n-nodes-base.httpRequest`: Official Meta Graph API v21.0, container status polling loop, exponential backoff on HTTP 429. |
| **Social Publishing** | Reddit & Blogger Syndication | **n8n (100%)** | `n8n-nodes-base.httpRequest`: Managed OAuth2 credentials, resilient Blogger email/webhook delivery with cold-start compensation. |
| **Human Review** | Telegram Interactive Approval Gate | **n8n (100%)** | `n8n-nodes-base.telegram`: Inline keyboard (`[✅ نشر فوري]`, `[❌ إلغاء]`, `[📝 تعديل الكابشن]`) pausing workflow via webhook callback. |
| **CRM & Leads** | Patient Intake & Sheet Sync | **n8n (100%)** | `n8n-nodes-base.webhook`: Ingests leads from `wa.html`, validates Egyptian phone regex, appends to Google Sheet `gid=513215731`. |
| **CRM & Leads** | Instant Staff Alerts | **n8n (100%)** | `n8n-nodes-base.telegram` / `whatsapp`: Sends immediate push notifications to on-duty recovery specialists with patient details. |

---

## 3. End-to-End Operational Architecture & Sequence Flows

### 3.1 Content Creation & Omnichannel Publishing Sequence (Flow 1)

This flow illustrates the progression from clinical content generation to multi-platform publishing with human oversight:

```
[Cron / Manual Run]
       │
       ▼
┌───────────────────────────────────────────────────────────┐
│              Python Local Automation Pipeline             │
│ 1. Harvest clinical topics & patient FAQs                 │
│ 2. Generate Playwright 1080x1080 & 1080x1920 PNG cards    │
│ 3. Execute FFmpeg to compile 59s vertical Reel / TikTok   │
│ 4. Build tailored Arabic copy and high-intent hashtags    │
└─────────────────────────────┬─────────────────────────────┘
                              │
               POST /webhook/publish-post
                              │
                              ▼
┌───────────────────────────────────────────────────────────┐
│               n8n Workflow Automation Engine              │
│ 1. Validate payload schema & authentication token         │
│ 2. Dispatch draft summary & card preview to Telegram      │
│ 3. Display inline keyboard: [✅ Approve] [❌ Reject]     │
│ 4. Pause execution (Wait for Callback)                    │
└─────────────────────────────┬─────────────────────────────┘
                              │
               Reviewer clicks [✅ Approve]
                              │
                              ▼
┌───────────────────────────────────────────────────────────┐
│                Multi-Platform Dispatch Nodes              │
│ ├─► Meta Graph API: Post photo to Facebook Page Feed      │
│ ├─► Instagram Graph API: Create media container & publish │
│ ├─► Reddit API: Submit Markdown article to subreddit      │
│ └─► Blogger Webhook: Post HTML guide with schema markup   │
│                                                           │
│ * Auto-retry up to 3 times with exponential backoff        │
│ * Record success URLs to Google Sheets log                │
└───────────────────────────────────────────────────────────┘
```

### 3.2 Sequence Diagram: Telegram Human-in-the-Loop Review Gate

```
Clinic Manager (Telegram)             n8n Orchestrator               Python Engine
       │                                     │                             │
       │                                     │  POST /webhook/publish-post │
       │                                     │◄────────────────────────────┤
       │                                     │  HTTP 202 Accepted          │
       │                                     ├────────────────────────────►│
       │  Send Photo + Summary + Buttons     │                             
       │◄────────────────────────────────────┤                             
       │  [✅ نشر فوري]   [❌ إلغاء الحزمة]   │                             
       │                                     │                             
       │  Clicks "✅ نشر فوري" (Callback)    │                             
       ├────────────────────────────────────►│                             
       │                                     │──┐                          
       │                                     │  │ Publish to Meta / APIs   
       │                                     │◄─┘ with Exponential Backoff 
       │  Confirmation: "تم النشر بنجاح! 🚀" │                             
       │◄────────────────────────────────────┤                             
```

### 3.3 Patient Lead Ingestion & Consultation Alert Sequence (Flow 2)

```
Patient on Website (wa.html)            n8n Webhook Intake           Google Sheets & Staff
       │                                     │                                 │
       │ Fills Name + Egyptian Phone Number  │                                 │
       │ Clicks "تأكيد وتفعيل كود HT10"      │                                 │
       │                                     │                                 │
       │ POST /webhook/lead-capture          │                                 │
       ├────────────────────────────────────►│                                 │
       │                                     │──┐                              
       │                                     │  │ Regex Validate Phone         
       │                                     │  │ Normalize to 201XXXXXXXXX    
       │                                     │◄─┘                              
       │ HTTP 200 OK + Lead ID               │                                 
       │◄────────────────────────────────────┤                                 
       │ (Redirects to WhatsApp with HT10)   │                                 
       │                                     │ Append Row (Retries on fail)    
       │                                     ├────────────────────────────────►│ (Google Sheet Tab 513215731)
       │                                     │                                 │
       │                                     │ Send Instant Alert              │
       │                                     ├────────────────────────────────►│ (Telegram / Staff WhatsApp)
       │                                     │ "🚨 استشارة جديدة: نورهان..."    │
```

---

## 4. Webhook Interface Contracts & JSON Schemas

### 4.1 Contract 1: Publishing Ingestion Webhook (`POST /webhook/publish-post`)

This contract defines the structured payload delivered from the Python local engine to the n8n orchestrator upon completion of media asset rendering.

- **URL Endpoint**: `http://localhost:5678/webhook/publish-post` (or public tunnel endpoint)
- **HTTP Method**: `POST`
- **Authentication**: Header `X-HealingTouch-Secret: <ENCRYPTED_HMAC_OR_TOKEN>`
- **Content-Type**: `application/json; charset=utf-8`

#### Complete JSON Schema Specification
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "PublishPostPayload",
  "type": "object",
  "required": [
    "event",
    "timestamp",
    "campaign_id",
    "product_name",
    "target_platforms",
    "media",
    "copywriting",
    "hashtags"
  ],
  "properties": {
    "event": {
      "type": "string",
      "enum": ["media_pack_ready", "manual_override_ready"]
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "campaign_id": {
      "type": "string",
      "enum": ["c-section", "rhinoplasty", "bariatric", "thyroid", "general_wound"]
    },
    "product_name": {
      "type": "string"
    },
    "target_platforms": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["facebook", "instagram", "reddit", "blogger", "tiktok", "youtube"]
      }
    },
    "media": {
      "type": "object",
      "required": ["square_card_url"],
      "properties": {
        "square_card_local_path": { "type": "string" },
        "square_card_url": { "type": "string", "format": "uri" },
        "story_card_local_path": { "type": "string" },
        "story_card_url": { "type": "string", "format": "uri" },
        "video_vertical_local_path": { "type": "string" },
        "video_vertical_url": { "type": "string", "format": "uri" },
        "video_horizontal_local_path": { "type": "string" },
        "video_horizontal_url": { "type": "string", "format": "uri" }
      }
    },
    "copywriting": {
      "type": "object",
      "required": ["facebook_caption", "instagram_caption"],
      "properties": {
        "facebook_caption": { "type": "string" },
        "instagram_caption": { "type": "string" },
        "reddit_title": { "type": "string" },
        "reddit_markdown": { "type": "string" },
        "blogger_title": { "type": "string" },
        "blogger_html": { "type": "string" }
      }
    },
    "hashtags": {
      "type": "string"
    },
    "promo_code": {
      "type": "string",
      "default": "HT10"
    },
    "tracking_url": {
      "type": "string",
      "format": "uri"
    }
  }
}
```

#### Production Payload Example
```json
{
  "event": "media_pack_ready",
  "timestamp": "2026-10-28T14:30:00Z",
  "campaign_id": "c-section",
  "product_name": "BUPY Silicone Scar Sheets 4cm x 3m",
  "target_platforms": ["facebook", "instagram", "reddit", "blogger"],
  "media": {
    "square_card_local_path": "c:/followUPSHEET/healing_touch/media_assets/branded_designs/2026-10-28_[فيسبوك]_c-section.png",
    "square_card_url": "https://raw.githubusercontent.com/Medon90ae/healing-touch-egypt/main/docs/assets/og-image.jpg",
    "story_card_local_path": "c:/followUPSHEET/healing_touch/media_assets/branded_designs/2026-10-28_[إنستجرام_ستوري]_c-section.png",
    "story_card_url": "https://raw.githubusercontent.com/Medon90ae/healing-touch-egypt/main/docs/assets/og-image.jpg",
    "video_vertical_local_path": "c:/followUPSHEET/healing_touch/media_assets/branded_designs/2026-10-28_[ريلز]_c-section.mp4"
  },
  "copywriting": {
    "facebook_caption": "أمهات كتير بعد الولادة القيصرية بيبعتوا يسألونا: إمتى أبدأ أستخدم شيت السيليكون لحماية الجرح من التضخم؟\n\nالبروتوكول السريري المعتمد يوصي بالبدء فور التئام الجرح السطحي وسقوط القشور...",
    "instagram_caption": "دليل تعافي جرح القيصرية خطوة بخطوة 🌸\nشيت السيليكون الطبي BUPY يحافظ على ترطيب الأنسجة ويمنع تكون الندبات البارزة والكلويد...",
    "reddit_title": "البروتوكول الطبي المعتمد للعناية بجرح الولادة القيصرية والوقاية من الندبات 2026",
    "reddit_markdown": "### بروتوكول التعافي السريري بعد القيصرية\n\nبناءً على أحدث التوصيات الطبية لعام 2026، تتطلب العناية بالجرح ثلاث مراحل أساسية...",
    "blogger_title": "دليل الأمهات الطبي: كيف تحمين جرح القيصرية من أثر الندبات البارزة؟",
    "blogger_html": "<div dir='rtl' style='font-family: Cairo, sans-serif;'><p>دليل شامل من هيلينج تاتش مصر يوضح التوقيت الطبي الدقيق لبدء استخدام شيت السيليكون الطبي...</p></div>"
  },
  "hashtags": "#ولادة_قيصرية_مصر #جرح_القيصرية #علاج_الندبات #شيت_سيليكون_بوبي #ضمادات_تيجاديرم #هيلينج_تاتش_مصر",
  "promo_code": "HT10",
  "tracking_url": "https://medon90ae.github.io/healing-touch-egypt/wa.html?case=c-section"
}
```

---

### 4.2 Contract 2: Lead Capture Intake Webhook (`POST /webhook/lead-capture`)

This contract defines the payload emitted from the client-side website modal (`docs/wa.html` and article modals) upon patient registration.

- **URL Endpoint**: `http://localhost:5678/webhook/lead-capture`
- **HTTP Method**: `POST`
- **Content-Type**: `application/json; charset=utf-8`

#### Complete JSON Schema Specification
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "LeadCapturePayload",
  "type": "object",
  "required": [
    "patient_name",
    "patient_phone",
    "context_topic",
    "channel",
    "promo_code",
    "submitted_at"
  ],
  "properties": {
    "patient_name": {
      "type": "string",
      "minLength": 2
    },
    "patient_phone": {
      "type": "string",
      "pattern": "^(01[0125][0-9]{8}|201[0125][0-9]{8})$"
    },
    "context_topic": {
      "type": "string"
    },
    "channel": {
      "type": "string",
      "enum": ["whatsapp", "instagram"]
    },
    "promo_code": {
      "type": "string",
      "default": "HT10"
    },
    "page_url": {
      "type": "string",
      "format": "uri"
    },
    "source": {
      "type": "string"
    },
    "submitted_at": {
      "type": "string",
      "format": "date-time"
    }
  }
}
```

#### Production Payload Example
```json
{
  "patient_name": "سارة محمود عبد العزيز",
  "patient_phone": "01098765432",
  "context_topic": "استشارة جرح القيصرية وشيت بوبي للندبات",
  "channel": "whatsapp",
  "promo_code": "HT10",
  "page_url": "https://medon90ae.github.io/healing-touch-egypt/articles/c-section-wound-care.html",
  "source": "زر الاستشارة الطبية المباشرة",
  "submitted_at": "2026-10-28T14:45:12Z"
}
```

#### Response Contract
- **Success (HTTP 200 OK)**:
  ```json
  {
    "status": "success",
    "lead_id": "HT-20261028-0042",
    "message": "Lead registered and routed to staff successfully",
    "whatsapp_redirect": "https://wa.me/201155803307?text=%D8%A3%D9%87%D9%84%D8%A7%D9%8B%D8%8C%20%D9%85%D8%B9%D8%A7%D9%83%D9%85%20%D8%B3%D8%A7%D8%B1%D8%A9%20%D9%85%D8%AD%D9%85%D9%88%D8%AF..."
  }
  ```
- **Validation Failure (HTTP 400 Bad Request)**:
  ```json
  {
    "status": "error",
    "code": "INVALID_PHONE_NUMBER",
    "message": "Phone number must be an 11-digit Egyptian mobile number starting with 010, 011, 012, or 015."
  }
  ```

---

## 5. Failure Mitigation & Resilience Strategies

The hybrid architecture incorporates comprehensive safeguards against real-world failure modes:

### 5.1 Meta Graph API Rate Limiting (HTTP 429 / Code 17)
- **Problem**: Posting too rapidly triggers Meta's application-level request limits.
- **Mitigation in n8n**:
  1. The `HTTP Request` node to Facebook/Instagram is configured with **"Retry On Fail"** enabled.
  2. Maximum retry attempts set to **4**.
  3. Exponential backoff interval set to `30s -> 60s -> 120s -> 300s`.
  4. If all 4 retries fail, an error trigger is raised, notifying the administrator on Telegram with the failure details without crashing the pipeline.

### 5.2 Instagram Video Container Processing Delays
- **Problem**: Calling `/media_publish` before Meta finishes transcoding returns error `#2207001` (`The media is not ready for publishing yet`).
- **Mitigation in n8n**:
  1. Step 1 executes `/media` to create the container ID.
  2. Step 2 enters a polling loop:
     * Node `Wait 15s` pauses execution.
     * Node `GET /{creation_id}?fields=status_code` checks status.
     * Node `If status_code == FINISHED` breaks the loop to call `/media_publish`.
     * If `status_code == IN_PROGRESS`, the loop repeats up to 6 times (maximum 90s total wait).
     * If `status_code == ERROR`, routes to error notification.

### 5.3 Google Apps Script Cold Start Tolerance
- **Problem**: Google Apps Script webhooks experience a 10–18 second initialization latency after idle periods, causing standard 15s client timeouts to fail silently.
- **Mitigation in n8n**:
  1. Set request timeout on Google Sheets / Apps Script HTTP nodes to **45 seconds**.
  2. Enable automatic retry on HTTP status `504` or `ETIMEDOUT` with a 5-second interval.

### 5.4 Lead Phone Validation & Anti-Garbage Injection
- **Problem**: Bot submissions or invalid numbers entered on `wa.html` polluting Google Sheet `gid=513215731`.
- **Mitigation in n8n**:
  1. A dedicated `Code Node` (`Validate Egyptian Lead`) validates incoming strings against the canonical Egyptian regex:
     ```javascript
     const cleanPhone = String($json.patient_phone || '').replace(/[\s\-\+]/g, '');
     const isValid = /^(01[0125][0-9]{8}|201[0125][0-9]{8})$/.test(cleanPhone);
     if (!isValid || String($json.patient_name || '').trim().length < 2) {
       return { json: { valid: false, reason: "Invalid phone or name" } };
     }
     // Normalize to international 201XXXXXXXXX
     const normalized = cleanPhone.startsWith('01') ? '2' + cleanPhone : cleanPhone;
     return { json: { valid: true, normalized_phone: normalized, ...$json } };
     ```
  2. A downstream `Switch Node` immediately returns HTTP 400 for invalid leads, halting further execution before spreadsheet or Telegram nodes are reached.

---

## 6. Implementation Roadmap & Rollout

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                               HYBRID IMPLEMENTATION PHASES                             │
├─────────┬───────────────────────────────┬──────────────────────────────────────────────┤
│ Phase   │ Description                   │ Deliverables / Actions                       │
├─────────┼───────────────────────────────┼──────────────────────────────────────────────┤
│ Phase 1 │ Local n8n Engine Deployment   │ • Start n8n locally via `npx n8n`            │
│         │                               │ • Verify UI at http://localhost:5678         │
│         │                               │ • Configure SQLite persistence               │
├─────────┼───────────────────────────────┼──────────────────────────────────────────────┤
│ Phase 2 │ Production Workflow Import    │ • Import `omnichannel_cross_post.json`       │
│         │                               │ • Import `ai_content_factory_hitl.json`      │
│         │                               │ • Import `whatsapp_sheets_crm.json`         │
├─────────┼───────────────────────────────┼──────────────────────────────────────────────┤
│ Phase 3 │ Credential Configuration      │ • Add Meta Permanent Page Token              │
│         │                               │ • Add Telegram Bot Token & Chat ID           │
│         │                               │ • Add Google Service Account JSON            │
├─────────┼───────────────────────────────┼──────────────────────────────────────────────┤
│ Phase 4 │ Bridge Integration            │ • Update `antigravity_social_automation.py`  │
│         │                               │   to POST to `/webhook/publish-post`         │
│         │                               │ • Update `docs/wa.html` TRACKING_ENDPOINT    │
│         │                               │   to POST to `/webhook/lead-capture`         │
├─────────┼───────────────────────────────┼──────────────────────────────────────────────┤
│ Phase 5 │ 24/7 Cloud Migration (Opt.)   │ • Deploy Docker Compose stack to Oracle      │
│         │                               │   Cloud Always Free (0.00$/mo)               │
└─────────┴───────────────────────────────┴──────────────────────────────────────────────┘
```

This hybrid architecture provides complete fault isolation: a failure in external social media APIs or internet connectivity can never break local video rendering or static site compilation, and heavy media workloads can never destabilize the network orchestration engine.
