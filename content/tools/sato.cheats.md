# Sato

**Type:** Python Tool
**Purpose:** AWS CloudFormation/Terraform static analysis
**Platform:** Linux, macOS, Windows
**Tags:** #aws #iac #security #static-analysis #terraform #cloudformation

---

## Purpose

Sato performs security analysis of:
- AWS CloudFormation templates
- Terraform configurations
- Infrastructure as Code (IaC)
- Identifies misconfigurations

---

## Installation

```bash
pip3 install sato
```

---

## Usage

```bash
# Analyze CloudFormation template
sato analyze template.yaml

# Analyze Terraform
sato analyze main.tf

# Multiple files
sato analyze *.tf
```

---

## What It Detects

- Security group misconfigurations
- S3 bucket public access
- IAM overly permissive policies
- Encryption not enabled
- Logging disabled
- And more IaC security issues

---

## Pro Tips

💡 **IaC Security**: Catches issues before deployment
💡 **AWS Focus**: Specialized for AWS resources
💡 **CI/CD Integration**: Use in build pipelines

Note: AWS tool, included for cloud coverage

---

## Resources

- GitHub: https://github.com/JonathanDC64/sato (or similar)
