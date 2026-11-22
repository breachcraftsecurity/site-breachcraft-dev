# Microsoft-Extractor-Suite

**Type:** PowerShell Module
**Purpose:** M365 and Azure forensics/IR data collection and analysis
**Platform:** Windows, PowerShell Core
**Tags:** #forensics #incident-response #m365 #azure #logs #audit #exfiltration #blue-team #red-team

---

## Installation & Setup

```powershell
# Install from PowerShell Gallery
Install-Module -Name Microsoft-Extractor-Suite

# Or import from local path
Import-Module .\Microsoft-Extractor-Suite.psd1

# Install required dependencies
Install-Module Az
Install-Module ExchangeOnlineManagement
Install-Module Microsoft.Graph

# Connect to services (choose based on what you're collecting)
Connect-M365              # Microsoft 365
Connect-MgGraph          # Microsoft Graph
Connect-AzAccount        # Azure
```

---

## Quick Reference (Most Common Commands)

```powershell
# Collect everything automatically
Get-AllEvidence -OutputDir .\evidence\

# Unified Audit Log
Get-UAL -UserIds user@company.com -StartDate 2024-01-01 -EndDate 2024-01-31

# Sign-in logs
Get-GraphEntraSignInLogs -StartDate 2024-01-01 -EndDate 2024-01-31

# Mailbox rules (persistence check)
Get-MailboxRules -OutputDir .\rules\

# OAuth permissions (malicious apps)
Get-OAuthPermissionsGraph -OutputDir .\oauth\
```

---

## EXFIL: Unified Audit Log Collection

### EXFIL: Collect Unified Audit Log
**Use Case:** Extract all M365 audit logs

```powershell
# Collect all UAL for date range
Get-UAL -StartDate 2024-01-01 -EndDate 2024-01-31 -OutputDir .\ual\

# Specific user
Get-UAL -UserIds user@company.com -StartDate 2024-01-01 -EndDate 2024-01-31

# Specific record types
Get-UAL -RecordType AzureActiveDirectory,ExchangeAdmin -StartDate 2024-01-01 -EndDate 2024-01-31

# Specific operations
Get-UAL -Operations UserLoggedIn,MailItemsAccessed -StartDate 2024-01-01 -EndDate 2024-01-31
```

### EXFIL: UAL Statistics
**Use Case:** Get overview of available logs

```powershell
# Display log counts by record type
Get-UALStatistics -StartDate 2024-01-01 -EndDate 2024-01-31

# Shows:
# - Total logs per RecordType
# - Helps identify what data is available
```

### EXFIL: Mailbox Audit Log
**Use Case:** Collect mailbox-specific audit logs

```powershell
# Specific mailbox
Get-MailboxAuditLog -Identity user@company.com -StartDate 2024-01-01 -EndDate 2024-01-31

# All mailboxes
Get-MailboxAuditLog -StartDate 2024-01-01 -EndDate 2024-01-31

# Specific operations (e.g., mail access)
Get-MailboxAuditLog -Operations MailItemsAccessed -StartDate 2024-01-01 -EndDate 2024-01-31
```

### EXFIL: Admin Audit Log
**Use Case:** Collect Exchange admin activity

```powershell
# Admin actions
Get-AdminAuditLog -StartDate 2024-01-01 -EndDate 2024-01-31 -OutputDir .\admin\

# Track admin changes
```

---

## EXFIL: Sign-In & Audit Logs

### EXFIL: Entra ID Sign-In Logs
**Use Case:** Collect authentication logs

```powershell
# All sign-ins
Get-GraphEntraSignInLogs -StartDate 2024-01-01 -EndDate 2024-01-31 -OutputDir .\signin\

# Specific user
Get-GraphEntraSignInLogs -UserPrincipalName user@company.com -StartDate 2024-01-01 -EndDate 2024-01-31

# Failed sign-ins only
Get-GraphEntraSignInLogs -StartDate 2024-01-01 -EndDate 2024-01-31 | Where-Object {$_.Status.ErrorCode -ne 0}
```

### EXFIL: Entra ID Audit Logs
**Use Case:** Collect Azure AD change logs

```powershell
# All audit logs
Get-GraphEntraAuditLogs -StartDate 2024-01-01 -EndDate 2024-01-31 -OutputDir .\audit\

# Specific activity type
Get-GraphEntraAuditLogs -ActivityType "Add user" -StartDate 2024-01-01 -EndDate 2024-01-31
```

---

## EXFIL: Azure Activity Logs

