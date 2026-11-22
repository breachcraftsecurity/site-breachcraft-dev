# o365enum

**Type:** Python Script
**Purpose:** Office 365 user enumeration via office.com
**Platform:** Linux, macOS, Windows
**Tags:** #o365 #enumeration #user-enum #python

---

## Installation

```bash
git clone https://github.com/gremwell/o365enum.git
cd o365enum
pip3 install -r requirements.txt
```

---

## Quick Reference

```bash
# Enumerate users
python3 o365enum.py -u users.txt

# With domain
python3 o365enum.py -u users.txt -d company.com

# Save valid users
python3 o365enum.py -u users.txt -v > valid-users.txt
```

---

## ENUM: User Enumeration

```bash
# From username list
python3 o365enum.py -u potential-users.txt

# With specific domain
python3 o365enum.py -u users.txt -d company.com

# Single user
python3 o365enum.py -u user@company.com
```

---

## Pro Tips

💡 **No Authentication**: Enumeration without login attempts
💡 **office.com Method**: Uses office.com endpoint
💡 **Fast**: Quick enumeration
💡 **Low Risk**: No lockout concerns

---

## Resources

- GitHub: https://github.com/gremwell/o365enum
- Author: @gremwell
