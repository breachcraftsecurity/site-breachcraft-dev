# Azure AD Incident Response PowerShell Module

**Type:** PowerShell Module
**Purpose:** Azure AD incident response automation
**Platform:** Windows, PowerShell Core
**Tags:** #azure #incident-response #powershell #automation

---

## Purpose

Automates Azure AD IR tasks:
- Log collection
- User investigation
- Threat detection
- Remediation actions

---

## Installation

```powershell
# Install from PowerShell Gallery
Install-Module -Name AzureADIncidentResponse
```

---

## Common Functions

```powershell
# Collect logs
Get-AADIRSignInLogs
Get-AADIRAuditLogs

# User investigation
Invoke-AADIRUserInvestigation -UserPrincipalName user@company.com

# Risky sign-ins
Get-AADIRRiskySignIns

# Suspicious apps
Get-AADIRSuspiciousApps
```

---

## Pro Tips

💡 **IR Automation**: Streamlines incident response
💡 **Azure AD Specialized**: Entra ID focus
💡 **Quick Investigation**: Rapid user/app investigation

---

## Resources

- PowerShell Gallery: Search for Azure AD Incident Response
