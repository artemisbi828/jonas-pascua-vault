Subscription = Billing
- Resource Group = Cluster
	- Resource = Solution

---
```
Azure (Global Cloud)
└─ Tenant (Entra ID / Azure AD)
   └─ Management Group (optional roll‑up layer)
      └─ Subscription
         ├─ Resource Group
         │  ├─ Resource (VM)
         │  ├─ Resource (Storage Account)
         │  └─ Resource (SQL Database)
         ├─ Resource Group
         │  ├─ Resource (App Service)
         │  └─ Resource (Key Vault)
         └─ Resource Group
            └─ Resource (Any Azure service)
```

### TLDR mental model

- **Tenant** = security & identity boundary
- **Management Group** = policy / governance rollup _across subscriptions_
- **Subscription** = billing + quota boundary
- **Resource Group** = lifecycle + deployment boundary
- **Resource** = the actual thing (VM, DB, etc.)

### One‑line roll‑up rule

```
Resources → Resource Groups → Subscription → (Management Groups) → Tenant
```

### Key constraints (important)

- A **resource belongs to exactly one resource group**
- A **resource group belongs to exactly one subscription**
- A **subscription belongs to exactly one tenant**
- Management Groups are **optional** but common in enterprise setups

If you want, I can:

- Strip this down to **only** Subscription → Resource Group
- Add **RBAC / policy inheritance** annotations
- Create a **“what scopes apply where”** ASCII overlay (RBAC, Policy, Cost)