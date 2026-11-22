# AzureHound

**Type:** Go Binary
**Purpose:** BloodHound data collector for Microsoft Azure/Entra ID
**Platform:** Windows, Linux, macOS
**Tags:** #azure #azuread #bloodhound #enumeration #graph-database #recon #attack-paths

---

## Installation & Setup

```bash
# Download pre-compiled binary
# https://github.com/SpecterOps/azurehound/releases

# Or compile from source
git clone https://github.com/SpecterOps/azurehound.git
cd azurehound
go build -ldflags="-s -w"

# Make executable (Linux/macOS)
chmod +x azurehound

# Verify installation
./azurehound --version
```

---

## Quick Reference (Most Common Commands)

```bash
# Collect all data with username/password
azurehound list -u "user@company.com" -p "password" -t "tenant.onmicrosoft.com"

# Collect with JWT token
JWT=$(az account get-access-token --resource https://graph.microsoft.com | jq -r .accessToken)
azurehound list --jwt "$JWT" -o output.json

# Collect with refresh token
azurehound list --refresh-token "$REFRESH_TOKEN" -o output.json

# Collect specific entities
azurehound list apps,users,groups -u "user@company.com" -p "password" -t "tenant.com"

# Configure for BloodHound Enterprise
azurehound configure
```

---

## Authentication Methods

### AUTH: Username & Password Authentication
**Use Case:** Basic authentication with credentials

```bash
# Full tenant enumeration
azurehound list -u "user@company.com" -p "P@ssw0rd!" -t "company.onmicrosoft.com" -o data.json

# Specify tenant ID instead of domain
azurehound list -u "user@company.com" -p "P@ssw0rd!" -t "aaaabbbb-cccc-dddd-eeee-ffffgggghhhh"
```

### AUTH: JWT Token Authentication
**Use Case:** Use existing access token (stealthier, no password in command line)

```bash
# Get token from Azure CLI
JWT=$(az account get-access-token --resource https://graph.microsoft.com | jq -r .accessToken)

# Collect data with JWT
azurehound list --jwt "$JWT" -o tenant-data.json

# Get token from AADInternals
# Import-Module AADInternals
# $token = Get-AADIntAccessTokenForMSGraph
# Save to file and use with --jwt
```

### AUTH: Refresh Token Authentication
**Use Case:** Use refresh token for long-lived access

```bash
# Collect with refresh token
azurehound list --refresh-token "$REFRESH_TOKEN" -o data.json

# Refresh token can be obtained from:
# - AADInternals: Get-AADIntAccessTokenForMSGraph (includes refresh token)
# - TokenTactics
# - Browser dev tools during authentication
```

### AUTH: Managed Identity (Azure VM)
**Use Case:** Collect from Azure VM with managed identity

```bash
# Get token from managed identity
JWT=$(curl 'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://graph.microsoft.com' -H Metadata:true | jq -r .access_token)

# Collect with token
azurehound list --jwt "$JWT" -o vm-collection.json
```

---

## ENUM: Data Collection

### ENUM: Collect All Data
**Use Case:** Full tenant enumeration for BloodHound analysis

```bash
# Collect everything (default)
azurehound list -u "user@company.com" -p "password" -t "tenant.com" -o full-tenant.json

# Output to stdout instead of file
azurehound list --jwt "$JWT"

# Verbose output
azurehound list --jwt "$JWT" -v 2 -o data.json
```

### ENUM: Collect Specific Entity Types
**Use Case:** Target specific Azure objects

```bash
# Available entity types:
# - apps (Applications)
# - devices
# - groups
# - managementgroups
# - resourcegroups
# - servicePrincipals
# - subscriptions
# - tenants
# - users
# - virtualmachines
# - roles (Directory Roles)
# - keyvaults

# Collect only users and groups
azurehound list users,groups --jwt "$JWT" -o users-groups.json

# Collect apps and service principals
azurehound list apps,servicePrincipals --jwt "$JWT" -o apps-sps.json

# Collect Azure resources
azurehound list subscriptions,resourcegroups,virtualmachines --jwt "$JWT" -o azure-resources.json

# Collect roles and assignments
azurehound list roles --jwt "$JWT" -o roles.json
```

### ENUM: Collection with Proxy
**Use Case:** Route traffic through proxy for OPSEC

```bash
# Use HTTP proxy
azurehound list --jwt "$JWT" --proxy "http://127.0.0.1:8080" -o data.json

# Use SOCKS proxy
azurehound list --jwt "$JWT" --proxy "socks5://127.0.0.1:1080" -o data.json
```

