```
git add -A
git commit -m "Global: PROD004 → UAT003 (prefer PROD on conflicts)"
```

Template
```
fix(infra): wire Key Vault RBAC scope and align KV module with CI and naming constraints

* wire key_vault_id into azure_rbac in dev so ADF can receive Key Vault Secrets User role scope
* add dev Key Vault name override key_vault_name = kv-sd-data-svc-${var.environment} to stay under Azure 24-char KV name limit
* update Key Vault resource name logic to use coalesce(key_vault_name, kv-prefix−prefix−{environment})
* add Checkov skip CKV2_AZURE_32 with explicit rationale until private endpoint story is implemented
* make tags required in azure_key_vault module by removing default {} to avoid accidental untagged resources
* add key_vault_name variable to azure_key_vault module with nullable default for backward-compatible override behavior
* remove lifecycle prevent_destroy from Key Vault resource definition
* update dev Terraform lockfile hash set for azurerm provider
```