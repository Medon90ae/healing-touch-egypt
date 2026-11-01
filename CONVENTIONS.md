# Architectural Conventions & Guidelines

## 1. Single Source of Truth for Data Validation & Normalization
- **Egyptian Phone Validation & Normalization**:
  - Python implementations must reside in a unified validation module (e.g., `core/validation.py` or `shared/validators.py`). Components such as `scripts/crm_sync_engine.py` and test suites must import and reuse this logic rather than redefining regex (`^01[0125][0-9]{8}$`) or string stripping rules locally.
  - TypeScript/JavaScript validation must be maintained in `portal_app/src/utils/validation.ts` and shared across frontend components and Apps Script adapters to ensure identical validation constraints across all client and ingestion surfaces.

## 2. Frontend Asset Deduplication & Single Source Distribution
- **WhatsApp Triage Script (`whatsapp-triage.js`)**:
  - Maintain a canonical source within the portal source directory (`portal_app/public/assets/whatsapp-triage.js` or as a reusable React module).
  - Web root targets (`docs/assets/whatsapp-triage.js`, `docs/portal/assets/whatsapp-triage.js`) must be generated or synced via an automated build or copy script rather than tracked and edited as independent duplicate files.
  - Configuration constants (webhook URLs, phone numbers, campaign tags) must remain strictly centralized.

## 3. Modular Engine Structure & Pipeline Isolation
- **Pipeline and Builder Separation**:
  - Engines responsible for content generation, scraping, and landing page builds (`campaign_landing_engine.py`, `github_seo_trend_engine.py`) should be grouped under modular packages (e.g., `engines/` or `src/pipeline/`).
  - Temporary or manual patch scripts (e.g., `scripts/patch_seo_engine_whatsapp.py`) must be phased out or merged directly into the core generation engines.
  - Audio/video rendering (`scripts/media_video_engine.py`, `antigravity_social_automation.py`) should share a common media layer under `engines/media/`.

## 4. Functional Test Suite Organization
- **Structure tests by domain and layer** rather than historical challenge labels:
  - `tests/unit/`: Logic validation, phone regex parsing, hashtag generators, and pure text sanitation.
  - `tests/e2e_publishing/`: External webhook dispatches, n8n integrations, social publication flows, and file artifact triage.
  - `tests/seo_compliance/`: HTML schema validation, internal link integrity, metadata audits, and medical compliance checks.
  - Common testing fixtures (DOM parsers, Arabic text normalization) must be centralized in `tests/helpers.py` or `tests/conftest.py` to prevent redundant parser implementations across test files.

## 5. Root Directory Hygiene
- Keep the repository root uncluttered:
  - Root should contain only primary configuration files, entry points (`menu.py`), and documentation.
  - Automated intake tools (`smart_intake_classifier.py`), harvesting pipelines (`clinical_research_harvester.py`), and asset builders should reside within structured subpackages (`src/intake/`, `src/research/`, `src/automation/`).
