# FindMeAccess

**Type:** PowerShell Module
**Purpose:** Find accessible resources and permissions in Azure/M365
**Platform:** Windows, PowerShell Core
**Tags:** #azure #permissions #enumeration #access-discovery

---

## Purpose

Discovers:
- Accessible Azure resources
- M365 permissions
- What you can access/modify
- Privilege mapping

---

## Usage

```powershell
# Import and run
Import-Module FindMeAccess
Invoke-FindMeAccess

# Discovers:
# - Accessible subscriptions
# - Resources you can modify
# - Assigned roles
# - Permission scope
```

---

## Pro Tips

💡 **Permission Discovery**: Maps your actual access
💡 **Post-Compromise**: Understand compromised account scope
💡 **Lateral Movement**: Identifies pivot opportunities

---

## Resources

- Search PowerShell Gallery for FindMeAccess
