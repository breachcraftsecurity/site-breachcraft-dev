# cloud_enum

**Type:** Python Script
**Purpose:** Multi-cloud OSINT tool - enumerate public resources in AWS, Azure, and GCP
**Platform:** Windows, Linux, macOS
**Tags:** #cloud #osint #recon #aws #azure #gcp #s3 #storage #enumeration #reconnaissance

---

## Installation & Setup

```bash
# Clone repository
git clone https://github.com/initstring/cloud_enum.git
cd cloud_enum

# Install dependencies
pip3 install -r requirements.txt

# Make executable (optional)
chmod +x cloud_enum.py
```

---

## Quick Reference (Most Common Commands)

```bash
# Basic scan with single keyword
./cloud_enum.py -k company

# Multiple keywords
./cloud_enum.py -k company -k company-io -k product

# Keywords from file
./cloud_enum.py -kf keywords.txt

# Disable specific cloud provider
./cloud_enum.py -k company --disable-aws --disable-gcp

# Quick scan (no mutations, faster)
./cloud_enum.py -k company --quickscan

# Save results to file
./cloud_enum.py -k company -l results.txt
```

---

## RECON: What cloud_enum Discovers

### AWS Resources
- S3 Buckets (open/protected)
- AWS Apps (WorkMail, WorkDocs, Connect, etc.)

### Azure Resources
- Storage Accounts
- Blob Storage Containers (open)
- Hosted Databases
- Virtual Machines
- Web Apps

### GCP Resources
- GCP Buckets (open/protected)
- Firebase Realtime Databases (open/protected)
- Google App Engine sites
- Cloud Functions
- Firebase Apps (open)

---

## ENUM: Basic Enumeration

### ENUM: Single Keyword
**Use Case:** Enumerate cloud resources for one company/keyword

```bash
# Basic scan
./cloud_enum.py -k companyname

# Scans all 3 clouds (AWS, Azure, GCP) by default
# Uses built-in mutations from enum_tools/fuzz.txt
```

### ENUM: Multiple Keywords
**Use Case:** Scan multiple variations of company name

```bash
# Multiple keywords
./cloud_enum.py -k somecompany -k somecompany-io -k productname

# Each keyword is mutated and tried
# Examples:
# - somecompany-dev
# - somecompany-prod
# - somecompany-test
# - dev-somecompany
# - prod.somecompany
# etc.
```

### ENUM: Keywords from File
**Use Case:** Bulk keyword enumeration

```bash
# Keywords file (one per line)
cat > keywords.txt << EOF
company
company-io
product
service
EOF

# Scan with keyword file
./cloud_enum.py -kf keywords.txt
```

---

## ENUM: Mutations & Brute Force

### ENUM: Custom Mutations
**Use Case:** Provide custom mutation list

```bash
# Custom mutations file
cat > mutations.txt << EOF
-dev
-prod
-test
-staging
-backup
dev-
prod-
test.
staging.
EOF

# Use custom mutations
./cloud_enum.py -k company -m mutations.txt

# Default: enum_tools/fuzz.txt
```

### ENUM: Custom Brute Force List
**Use Case:** Custom list for second-level brute force (Azure containers, GCP functions)

```bash
# Brute force file
cat > brute.txt << EOF
public
private
data
files
images
backups
EOF

# Use custom brute list
./cloud_enum.py -k company -b brute.txt

# Used for:
# - Azure Blob Storage container names
# - GCP Cloud Function names
```

---

## ENUM: Quick Scan Mode

### ENUM: Quick Scan
**Use Case:** Fast scan without mutations

```bash
# Quick scan (no mutations, no second-level brute force)
./cloud_enum.py -k company --quickscan

# Much faster but finds fewer resources
# Good for initial recon
```

---

## ENUM: Cloud-Specific Scans

### ENUM: Azure Only
**Use Case:** Scan Azure resources only

```bash
# Azure only
./cloud_enum.py -k company --disable-aws --disable-gcp

# Finds:
# - Storage accounts
# - Blob containers
# - Databases
# - VMs
# - Web Apps
```