### EXFIL: Azure Activity Logs
**Use Case:** Collect Azure resource activity

```powershell
# All activity logs
Get-ActivityLogs -StartDate 2024-01-01 -EndDate 2024-01-31 -OutputDir .\azure\

# Specific subscription
Get-ActivityLogs -SubscriptionId "sub-id" -StartDate 2024-01-01 -EndDate 2024-01-31
```

### EXFIL: Directory Activity Logs
**Use Case:** Collect directory-level changes

```powershell
# Directory activity
Get-DirectoryActivityLogs -StartDate 2024-01-01 -EndDate 2024-01-31 -OutputDir .\directory\
```

---

## EXFIL: Email & Message Tracking

### EXFIL: Message Trace Logs
**Use Case:** Track email flow

```powershell
# Message tracking
Get-MessageTraceLog -StartDate 2024-01-01 -EndDate 2024-01-31 -OutputDir .\messages\

# Specific sender/recipient
Get-MessageTraceLog -SenderAddress attacker@evil.com -StartDate 2024-01-01 -EndDate 2024-01-31
Get-MessageTraceLog -RecipientAddress victim@company.com -StartDate 2024-01-01 -EndDate 2024-01-31
```

### EXFIL: Download Emails
**Use Case:** Extract specific emails

```powershell
# Download email by message ID
Get-Email -UserPrincipalName user@company.com -MessageId "<message-id>" -OutputDir .\emails\

# Bulk download
Get-Email -UserPrincipalName user@company.com -Subject "Confidential" -OutputDir .\emails\

# Show email content
Show-Email -UserPrincipalName user@company.com -MessageId "<message-id>"
```

### EXFIL: Download Attachments
**Use Case:** Extract email attachments

```powershell
# Get attachments
Get-Attachment -UserPrincipalName user@company.com -MessageId "<message-id>" -OutputDir .\attachments\

# Bulk attachment extraction
```

### EXFIL: Email Session Information
**Use Case:** Correlate MailItemsAccessed events

```powershell
# Get session information
Get-Sessions -UserPrincipalName user@company.com -StartDate 2024-01-01 -EndDate 2024-01-31

# Extract message IDs from MailItemsAccessed
Get-MessageIDs -UserPrincipalName user@company.com -StartDate 2024-01-01 -EndDate 2024-01-31
```

---

## ENUM: Mailbox Rules & Transport Rules

### ENUM: Mailbox Rules
**Use Case:** Detect persistence via mailbox rules

```powershell
# Show mailbox rules (console output)
Show-MailboxRules -Identity user@company.com

# Export all mailbox rules
Get-MailboxRules -OutputDir .\rules\

# Specific mailbox
Get-MailboxRules -Identity user@company.com -OutputDir .\rules\

# Look for suspicious rules:
# - Forwarding to external addresses
# - Auto-delete rules
# - Moving emails to hidden folders
```

### ENUM: Transport Rules
**Use Case:** Detect email redirection/interception

```powershell
# Show transport rules
Show-TransportRules

# Export transport rules
Get-TransportRules -OutputDir .\transport\

# Look for:
# - Forwarding rules
# - BCC rules
# - Conditional routing
```

---

## ENUM: OAuth & Application Permissions

### ENUM: OAuth Application Permissions
**Use Case:** Detect malicious applications

```powershell
# Via Az module
Get-OAuthPermissions -OutputDir .\oauth\

# Via Graph API (more detailed)
Get-OAuthPermissionsGraph -OutputDir .\oauth\

# Review for:
# - Suspicious app names
# - Excessive permissions
# - Recently added apps
# - External/unverified publishers
```

---

## ENUM: User Information

### ENUM: User Enumeration
**Use Case:** Collect user details

```powershell
# All users
Get-Users -OutputDir .\users\

# Specific user
Get-Users -UserPrincipalName user@company.com -OutputDir .\users\

# Includes:
# - Creation date
# - Last password change
# - Account status
# - Assigned licenses
```

### ENUM: Admin Users
**Use Case:** Identify privileged accounts

```powershell
# All users with admin roles
Get-AdminUsers -OutputDir .\admins\

# Shows:
# - Directory role assignments
# - Privileged users
# - Admin activity
```

### ENUM: MFA Status
**Use Case:** Identify accounts without MFA

```powershell
# MFA status for all users
Get-MFA -OutputDir .\mfa\

# Shows:
# - MFA enabled/disabled
# - MFA methods configured
# - Accounts vulnerable to compromise
```

### ENUM: Risky Users
**Use Case:** Identify compromised accounts

