**New rule** — `has_lifetime_retainer_attachment = TRUE` when the contract is:

1. `is_contract_start = TRUE`
2. `is_phase_1 = FALSE`
3. `addon_attachment_total_amount >= 300` (all governed add-on dollars, not just retainer-flagged ones)
4. carries at least one charge/transaction flagged `isretainerassurance = TRUE` (presence only, no dollar threshold on that subset)