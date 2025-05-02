# Azure-AD-Sign-In-Failure-Monitor
A simple PowerShell script to watch for Azure AD sign‑in failures—especially brute‑force attempts against the Azure CLI—log offenders to a CSV, and send desktop notifications via BurntToast.
Background

Over the past weeks, our organization has seen a sharp rise in automated brute‑force attempts targeting the Azure CLI. Attackers are hammering account credentials to gain directory access. Early detection and rapid response are critical to limit risk and prevent account lockouts or unauthorized access.

This tool helps you:

Continuously monitor Azure AD sign‑in logs via Microsoft Graph

Alert when any user has ≥ 10 failures in the last 24 hours

Log offending users and counts to AuthFailureLog.csv

Notify on your desktop with a direct “View Log” button

Features

Headless monitoring: Run in PowerShell 7+ without user interaction

OAuth2 client‑credentials flow: Securely authenticate to Microsoft Graph

Configurable threshold: Default is 10 failures per 24h

CSV logging: Append Timestamp, UserPrincipalName, FailureCount

BurntToast notifications: Instant pop‑ups with a link to view the log

Prerequisites

PowerShell 7+: Ensure pwsh.exe is installed and in PATH

Azure AD App Registration:

Application (client) type with Client Credentials

API permission: AuditLog.Read.All (Application)

Grant admin consent

BurntToast module: The script will auto‑install if missing

Windows 10/11 for desktop notifications

Installation

Clone the repo

git clone https://github.com/your-org/azure-ad-auth-monitor.git

Change to the script directory

cd azure-ad-auth-monitor

Configuration

1) Secure your credentials

Store your Azure AD credentials in environment variables (recommended):

$env:AZ_TENANT_ID     = 'your-tenant-id'
$env:AZ_CLIENT_ID     = 'your-client-id'
$env:AZ_CLIENT_SECRET = 'your-client-secret'

Tip: Use Azure Key Vault or a secrets manager to inject these at runtime.

2) (Optional) Customize thresholds & paths

Threshold: Edit the $Threshold variable in AuthFailuresCheck.ps1 to change the failure count trigger.

Log location: Adjust $csvLog to point to a different file or folder.

Usage

Run the script manually or via a scheduler:

pwsh.exe -NoProfile -ExecutionPolicy Bypass -File AuthFailuresCheck.ps1

What happens:

Queries Graph for sign‑ins in the last 24 h

Filters out successful attempts

Groups by userPrincipalName and checks if count ≥ Threshold

Appends offenders to AuthFailureLog.csv

Fires a BurntToast notification with a “View Log” button

Scheduling via Task Scheduler

Open Task Scheduler and select Create Task.

General: Run whether user is logged on or not; configure for Windows 10/11.

Triggers:

New → Begin the task: On a schedule

Daily; Recur every 1 day

Advanced → Repeat task every 1 hour for a duration of 24 hours

Actions:

New → Action: Start a program

Program/script: pwsh.exe

Add arguments: -NoProfile -ExecutionPolicy Bypass -File "C:\Scripts\AuthFailuresCheck.ps1"

OK to save. Ensure the account has “Log on as a batch job” rights.