```powershell
# Risky users (Identity Protection)
Get-RiskyUsers -OutputDir .\risky\

# Risky detections
Get-RiskyDetections -OutputDir .\detections\

# Shows:
# - Risk level (High/Medium/Low)
# - Risk reasons
# - Detection timestamps
```

---

## ENUM: Conditional Access & Security

### ENUM: Conditional Access Policies
**Use Case:** Audit CA configuration

```powershell
# Export all CA policies
Get-ConditionalAccessPolicies -OutputDir .\ca\

# Review for:
# - Policy gaps
# - Excluded users/groups
# - Weak controls
# - MFA exemptions
```

### ENUM: Security Alerts
**Use Case:** Collect security alerts

```powershell
# Get security alerts
Get-SecurityAlerts -OutputDir .\alerts\

# Review active threats
```

### ENUM: Security Defaults Status
**Use Case:** Check if security defaults enabled

```powershell
# Check Entra ID security defaults
Get-EntraSecurityDefaults
```

---

## ENUM: Device Information

### ENUM: Registered Devices
**Use Case:** Audit device registrations

```powershell
# All registered devices
Get-Devices -OutputDir .\devices\

# Shows:
# - Device ID
# - Device type/OS
# - Registration date
# - Compliance status
# - Owners
```

---

## ENUM: Mailbox Permissions & Audit

### ENUM: Mailbox Permissions
**Use Case:** Detect delegated access

```powershell
# All delegated permissions
Get-MailboxPermissions -OutputDir .\permissions\

# Specific mailbox
Get-MailboxPermissions -Identity user@company.com -OutputDir .\permissions\

# Look for:
# - FullAccess permissions
# - SendAs permissions
# - SendOnBehalf permissions
# - Unusual delegations
```

### ENUM: Mailbox Audit Status
**Use Case:** Verify audit configuration

```powershell
# Audit status for all mailboxes
Get-MailboxAuditStatus -OutputDir .\audit-status\

# Shows:
# - Audit enabled/disabled
# - Audit actions logged
# - Retention settings
```

---

## ENUM: Groups & Licenses

### ENUM: Group Information
**Use Case:** Enumerate groups

```powershell
# All groups
Get-Groups -OutputDir .\groups\

# Group members
Get-GroupMembers -OutputDir .\group-members\

# Dynamic groups (potential abuse)
Get-DynamicGroups -OutputDir .\dynamic-groups\

# Review dynamic group membership rules
```

### ENUM: License Information
**Use Case:** Understand tenant licensing

```powershell
# All licenses
Get-Licenses -OutputDir .\licenses\

# License compatibility check
Get-LicenseCompatibility

# User license assignments
Get-LicensesByUser -OutputDir .\user-licenses\
```

---

## ENUM: Role Management

### ENUM: PIM Role Assignments
**Use Case:** Audit Privileged Identity Management

```powershell
# PIM assignments
Get-PIMAssignments -OutputDir .\pim\

# Shows:
# - Eligible role assignments
# - Active role assignments
# - PIM activation history
```

### ENUM: Role Activity
**Use Case:** Track role usage

```powershell
# All role activity
Get-AllRoleActivity -OutputDir .\role-activity\

# Shows:
# - Directory role memberships
# - Last login per role
# - Inactive admins
```

---

## AUTO: Automated Collection

### AUTO: Collect All Evidence
**Use Case:** One-command full collection

```powershell
# Collect everything
Get-AllEvidence -OutputDir .\full-evidence\

# Automatically collects:
# - UAL
# - Sign-in logs
# - Audit logs
# - Mailbox rules
# - OAuth apps
# - Users
# - Groups
# - CA policies
# - And more...

# Great for initial IR response
```

### AUTO: Quick Triage
**Use Case:** Focused user investigation

```powershell
# Triage specific user
Start-MESTriage -UserPrincipalName compromised@company.com -OutputDir .\triage\

# Customizable templates for quick investigation
```

---

## Attack Patterns (Red Team Use)

### Pattern: Post-Compromise Evidence Collection
```powershell
# After compromising account with privileges

# 1. Connect
Connect-M365
Connect-MgGraph

# 2. Collect audit logs to understand detection
Get-UAL -StartDate (Get-Date).AddDays(-30) -EndDate (Get-Date) -OutputDir .\logs\

# 3. Identify other admins
Get-AdminUsers -OutputDir .\admins\

# 4. Check for monitoring gaps
Get-MailboxAuditStatus -OutputDir .\audit\

# 5. Find accounts without MFA
Get-MFA -OutputDir .\mfa\

# 6. Look for malicious apps already present
Get-OAuthPermissionsGraph -OutputDir .\oauth\
```

