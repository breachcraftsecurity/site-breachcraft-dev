# Mandiant Azure AD Investigator

**Type:** PowerShell Module
**Purpose:** Azure AD incident response and investigation
**Platform:** Windows, PowerShell Core
**Tags:** #azure #incident-response #forensics #investigation #mandiant

---

## Purpose

Mandiant Azure AD Investigator helps:
- Investigate Azure AD compromises
- Collect relevant logs and data
- Identify suspicious activities
- Support incident response

Developed by Mandiant (Google Cloud)

---

## Installation

```powershell
Install-Module -Name Mandiant-Azure-AD-Investigator
```

---

## Investigation Functions

```powershell
# Collect Azure AD logs
Get-AzureADAuditLogs
Get-AzureADSignInLogs

# User investigation
Get-AzureADUserInvestigation -UserPrincipalName user@company.com

# App investigation
Get-AzureADAppInvestigation

# Role investigation
Get-AzureADRoleInvestigation
```

---

## Pro Tips

💡 **Mandiant Tool**: From leading IR firm
💡 **Azure AD Focus**: Specialized for EntraID investigation
💡 **Incident Response**: Designed for compromise investigations
💡 **Comprehensive**: Collects multiple log sources

---

## Resources

- PowerShell Gallery: Search for Mandiant-Azure-AD-Investigator
- Company: Mandiant (Google Cloud)
