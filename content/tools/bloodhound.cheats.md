# BloodHound

**Type:** Graph-Based AD/Azure Analysis Tool
**Purpose:** Active Directory and Azure AD attack path analysis
**Platform:** Windows, Linux, macOS
**Tags:** #active-directory #azure #attack-paths #graph-database #neo4j #enumeration

---

## Installation

```bash
# Install Neo4j
# Download from https://neo4j.com/download/

# Start Neo4j
neo4j console

# Download BloodHound
# https://github.com/BloodHoundAD/BloodHound/releases

# Run BloodHound
./BloodHound --no-sandbox
```

---

## Quick Reference

```bash
# Collect AD data with SharpHound
./SharpHound.exe -c All

# Collect Azure data with AzureHound
azurehound list --jwt "$TOKEN" -o tenant.json

# Import into BloodHound
# Drag and drop JSON/ZIP files into BloodHound UI

# Run pre-built queries
# Click "Queries" tab in BloodHound
```

---

## Data Collection

**Active Directory:**
- Use SharpHound.exe or SharpHound.ps1
- Collects: Users, Groups, Computers, Trusts, ACLs, Sessions

**Azure/Entra ID:**
- Use AzureHound
- Collects: Users, Groups, Service Principals, Roles, Permissions

---

## Pre-Built Queries

**AD Queries:**
- Find all Domain Admins
- Shortest Path to Domain Admins
- Find Kerberoastable Users
- Find AS-REP Roastable Users
- Find Computers with Unconstrained Delegation

**Azure Queries:**
- Find all Global Admins
- Shortest Path to Global Admin
- Find Service Principals with High Permissions
- Find Users with PIM Eligible Roles

---

## Custom Cypher Queries

```cypher
# Find path from user to DA
MATCH p=shortestPath((u:User {name:"USER@DOMAIN.COM"})-[*1..]->(g:Group {name:"DOMAIN ADMINS@DOMAIN.COM"}))
RETURN p

# Find Azure Global Admins
MATCH (u:AZUser)-[r:AZGlobalAdmin]->(t:AZTenant)
RETURN u,r,t
```

---

## Pro Tips

💡 **Graph Database**: Uses Neo4j for fast path analysis
💡 **Visual**: Interactive graph visualization
💡 **Attack Paths**: Identifies privilege escalation routes
💡 **Both AD and Azure**: Supports on-prem and cloud
💡 **Custom Queries**: Learn Cypher for advanced analysis
💡 **Regular Collection**: Re-collect data to track changes
💡 **Community Queries**: Many community-contributed queries available

---

## Resources

- GitHub: https://github.com/BloodHoundAD/BloodHound
- Docs: https://bloodhound.readthedocs.io/
- Company: SpecterOps
