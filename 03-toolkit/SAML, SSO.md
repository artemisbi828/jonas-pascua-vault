**SAML = Security Assertion Markup Language.** In Datadog, it enables **Single Sign-On (SSO)** using your organization's identity provider, such as Microsoft Entra ID, Okta, or Active Directory.

```
You
 │
 ▼
Datadog
 │
 │ "I don't authenticate Jonas myself.
 │  Go prove who you are to your company."
 ▼
Company Identity Provider
(Microsoft Entra ID / Okta / etc.)
 │
 │  password + MFA, if required
 ▼
SAML assertion
"I verified this is Jonas."
 │
 ▼
Datadog
 │
 ▼
✅ Logged in

---
SAML:
Datadog trusts your company's identity system
        ↓
Company vouches for you
        ↓
Datadog lets you in
```

The important distinction:

|Thing|Role|
|---|---|
|**Datadog**|Service Provider (SP), the app you're trying to use|
|**Your company login system**|Identity Provider (IdP), proves who you are|
|**SAML**|The standardized way the IdP tells Datadog "yes, this person is authenticated"|
|**SSO**|The overall experience of using your organizational identity across apps|

Datadog specifically says that when SAML authentication occurs, the identity provider sends Datadog a **SAML Assertion containing the user's authorization**. [[docs.datadoghq.com]](https://docs.datadoghq.com/account_management/saml/)

Given your recent work with SSH keys/passkeys, there's a useful conceptual parallel: