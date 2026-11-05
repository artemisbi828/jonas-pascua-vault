Sourced from Angela's notes for describing cc9 vs ofi net_contract_amount (semantic-collision, semantic-falsity)

```
_contract_field_net_contract_amount

Single-measure contract attribute: net_contract_amount (DOUBLE).

Net is NOT a uniform gross - discount across both systems, so it is modeled per source (ref: "Contracts: Gross Amount, Net Amount") 
- CentralC9: tfpfee - SUM(tfpddiscount) (active TFPs only)

Gross fee (silver_centralc9_treatmentfeeplan.tfpfee) minus the sum of
contract-level discounts from silver_centralc9_treatmentfeeplandiscount
(summed per tfpguid). This equals gross - discount for C9.

OrthoFi: production
silver_orthofi_contracts.production is already the net contract fee as
OrthoFi presents it (post internal adjustments). Discounts are NOT
deducted here, so net != gross - discount for OrthoFi.
```