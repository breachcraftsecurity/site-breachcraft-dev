# ScubaGear

**Type:** PowerShell Module
**Purpose:** Microsoft 365 security configuration assessment
**Platform:** Windows, PowerShell Core
**Tags:** #m365 #security-assessment #cisa #compliance #configuration-review

---

## Purpose

ScubaGear assesses M365 security:
- Compliance with CISA baselines
- Security configuration review
- Best practice validation
- Gap analysis

Developed by CISA

---

## Installation

```powershell
Install-Module -Name ScubaGear
```

---

## Assessment

```powershell
# Run full assessment
Invoke-SCuBA

# Generates HTML report with:
# - Configuration findings
# - Compliance status
# - Remediation guidance
```

---

## What It Checks

- Azure AD / Entra ID settings
- Exchange Online configuration
- SharePoint settings
- Teams security
- OneDrive configurations
- Defender settings

Compares against CISA security baselines

---

## Pro Tips

💡 **CISA Baselines**: Official government recommendations
💡 **Comprehensive**: Checks multiple M365 services
💡 **HTML Report**: Easy-to-read assessment output
💡 **Compliance**: Helps meet security standards

---

## Resources

- GitHub: https://github.com/cisagov/ScubaGear
- Organization: CISA
