Editorial Refactoring
Content Polishing / Content Cleanup

# Sample Documentation
Your strategy mentions "Docling or Marker" for MD conversion
Should I: (a) Use only Docling, (b) Use only Marker, or (c) Implement both with fallback logic?
Recommendation for MVP: Start with Docling only (simpler, faster time-to-value)
3. Schema Mismatch in Example Table

Your example table shows 7 columns but schema lists 6 fields
The first two columns both appear to be "id" values
Clarification needed: Should I:
(a) Ignore the first column (treating it as a row number for reference only)
(b) Use only one id column from the actual PDF data
4. Handling Empty Fields (Rows 150-152)

---
### 🔍 **Troubleshooting Preview**

If you see: `ModuleNotFoundError: No module named 'docling'`  
→ Ensure venv activated: [Activate.ps1](vscode-file://vscode-app/c:/Users/jonas-adam.pascua/AppData/Local/Programs/Microsoft%20VS%20Code/ce099c1ed2/resources/app/out/vs/code/electron-browser/workbench/workbench.html)

If you see: `ImportError: DLL load failed` (Windows)  
→ Install [Visual C++ Redistributable]

---
# Tool Summary

- **The Problem it Solves:** traditionally, web pages only update when you refresh them (HTTP requests). If you want a live chat, you don't want to hit "refresh" every second to see new messages.
    
- **The Solution:** SignalR creates a persistent connection between the client (browser) and the server. This allows the server to **push** content to clients instantly as it happens.
    
- **How it works:** It uses "WebSockets" under the hood (the gold standard for real-time), but if WebSockets aren't available (e.g., on an old browser), it automatically falls back to older techniques like "Long Polling" so the app still works.

---

# Debugging
```
Symptom: You installed Streamlit (pip install streamlit), but typing streamlit run resulted in command not found.

Cause: pip installed the executable into a hidden folder (~/.local/bin) that wasn't in your system's "address book" (the $PATH variable). Linux didn't know where to look.

The Fix (Workaround): We used python3 -m streamlit. This tells Python to find the module itself, bypassing the system PATH lookup.
```

```
Symptom: You had the server running, but couldn't connect via the browser (http://IP:8501).

Cause: Public Wi-Fi (like at ATL airport) creates a "Firewall Sandwich":

1. **Google Firewall:** We opened this correctly using `gcloud compute firewall-rules`.
2. Airport Firewall: This was likely blocking outgoing traffic on "weird" ports like 8501. It usually only permits Port 80 (Web) and 443 (SSL).

    Solution: Wait for a non-restricted network (Home/Cellular) or use a standard port (requires sudo privileges).
```

```
Symptom: Constraint constraints/compute.vmExternalIpAccess violated.

Cause: Google Cloud protects new projects by forbidding Public IPs to prevent accidental exposure.

Fix: We created a policy.yaml file to explicitly override this rule and applied it via gcloud resource-manager.
```

# Tickets
Extracted from freshbooks
```
**Root Cause:**
The referral detail report for R27 does not populate any data due to the absence of pre-conversion data in the dashboard and the specific dashboard start dates for the offices.

**Actions Taken:**
The agent advised to remove any filters and explained the limitations on Cloud9, including the logic based on the most recent referral edit on record. The agent also clarified that no pre-conversion data is included in the dashboard and provided examples of dashboard start dates to illustrate the issue.

**Resolution:**
The requester acknowledged the explanation and mentioned that the issue might be related to the PAN form in Dayforce for the new region. The ticket was closed with the option to reopen if needed.
```