### Pattern: Exfiltrate Intelligence
```powershell
# Collect organizational intelligence

# Users and structure
Get-Users -OutputDir .\intel\users\
Get-Groups -OutputDir .\intel\groups\
Get-AdminUsers -OutputDir .\intel\admins\

# Security posture
Get-ConditionalAccessPolicies -OutputDir .\intel\ca\
Get-MFA -OutputDir .\intel\mfa\

# Infrastructure
Get-Devices -OutputDir .\intel\devices\
Get-Licenses -OutputDir .\intel\licenses\
```

---

## Defensive Use (Blue Team)

### Pattern: Incident Response Collection
```powershell
# Compromise suspected on 2024-01-15

# 1. Automated collection
Get-AllEvidence -OutputDir .\IR-Case-001\

# 2. Focused user investigation
Start-MESTriage -UserPrincipalName victim@company.com -OutputDir .\IR-Case-001\victim\

# 3. Check for persistence
Get-MailboxRules -OutputDir .\IR-Case-001\rules\
Get-OAuthPermissionsGraph -OutputDir .\IR-Case-001\oauth\

# 4. Timeline creation
Get-UAL -UserIds victim@company.com -StartDate 2024-01-10 -EndDate 2024-01-20 -OutputDir .\IR-Case-001\timeline\
```

### Pattern: Threat Hunting
```powershell
# Hunt for suspicious activity

# 1. Find risky users
Get-RiskyUsers -OutputDir .\hunt\risky\
Get-RiskyDetections -OutputDir .\hunt\detections\

# 2. Check for suspicious mailbox rules
Get-MailboxRules -OutputDir .\hunt\rules\
# Review for forwarding/auto-delete

# 3. OAuth app review
Get-OAuthPermissionsGraph -OutputDir .\hunt\oauth\
# Look for recently added, high-permission apps

# 4. Failed sign-ins
Get-GraphEntraSignInLogs -StartDate (Get-Date).AddDays(-7) -EndDate (Get-Date) | Where-Object {$_.Status.ErrorCode -ne 0}
```

---

## Pro Tips

💡 **Full Collection**: Use Get-AllEvidence for comprehensive IR
💡 **Date Ranges**: Audit log retention varies by license (90 days for E5)
💡 **OAuth Apps**: Get-OAuthPermissionsGraph more detailed than Get-OAuthPermissions
💡 **Mailbox Rules**: Check regularly for persistence
💡 **MFA Gaps**: Get-MFA identifies vulnerable accounts
💡 **PIM Audit**: Get-PIMAssignments tracks privileged access
💡 **Triage Template**: Start-MESTriage great for quick user investigation
💡 **Sign-In Logs**: Look for impossible travel, suspicious IPs
💡 **License Limits**: Some features require E5/P2 licenses
💡 **Retention**: Collect logs before they age out (90 days typically)

---

## Output Formats

All collection functions output to:
- CSV files (default)
- JSON (some functions)
- Console output (Show- functions)

Results are organized in the specified OutputDir with timestamps.

---

## Authentication & Connection

### Connect to Services
```powershell
# Microsoft 365 (Exchange Online)
Connect-M365

# Microsoft Graph
Connect-MgGraph -Scopes "AuditLog.Read.All","Directory.Read.All"

# Azure
Connect-AzAccount
# Or
Connect-AzureAZ

# Disconnect
Disconnect-M365
Disconnect-Azure
Disconnect-AzureAZ
```

---

## Required Permissions

### Microsoft Graph Permissions Needed:
- AuditLog.Read.All
- Directory.Read.All
- User.Read.All
- Group.Read.All
- Policy.Read.All
- SecurityEvents.Read.All

### Exchange Online Permissions:
- View-Only Audit Logs
- Mailbox Import Export (for email collection)

### Azure Permissions:
- Reader role (minimum)
- Security Reader (for security data)

---

## Resources

- GitHub: https://github.com/invictus-ir/Microsoft-Extractor-Suite
- Documentation: https://microsoft-365-extractor-suite.readthedocs.io/
- PowerShell Gallery: https://www.powershellgallery.com/packages/Microsoft-Extractor-Suite
- Related: Microsoft-Analyzer-Suite (LETHAL FORENSICS)
- Company: Invictus IR
- Authors: Joey Rentenaar, Korstiaan Stam