### ENUM: AWS Only
**Use Case:** Scan AWS resources only

```bash
# AWS only
./cloud_enum.py -k company --disable-azure --disable-gcp

# Finds:
# - S3 buckets
# - WorkMail
# - WorkDocs
# - Connect
# etc.
```

### ENUM: GCP Only
**Use Case:** Scan GCP resources only

```bash
# GCP only
./cloud_enum.py -k company --disable-aws --disable-azure

# Finds:
# - GCS buckets
# - Firebase databases
# - App Engine
# - Cloud Functions
# - Firebase apps
```

---

## Performance & Threading

### Thread Configuration
**Use Case:** Adjust scan speed

```bash
# Increase threads (default: 5)
./cloud_enum.py -k company -t 10

# WARNING: Too many threads may trigger rate limiting
# Recommended: 5-10 threads
```

### DNS Configuration
**Use Case:** Custom DNS server

```bash
# Use specific DNS server
./cloud_enum.py -k company -ns 8.8.8.8

# May help avoid DNS rate limiting
```

---

## Output & Logging

### Save Results
**Use Case:** Log discovered resources

```bash
# Save to text file (default format)
./cloud_enum.py -k company -l results.txt

# JSON format
./cloud_enum.py -k company -l results.json -f json

# CSV format
./cloud_enum.py -k company -l results.csv -f csv

# APPENDS to file (doesn't overwrite)
```

---

## Region Configuration

### Configure Azure Regions
**Use Case:** Scan specific Azure regions

```bash
# Edit cloudenum/azure_regions.py
# REGIONS variable defaults to 1 region for speed

# Edit to include your target regions:
REGIONS = [
    'eastus',
    'westus',
    'northeurope',
    'westeurope',
    # etc.
]
```

### Configure GCP Regions
**Use Case:** Scan specific GCP regions

```bash
# Edit cloudenum/gcp_regions.py
# REGIONS variable defaults to 1 region

# Edit to include your target regions:
REGIONS = [
    'us-central1',
    'us-east1',
    'europe-west1',
    # etc.
]
```

---

## Attack Patterns

### Pattern: Company Recon → Resource Discovery
```bash
# 1. Gather keywords about target
# - Company name
# - Product names
# - Domain variations

# 2. Create keyword list
cat > company-keywords.txt << EOF
acme
acmecorp
acme-corp
acmeproduct
acme.com
acme.io
EOF

# 3. Run full enumeration
./cloud_enum.py -kf company-keywords.txt -l acme-results.txt

# 4. Review results for:
# - Open S3 buckets
# - Open Azure blob containers
# - Exposed databases
# - Public-facing web apps
# - Firebase databases
```

### Pattern: Quick Initial Scan → Deep Dive
```bash
# 1. Quick scan to identify cloud presence
./cloud_enum.py -k company --quickscan

# 2. If Azure resources found, deep dive Azure only
./cloud_enum.py -k company --disable-aws --disable-gcp -m custom-mutations.txt

# 3. Manually browse discovered resources for sensitive data
```

### Pattern: Multi-Cloud Reconnaissance
```bash
# 1. Comprehensive scan all clouds
./cloud_enum.py -k targetcompany -k targetproduct -l target-clouds.txt

# 2. Check each cloud for misconfigurations:

# AWS S3 buckets
aws s3 ls s3://found-bucket-name --no-sign-request

# Azure Blob containers
az storage blob list --account-name foundstorageaccount --container-name foundcontainer --auth-mode login

# GCP buckets
gsutil ls -r gs://found-gcp-bucket
```

---

## Discovered Resource Examples

### AWS S3 Buckets
```
http://company-dev.s3.amazonaws.com
http://company-backup.s3.amazonaws.com
http://company-prod-files.s3.amazonaws.com
```

### Azure Storage & Resources
```
https://companydata.blob.core.windows.net
https://company-dev.azurewebsites.net
https://company-db.database.windows.net
https://company-vm.westus.cloudapp.azure.com
```

