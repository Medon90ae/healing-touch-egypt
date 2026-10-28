# Zero-Cost n8n Quickstart & Production Setup Guide
## دليل التنفيذ والتشغيل السريع المجاني لمنصة n8n: ويندوز والسحابة والربط البرمجي

- **Project**: Healing Touch Egypt (هيلينج تاتش مصر) — `c:\followUPSHEET\healing_touch`
- **Document ID**: `HT-QUICKSTART-GUIDE-2026-R4`
- **Date**: 2026-10-28
- **Classification**: Operational Setup Manual & Credential Handbook

---

## 1. Quickstart Architecture & Options

This guide provides step-by-step instructions for deploying and configuring **n8n** at **$0.00 zero cost** to orchestrate social media publishing, Human-in-the-Loop review gates, and patient consultation intake for Healing Touch Egypt.

Two primary zero-cost deployment paths are supported:
1. **Local Workstation on Windows (Fastest & Lightest)**: Running n8n directly on Windows 10/11 via `npx n8n` (or Docker Desktop) with a free Cloudflare Tunnel for public webhooks.
2. **24/7 Cloud Server on Oracle Cloud Always Free (Production Permanent)**: Running n8n in a Docker container on an Oracle Cloud ARM Ampere A1 instance (4 vCPU, 24GB RAM, 200GB SSD) for permanent 24/7 uptime at **$0.00/month lifetime**.

> **⚠️ Deprecation Warning: n8n Desktop App**  
> The legacy Electron-based n8n Desktop application was **officially deprecated and discontinued by n8n in 2023**. Do NOT attempt to install the outdated desktop `.exe` installer. Use the lightweight Node.js `npx` method or Docker.

---

## 2. Option A: Local Zero-Cost Setup on Windows (via `npx n8n`)

This is the recommended local development and operational setup. It requires no virtual machines, no WSL2, and consumes only ~420 MB of RAM.

