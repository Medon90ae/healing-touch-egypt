/**
 * ============================================================================
 * هيلينج تاتش مصر — Healing Touch Egypt
 * Production Zero-Cloud CRM Bridge Backend (Google Apps Script Web App)
 * ============================================================================
 * 
 * Purpose:
 * Provides a 100% free, production-grade Google Sheets CRM bridge that completely
 * bypasses Google Cloud Platform (GCP) Console, OAuth2 consent screens, service
 * account JSON keys, and cloud billing requirements.
 * 
 * Configured Web App Endpoint:
 * https://script.google.com/macros/s/AKfycbwDYeWbB9SjUqX1RXH7DaZ8yqG6V5Ay7yAiJ9L27Du1pJ8zb-NVgXzw6oz_0wJVp8Fr/exec
 * 
 * Target Google Spreadsheet:
 * ID: 12yAqzm-pSykfv7nRlvgocAHmwIYD_NPxqcNxrRKzA8k
 * Target Tab GID: 513215731 ("محرك التريند والمقالات الطبية (GitHub SEO)")
 * 
 * Deployment Guide (Zero-GCP):
 * 1. Open Google Sheet: https://docs.google.com/spreadsheets/d/12yAqzm-pSykfv7nRlvgocAHmwIYD_NPxqcNxrRKzA8k/edit
 * 2. Click Extensions (التطبيقات الملحقة) > Apps Script.
 * 3. Replace any existing Code.gs content with this entire file.
 * 4. Click "Deploy" (نشر) > "New deployment" (نشر جديد).
 * 5. Select type: "Web app" (تطبيق ويب).
 * 6. Configuration:
 *    - Description: "Healing Touch Egypt Production Zero-GCP CRM Bridge"
 *    - Execute as: "Me" (حسابي - Owner)
 *    - Who has access: "Anyone" (أي مستخدم - allows webhooks without Google login)
 * 7. Click "Deploy" and authorize spreadsheet access once.
 * 8. Copy the Web App URL (starts with https://script.google.com/macros/s/.../exec).
 * ============================================================================
 */

const CONFIG = {
  SPREADSHEET_ID: "12yAqzm-pSykfv7nRlvgocAHmwIYD_NPxqcNxrRKzA8k",
  TARGET_TAB_GID: 513215731,
  FALLBACK_SHEET_NAMES: [
    "محرك التريند والمقالات الطبية (GitHub SEO)",
    "Consultation Leads",
    "Leads",
    "الاستشارات الطبية"
  ],
  DEFAULT_PROMO_CODE: "HT10",
  DEFAULT_SOURCE: "website_consultation_bridge",
  HEADERS: [
    "Timestamp",
    "Lead ID",
    "Patient Name",
    "Phone Number",
    "Normalized Phone",
    "Surgical Case",
    "Promo Code",
    "Source Channel",
    "Page URL",
    "Notes",
    "CRM Status"
  ]
};

/**
 * Handle HTTP POST requests (Webhooks from n8n, Python CRM Sync Engine, and wa.html)
 */
function doPost(e) {
  var lock = LockService.getScriptLock();
  // Wait up to 10 seconds for concurrent requests to release lock
  var hasLock = lock.tryLock(10000);
  if (!hasLock) {
    return createJsonResponse({
      status: "busy",
      error: "Lock timeout: Another lead write is currently in progress. Please retry."
    }, 429);
  }

  try {
    var ss = SpreadsheetApp.openById(CONFIG.SPREADSHEET_ID);
    var sheet = getTargetSheet(ss);

    if (!sheet) {
      throw new Error("Target sheet could not be located by GID or name in spreadsheet: " + CONFIG.SPREADSHEET_ID);
    }

    // Ensure header row exists if sheet is fresh/empty
    ensureHeaderRow(sheet);

    // Parse incoming payload
    var payload = parsePayload(e);

    // Validate minimum required fields
    var patientName = (payload.patient_name || payload.name || "").toString().trim();
    var patientPhone = (payload.patient_phone || payload.phone || "").toString().trim();

    if (!patientName || patientName.length < 2) {
      patientName = "مريضة هيلينج تاتش (زائر غير محدد)";
    }

    // Clean & normalize Egyptian phone
    var normalizedPhone = normalizeEgyptianPhone(patientPhone);

    var now = new Date();
    var timestamp = payload.timestamp || Utilities.formatDate(now, "Africa/Cairo", "yyyy-MM-dd'T'HH:mm:ssXXX");
    var leadId = payload.lead_id || ("HT-" + Utilities.formatDate(now, "Africa/Cairo", "yyyyMMdd-HHmmss") + "-" + Math.floor(1000 + Math.random() * 9000));
    var surgicalCase = (payload.context_topic || payload.surgical_case || payload.topic || payload.case || "استشارة عامة لتعافي الجروح").toString().trim();
    var promoCode = (payload.promo_code || CONFIG.DEFAULT_PROMO_CODE).toString().trim();
    var source = (payload.source || payload.channel || CONFIG.DEFAULT_SOURCE).toString().trim();
    var pageUrl = (payload.page_url || payload.url || "").toString().trim();
    var notes = (payload.notes || "مسجل عبر جسر Apps Script Web App المجاني (Zero-GCP)").toString().trim();
    var crmStatus = (payload.crm_status || "NEW").toString().trim();

    // Append CRM row
    sheet.appendRow([
      timestamp,
      leadId,
      patientName,
      patientPhone,
      normalizedPhone,
      surgicalCase,
      promoCode,
      source,
      pageUrl,
      notes,
      crmStatus
    ]);

    var responseData = {
      status: "success",
      lead_id: leadId,
      patient_name: patientName,
      patient_phone: patientPhone,
      normalized_phone: normalizedPhone,
      promo_code: promoCode,
      message: "Lead recorded in Google Sheet successfully (Zero-GCP Bypass)",
      timestamp: timestamp,
      sheet_name: sheet.getName(),
      total_rows: sheet.getLastRow()
    };

    return createJsonResponse(responseData);

  } catch (err) {
    return createJsonResponse({
      status: "error",
      error: err.toString(),
      stack: err.stack || "N/A"
    });
  } finally {
    lock.releaseLock();
  }
}

