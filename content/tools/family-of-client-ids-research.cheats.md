# Family of Client IDs Research

**Type:** Research/Documentation
**Purpose:** Microsoft application Client ID reference
**Platform:** Documentation
**Tags:** #azure #client-ids #oauth #research #tokens

---

## Purpose

Documents known Microsoft application Client IDs:
- Official Microsoft apps
- Service principals
- OAuth client IDs
- Resource identifiers

---

## Why Important

Client IDs are used for:
- Token requests
- OAuth flows
- Resource access
- Authentication flows

Different Client IDs have different:
- Default permissions
- Allowed resources
- Authentication flows
- MFA requirements

---

## Common Client IDs

```
# Microsoft Graph PowerShell
14d82eec-204b-4c2f-b7e8-296a70dab67e

# Azure PowerShell
1950a258-227b-4e31-a9cf-717495945fc2

# Azure CLI
04b07795-8ddb-461a-bbee-02f9e1bf7b46

# Microsoft Office
d3590ed6-52b3-4102-aeff-aad2292ab01c

# Microsoft Teams
1fec8e78-bce4-4aaf-ab1b-5451cc387264

# And many more...
```

---

## Usage in Attacks

- Token request manipulation
- Bypassing CA policies
- Finding single-factor flows
- OAuth abuse

See: TokenTactics, ROADtools, AADInternals

---

## Pro Tips

💡 **Client ID Matters**: Different IDs have different behaviors
💡 **MFA Bypass**: Some client IDs bypass MFA in misconfigured tenants
💡 **Research**: Continuously updated list
💡 **Tool Integration**: Used by offensive tools

---

## Resources

- GitHub: Search for "family of client IDs"
- Related: Microsoft OAuth documentation
