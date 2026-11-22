# basicblobfinder

**Type:** Python Script
**Purpose:** Find publicly accessible Azure Blob Storage containers
**Platform:** Linux, macOS, Windows
**Tags:** #azure #blob-storage #osint #enumeration #reconnaissance

---

## Installation

```bash
# Clone repository
git clone https://github.com/ewpratten/basicblobfinder.git
cd basicblobfinder

# No dependencies required (uses standard library)
python3 basicblobfinder.py -h
```

---

## Quick Reference

```bash
# Basic search
python3 basicblobfinder.py companyname

# Multiple keywords
python3 basicblobfinder.py company product division

# Save results
python3 basicblobfinder.py company > results.txt
```

---

## RECON: Blob Storage Discovery

```bash
# Single keyword
python3 basicblobfinder.py acmecorp

# Tries variations like:
# acmecorp.blob.core.windows.net
# acmecorp-files.blob.core.windows.net
# acmecorp-backup.blob.core.windows.net
# etc.

# Multiple keywords
python3 basicblobfinder.py company product
```

---

## Common Patterns Tested

The tool tests common naming patterns:
- `{keyword}.blob.core.windows.net`
- `{keyword}-files.blob.core.windows.net`
- `{keyword}-backup.blob.core.windows.net`
- `{keyword}-data.blob.core.windows.net`
- `{keyword}-public.blob.core.windows.net`
- etc.

---

## What to Look For

**Publicly Accessible Storage:**
- Configuration files
- Backups
- Database dumps
- Application code
- Credentials
- Customer data
- Internal documents

---

## Manual Verification

```bash
# After finding storage account
az storage blob list --account-name foundaccount --container-name public --auth-mode login

# Or use browser
https://{account}.blob.core.windows.net/{container}/
```

---

## Integration

```bash
# Chain with cloud_enum for comprehensive coverage
./cloud_enum.py -k company --disable-aws --disable-gcp

# Then verify with basicblobfinder
python3 basicblobfinder.py company
```

---

## Pro Tips

💡 **Keywords Matter**: Use company names, products, domains
💡 **Common Patterns**: -backup, -data, -files, -public most common
💡 **Manual Follow-up**: Always manually verify discovered storage
💡 **Azure CLI**: Use `az storage` commands to list/download contents
💡 **Permissions**: Look for public read access (misconfiguration)

---

## Resources

- GitHub: https://github.com/ewpratten/basicblobfinder
- Author: @ewpratten
