
```table-of-contents
```
# Governance Cheat Sheet
```
Need someone to VIEW reports?
    → Viewer

Need someone to BUILD reports?
    → Build Permission
      or Contributor

Need someone to MANAGE reports?
    → Member

Need workspace ownership?
    → Admin

Need to restrict DATA?
    → RLS

Need to restrict specific report audience?
    → Share/App Audience

Need page security?
    → Separate reports
````


# High Level
Tenant
└── Workspace
    ├── Reports
    ├── Dashboards
    ├── Semantic Models
    └── Dataflows

Access happens at multiple layers:

1. Workspace Role
2. Item Permission (Report / Semantic Model)
3. RLS / OLS Data Security

# Build Permission
Build Permission
│
├── Can create new reports
├── Can Analyze in Excel
├── Can export underlying data
└── Can connect directly to model

# Workspace Access

Admins        = Workspace owners
Members       = BI leads
Contributors  = Developers
Viewers       = Business users

Workspace
│
├── Admin
│   ├── Manage workspace
│   ├── Add/remove users
│   ├── Publish/edit/delete content
│   └── Full control
│
├── Member
│   ├── Publish/edit content
│   ├── Manage app
│   └── Nearly full control
│
├── Contributor
│   ├── Create reports
│   ├── Edit content
│   └── Cannot manage workspace
│
└── Viewer
    ├── View content
    └── Read only

# Semantic Model Access
Build access for XLS. Modify semantic model is **not recommended.**
![300]

✅ Modify semantic model settings
✅ Republish model
✅ Refresh model
✅ Make XMLA changes
✅ Edit model

❌ Grant access to others
❌ Explicitly build new reports from this model
❌ Analyze in Excel
❌ XMLA read access via Build permission

Semantic Model
│
├── Read
│   └── Consume reports
│
├── Build
│   ├── Create reports
│   ├── Analyze in Excel
│   ├── Export underlying data
│   └── Connect via XMLA
│
├── Reshare
│   └── Grant permissions to others
│
└── Write
    ├── Modify model
    └── Refresh/republish




## Power BI UI - App ^PBI-Access-1

## Power BI Datasets ^PBI-Access-2

## Power BI Row Level Restriction ^PBI-Access-3
### Direct Offices Only
### +1 Provisioning