---

## Output & Logging

### Output to File
**Use Case:** Save JSON data for BloodHound ingestion

```bash
# Standard output file
azurehound list --jwt "$JWT" -o tenant-data.json

# Timestamped output
azurehound list --jwt "$JWT" -o "tenant-$(date +%Y%m%d-%H%M%S).json"
```

### Logging Configuration
**Use Case:** Control verbosity and log to file

```bash
# Silent mode (-1)
azurehound list --jwt "$JWT" -v -1 -o data.json

# Normal (0, default)
azurehound list --jwt "$JWT" -o data.json

# Verbose (1)
azurehound list --jwt "$JWT" -v 1 -o data.json

# Very verbose (2)
azurehound list --jwt "$JWT" -v 2 -o data.json

# JSON formatted logs
azurehound list --jwt "$JWT" --json -o data.json

# Log to file
azurehound list --jwt "$JWT" --log-file azurehound.log -o data.json
```

---

## BloodHound Enterprise Integration

### Configure for BHE
**Use Case:** Set up continuous collection for BloodHound Enterprise

```bash
# Interactive configuration
azurehound configure

# Prompts for:
# - API endpoint
# - API key
# - Collection interval
# - Credentials/token

# View current config
cat ~/.config/azurehound/config.json
```

### Start Collection Service
**Use Case:** Begin automated data collection

```bash
# Start service (uses config from 'configure')
azurehound start

# Use custom config file
azurehound start -c /path/to/config.json
```

---

## BloodHound Community Edition Workflow

### Pattern: Collect → Import → Analyze
```bash
# 1. Collect Azure data
azurehound list --jwt "$JWT" -o azure-tenant.json

# 2. Start BloodHound CE
# (Ensure Neo4j database is running)

# 3. Import JSON file into BloodHound
# Open BloodHound UI → Upload Data → Select azure-tenant.json

# 4. Run queries to find attack paths
# - Pre-built queries for Azure
# - Custom Cypher queries
# - Path finding between users/apps/resources
```

---

## Attack Patterns

### Pattern: Compromised User → Full Tenant Mapping
```bash
# 1. Get access token from compromised account
JWT=$(az account get-access-token --resource https://graph.microsoft.com | jq -r .accessToken)

# 2. Collect all tenant data
azurehound list --jwt "$JWT" -o compromised-tenant.json

# 3. Import into BloodHound and analyze:
# - Privilege escalation paths
# - High-value targets (Global Admins, etc.)
# - Application permissions
# - Service principal relationships
```

### Pattern: Limited User → Target High-Value Accounts
```bash
# 1. Collect with limited user account
azurehound list -u "lowpriv@company.com" -p "password" -t "company.com" -o recon.json

# 2. Import into BloodHound

# 3. Run queries to find:
# - Who has Global Admin role?
# - Shortest path to privileged role
# - Applications with high permissions
# - Users with PIM-eligible roles
```

### Pattern: Azure VM Managed Identity → Tenant Recon
```bash
# 1. Compromise Azure VM
# 2. Use managed identity to get token
JWT=$(curl 'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://graph.microsoft.com' -H Metadata:true | jq -r .access_token)

# 3. Collect tenant data
azurehound list --jwt "$JWT" -o from-vm.json

# 4. Analyze in BloodHound
# - Find other resources managed identity can access
# - Map lateral movement options
```

---

## BloodHound Queries for Azure

### Pre-Built Azure Queries
```cypher
# Find all Global Admins
MATCH (u:AZUser)-[r:AZGlobalAdmin]->(t:AZTenant) RETURN u,r,t

# Find users who can reset passwords
MATCH (u:AZUser)-[r:AZResetPassword]->(victim:AZUser) RETURN u,r,victim

# Find service principals with high permissions
MATCH (sp:AZServicePrincipal)-[r:AZMGGrantAppRoles]->(t:AZTenant) RETURN sp,r,t

# Find applications owned by users
MATCH (u:AZUser)-[r:AZOwns]->(app:AZApp) RETURN u,r,app

# Find VMs with managed identities
MATCH (vm:AZVM)-[r:AZManagedIdentity]->(sp:AZServicePrincipal) RETURN vm,r,sp

# Shortest path to Global Admin
MATCH (start:AZUser {name: "lowpriv@company.com"}),
      (end:AZRole {name: "Global Administrator"}),
      p = shortestPath((start)-[*1..]->(end))
RETURN p
```

---

## Data Collected by AzureHound

