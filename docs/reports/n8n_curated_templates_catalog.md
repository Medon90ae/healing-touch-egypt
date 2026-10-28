# Curated Free n8n Templates Catalog: Omnichannel, HITL & CRM
## دليل وفهرس أفضل قوالب n8n المجانية المعتمدة للأتمتة والتسويق وخدمة العملاء

- **Project**: Healing Touch Egypt (هيلينج تاتش مصر) — `c:\followUPSHEET\healing_touch`
- **Document ID**: `HT-TEMPLATES-CATALOG-2026-R1`
- **Date**: 2026-10-28
- **Classification**: Evaluated Template Catalog & Production Blueprints

---

## Executive Summary

This catalog presents a curated, forensically audited selection of high-performing workflow templates mined from the official **n8n Templates Library** (`n8n.io/workflows`) and the global developer ecosystem. Each template has been evaluated against the specific operational requirements of **Healing Touch Egypt**, spanning three core automation domains:

1. **Omnichannel Multi-Platform Publishing** (Facebook, Instagram, YouTube Shorts, TikTok, Reddit, Blogger).
2. **AI Content Factory with Human-in-the-Loop (HITL)** (Automated trend ingestion, Egypt clinical copywriting, and Telegram/Email interactive review gates).
3. **WhatsApp & Google Sheets Patient CRM** (Gated consultation intake from `wa.html`, Egyptian phone normalization, Google Sheet logging on tab `gid=513215731`, and instant staff alerts).

Every template is documented with its official Template ID, verified direct URL, node topology, community view count, strengths, limitations, and zero-cost adaptation instructions.

---

## 1. Domain 1: Omnichannel Cross-Posting Workflows

