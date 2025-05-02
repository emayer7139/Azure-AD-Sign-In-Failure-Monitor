<#
  File: C:\Scripts\AuthFailuresCheck.ps1
  Purpose:
    • Headless monitor for Azure AD sign-in failures (non-desktop)
    • Logs users with ≥10 failures in the last 24 h to a CSV
    • Pops a BurntToast “View Log” notification
#>

# 1) Ensure PS 7+
if ($PSVersionTable.PSVersion.Major -lt 7) {
    Throw "Please run under PowerShell 7+ (pwsh.exe)."
}

# 2) CSV log path
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$csvLog    = Join-Path $scriptDir 'AuthFailureLog.csv'
if (-not (Test-Path $csvLog)) {
    "Timestamp,UserPrincipalName,Failures" | Out-File $csvLog -Encoding UTF8
}

# 3) Your Azure AD app credentials
$TenantId     = 
$ClientId     = 
$ClientSecret = 

# 4) Get an OAuth2 token via client-credentials
$tokenEndpoint = "https://login.microsoftonline.com/$TenantId/oauth2/v2.0/token"
$tokenBody = @{
    client_id     = $ClientId
    scope         = 'https://graph.microsoft.com/.default'
    client_secret = $ClientSecret
    grant_type    = 'client_credentials'
}
$tokenResp = Invoke-RestMethod -Method Post -Uri $tokenEndpoint -Body $tokenBody
if (-not $tokenResp.access_token) { Throw "Token request failed: $($tokenResp | Out-String)" }
$token = $tokenResp.access_token

# 5) Prepare your query
$Threshold = 10
$since     = (Get-Date).AddHours(-24).ToString('o')
$odataFilter = [Uri]::EscapeDataString("createdDateTime ge $since and appDisplayName ne 'Windows'")
$uri = "https://graph.microsoft.com/v1.0/auditLogs/signIns?`$filter=$odataFilter&`$top=1000"

# 6) Call Graph via REST
$headers = @{ Authorization = "Bearer $token" }
$resp    = Invoke-RestMethod -Method Get -Uri $uri -Headers $headers
if (-not $resp.value) { Write-Host "No data returned."; exit }
$raw     = $resp.value

# 7) Filter failures & group
$failures = $raw | Where-Object { $_.status.errorCode -ne 0 }
$groups   = $failures |
    Group-Object userPrincipalName |
    Where-Object Count -ge $Threshold

# 8) If any offenders, log and toast
if ($groups) {
    $ts = (Get-Date).ToString('s')
    foreach ($g in $groups) {
        "$ts,$($g.Name),$($g.Count)" | Out-File $csvLog -Append -Encoding UTF8
    }

    if (-not (Get-Module BurntToast -ListAvailable)) {
        Install-Module BurntToast -Scope CurrentUser -Force
    }
    Import-Module BurntToast

    $bodyText = (
      $groups |
        ForEach-Object { "$($_.Name): $($_.Count) failures" }
    ) -join "`n"

    $uriView = 'file:///' + ($csvLog -replace '\\','/')
    $btn     = New-BTButton -Content "View Log" -Arguments $uriView -ActivationType Protocol

    New-BurntToastNotification `
      -Text "Azure AD Sign-In Alert", "Users ≥ $Threshold failures:`n$body" `
      -Button $btn
}

Write-Host "✅ AuthFailuresCheck completed at $(Get-Date)" -ForegroundColor Green
