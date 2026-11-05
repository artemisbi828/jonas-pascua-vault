# Finance & Business Concepts Reference

Authoritative definitions using **prime names** (see `terminology-prime-names.md` for naming conventions). All definitions are succinct, action-oriented where applicable, and distinct (no semantic overlap).

---

## Charges & Adjustments

**charge**
- A service or product amount billed to a customer or payer; the initial transaction amount before adjustments.

**adjustment**
- Any change to a charge after initial posting. Parent category for: void, write-off, bad debt, discount, or correction.

**posting (cash)**
- Money actually received or collected; subset of adjustments. Distinct from charge (which may not be collected).

**void**
- Administrative reversal of a charge with no financial recourse; charge effectively never happened.

**write-off**
- Accounting action to remove an uncollectible charge from receivables; recognized as loss.

**bad debt**
- Charge deemed uncollectible, triggering write-off; represents credit risk materialized.

---

## Revenue & Profitability (Core P&L)

[[Revenue|revenue]]
- Money earned from core operations (e.g., patient fees, service billings); starting point of P&L.
- Measure Type: Sum
- Formula: Aggregate of all charges collected or earned in period.

**cogs** (Cost of Goods Sold)
- Direct, variable costs tied to revenue generation (e.g., clinical supplies, variable labor tied to volume).
- Measure Type: Sum
- Excludes overhead and fixed costs.

**gross profit**
- Operating contribution before indirect costs and overhead.
- Measure Type: Sum
- Formula: Revenue − COGS

**gross margin**
- Proportion of each revenue dollar remaining after direct costs.
- Measure Type: Ratio
- Formula: (Revenue − COGS) / Revenue
- Context: Tracks pricing power and production efficiency.

---

## Operating Expenses

**cost (labor)**
- Wages, salaries, benefits, and labor-related taxes/insurance for personnel.
- Measure Type: Sum
- Includes full-time, part-time, and contract labor.

**cost (marketing)**
- Direct marketing and promotional spend (e.g., 4-wall marketing, digital ads, patient acquisition).
- Measure Type: Sum
- Excludes overhead allocated to sales functions.

**cost (other)**
- All other operating costs not classified as labor or marketing (e.g., utilities, supplies, IT, facilities).
- Measure Type: Sum

**overhead** (or **G&A**, **support costs**)
- Indirect costs not directly attributable to patient care or product delivery (e.g., administration, finance, HR, IT shared services).
- Measure Type: Sum
- Enables operations but doesn't scale linearly with revenue.

---

## EBITDA & Margins

**ebitda**
- Earnings Before Interest, Taxes, Depreciation, Amortization; core operating profitability.
- Measure Type: Sum
- Formula: Gross Profit − Labor Costs − Marketing Costs − Other Opex
- Context: Isolates operational performance from financing and accounting choices.

**ebitda margin**
- Proportion of revenue converted to operating profit before capital structure effects.
- Measure Type: Ratio
- Formula: EBITDA / Revenue
- Context: Benchmarks operational efficiency; higher is better, comparable across businesses.

**addback**
- Non-cash item restored to EBITDA for normalization (e.g., depreciation, amortization, stock-based compensation).
- Measure Type: Unit
- Rationale: Excludes non-recurring or non-cash charges to reveal sustainable earnings.

**capex** (Capital Expenditure)
- Spending on long-lived assets (equipment, facilities, systems); expensed via depreciation over time.
- Measure Type: Sum
- Distinct from opex; creates balance sheet asset.

---

## Profit Drivers & Efficiency

**conversion (profit)**
- Proportion of revenue flowing to operating profit; efficiency of cost control.
- Measure Type: Ratio
- Formula: EBITDA / Revenue (same as EBITDA Margin)
- Context: Leadership indicator — confirms growth is profitable, not just top-line scale.

**conversion (sales)**
- Proportion of prospects, traffic, or leads becoming customers.
- Measure Type: Ratio
- Formula: Customers Acquired / Prospects or Traffic / Purchases
- Context: Marketing efficiency; higher is better for customer acquisition cost.

---

## Customer Metrics

**satisfaction (aggregate)** or **CSAT**
- Overall rating of customer satisfaction with experience; typically 1–5 scale or 0–100 index.
- Measure Type: Ratio (average rating)
- Collection: "How would you rate your overall experience?" or similar.
- Context: Operational execution; directly tied to retention and referral.

**effort (customer)** or **CES**
- Ease with which customer met their needs or navigated service/tools.
- Measure Type: Ratio (average ease score, 1–5 scale)
- Collection: "How easy was it to meet your needs?" or similar.
- Context: Identifies friction points; high effort → churn risk.

**promoter (net)** or **NPS**
- Likelihood customer will recommend to others; proxy for loyalty and satisfaction.
- Measure Type: Ratio (0–100 scale; % detractors subtracted from % promoters)
- Collection: "How likely are you to refer us?" (0–10 scale, then bucketed).
- Context: Leading indicator of organic growth and brand health.

---

## Concept Cross-Reference (Prime Names Master List)

For consistency checks and automated scrub processes:

**All Prime Names Used in This Document:**
aggregate, margin, collection, posting, void, write-off, bad debt, addback, capex, opex, overhead, conversion, score, satisfaction, effort, promoter, charge, adjustment, revenue, cogs, gross profit, cost (labor), cost (marketing), cost (other), ebitda, ebitda margin

**Status:** Last updated 2026-07-15. All names must appear in both this document and `terminology-prime-names.md`.
