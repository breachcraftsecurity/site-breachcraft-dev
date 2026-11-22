# MicroBurst

**Type:** PowerShell Module
**Purpose:** Azure Services discovery, weak configuration auditing, and post-exploitation
**Platform:** Windows
**Tags:** #azure #powershell #enumeration #credentials #persistence #post-exploitation

---

## Installation & Setup

```powershell
# Import module
Import-Module .\MicroBurst.psm1

# Trust downloaded files
dir -Recurse .\MicroBurst-master | Unblock-File

# Install dependencies
Install-Module Az
Install-Module AzureAD
Install-Module MSOnline
```

---

## Quick Reference

### ENUM: Domain Information
```powershell
Get-AzDomainInfo
```
**Purpose:** Gather domain information from Azure AD
**Use Case:** Initial reconnaissance

### ENUM: Enumerate Subdomains
```powershell
Invoke-EnumerateAzureSubDomains -Base <company>
```
**Purpose:** Anonymously enumerate Azure subdomains
**Use Case:** External enumeration without authentication

### ENUM: Enumerate Azure Blobs
```powershell
Invoke-EnumerateAzureBlobs -Base <company>
```
**Purpose:** Discover publicly accessible Azure storage blobs
**Use Case:** Find exposed data in blob storage

### CRED: Dump Automation Passwords
```powershell
Get-AzPasswords
Get-AzurePasswords
```
**Purpose:** Extract credentials from Azure Automation accounts
**Use Case:** Credential harvesting from compromised subscription

### CRED: Dump RunAs Certificates
```powershell
Get-AzurePasswords -ExportCerts
```
**Purpose:** Export Azure RunAs certificates for persistence
**Use Case:** Maintaining access via automation certificates

### PRIVESC: Enumerate Managed Identities
```powershell
Get-AzureManagedIdentity
```
**Purpose:** Find managed identities for privilege escalation
**Use Case:** Identify paths for privilege escalation

### PERSIST: Automation Account Persistence
```powershell
# Use automation accounts to maintain access
```
**Purpose:** Maintain persistence via automation accounts
**Use Case:** Long-term access maintenance

### EXEC: Run PowerShell on Azure VMs
```powershell
Invoke-AzVMBulkCMD -Script <scriptblock>
```
**Purpose:** Execute PowerShell at scale across Azure VMs
**Use Case:** Lateral movement and bulk operations

### LATERAL: Azure App Services Movement
```powershell
# App Services lateral movement techniques
```
**Purpose:** Move between Azure App Services
**Use Case:** Lateral movement within Azure environment

---

## Common Attack Patterns

### Pattern 1: Initial Enumeration (Unauthenticated)
```powershell
# Enumerate subdomains
Invoke-EnumerateAzureSubDomains -Base contoso -Verbose

# Enumerate blob storage
Invoke-EnumerateAzureBlobs -Base contoso

# Enumerate file shares
Invoke-EnumerateAzureFiles -Base contoso
```
**Explanation:** Start with anonymous enumeration to discover Azure resources
**Output:** Lists of discovered subdomains, storage accounts, exposed files

### Pattern 2: Post-Compromise Credential Harvesting
```powershell
# Dump all accessible passwords
Get-AzPasswords -Verbose

# Export certificates for persistence
Get-AzPasswords -ExportCerts -Verbose
```
**Explanation:** After gaining access, extract credentials from automation accounts
**Output:** Passwords, certificates, connection strings

### Pattern 3: VM Extension Abuse
```powershell
# Decrypt VM extension settings
Get-AzureVMExtensionSettings

# Deploy custom script extension
# Attack using custom script extensions
```
**Explanation:** Abuse Azure VM extensions for code execution
**Use Case:** Remote code execution on target VMs

---

## Key Functions by Category

### Enumeration
- `Get-AzDomainInfo` - Azure AD domain information
- `Invoke-EnumerateAzureSubDomains` - Subdomain enumeration
- `Invoke-EnumerateAzureBlobs` - Blob storage enumeration
- `Invoke-EnumerateAzureFiles` - File share enumeration
- `Get-AzureManagedIdentity` - Managed identity discovery

### Credential Access
- `Get-AzPasswords` / `Get-AzurePasswords` - Automation account credential dumping
- `Get-AzureVMExtensionSettings` - VM extension settings decryption
- `Get-AzKeyVaultSecrets` - Key Vault secret extraction

### Execution
- `Invoke-AzVMBulkCMD` - Bulk PowerShell execution on VMs
- Custom Script Extensions - Remote code execution

### Persistence
- Automation Account abuse
- Desired State Configuration (DSC)
- Managed Identity certificates
- RunAs certificates

---

## Prerequisites & Dependencies

**Required Modules:**
- Az (modern Azure module)
- AzureRM (legacy, some scripts)
- AzureAD
- MSOnline

**Platform:**
- Windows only

**Permissions Needed:**
- Varies by function
- Some functions work anonymously
- Post-exploitation functions require authenticated access

---

## Pro Tips

- Use `-Verbose` flag for detailed output
- Start with unauthenticated enumeration functions
- Export certificates immediately after credential dumping
- Automation accounts are goldmines for credentials
- VM extensions can contain sensitive data
- Managed identities enable privilege escalation

---

## References

- **GitHub:** https://github.com/NetSPI/MicroBurst
- **Documentation:** https://github.com/NetSPI/MicroBurst/wiki
- **Author:** Karl Fosaaen (@kfosaaen), NetSPI
- **Key Blog Posts:**
  - [A Beginners Guide to Gathering Azure Passwords](https://blog.netspi.com/a-beginners-guide-to-gathering-azure-passwords/)
  - [Anonymously Enumerating Azure Services](https://blog.netspi.com/enumerating-azure-services/)
  - [Azure Privilege Escalation Using Managed Identities](https://blog.netspi.com/azure-privilege-escalation-using-managed-identities/)
