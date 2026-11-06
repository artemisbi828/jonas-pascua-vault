# Terminology: Prime Names & Anti-Patterns

This table enforces semantic precision and reduces concept collisions. Use **Prime Name** in all documentation and notes. Measure types indicate aggregation logic.

| Prime Name | Anti-Patterns (Avoid) | Measure Type | Notes |
|---|---|---|---|
| **aggregate** | total, overall, combined, sum total | sum, count | Use "aggregate" for collections; avoid "total" before nouns (e.g., "total customer satisfaction" → "aggregate satisfaction score") |
| **margin (noun)** | margin % | ratio | Margin is % by definition; never say "margin percentage" |
| **margin (ratio)** | efficiency ratio, profitability % | ratio | Express as decimal (.34) or basis points; label context (Gross Margin, EBITDA Margin) |
| **collect, collection** | capture, gather, receipt | sum | Finances: money received. Notes: use "collect" not "capture" for cash transactions |
| **posting** | transaction, entry, record | unit | Specifically: payment received or journalized expense; not generic transaction |
| **posting (cash)** | cash receipt, payment received, cash in | sum | Subset of postings; money actually received/collected |
| **void** | cancel, reverse, nullify | unit | Specific to charge reversal; administrative action |
| **write-off** | forgiveness, loss, bad debt expense | unit | Charge recognized as uncollectible; accounting action |
| **bad debt** | write-off, loss, receivable loss | unit | Debt deemed uncollectible; triggers write-off |
| **add-back** | addback, add back, non-cash item, excluded expense | unit | Item removed from EBITDA (depreciation, amortization, stock comp) |
| **capex** | capital expenditure, PPE purchase, investment | sum | Capital expense; distinct from opex |
| **opex** | operating expense, SG&A, overhead | sum | Operating expense; distinct from capex |
| **overhead** | support, G&A, shared services, burden | sum | Indirect costs (not directly attributable to product/service) |
| **conversion (profit)** | profit translate, earnings generation | ratio | % of revenue → EBITDA; or % of growth → profit |
| **conversion (sales)** | close rate, win rate, acquisition rate | ratio | % of prospects → customers or % of traffic → purchases |
| **score** | rating, index, metric, KPI | ratio/point | Generic term; always specify type (NPS, CSAT, CES) |
| **satisfaction (aggregate)** | overall satisfaction, CSAT | ratio | Aggregate customer satisfaction; typically 1-5 scale or NPS proxy |
| **effort (customer)** | ease of use, usability, CES | ratio | How easy for customer to meet needs; 1-5 scale |
| **promoter (net)** | NPS, referral likelihood | ratio | Likelihood to refer; basis for Net Promoter Score |
| **charge** | fee, rate, amount, line item | unit | Specific: clinical charge or service charge billed |
| **adjustment** | correction, variance, delta | unit | Change to charge (write-off, void, discount); parent category |
| **revenue** | income, sales, top line | sum | Money earned from operations; before COGS |
| **cogs** | cost of goods sold, direct costs, product cost | sum | Direct variable costs tied to revenue generation |
| **gross profit** | contribution margin, margin dollars | sum | Revenue − COGS |
| **gross margin** | margin (revenue), contribution %, GP% | ratio | (Revenue − COGS) / Revenue |
| **ebitda** | operating profit, adjusted earnings, pre-tax | sum | Earnings Before Interest, Taxes, Depreciation, Amortization |
| **ebitda margin** | ebitda %, operating margin % | ratio | EBITDA / Revenue |
| **cost (labor)** | labor costs, payroll, personnel expense | sum | Wages, benefits, labor-related expenses |
| **cost (marketing)** | marketing expense, promotional spend, ads | sum | Direct marketing spend or 4-wall marketing |
| **cost (other)** | miscellaneous, other opex, unallocated | sum | Catch-all for non-labor, non-marketing opex |

---

## Framework Rules

- **Use Prime Names in:** All definitions, KPI descriptions, dashboard labels, data dictionaries, and note titles.
- **Flag Anti-Patterns in:** Automated scrub process; replace if mechanical, flag for manual review if context-dependent.
- **Measure Type:** Indicates default aggregation; override only with explicit justification.
- **Context Labels:** Always pair generic term with context (e.g., "Gross Margin" not just "margin").