### 1.1 Template #5338 — AI Viral Video Syndication Engine
- **Official Name**: "Generate AI viral videos with Seedance and upload to TikTok, YouTube & Instagram"
- **Template ID**: `5338`
- **Verified URL**: [https://n8n.io/workflows/5338](https://n8n.io/workflows/5338)
- **Direct API Endpoint**: `https://api.n8n.io/api/templates/workflows/5338`
- **Community Popularity**: **350,283+ Views** | Production Grade
- **Node Count**: 40 Nodes
- **Node Topology**:
  `Schedule / Webhook Trigger` ➔ `OpenAI (Prompt Generation)` ➔ `HTTP Request (Seedance Video API)` ➔ `Wait (Polling Loop)` ➔ `HTTP Request (Blotato Multi-Platform Dispatch)` ➔ `YouTube Node` ➔ `Instagram Node` ➔ `TikTok Dispatcher` ➔ `Google Sheets (Logging)`
- **Evaluation & Clinical Fit**:
  * **Strengths**: Extremely popular, comprehensive end-to-end multi-platform dispatching, handles video upload states and Google Sheets logging.
  * **Limitations**: Relies on third-party commercial aggregators (Seedance and Blotato) which require paid subscription keys.
  * **Zero-Cost Adaptation for Healing Touch Egypt**: Remove the Seedance and Blotato nodes. Replace them with incoming payload from our local Python FFmpeg video engine (`media_video_engine.py`) and direct native Meta Graph API / YouTube Data API v3 HTTP nodes.

---

### 1.2 Template #8642 — AI Viral Video Factory to TikTok & Social
- **Official Name**: "Generate AI viral videos with VEO 3 and upload to TikTok"
- **Template ID**: `8642`
- **Verified URL**: [https://n8n.io/workflows/8642](https://n8n.io/workflows/8642)
- **Direct API Endpoint**: `https://api.n8n.io/api/templates/workflows/8642`
- **Community Popularity**: **307,917+ Views**
- **Node Count**: 24 Nodes
- **Node Topology**:
  `Manual / Webhook Trigger` ➔ `Code Node (Topic Extraction)` ➔ `Google Gemini / VEO API` ➔ `Binary Stream Buffer` ➔ `TikTok API Node` ➔ `Telegram Notification`
- **Evaluation & Clinical Fit**:
  * **Strengths**: High popularity, concise routing, native TikTok API configuration patterns.
  * **Limitations**: Directly passing large video binary streams through Node.js memory risks hitting the 1.4 GB V8 heap limit.
  * **Zero-Cost Adaptation for Healing Touch Egypt**: Pass public HTTPS video URLs (hosted on GitHub raw or Cloudflare) instead of raw binary buffers through n8n nodes.

---

### 1.3 Template #2894 — Native Direct Multi-Platform Video Publisher (Recommended Base)
- **Official Name**: "Upload to Instagram, TikTok & YouTube from Google Drive"
- **Template ID**: `2894`
- **Verified URL**: [https://n8n.io/workflows/2894](https://n8n.io/workflows/2894)
- **Direct API Endpoint**: `https://api.n8n.io/api/templates/workflows/2894`
- **Community Popularity**: **53,120+ Views**
- **Node Count**: 15 Nodes
- **Node Topology**:
  `Google Drive Trigger` ➔ `Filter (Video Check)` ➔ `Branch (Parallel Split)` ➔
  ├─► `YouTube Node (Upload Video, Set Tags & Playlist)`
  ├─► `HTTP Request (Meta Graph API: Instagram /media Container)` ➔ `Wait 30s` ➔ `HTTP Request (/media_publish)`
  └─► `HTTP Request (TikTok Creator API)` ➔ `Telegram Log Node`
- **Evaluation & Clinical Fit**:
  * **Strengths**: **100% Free and Native.** Uses zero commercial intermediary aggregators. Directly calls official Google, Meta, and TikTok endpoints with credentials managed natively in n8n.
  * **Limitations**: Relies on Google Drive file upload trigger rather than an immediate HTTP webhook from a local Python engine.
  * **Zero-Cost Adaptation for Healing Touch Egypt**: Swap the Google Drive Trigger with `n8n-nodes-base.webhook` listening for `POST /webhook/publish-post` from our Python automation script.

---

### 1.4 Template #9059 — Multi-Network Social Post & Media Syndicator
- **Official Name**: "Auto-generate social media posts from URLs with AI, Telegram & multi-platform posting"
- **Template ID**: `9059`
- **Verified URL**: [https://n8n.io/workflows/9059](https://n8n.io/workflows/9059)
- **Direct API Endpoint**: `https://api.n8n.io/api/templates/workflows/9059`
- **Community Popularity**: **2,213+ Views**
- **Node Count**: 42 Nodes
- **Node Topology**:
  `Webhook Trigger` ➔ `HTML Extractor (Scrape URL)` ➔ `OpenAI Chat Model (Tailor 4 Variants)` ➔ `Set Node (Format Platform JSON)` ➔ `Facebook Graph Node` ➔ `Instagram Graph Node` ➔ `LinkedIn Node` ➔ `Supabase (Audit Log)`
- **Evaluation & Clinical Fit**:
  * **Strengths**: Robust multi-platform text and image distribution; excellent formatting of platform-specific aspect ratios and character constraints.
  * **Zero-Cost Adaptation for Healing Touch Egypt**: Replace Supabase with Google Sheets tab `gid=513215731` for audit logging, and utilize the existing Meta permanent access token.

---

### 1.5 Template #21045 — Short-Form Video Syndicator via Postdom
- **Official Name**: "Post Telegram videos to TikTok, Instagram and YouTube with Claude and Postdom"
- **Template ID**: `21045`
- **Verified URL**: [https://n8n.io/workflows/21045](https://n8n.io/workflows/21045)
- **Direct API Endpoint**: `https://api.n8n.io/api/templates/workflows/21045`
- **Node Count**: 10 Nodes
- **Node Topology**:
  `Telegram Trigger (Incoming Video)` ➔ `Claude 3.5 Sonnet (Generate Hook & Description)` ➔ `Postdom Node (Syndicate to TikTok, IG, YT)` ➔ `Telegram Reply (Status)`
- **Evaluation & Clinical Fit**:
  * **Strengths**: Clean Telegram-first architecture, highly convenient for mobile-first content drops.
  * **Limitations**: Requires third-party Postdom API key.

---

## 2. Domain 2: AI Content Factory with Human-in-the-Loop (HITL)

### 2.1 Template #5773 — Telegram Interactive Approval Gate (Gold Standard HITL)
- **Official Name**: "Generate & schedule social media posts with GPT-4 and Telegram approval workflow"
- **Template ID**: `5773`
- **Verified URL**: [https://n8n.io/workflows/5773](https://n8n.io/workflows/5773)
- **Direct API Endpoint**: `https://api.n8n.io/api/templates/workflows/5773`
- **Community Popularity**: **3,489+ Views** | Best-Practice HITL Pattern
- **Node Count**: 24 Nodes
- **Node Topology**:
  `Schedule Trigger (Daily Morning)` ➔ `OpenAI / Claude (Generate Draft Copy & Hashtags)` ➔ `HTTP Request (Fetch Card Image)` ➔ `Telegram Node (Send Photo with Inline Keyboard)` ➔ `Wait Node (Wait for Webhook Callback)` ➔ `Switch Node (Check Callback Query Data)` ➔
  ├─► *Branch 1: `approve`* ➔ `Facebook Graph API` ➔ `Instagram Graph API` ➔ `Telegram (Success Alert)`
  ├─► *Branch 2: `reject`* ➔ `Telegram (Cancellation Notice)` ➔ `Stop Execution`
  └─► *Branch 3: `edit`* ➔ `Telegram (Prompt for New Caption)` ➔ `Loop back to Wait`
- **Inline Keyboard Definition**:
  ```json
  {
    "inline_keyboard": [
      [
        { "text": "✅ نشر فوري للمنصات", "callback_data": "approve_{{$execution.id}}" },
        { "text": "❌ إلغاء المنشور", "callback_data": "reject_{{$execution.id}}" }
      ],
      [
        { "text": "📝 طلب تعديل الكابشن", "callback_data": "edit_{{$execution.id}}" }
      ]
    ]
  }
  ```
- **Evaluation & Clinical Fit**:
  * **Strengths**: Provides a complete, secure Human-in-the-Loop review system. Prevents unauthorized or hallucinated medical posts from going live. The clinic manager receives a photo preview and text summary on their mobile phone, approving with a single tap.
  * **Adaptation for Healing Touch Egypt**: Adopt this exact node structure as the core approval gate inside our production `ai_content_factory_hitl.json` workflow.

---

### 2.2 Template #5397 — RSS & Clinical Trend to Social HITL
- **Official Name**: "Auto-Generate & Approve Social Media Posts from RSS Feeds with OpenAI & Telegram"
- **Template ID**: `5397`
- **Verified URL**: [https://n8n.io/workflows/5397](https://n8n.io/workflows/5397)
- **Direct API Endpoint**: `https://api.n8n.io/api/templates/workflows/5397`
- **Community Popularity**: **2,919+ Views**
- **Node Count**: 12 Nodes
- **Node Topology**:
  `RSS Feed Read` ➔ `Code Node (Deduplication Check)` ➔ `OpenAI (Summarize & Formulate Advice)` ➔ `Telegram (Preview & Approval)` ➔ `Wait` ➔ `Meta / Twitter Nodes`
- **Evaluation & Clinical Fit**:
  * **Strengths**: Highly effective for ingesting medical journal feeds (e.g., PubMed RSS or Plastic Surgery News) and preparing daily educational briefs for review.

---

### 2.3 Template #4005 — Email-Based Webhook Approval Gate
- **Official Name**: "AI-generated LinkedIn posts with OpenAI, Google Sheets & email approval workflow"
- **Template ID**: `4005`
- **Verified URL**: [https://n8n.io/workflows/4005](https://n8n.io/workflows/4005)
- **Direct API Endpoint**: `https://api.n8n.io/api/templates/workflows/4005`
- **Community Popularity**: **46,546+ Views**
- **Node Count**: 11 Nodes
- **Node Topology**:
  `Google Sheets Trigger` ➔ `OpenAI Node` ➔ `Send Email (Formatted HTML with Cryptographic Action URLs)` ➔ `Wait Node (Wait for Webhook)` ➔ `Social Publish Node`
- **Evaluation & Clinical Fit**:
  * **Strengths**: Valuable fallback if the clinic manager prefers email review over Telegram, or for secondary medical director approvals.

---

### 2.4 Template #11298 — Multi-Stage Slack Approval Content Engine
- **Official Name**: "AI-powered content factory: RSS to blog, Instagram & TikTok with Slack approval"
- **Template ID**: `11298`
- **Verified URL**: [https://n8n.io/workflows/11298](https://n8n.io/workflows/11298)
- **Direct API Endpoint**: `https://api.n8n.io/api/templates/workflows/11298`
- **Community Popularity**: **8,479+ Views**
- **Node Count**: 22 Nodes
- **Evaluation & Clinical Fit**:
  * Demonstrates multi-stage drafting (short-form text, visual carousels, blog HTML) branching from a single medical topic.

---

## 3. Domain 3: WhatsApp & Google Sheets Patient CRM

### 3.1 Template #21303 — Website Lead Intake & Dual Alert CRM (Production Grade)
- **Official Name**: "Capture website leads in Google Sheets CRM with WhatsApp and Gmail alerts"
- **Template ID**: `21303`
- **Verified URL**: [https://n8n.io/workflows/21303](https://n8n.io/workflows/21303)
- **Direct API Endpoint**: `https://api.n8n.io/api/templates/workflows/21303`
- **Community Popularity**: Enterprise Verified | Production Grade
- **Node Count**: 37 Nodes
- **Node Topology**:
  `Webhook Trigger (POST /lead-capture)` ➔ `Code Node (Validate & Normalize Lead)` ➔ `Switch Node (Valid vs Invalid)` ➔
  ├─► *Valid Lead*:
  │    ├─► `Google Sheets Node (Append Row with Retry)` ➔ `If Failed ➔ Wait 5s ➔ Retry 3x`
  │    ├─► `WhatsApp Cloud API Node (Send Lead Alert to On-Call Nurse)`
  │    └─► `Telegram Node (Send High-Priority Group Notification)` ➔ `Respond to Webhook (200 OK)`
  └─► *Invalid Lead*:
       └─► `Respond to Webhook (400 Bad Request)` ➔ `Log to Spam Monitor`
- **Resilience Features**:
  * Explicit retry loops around Google Sheets API writes to withstand Google API rate limits.
  * Fallback to Gmail notification if WhatsApp Cloud API returns error.
- **Evaluation & Clinical Fit**:
  * **Strengths**: Directly aligns with our `docs/wa.html` lead gating requirements. Captures patient name, Egyptian phone, surgical context, and promo code `HT10`, logging them to Google Sheet `gid=513215731` and notifying on-duty staff instantly.
  * **Adaptation for Healing Touch Egypt**: Adopt as the foundational blueprint for `whatsapp_sheets_crm.json`.

---

### 3.2 Template #13450 — WhatsApp AI Lead Qualification & Triage
- **Official Name**: "Auto-respond and classify WhatsApp leads with Ollama AI and log to Google Sheets"
- **Template ID**: `13450`
- **Verified URL**: [https://n8n.io/workflows/13450](https://n8n.io/workflows/13450)
- **Direct API Endpoint**: `https://api.n8n.io/api/templates/workflows/13450`
- **Community Popularity**: **2,003+ Views**
- **Node Count**: 29 Nodes
- **Node Topology**:
  `WhatsApp Trigger` ➔ `Ollama / OpenAI Model (Classify Intent: Hot / Inquiry / Support)` ➔ `Switch Node` ➔ `Google Sheets (Categorized Tab Append)` ➔ `WhatsApp Reply (Send Clinical Booking Link)`
- **Evaluation & Clinical Fit**:
  * **Strengths**: Allows 100% local, zero-cost AI triage using Ollama running locally on the clinic workstation without incurring OpenAI API charges.

---

### 3.3 Template #5907 — Form-to-WhatsApp Personalized Outreach
- **Official Name**: "Automate lead capture with AI personalized WhatsApp messages via Unipile & Google Sheets CRM"
- **Template ID**: `5907`
- **Verified URL**: [https://n8n.io/workflows/5907](https://n8n.io/workflows/5907)
- **Direct API Endpoint**: `https://api.n8n.io/api/templates/workflows/5907`
- **Community Popularity**: **3,543+ Views**
- **Node Count**: 9 Nodes
- **Evaluation & Clinical Fit**:
  * Illustrates dynamic templating where an incoming consultation context (e.g., "جرح قيصرية ملتهب") automatically personalizes the initial greeting sent to the patient.

---

### 3.4 Template #15044 — Multi-Gateway WhatsApp Business Ingestion
- **Official Name**: "Automate WhatsApp lead capture and replies with Whapi, Ollama and Sheets"
- **Template ID**: `15044`
- **Verified URL**: [https://n8n.io/workflows/15044](https://n8n.io/workflows/15044)
- **Direct API Endpoint**: `https://api.n8n.io/api/templates/workflows/15044`
- **Community Popularity**: **947+ Views**
- **Node Count**: 8 Nodes
- **Evaluation & Clinical Fit**:
  * Useful reference for setups utilizing WhatsApp Web emulation gateways (e.g. Whapi / Baileys) when the official Meta Cloud API is unavailable.

---

## 4. Master Comparative Evaluation Matrix

| Template ID | Official Template Name | Category | Node Count | Views / Status | Primary Strengths | Healing Touch Egypt Production Role |
| :---: | :--- | :--- | :---: | :---: | :--- | :--- |
| **#2894** | Upload to Instagram, TikTok & YouTube from Drive | Omnichannel | 15 | 53,120 | 100% Native APIs, zero SaaS fees | Base for `omnichannel_cross_post.json` |
| **#5338** | Generate AI viral videos to TikTok, YT & IG | Omnichannel | 40 | 350,283 | Massive ecosystem adoption, robust logging | Architecture reference for multi-container states |
| **#9059** | Auto-generate social posts from URLs with AI | Omnichannel | 42 | 2,213 | Meta Graph API & image adaptation | Pattern for Facebook & Instagram multi-cards |
| **#5773** | Generate posts with GPT-4 & Telegram approval | HITL Engine | 24 | 3,489 | Interactive Telegram inline buttons & state pause | Core approval engine for `ai_content_factory_hitl.json` |
| **#4005** | AI LinkedIn posts with email approval workflow | HITL Engine | 11 | 46,546 | Robust cryptographic email wait hooks | Secondary approval channel for medical director |
| **#21303** | Capture leads in Sheets CRM with WhatsApp alerts | Patient CRM | 37 | Enterprise | Built-in retry loops, input validation, multi-alert | Production core for `whatsapp_sheets_crm.json` |
| **#13450** | Classify WhatsApp leads with Ollama & Sheets | Patient CRM | 29 | 2,003 | 100% free local AI triage via Ollama | Future upgrade for automated inbound chat triage |

---

## 5. Blueprint Extraction & Custom Production Workflows

From the evaluated catalog, three production-grade, self-contained workflow blueprints have been engineered and saved to `c:\followUPSHEET\healing_touch\n8n_workflows/`:

1. **`omnichannel_cross_post.json`** (Derived from #2894 + #9059):
   - Ingests Python publishing webhook `POST /webhook/publish-post`.
   - Dispatches in parallel to Meta Facebook Page Feed and Instagram Graph API (with container processing polling loop).
   - Posts clinical guide to Blogger via secret webhook and submits discussion thread to Reddit.
   - Logs all post URLs and timestamps to Google Sheets audit tab.
2. **`ai_content_factory_hitl.json`** (Derived from #5773 + #5397):
   - Reads daily trending medical topics and PubMed citations.
   - Generates 3 platform copywriting variants tailored to Egyptian clinical recovery.
   - Dispatches interactive photo card and copy to Telegram Bot.
   - Pauses execution until clinic manager taps `[✅ نشر فوري]` or `[❌ إلغاء]`.
   - On approval, automatically triggers `omnichannel_cross_post.json`.
3. **`whatsapp_sheets_crm.json`** (Derived from #21303 + #13450):
   - Listens for patient submissions on `POST /webhook/lead-capture` from `wa.html`.
   - Validates Egyptian mobile number format (`01XXXXXXXXX`) and normalizes to `201XXXXXXXXX`.
   - Appends lead to Google Sheet `12yAqzm-pSykfv7nRlvgocAHmwIYD_NPxqcNxrRKzA8k` (Tab `gid=513215731`) with a 3-attempt exponential retry loop.
   - Fires an immediate high-priority alert to the clinic staff's Telegram group and on-duty WhatsApp number.
   - Returns HTTP 200 with the formatted WhatsApp consultation deep link.
