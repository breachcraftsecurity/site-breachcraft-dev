# SharpHound

**Type:** C# / PowerShell Data Collector
**Purpose:** Active Directory data collection for BloodHound
**Platform:** Windows
**Tags:** #active-directory #enumeration #bloodhound #data-collection

---

## Installation

```powershell
# Download from BloodHound releases
# https://github.com/BloodHoundAD/BloodHound/releases

# Or compile from source
# https://github.com/BloodHoundAD/SharpHound
```

---

## Quick Reference

```powershell
# Collect all data
.\SharpHound.exe -c All

# Stealth collection
.\SharpHound.exe -c DCOnly

# PowerShell version
Import-Module .\SharpHound.ps1
Invoke-BloodHound -CollectionMethod All
```

---

## Collection Methods

```powershell
# All (recommended)
.\SharpHound.exe -c All

# Domain Controller only (stealthier)
.\SharpHound.exe -c DCOnly

# Specific methods
.\SharpHound.exe -c Session,LoggedOn
.\SharpHound.exe -c Group,LocalAdmin,Session
.\SharpHound.exe -c ACL,ObjectProps
.\SharpHound.exe -c Container,GPOLocalGroup

# No session collection (quieter)
.\SharpHound.exe -c All --ExcludeDCs
```

---

## Output

```powershell
# Default output
# Creates ZIP file: 20240101120000_BloodHound.zip

# Custom output
.\SharpHound.exe -c All --OutputDirectory C:\Temp\
.\SharpHound.exe -c All --OutputPrefix Company

# Import into BloodHound
# Drag and drop ZIP file
```

---

## Stealth Options

```powershell
# Skip ping checks
.\SharpHound.exe -c All --SkipPing

# Throttle requests
.\SharpHound.exe -c All --Throttle 1000

# Jitter (randomize timing)
.\SharpHound.exe -c All --Jitter 20

# Stealth collection (DC only, no sessions)
.\SharpHound.exe -c DCOnly --Stealth
```

---

## Pro Tips

💡 **Run as Domain User**: Needs authenticated domain access
💡 **All Method**: Collects everything, best for analysis
💡 **DCOnly**: Stealthier, no lateral queries
💡 **ZIP Output**: Directly importable into BloodHound
💡 **Regular Collection**: Re-run to track environment changes
💡 **OPSEC**: Use stealth options for quieter collection

---

## Resources

- GitHub: https://github.com/BloodHoundAD/SharpHound
- BloodHound: https://github.com/BloodHoundAD/BloodHound