### GCP Resources
```
https://storage.googleapis.com/company-backups
https://company-db.firebaseio.com
https://company-app.appspot.com
https://us-central1-project.cloudfunctions.net/functionname
```

---

## Common Mutation Patterns

### Built-in Mutations (enum_tools/fuzz.txt)
```
-dev
-development
-prod
-production
-test
-testing
-uat
-stage
-staging
-backup
-backups
-data
-files
-public
-private
-internal
-external
dev-
prod-
test-
```

### Additional Recommended Mutations
```
-api
-web
-app
-mobile
-admin
-assets
-static
-media
-images
-docs
-archive
-logs
-audit
-compliance
```

---

## Pro Tips

💡 **Keywords Matter**: Better keywords = better results (company names, products, domains)
💡 **Multiple Variations**: Try domain variations (company, company-io, companyio, etc.)
💡 **Region Config**: Edit region files for comprehensive coverage
💡 **Threading**: 5-10 threads optimal (more triggers rate limiting)
💡 **Quick First**: Run `--quickscan` first for fast results
💡 **Cloud Specific**: If you know target uses Azure, disable others for speed
💡 **Log Results**: Always use `-l` to save findings
💡 **Appends Logs**: Log file appends, so you can run multiple scans
💡 **Custom Mutations**: Build industry-specific mutation lists
💡 **Verify Manually**: Always manually verify discovered resources

---

## OPSEC Considerations

⚠️ **OSINT Tool**: This is passive reconnaissance
- No authentication required
- No exploitation
- Just HTTP/DNS queries

✅ **Legal & Ethical**:
- Only discovers publicly accessible resources
- No bypassing of access controls
- Pure OSINT

**Detection**:
- Minimal (just web requests)
- Rate limiting possible if too aggressive
- No authentication events generated

---

## What to Look For in Results

### High-Value Discoveries

**Open S3 Buckets:**
- ListBucket enabled → Can list all files
- GetObject enabled → Can download files
- Look for: configs, backups, credentials, PII

**Open Azure Blob Containers:**
- Public read access
- Look for: same as S3

**Open Firebase Databases:**
- `.json` access with no auth
- May contain sensitive application data

**Exposed Databases:**
- SQL/NoSQL endpoints discoverable
- May indicate misconfiguration

**Web Apps/Functions:**
- Development/staging environments
- May have debug features enabled
- Looser security than production

---

## Integration with Other Tools

### Use with AWS CLI
```bash
# After discovering S3 bucket
aws s3 ls s3://discovered-bucket --no-sign-request
aws s3 cp s3://discovered-bucket/file.txt . --no-sign-request
```

### Use with Azure CLI
```bash
# After discovering storage account
az storage blob list --account-name discoveredaccount --container-name public --auth-mode login
```

### Use with Google Cloud SDK
```bash
# After discovering GCS bucket
gsutil ls -r gs://discovered-bucket
gsutil cp gs://discovered-bucket/file.txt .
```

---

## Troubleshooting

### Rate Limiting
```bash
# Reduce threads
./cloud_enum.py -k company -t 3

# Add delays (edit source code threading)
```

### No Results
```bash
# Try more keywords
./cloud_enum.py -k company -k company-corp -k companyproduct

# Try custom mutations relevant to target
./cloud_enum.py -k company -m industry-specific-mutations.txt
```

### DNS Issues
```bash
# Use alternative DNS server
./cloud_enum.py -k company -ns 1.1.1.1
```

---

## Future: Nuclei Templates

Per the author, cloud_enum functionality is being migrated to Nuclei templates:
- https://github.com/projectdiscovery/nuclei-templates/pull/6865

Consider using Nuclei for cloud enumeration going forward.

---

## Resources

- GitHub: https://github.com/initstring/cloud_enum
- Author: @initstring
- Nuclei Migration: https://github.com/projectdiscovery/nuclei-templates/pull/6865
- Video Demo: https://www.youtube.com/embed/pTUDJhWJ1m0 (by Codingo)
