# Sparrow

**Type:** PowerShell Module
**Purpose:** Microsoft 365 and Azure compromise detection
**Platform:** Windows, PowerShell Core
**Tags:** #forensics #incident-response #m365 #azure #detection #blue-team

---

## Purpose

Sparrow helps detect:
- APT compromise indicators
- Suspicious OAuth applications
- Mailbox persistence
- Azure AD abuse
- M365 tenant compromise

Developed by CISA for incident response

---

## Installation

```powershell
Install-Module -Name Sparrow
```

---

## Quick Reference

```powershell
# Run all checks
Invoke-Sparrow

# Specific checks
Get-SparrowMailboxAuditLog
Get-SparrowMailboxRule
Get-SparrowOAuthApp
```

---

## Detection Modules

```powershell
# Check for suspicious OAuth apps
Get-SparrowOAuthApp

# Check mailbox rules
Get-SparrowMailboxRule

# Check unified audit log
Get-SparrowMailboxAuditLog

# Check Azure AD sign-ins
Get-SparrowAzureADSignInLogs
```

---

## Pro Tips

💡 **IR Tool**: Designed for incident response
💡 **CISA Developed**: Government-backed detection tool
💡 **APT Focus**: Targets nation-state TTPs
💡 **Comprehensive**: Checks multiple compromise vectors

---

## Resources

- GitHub: https://github.com/cisagov/Sparrow
- Organization: CISA (Cybersecurity and Infrastructure Security Agency)