### Step 1: Prerequisites Check
Ensure you have **Node.js (LTS version 20 or higher)** installed on Windows. Open PowerShell and run:
```powershell
node -v
npm -v
```
*(If Node.js is missing, install it via `winget install OpenJS.NodeJS.LTS` or download from [nodejs.org](https://nodejs.org/)).*

### Step 2: Initialize n8n Configuration & Start
Open PowerShell as your standard user and run:
```powershell
# Set environment variables for storage and filesystem binary mode
$env:N8N_DEFAULT_BINARY_DATA_MODE = "filesystem"
$env:EXECUTIONS_DATA_PRUNE = "true"
$env:EXECUTIONS_DATA_MAX_AGE = "168" # Retain 7 days of execution history

# Launch n8n directly without global installation
npx n8n
```
When first run, n8n will:
1. Initialize a local SQLite database in `C:\Users\<YourUsername>\.n8n\database.sqlite`.
2. Start the local HTTP server and WebSocket daemon.
3. Output: `Editor is now accessible via: http://localhost:5678`.

Open your browser to `http://localhost:5678` and complete the initial one-time owner account setup (name, email, password).

### Step 3: Run n8n as a Background Windows Service (Optional)
To ensure n8n runs automatically in the background on system startup without keeping a PowerShell window open:
```powershell
# Install PM2 process manager globally
npm install -g pm2

# Start n8n under PM2
pm2 start npx --name "n8n-healing-touch" -- n8n

# Save process list for system reboot
pm2 save
```

---

## 3. Option B: Local Docker Compose Setup on Windows

If you already use Docker Desktop on Windows with WSL2:

### Step 1: Create `docker-compose.yml`
In a directory of your choice (e.g., `c:\followUPSHEET\healing_touch\n8n_docker`):
```yaml
version: '3.8'

services:
  n8n:
    image: docker.n8n.io/n8nio/n8n:latest
    container_name: n8n_healing_touch
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      - N8N_HOST=localhost
      - N8N_PORT=5678
      - N8N_PROTOCOL=http
      - NODE_ENV=production
      - WEBHOOK_URL=http://localhost:5678/
      - GENERIC_TIMEZONE=Africa/Cairo
      - TZ=Africa/Cairo
      - N8N_DEFAULT_BINARY_DATA_MODE=filesystem
      - EXECUTIONS_DATA_PRUNE=true
      - EXECUTIONS_DATA_MAX_AGE=168
    volumes:
      - n8n_data:/home/node/.n8n
      - c:/followUPSHEET/healing_touch/media_assets:/data/media_assets:ro

volumes:
  n8n_data:
```

### Step 2: Launch Container
```powershell
docker compose up -d
```
Access the dashboard at `http://localhost:5678`.

---

## 4. Option C: Permanent 24/7 Zero-Cost Cloud Setup (Oracle Cloud Always Free)

For true 24/7 operation—allowing website lead capture and instant WhatsApp/Telegram alerts even when your local PC is turned off—Oracle Cloud Infrastructure (OCI) offers the most generous free tier in the cloud industry:

### Step 1: Provision Oracle Cloud Compute Instance
1. Sign up for an **Oracle Cloud Always Free** account at [oracle.com/cloud/free](https://www.oracle.com/cloud/free/).
2. Create an **Ampere A1 Compute Instance** (Select: Shape `VM.Standard.A1.Flex`, 4 OCPUs, 24 GB RAM, Canonical Ubuntu 22.04 LTS or 24.04 LTS, 100 GB Boot Volume).
3. Assign a reserved Public IPv4 address.
4. In your VCN Security List, open Ingress ports `80` (HTTP), `443` (HTTPS), and `22` (SSH).

### Step 2: SSH into the Server & Install Docker + Caddy
Connect via terminal:
```bash
ssh -i ~/.ssh/id_rsa ubuntu@<YOUR_ORACLE_PUBLIC_IP>
```
Install Docker and Caddy (reverse proxy with automatic SSL):
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y docker.io docker-compose-plugin caddy git

# Add ubuntu user to docker group
sudo usermod -aG docker ubuntu
newgrp docker
```

### Step 3: Deploy Production `docker-compose.yml`
Create directory `/home/ubuntu/n8n` and save `docker-compose.yml`:
```yaml
version: '3.8'

services:
  n8n:
    image: docker.n8n.io/n8nio/n8n:latest
    container_name: n8n_production
    restart: always
    ports:
      - "127.0.0.1:5678:5678"
    environment:
      - N8N_HOST=n8n.healingtouch-egypt.com
      - N8N_PORT=5678
      - N8N_PROTOCOL=https
      - WEBHOOK_URL=https://n8n.healingtouch-egypt.com/
      - GENERIC_TIMEZONE=Africa/Cairo
      - TZ=Africa/Cairo
      - N8N_DEFAULT_BINARY_DATA_MODE=filesystem
      - EXECUTIONS_DATA_PRUNE=true
      - EXECUTIONS_DATA_MAX_AGE=336 # 14 days
    volumes:
      - /home/ubuntu/n8n_data:/home/node/.n8n
```

### Step 4: Configure Caddy Automatic HTTPS
Edit `/etc/caddy/Caddyfile`:
```caddy
n8n.healingtouch-egypt.com {
    reverse_proxy 127.0.0.1:5678 {
        header_up Host {upstream_hostport}
        header_up X-Real-IP {remote}
    }
}
```
Reload Caddy:
```bash
sudo systemctl reload caddy
```
Launch n8n:
```bash
docker compose up -d
```
Your n8n instance is now live at `https://n8n.healingtouch-egypt.com` with a valid Let's Encrypt SSL certificate at **$0.00/month**.

---

## 5. Free Cloudflare Tunnel Setup for Local Webhooks

When running n8n locally on Windows, external platforms (Meta, WhatsApp, website `wa.html`) cannot reach `http://localhost:5678` directly without port forwarding or a public tunnel. **Cloudflare Tunnel (`cloudflared`)** provides a zero-cost, encrypted HTTPS bridge:

1. Download `cloudflared.exe` from [cloudflare.com](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/).
2. Run a zero-config ad-hoc tunnel:
   ```powershell
   cloudflared.exe tunnel --url http://localhost:5678
   ```
3. Cloudflare outputs a public HTTPS address:
   `https://random-subdomain.trycloudflare.com`
4. Set your n8n environment variable:
   ```powershell
   $env:WEBHOOK_URL = "https://random-subdomain.trycloudflare.com/"
   ```
   Now, external webhooks from Meta Graph API and `docs/wa.html` reach your local n8n instance.

---

## 6. How to Import the Healing Touch Production Workflows

Three production-ready workflow JSON files are located in `c:\followUPSHEET\healing_touch\n8n_workflows/`:
1. `omnichannel_cross_post.json`
2. `ai_content_factory_hitl.json`
3. `whatsapp_sheets_crm.json`

### Import Procedure
1. Open n8n in your browser (`http://localhost:5678` or your domain).
2. Click **"Workflows"** in the left sidebar ➔ Click **"Add Workflow"** (or press `Ctrl + O`).
3. Click the **"..."** (three dots) icon in the top-right corner of the canvas.
4. Select **"Import from File"**.
5. Browse to `c:\followUPSHEET\healing_touch\n8n_workflows\` and select the desired `.json` file.
6. The full node graph, expressions, error retry loops, and routing logic will instantly render on the canvas.
7. Click **"Save"** in the top-right corner.
8. Toggle the workflow status switch from **"Inactive"** to **"Active"**.

---

## 7. Step-by-Step API Credentials Configuration

### 7.1 Meta Graph API (Facebook Page & Instagram Business)
In n8n, click **"Credentials"** in the left sidebar ➔ **"Add Credential"** ➔ search for **"Header Auth"** (or use HTTP Request parameters):

1. **Credential Name**: `Meta Permanent Graph API`
2. **Facebook Page ID**: `1371809382684781`
3. **Instagram Scoped User ID**: `27911522148524499`
4. **Graph API Version**: `v21.0`
5. **Access Token Configuration**:
   - In the HTTP Request node header:
     * Header Name: `Authorization`
     * Header Value: `Bearer <META_PERMANENT_PAGE_TOKEN>` (Retrieved from `antigravity_social_automation.py` line 66).
6. **Required Scopes on Meta Developer Portal**:
   - `pages_show_list`, `pages_read_engagement`, `pages_manage_posts`, `instagram_basic`, `instagram_content_publish`.

---

### 7.2 Google Sheets Service Account / OAuth2
To enable n8n to read and append rows to Google Sheet Tab `gid=513215731`:

1. **Create Service Account in Google Cloud Console**:
   - Go to [console.cloud.google.com](https://console.cloud.google.com/).
   - Create a project: `Healing-Touch-Egypt`.
   - Enable **Google Sheets API** and **Google Drive API**.
   - Navigate to **IAM & Admin** ➔ **Service Accounts** ➔ **Create Service Account**.
   - Create a JSON Key and download `credentials.json`.
2. **Share the Target Google Sheet**:
   - Open Google Sheet `12yAqzm-pSykfv7nRlvgocAHmwIYD_NPxqcNxrRKzA8k`.
   - Click **Share** ➔ paste the Service Account email address (e.g. `n8n-crm@healing-touch-egypt.iam.gserviceaccount.com`) with **Editor** permissions.
3. **Configure in n8n**:
   - In n8n, click **"Credentials"** ➔ **"Google Sheets OAuth2 API"** or **"Google Service Account"**.
   - Paste the Service Account Email and Private Key from `credentials.json`.
   - In the workflow node:
     * Document ID: `12yAqzm-pSykfv7nRlvgocAHmwIYD_NPxqcNxrRKzA8k`
     * Sheet Name / GID: Tab `gid=513215731` (`محرك التريند والمقالات الطبية`).

---

### 7.3 WhatsApp Cloud API (Official Meta Gateway)
1. **Meta Business & WhatsApp Developer Portal**:
   - Go to [developers.facebook.com](https://developers.facebook.com/) ➔ Select your App.
   - Navigate to **WhatsApp** ➔ **API Setup**.
   - Note the **Phone Number ID** and **WhatsApp Business Account ID**.
2. **Obtain System User Permanent Access Token**:
   - In Meta Business Suite ➔ Business Settings ➔ System Users ➔ Add System User (`n8n-whatsapp-dispatcher`).
   - Assign WhatsApp Assets with `Full Control` ➔ Generate Permanent Token with `whatsapp_business_messaging` scope.
3. **Configure in n8n**:
   - In n8n, click **"Credentials"** ➔ **"WhatsApp Cloud API"**.
   - Paste the Access Token, Phone Number ID, and Business Account ID.
   - Test by sending a templated alert message to the clinic manager's number `201155803307`.

---

### 7.4 Telegram Bot (Human-in-the-Loop & Instant Alerts)
1. **Create Telegram Bot via BotFather**:
   - Open Telegram and message `@BotFather`.
   - Send `/newbot` ➔ Name: `Healing Touch Egypt Approvals` ➔ Username: `healing_touch_approvals_bot`.
   - Copy the generated API Token (e.g., `7182938475:AAFx...`).
2. **Find Your Telegram Chat ID**:
   - Start a conversation with your new bot by clicking `Start`.
   - Message `@userinfobot` on Telegram to view your unique numeric `Id` (e.g., `123456789`).
   - If using a staff group, add the bot to the group, send a test message, and fetch the Group Chat ID (e.g., `-100192837465`).
3. **Configure in n8n**:
   - In n8n, click **"Credentials"** ➔ **"Telegram API"**.
   - Paste the Access Token.
   - In the Telegram Node:
     * Resource: `Message`
     * Operation: `Send Photo` (or `Send Message`)
     * Chat ID: `<YOUR_CHAT_ID>`
     * Reply Markup: `Inline Keyboard` for HITL approval buttons.

---

## 8. Integration Verification Checklist

To confirm that the zero-cost n8n environment is fully operational:

- [ ] **Engine Status**: `http://localhost:5678` (or your domain) displays the active n8n dashboard.
- [ ] **Workflows Active**: `omnichannel_cross_post`, `ai_content_factory_hitl`, and `whatsapp_sheets_crm` toggle switches are set to **Active**.
- [ ] **Webhook Test (`/webhook/lead-capture`)**: Send a test POST request via PowerShell:
  ```powershell
  Invoke-RestMethod -Uri "http://localhost:5678/webhook/lead-capture" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"patient_name":"أحمد ممدوح","patient_phone":"01012345678","context_topic":"اختبار تجريبي للتعافي","channel":"whatsapp","promo_code":"HT10","submitted_at":"2026-10-28T15:00:00Z"}'
  ```
  *Expected Result*: Returns HTTP 200 OK with `lead_id`, appends row to Google Sheet `gid=513215731`, and sends push notification to Telegram.
- [ ] **Telegram HITL Test**: Trigger `ai_content_factory_hitl`, verify Telegram Bot sends card preview with `[✅ نشر فوري]` and `[❌ إلغاء]` buttons, tap approve, and confirm downstream execution resumes.
- [ ] **Meta Graph API Connection**: Verify Facebook test photo post reaches draft or test page feed without rate limit errors.

This completes the zero-cost quickstart setup for Healing Touch Egypt.
