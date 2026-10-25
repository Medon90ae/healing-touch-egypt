# Project: Healing Touch Egypt (هيلينج تاتش مصر)

## Architecture
- **Generator Core:** `c:\followUPSHEET\healing_touch\github_seo_trend_engine.py`
- **Product Registry:** `c:\followUPSHEET\healing_touch\products_registry.json` (Dynamic configuration of all current and future medical recovery products)
- **Promo & Contact Config:** `c:\followUPSHEET\healing_touch\promo_config.json` (Promo code `HT10`, WhatsApp `201155803307`, Instagram `tapistorefamily2026`, Webhook/Beacon tracking endpoint)
- **Static Site Output (GitHub Pages):** `c:\followUPSHEET\healing_touch\docs/`
  - Homepage: `docs/index.html` (Interactive surgery selector, knowledge hub, promo drawers)
  - Dedicated Product Profiles: `docs/products/<product-slug>.html` (Full clinical specs, timelines, FAQs, linked articles)
  - Clinical Articles: `docs/articles/<article-slug>.html` (15+ interlinked articles, 10-12 PubMed references each, SVG timelines, comparison tables, high-intent hashtags)
  - Hashtag Index: `docs/hashtags_index.json` (Structured Egyptian patient hashtag bank)
  - Technical SEO: `docs/robots.txt`, `docs/sitemap.xml`, JSON-LD structured data on all pages
- **Deployment Remote:** `origin main` (`https://github.com/Medon90ae/healing-touch-egypt.git`)

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Zero Internal Meta-Labels Scan | Purge all marketing funnel jargon (`طمأنة المريض`, `المرحلة 1`, `المرحلة 2`, `الإقناع النفسي`, `Persuasion Triggers`, `Social Hook`, `E-E-A-T`, `محرك التريند`, etc.) | M1 | ORIGINAL_REQUEST §R1 |
| 2 | Empathetic Patient-Centric Copy | Authentic clinical Arabic text across all UI elements, buttons, badges, and body content | M1 | ORIGINAL_REQUEST §R1 |
| 3 | Dynamic Products Registry & Pages | `products_registry.json` supporting the 5 core products + generating `docs/products/<slug>.html` | M2 | ORIGINAL_REQUEST §R6 |
| 4 | Daily 3-Interlinked-Articles Per Product | Automated engine generating 3 clinical articles per product (15 minimum), 10-12 PubMed references each, sibling bidirectional links | M3 | ORIGINAL_REQUEST §R6 |
| 5 | Visual Diagrams & SVG Recovery Timelines | Step-by-step healing timelines (Week 1 to Month 3) and SVG illustrations in all articles | M4 | ORIGINAL_REQUEST §R2 |
| 6 | Clinical Comparison & Protocol Tables | Structured HTML tables comparing recommended protocol vs. traditional methods for all products | M4 | ORIGINAL_REQUEST §R2 |
| 7 | Homepage Surgery Selector & Knowledge Hub | Interactive surgery category triage + real-time search, category pills, and compact view | M4 | ORIGINAL_REQUEST §R2 |
| 8 | High-Intent Egyptian Patient Hashtags | 25–30 categorized Egyptian patient hashtags per article + `docs/hashtags_index.json` + one-click copy UI | M5 | ORIGINAL_REQUEST §R7 |
| 9 | Interactive Promo Micro-Popup Drawer | HT10 benefit confirmation drawer on WhatsApp/Instagram CTA clicks with automatic code copy | M6 | ORIGINAL_REQUEST §R3 |
| 10 | LocalStorage + Webhook Lead Tracking | Logging clicks locally (`localStorage` + `window.getLeadLog()`) and via asynchronous beacon/webhook | M6 | ORIGINAL_REQUEST §R3 |
| 11 | 2026 Medical SEO & JSON-LD Schemas | `MedicalWebPage`, `Article`, `FAQPage`, `MedicalBusiness` schemas, canonicals, OpenGraph & Twitter | M7 | ORIGINAL_REQUEST §R4 |
| 12 | Robots.txt & Comprehensive Sitemap.xml | Valid `docs/robots.txt` and full `docs/sitemap.xml` covering homepage, all products, and all articles | M7 | ORIGINAL_REQUEST §R4 |
| 13 | Deterministic Regeneration & Git Deploy | `python github_seo_trend_engine.py --build-site` exit code 0 + commit & push to `origin main` | M7 | ORIGINAL_REQUEST §R5 |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Copywriting Purity & Meta-Label Purge (R1) | Eliminate 100% of internal marketing terms from generator templates, Google Sheet sync, and HTML output | None | PLANNED |
| M2 | Dynamic Product Registry & Profiles (R6) | Create `products_registry.json` (5 products) and generator logic for `docs/products/<slug>.html` | None | PLANNED |
| M3 | Daily 3-Interlinked-Articles Engine (R6) | Generate 15 interlinked articles (3 per product), 10-12 citations, bidirectional links + parent link | M2 | PLANNED |
| M4 | Visual Polish, Timelines & Comparison Tables (R2) | Inject SVG healing timelines, HTML comparison tables, interactive homepage selector & hub filters | M1, M3 | PLANNED |
| M5 | Egyptian Patient Hashtag Research Engine (R7) | Researched hashtag sets per article, `docs/hashtags_index.json`, one-click copy UI | M3 | PLANNED |
| M6 | Promo Micro-Popup & Lead Tracker (R3) | Micro-popup drawer, clipboard copy HT10, localStorage tracker (`getLeadLog`) + beacon/webhook | M1 | PLANNED |
| M7 | Technical SEO, Regeneration & Deployment (R4, R5) | JSON-LD schemas, robots.txt, sitemap.xml, `--build-site` verification, git commit & push to `origin main` | M1-M6 | PLANNED |

## Code Layout
- `products_registry.json` — Product database and metadata
- `promo_config.json` — Promo codes, phone numbers, tracking endpoints
- `github_seo_trend_engine.py` — Complete site and cluster generator
- `docs/index.html` — Homepage
- `docs/products/*.html` — Product profile pages
- `docs/articles/*.html` — Medical cluster articles
- `docs/hashtags_index.json` — Hashtags export
- `docs/sitemap.xml` — XML sitemap
- `docs/robots.txt` — Search engine directives
