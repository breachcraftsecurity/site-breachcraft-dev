# AzSubEnum

**Type:** Python Script
**Purpose:** Azure subscription enumeration via authentication token
**Platform:** Windows, Linux, macOS
**Tags:** #azure #enumeration #subscription #reconnaissance

---

## Installation

```bash
git clone https://github.com/yuyudhn/AzSubEnum.git
cd AzSubEnum
pip3 install -r requirements.txt
```

---

## Quick Reference

```bash
# Enumerate subscriptions
python3 azsubenum.py -t <access-token>

# With output file
python3 azsubenum.py -t <access-token> -o subscriptions.txt
```

---

## ENUM: Subscription Enumeration

```bash
# Basic enumeration
python3 azsubenum.py -t "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIs..."

# Save results
python3 azsubenum.py -t <token> -o output.txt

# Get token first (using Az CLI)
TOKEN=$(az account get-access-token --resource https://management.azure.com/ --query accessToken -o tsv)
python3 azsubenum.py -t "$TOKEN"
```

---

## What It Discovers

- Subscription IDs
- Subscription names
- Subscription states
- Tenant associations
- Access levels

---

## Token Requirements

Requires Azure Management API access token:
- Resource: `https://management.azure.com/`
- Get via Az CLI, AADInternals, TokenTactics, etc.

---

## Integration

```bash
# Chain with other tools
TOKEN=$(az account get-access-token --resource https://management.azure.com/ --query accessToken -o tsv)

# Enumerate subscriptions
python3 azsubenum.py -t "$TOKEN" -o subs.txt

# Use discovered subscriptions
az account set --subscription <discovered-sub-id>
```

---

## Pro Tips

💡 **Token Source**: Works with any valid Azure Management token
💡 **Multi-Sub**: Discovers all accessible subscriptions
💡 **Quick Recon**: Fast way to understand Azure footprint
💡 **Integration**: Chain with PowerZure, Az CLI, etc.

---

## Resources

- GitHub: https://github.com/yuyudhn/AzSubEnum
- Author: @yuyudhn
