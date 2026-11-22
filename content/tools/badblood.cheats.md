# BadBlood

**Type:** PowerShell Script
**Purpose:** Populate Active Directory with test data
**Platform:** Windows
**Tags:** #active-directory #testing #lab #bloodhound #red-team-lab

---

## Purpose

Creates realistic AD environment with:
- Thousands of users
- Hundreds of groups
- Complex ACLs
- Nested groups
- Service accounts
- Kerberoastable users
- AS-REP roastable users
- Intentional vulnerabilities

---

## Usage

```powershell
# Run on Domain Controller
Invoke-BadBlood

# Populates AD with test data
# Use for:
# - BloodHound testing
# - Tool development
# - Red team training
# - Detection engineering
```

---

## Pro Tips

💡 **Lab Environment**: ONLY use in test domains
💡 **BloodHound Training**: Great for learning attack paths
💡 **Realistic**: Creates realistic misconfigurations
💡 **Detection Testing**: Test SIEM/EDR detection capabilities

---

## Resources

- GitHub: https://github.com/davidprowe/BadBlood
- Author: @davidprowe (David Rowe)
