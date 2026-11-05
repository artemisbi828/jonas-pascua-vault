> [!abstract] TLDR
MVP site: concise mid‑market messaging (Dashboards, Doc‑Scrapers, Apps), embedded PBI demo, Office Script GIF, resume, pricing, use cases, and a tracked “Schedule a Call” CTA.

# Artemis‑BI Website Plan (MVP → Extensible)

## Goals → Outcomes
- Serve LinkedIn/interview traffic with proof → embedded PBI, Office Script GIF, resume, services, pricing, concise use cases.
- CTA → "Schedule a Call" via Google Business Calendar.
- Tracking → short links (Bitly‑style or custom) + GA4 + server‑side events → iterate on structure.

## Sitemap → IA
- Home → headline/tagline; 3 icon metrics; featured services.
- Services → Dashboards; Doc‑Scrapers; App Builds/Websites; engagement models.
- Use Cases → 6–8 concise cards (Problem → Approach → Outcome → Metrics).
- Pricing → Tier cards (Professional/Business/Enterprise) with bands; −20% competitive.
- Resume → adapted highlights.
- Embedded PBI → sample report.
- Office Script GIF → 10–20s automation clip.
- Contact → form + links → schedule a call.

## CTA Funnel → Tracking
```mermaid
graph TD
  X[Short Link (LinkedIn/Email)] --> Y[Landing Page]
  Y --> Z[CTA: Schedule a Call]
  X --> GA[GA4 + UTM]
  GA --> CE[Server Event Log (Cosmos)]
  Z --> CAL[Google Business Calendar]
  CAL --> CONF[Confirmation + Optional Pre‑Intake]
```

## Copy Skeletons (HiHello‑inspired, mid‑market tone)
- Home
  - Headline → "BI, Automations, and Analytics—Built for Mid‑Market Momentum."
  - Tagline → "From raw data to boardroom clarity—fast."
  - 3 Icons → "Dashboards that explain ‘why’", "Automate the boring", "Ready‑to‑run workflows".
  - CTA → "Schedule a Call".
- Services (lead with these 3)
  - Dashboards → Exec insights; capacity; leaderboards; exception alerts.
  - Doc‑Scrapers → PDFs/XLS → clean CSV/JSON; compliance‑aware intake.
  - App Builds/Websites → Call‑Work‑Queue; intake forms; SMS; static site.
  - Engagement Models → Embedded / Injected / Hosted / Bridged.
- Use Cases (cards)
  - Orthodontics → No‑show reduction (SlideSMS + capacity); patient systems Cloud9/OrthoFi.
  - Manufacturing → ERP migration ops signals; bridging accounting/receiving/purchasing.
  - Tax Firms → Shoebox to structured CSV; prep time ↓.
  - Sales Ops → Lead recovery; drip alarms; $2K baseline.
  - FP&A → Cash/AR/AP; AP dispersion; vendor term insights.
  - Restaurant → Inventory expiry warnings; specials planning; vendor APIs.
- Pricing
  - Professional → $299–$699; $49–$149/mo; $99 setup + $19–$39/mo; upsell mini dashboard.
  - Business → $2.5K–$4K; $2K–$3K; $3K–$6K; ~$2K app; $750–$1,500/mo retainer.
  - Enterprise → $25K–$75K projects; $15K–$40K dashboards; $8K–$14K/mo premium retainer.
- Resume → distilled highlights (BI, DE, FP&A); link to full resume.
- Embedded PBI → sample Exec Insights report (WDE/SSS demo).
- Office Script GIF → data cleanup → export → email/sync.
- Contact → calendar link; optional pre‑intake upload.

## "What is a Data Engineer?" — Site Copy Block
- Data must flow: source → pipelines → models → surfaces (dashboards/apps) → decisions.
- If data stagnates (unmaintained spreadsheets, ad‑hoc exports), it becomes noisy, unreliable, and costly.
- A data engineer designs flow and reliability:
  - Capture → connect systems and APIs safely.
  - Normalize → enforce consistent shapes and definitions.
  - Orchestrate → keep data fresh on schedules with error handling.
  - Secure → apply row‑level security and audit trails.
  - Observe → track latency, errors, and usage; improve iteratively.
- Partnership promise: I build the infrastructure that keeps your decisions nimble as you grow—so you steer the business, not wrangle files.

## Artemis Version of HiHello Elements (Mapped)
- Features → Digital Cards analogs → "Service Tiles" with concise copy and consistent branding.
- Email Signature → turn card details into signature → optional.
- Virtual Backgrounds → replace with "Demo GIFs" that show automations.
- Lead Capture → pre‑intake form; compliant flows.
- Scanning → replace with "Doc‑Scraper" pitch.
- Business Contact Manager → CRM sync (Salesforce/Dynamics/HubSpot) as roadmap.
- Integrations → provisioning (user management), CRM/marketing, analytics/insights.

## Assets to Assemble (MVP)
- Embedded PBI report URL (Pro for MVP; consider Embedded/Fabric for scale).
- Office Script GIF (10–20s, <5MB).
- Resume highlights (condensed block + link).
- Short link generator (Bitly/Rebrandly or simple custom redirect service).
- GA4 property + UTM scheme; Cosmos event logging (server‑side).
- Google Business Calendar link/booking.

## Tech Choices → Notes
- PBI Embedding
  - MVP → Pro sharing or secure link; avoid "Publish to web".
  - Scale → Embedded (A SKUs) or Fabric capacity; confirm budget.
- AI/RAG
  - Authoring → Azure OpenAI GPT‑4.1/4o; drafts → GPT‑4o‑mini.
  - Vector store → Cosmos DB vector search; HPK `tenantId:userId`.
- Tracking
  - Client → GA4 + UTM.
  - Server → minimal event capture (clicks, page views, CTA conversions) into Cosmos with diagnostics.

## Next Iterations → Extensions
- Testimonials/metrics → 3 punchy stats.
- Video demo → 5–10 minutes of dashboard walkthrough.
- Intake automation → secure file upload; pre‑classification.

## Regional & Channel Strategy
- Asheville‑first → local events + referrals.
- Online LinkedIn → DMs with tracked short links → book calls.