/**
 * Handle HTTP GET requests (Health check, monitoring, and status probes)
 */
function doGet(e) {
  var action = (e && e.parameter && e.parameter.action) ? e.parameter.action : "health";

  try {
    var ss = SpreadsheetApp.openById(CONFIG.SPREADSHEET_ID);
    var sheet = getTargetSheet(ss);

    if (action === "stats") {
      return createJsonResponse({
        status: "ok",
        spreadsheet_id: CONFIG.SPREADSHEET_ID,
        spreadsheet_name: ss.getName(),
        target_tab_name: sheet ? sheet.getName() : "NOT_FOUND",
        target_tab_gid: sheet ? sheet.getSheetId() : null,
        total_rows: sheet ? sheet.getLastRow() : 0,
        total_cols: sheet ? sheet.getLastColumn() : 0
      });
    }

    // Default health response
    return createJsonResponse({
      status: "alive",
      service: "Healing Touch Egypt CRM Apps Script Web App",
      endpoint_type: "free_zero_gcp_bypass",
      spreadsheet_id: CONFIG.SPREADSHEET_ID,
      tab_gid: CONFIG.TARGET_TAB_GID,
      timestamp: new Date().toISOString()
    });

  } catch (err) {
    return createJsonResponse({
      status: "error",
      message: "Spreadsheet access error: " + err.toString()
    });
  }
}

/**
 * Helper: Find sheet tab by GID or fallbacks
 */
function getTargetSheet(spreadsheet) {
  var sheets = spreadsheet.getSheets();
  for (var i = 0; i < sheets.length; i++) {
    if (sheets[i].getSheetId() === CONFIG.TARGET_TAB_GID) {
      return sheets[i];
    }
  }

  // Fallback to recognized names
  for (var j = 0; j < CONFIG.FALLBACK_SHEET_NAMES.length; j++) {
    var fallback = spreadsheet.getSheetByName(CONFIG.FALLBACK_SHEET_NAMES[j]);
    if (fallback) {
      return fallback;
    }
  }

  // Final fallback to the very first sheet
  return sheets.length > 0 ? sheets[0] : null;
}

/**
 * Helper: Ensure header row exists
 */
function ensureHeaderRow(sheet) {
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(CONFIG.HEADERS);
    var headerRange = sheet.getRange(1, 1, 1, CONFIG.HEADERS.length);
    headerRange.setFontWeight("bold");
    headerRange.setBackground("#1a365d");
    headerRange.setFontColor("#ffffff");
  }
}

/**
 * Helper: Parse incoming request payload (handles JSON strings and Form URL Encoded)
 */
function parsePayload(e) {
  if (!e) return {};

  if (e.postData && e.postData.contents) {
    try {
      return JSON.parse(e.postData.contents);
    } catch (parseErr) {
      // Not JSON, check parameters
    }
  }

  if (e.parameter) {
    return e.parameter;
  }

  return {};
}

/**
 * Helper: Clean and normalize Egyptian phone number to 201XXXXXXXXX format
 */
function normalizeEgyptianPhone(phone) {
  if (!phone) return "";
  var clean = phone.toString().replace(/[^0-9]/g, "");

  // Starts with 01X -> add 2
  if (/^01[0125][0-9]{8}$/.test(clean)) {
    return "2" + clean;
  }

  // Starts with 201X
  if (/^201[0125][0-9]{8}$/.test(clean)) {
    return clean;
  }

  // Starts with +201X (cleaned of + already)
  if (/^00201[0125][0-9]{8}$/.test(clean)) {
    return clean.substring(2);
  }

  return clean;
}

/**
 * Helper: Create standardized JSON ContentService response
 */
function createJsonResponse(data) {
  return ContentService.createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
}
