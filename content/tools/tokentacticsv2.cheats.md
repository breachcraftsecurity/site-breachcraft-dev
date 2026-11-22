# TokenTacticsV2

**Type:** PowerShell Module
**Purpose:** Enhanced version of TokenTactics with additional features
**Platform:** Windows, PowerShell Core
**Tags:** #tokens #jwt #device-code #mfa-bypass #azure #powershell

---

## Note

TokenTacticsV2 is the updated version of TokenTactics with enhanced capabilities. See the TokenTactics cheatsheet for core functionality.

**Key Enhancements:**
- Improved token refresh mechanisms
- Additional resource support
- Enhanced error handling
- Better token management

---

## Installation

```powershell
git clone https://github.com/rvrsh3ll/TokenTacticsV2.git
cd TokenTacticsV2
Import-Module .\TokenTacticsV2.psd1
```

---

## Usage

Similar to TokenTactics with enhancements:
```powershell
# Get tokens
Get-AzureToken -Client MSGraph

# Enhanced refresh capabilities
Invoke-RefreshToMSGraphToken -domain company.com -refreshToken $rt
```

---

## Resources

- GitHub: https://github.com/rvrsh3ll/TokenTacticsV2
- Original: TokenTactics
- Author: @rvrsh3ll