**Azure AD / Entra ID:**
- Users and their properties
- Groups and memberships
- Applications
- Service Principals
- Devices
- Directory Roles and assignments
- Administrative Units

**Azure Resources:**
- Subscriptions
- Management Groups
- Resource Groups
- Virtual Machines
- Key Vaults
- Role assignments (RBAC)
- Managed Identities

**Relationships:**
- Group memberships
- Role assignments
- Application ownership
- Service principal permissions
- Resource ownership
- Management relationships

---

## Pro Tips

💡 **Token Permissions**: Ensure token has Microsoft Graph permissions (User.Read.All, Group.Read.All, etc.)
💡 **Minimal Permissions**: Even a basic user can enumerate much of the tenant
💡 **Combine with AADInternals**: Use AADInternals to get tokens, AzureHound to map environment
💡 **Regular Collections**: Tenant changes frequently, re-run collection periodically
💡 **Large Tenants**: Collection can take time for large organizations (100k+ users)
💡 **OPSEC**: Use `--proxy` flag to route through C2 infrastructure
💡 **JSON Output**: Can be imported directly into BloodHound CE or Enterprise
💡 **Custom Queries**: Learn Cypher to write custom attack path queries
💡 **Compare Collections**: Import multiple collections to track changes over time
💡 **VM Managed Identity**: Often overlooked attack vector with high privileges

---

## Relationship Types in BloodHound

**Azure AD Relationships:**
- `AZGlobalAdmin` - User is Global Administrator
- `AZResetPassword` - Can reset user password
- `AZOwns` - Owns an object (app, service principal, etc.)
- `AZMemberOf` - Group membership
- `AZHasRole` - Has directory role assignment
- `AZAddMembers` - Can add members to group
- `AZAddSecret` - Can add secrets to app/SP
- `AZExecuteCommand` - Can execute commands on VM

**Azure RBAC Relationships:**
- `AZContributor` - Contributor role on resource
- `AZOwner` - Owner role on resource
- `AZUserAccessAdministrator` - Can manage access
- `AZVMContributor` - Can manage virtual machines
- `AZManagedIdentity` - VM has managed identity

---

## OPSEC Considerations

⚠️ **High Risk:**
- Using compromised Global Admin credentials (generates many API calls)
- Collecting from suspicious/unusual locations
- Repeated rapid collections (rate limiting, logs)

⚠️ **Medium Risk:**
- Large-scale enumeration (generates Graph API audit logs)
- Collection from user accounts (shows in sign-in logs)

✅ **Lower Risk:**
- Using existing legitimate tokens (no new authentication)
- Collecting through proxy
- Spacing out collections over time
- Using service account that regularly queries Graph API

**Detection Vectors:**
- Azure AD Sign-in logs
- Microsoft Graph API audit logs
- Unusual number of Graph API calls
- Collection from new/unusual IP addresses

---

## Configuration File Format

**Location:** `~/.config/azurehound/config.json` (Linux/macOS) or `%APPDATA%\azurehound\config.json` (Windows)

```json
{
  "api_endpoint": "https://bloodhound.example.com",
  "api_key": "your-bhe-api-key",
  "tenant_id": "tenant-id",
  "client_id": "app-client-id",
  "client_secret": "app-secret",
  "refresh_token": "long-lived-refresh-token",
  "proxy": "http://127.0.0.1:8080"
}
```

---

## Troubleshooting

### Authentication Errors
```bash
# Verify token is valid
echo "$JWT" | cut -d. -f2 | base64 -d | jq

# Check token expiration
# Token typically valid for 1 hour

# Get fresh token
JWT=$(az account get-access-token --resource https://graph.microsoft.com | jq -r .accessToken)
```

### Permission Errors
```bash
# Ensure token has Graph permissions
# Minimum: User.Read.All, Group.Read.All, Application.Read.All

# Test with Azure CLI
az ad user list --query "[0]"
```

### Large Tenant Collection
```bash
# Collect in chunks
azurehound list users -o users.json --jwt "$JWT"
azurehound list groups -o groups.json --jwt "$JWT"
azurehound list apps -o apps.json --jwt "$JWT"

# Then merge JSON files or import separately into BloodHound
```

---

## Resources

- GitHub: https://github.com/SpecterOps/azurehound
- Documentation: https://bloodhound.specterops.io/collect-data/ce-collection/azurehound
- BloodHound CE: https://github.com/SpecterOps/BloodHound
- BloodHound Enterprise: https://bloodhoundenterprise.io
