# hawk

**Type:** PowerShell Module
**Purpose:** Microsoft 365 and Azure AD threat hunting
**Platform:** Windows, PowerShell Core
**Tags:** #threat-hunting #m365 #azure #forensics #incident-response

---

## Purpose

Hawk provides:
- Automated M365/Azure AD log collection
- Threat hunting capabilities
- Compromise detection
- Incident response automation

---

## Installation

```powershell
Install-Module -Name Hawk
```

---

## Quick Reference

```powershell
# Start investigation
Start-HawkTenantInvestigation

# User-specific investigation
Start-HawkUserInvestigation -UserPrincipalName user@company.com

# Mailbox investigation
Get-HawkUserMailboxAuditing -UserPrincipalName user@company.com
```

---

## Investigation Types

```powershell
# Full tenant investigation
Start-HawkTenantInvestigation

# User investigation
Start-HawkUserInvestigation -UserPrincipalName user@company.com

# Mailbox audit
Get-HawkUserMailboxAuditing -UserPrincipalName user@company.com

# Admin audit logs
Get-HawkTenantAdminAudit

# Investigate inbox rules
Get-HawkUserInboxRule -UserPrincipalName user@company.com
```

---

## Pro Tips

💡 **Automated Collection**: Gathers relevant logs automatically
💡 **Threat Hunting**: Identifies suspicious patterns
💡 **IR Focus**: Designed for incident response
💡 **Comprehensive**: Collects from multiple M365 sources

---

## Resources

- GitHub: https://github.com/T0pCyber/hawk
- PowerShell Gallery: https://www.powershellgallery.com/packages/Hawk
