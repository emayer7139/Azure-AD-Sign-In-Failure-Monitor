# AuthFailuresCheck

A headless PowerShell script to monitor and alert on Azure AD sign-in failures (e.g. brute-force Azure CLI attacks), log offenders to CSV, and pop a desktop notification via BurntToast.

---

## 🛡️ Why This Matters

Over the past weeks, our organization has seen a large number of automated Azure CLI authentication attempts—likely brute-force or spray attacks—targeting our Azure AD tenants. Left unchecked, these failures can indicate compromised credentials or vulnerability scans that precede a real breach.

**AuthFailuresCheck** helps you:

- **Detect** high-volume sign-in failures (configurable threshold)
- **Log** offending user principal names (UPNs) and failure counts
- **Notify** admins immediately with a BurntToast popup

---

## 🚀 Features

- **OAuth2 Client-Credentials** against Microsoft Graph
- **24-hour sliding window** of sign-in data
- **Configurable threshold** (default: 10 failures)
- **CSV audit log** (`AuthFailureLog.csv`)
- **BurntToast** push notifications to Windows 10/11 desktops

---

## 🧩 Requirements

- **PowerShell 7+** (`pwsh.exe`)
- An **Azure AD App Registration** with:
  - **Application (client) ID**  
  - **Directory (tenant) ID**  
  - **Client secret**  
  - API permission: **AuditLog.Read.All** (granted/admin-consented)
- **BurntToast** PowerShell module (auto-installed at first run)

---

## ⚙️ Installation
   **Clone the repo**  
   ```bash
   git clone https://github.com/your-org/AuthFailuresCheck.git
   cd AuthFailuresCheck
  ```

## ⏰ Scheduling
To get continuous monitoring, schedule via Task Scheduler:

**Action**
  Program/script: pwsh.exe
  Arguments: -NoProfile -ExecutionPolicy Bypass -File "C:\path\AuthFailuresCheck.ps1"

**Trigger**
  e.g. Every hour, or At startup

## 🔍 How It Helps Monitor Azure CLI Brute-Force Attempts
Azure CLI uses modern auth: each failure is logged under Microsoft Graph sign-in audit logs.
AuthFailuresCheck queries those logs for non-interactive failures (appDisplayName ne 'Windows'), so it captures Azure CLI, PowerShell Az module, REST-API calls, etc.
By grouping failures per UPN and applying a failure threshold, you get early warning of potential credential-guessing attacks—without manually scrolling through hundreds of sign-in events.
