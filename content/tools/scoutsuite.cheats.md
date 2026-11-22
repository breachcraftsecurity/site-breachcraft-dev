# ScoutSuite

**Type:** Python Tool
**Purpose:** Multi-cloud security auditing tool (AWS, Azure, GCP, etc.)
**Platform:** Windows, Linux, macOS
**Tags:** #cloud #security-audit #aws #azure #gcp #configuration-review #assessment

---

## Installation

```bash
# Install via pip
pip install scoutsuite

# Or from source
git clone https://github.com/nccgroup/ScoutSuite.git
cd ScoutSuite
pip install -r requirements.txt
python scout.py --help
```

---

## Quick Reference

```bash
# Azure audit
scout azure --cli

# AWS audit
scout aws --profile default

# GCP audit
scout gcp --user-account

# Generate report
# Opens HTML report in browser automatically
```

---

## Azure Auditing

```bash
# Using Azure CLI credentials
scout azure --cli

# Using service principal
scout azure --tenant <tenant-id> --client-id <client-id> --client-secret <secret>

# Specific subscription
scout azure --cli --subscription-ids <sub-id>

# All subscriptions
scout azure --cli --all-subscriptions

# Custom report directory
scout azure --cli --report-dir ./azure-audit-2024/
```

---

## AWS Auditing

```bash
# Using default profile
scout aws

# Specific profile
scout aws --profile prod

# Specific regions
scout aws --regions us-east-1,us-west-2

# All regions
scout aws --all-regions
```

---

## GCP Auditing

```bash
# Using user account
scout gcp --user-account

# Service account
scout gcp --service-account <path-to-key.json>

# Specific project
scout gcp --project-id <project-id>

# All projects
scout gcp --all-projects
```

---

## What ScoutSuite Checks

**Azure:**
- IAM configurations
- Network security groups
- Storage account settings
- VM configurations
- SQL database security
- Key Vault access policies
- Conditional Access policies
- And more...

**AWS:**
- IAM policies and users
- S3 bucket permissions
- EC2 security groups
- RDS configurations
- CloudTrail logging
- And more...

**GCP:**
- IAM bindings
- GCS bucket permissions
- Compute Engine settings
- Cloud SQL configurations
- And more...

---

## Report Features

- HTML dashboard
- Risk ratings (danger, warning, info)
- Detailed findings
- Remediation guidance
- Export to JSON
- Customizable rule sets

---

## Common Use Cases

### Post-Compromise Assessment
```bash
# After gaining Azure access
az login
scout azure --cli --report-dir ./compromise-assessment/

# Review report for:
# - Weak configurations
# - Lateral movement opportunities
# - Privilege escalation paths
# - Additional access points
```

### Security Audit
```bash
# Multi-cloud audit
scout azure --cli --report-dir ./audits/azure/
scout aws --profile client --report-dir ./audits/aws/
scout gcp --user-account --report-dir ./audits/gcp/

# Review all reports for security gaps
```

---

## Pro Tips

💡 **Multi-Cloud**: Single tool for AWS, Azure, GCP, and more
💡 **HTML Reports**: Easy to read, shareable dashboards
💡 **Comprehensive**: Checks 100+ services across clouds
💡 **Remediation**: Provides fix guidance
💡 **Custom Rules**: Extensible rule engine
💡 **Credential Reuse**: Uses existing cloud CLI credentials
💡 **Audit Logging**: Run regularly to track security posture
💡 **Red Team**: Identify misconfigurations for exploitation
💡 **Blue Team**: Continuous security monitoring

---

## Output

Reports saved to `scoutsuite-report/` by default:
- `scoutsuite_results_<provider>-<account>.html` - Main report
- `scoutsuite_results_<provider>-<account>.js` - Data file
- Opens in browser automatically

---

## Resources

- GitHub: https://github.com/nccgroup/ScoutSuite
- Documentation: https://github.com/nccgroup/ScoutSuite/wiki
- Company: NCC Group
