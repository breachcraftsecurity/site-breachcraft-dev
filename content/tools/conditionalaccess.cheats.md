# ConditionalAccess

**Type:** PowerShell Scripts/Tools
**Purpose:** Azure AD Conditional Access policy management and analysis
**Platform:** Windows, PowerShell Core
**Tags:** #azure #conditional-access #policies #security #analysis

---

## Purpose

Tools for:
- CA policy enumeration
- Policy analysis
- Gap identification
- Configuration review

---

## Common Operations

```powershell
# List all CA policies
Get-AzureADMSConditionalAccessPolicy

# Get specific policy
Get-AzureADMSConditionalAccessPolicy -PolicyId <policy-id>

# Export policies
Get-AzureADMSConditionalAccessPolicy | ConvertTo-Json | Out-File policies.json
```

---

## Analysis

Review policies for:
- MFA enforcement
- Device compliance requirements
- Location-based rules
- Application assignments
- Exclusions (potential gaps)

---

## Pro Tips

💡 **Gap Analysis**: Look for excluded users/apps
💡 **Legacy Auth**: Ensure legacy protocols blocked
💡 **MFA Coverage**: Verify MFA enforcement
💡 **Device Trust**: Check device compliance requirements

---

## Resources

- Azure AD PowerShell Module
- Microsoft Graph PowerShell
