related-to: [[GIT]]
```
jpascua@gmail.com --> slidesms.com
jonas.pascua@artemis-bi.com (via google-account\jonas.pascua@artemisbi.com) --> artemisbi.com
```


- **Domain Ownership (Registrar):** Continue buying domains through a registrar (like Cloudflare, Namecheap, or Google). It is best practice to keep your domain registrar separate from your cloud infrastructure provider to prevent "vendor lock-in."
    
- **DNS & Security (Cloudflare):** Point your domain's nameservers to Cloudflare. Even if you use Firebase for hosting, Cloudflare acts as an excellent "shield" in front of your origin server. It handles WAF (Web Application Firewall), DDoS protection, and cache rules that are often more granular than what is available natively in Firebase.
    
- **Hosting (Firebase):** Build your site and deploy it to Firebase Hosting. Because Firebase handles the SSL certificate lifecycle automatically, you don't have to manually manage certs.
    
- **The "Integration":** Once the domain is pointed to Cloudflare, you simply add that custom domain in the Firebase Console. Firebase will provide you with a few TXT/CNAME records to add to Cloudflare, proving you own the domain. Once verified, the connection is permanent.

The One Big Fix: Proxy Status
Your instructions explicitly state to set the Proxy to DNS only (gray cloud).

Current State: In your screenshot, the toggle is orange (Proxied).

Action Needed: Click that toggle so it becomes gray. When Cloudflare is "Proxied," it masks your IP and uses its own SSL certificates. Since your instructions mention handling SSL separately (likely on your Google VM), keeping it orange could cause a "Redirect Loop" or SSL mismatch error.


---
Moving a domain between two Cloudflare accounts can be a bit of a "hoop-jumping" exercise because Cloudflare separates the **DNS/Zone settings** from the **Domain Registration (Registrar)**.

Since you bought the domain directly through Cloudflare, here is the most efficient way to handle this in 2026.

### The Two-Part Transfer Process

#### 1. Move the Website/DNS (The "Zone")

This part is relatively quick and ensures your site stays live.

* **Export DNS:** In your current account, go to **DNS** > **Records** > **Export** to download your BIND file.
* **Add Site to New Account:** Log in to your second account and click **Add a Site**. Use the "Free" or same plan level.
* **Import DNS:** Upload the file you just exported so your Firebase/Cloud Run records are preserved.
* **Update Nameservers:** Cloudflare will give the new account a different set of nameservers (e.g., `emma.ns.cloudflare.com` and `oliver.ns.cloudflare.com`).
* *Crucial Note:* Because Cloudflare is your registrar, you must update these nameservers under the **Domain Registration** > **Manage Domains** section of the *original* account to point to the *new* account’s nameservers.



#### 2. Move the Domain Registration (The "Registrar")

Moving the "billing and ownership" of the registration itself is now supported natively without needing to leave Cloudflare.

* **Verify Requirements:** Ensure the domain hasn't been registered or transferred in the last **60 days** (ICANN rule).
* **Initiate Move:** In the source account, go to **Domain Registration** > **Manage Domains** > **Configuration** and look for **Move to another Cloudflare account**.
* **Account ID:** You will need the **Account ID** of your new account (found on the right sidebar of the new account's dashboard).
* **Accept the Move:** You will receive an email in the new account’s inbox. Follow the link to accept the transfer.

---

### Important "Gotchas" to Watch Out For

* **DNSSEC:** If you have DNSSEC enabled, **disable it** in the old account and wait about 12-24 hours before moving. Leaving it on during a transfer is the #1 cause of "site not found" errors.
* **Page Rules/WAF:** These do **not** export with DNS. If you have custom redirect rules or security firewall rules, you’ll need to manually recreate them in the new account.
* **Wait Period:** Once you move the *registration*, the domain will be locked for another 30–60 days for any further transfers.

**Would you like me to find your Account ID for the new account so you have it ready for the transfer?**


# Secret
jonas_pascua_artemis_bi_com@antigravity-box:~$ ssh-keygen -t ed25519 -C "jonas_pascua_artemis_bi_com" -f ~/.ssh/id_ed25519 -N ""
Generating public/private ed25519 key pair.
Your identification has been saved in /home/jonas_pascua_artemis_bi_com/.ssh/id_ed25519
Your public key has been saved in /home/jonas_pascua_artemis_bi_com/.ssh/id_ed25519.pub
The key fingerprint is:
SHA256:zdo16gmSt+alYrm/YSmxGFfDPe+q7vMYIplCxZ4X0BQ jonas_pascua_artemis_bi_com
The key's randomart image is:
+--[ED25519 256]--+
|    .oE.         |
|   . ... .       |
|    o . + o      |
|   o . o + o     |
|  . + + S o +    |
| .   B + + + .   |
|  . = *.O + .    |
|   . .+*oX o     |
|     ..O@==      |
+----[SHA256]-----+
jonas_pascua_artemis_bi_com@antigravity-box:~$ 