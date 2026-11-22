# Pacu

**Type:** Python Framework
**Purpose:** AWS exploitation framework
**Platform:** Windows, Linux, macOS
**Tags:** #aws #post-exploitation #enumeration #privilege-escalation #lateral-movement

---

## Installation

```bash
git clone https://github.com/RhinoSecurityLabs/pacu.git
cd pacu
pip3 install -r requirements.txt
python3 pacu.py
```

---

## Quick Reference

```bash
# Start Pacu
python3 pacu.py

# Within Pacu shell:
set_keys
import_keys --all
whoami
run <module_name>
```

---

## Common Modules

```
# Enumeration
run iam__enum_users_roles_policies_groups
run iam__enum_permissions
run ec2__enum
run s3__bucket_finder

# Privilege Escalation
run iam__privesc_scan

# Persistence
run iam__backdoor_users_keys
run lambda__backdoor_new_roles

# Data Exfiltration
run s3__download_bucket
run rds__explore_snapshots

# Lateral Movement
run ec2__startup_shell_script
```

---

## Basic Workflow

```bash
# 1. Start Pacu
python3 pacu.py

# 2. Set AWS keys
Pacu> set_keys

# 3. Check permissions
Pacu> whoami

# 4. Enumerate environment
Pacu> run iam__enum_users_roles_policies_groups
Pacu> run ec2__enum
Pacu> run s3__bucket_finder

# 5. Find privilege escalation paths
Pacu> run iam__privesc_scan

# 6. Exploit/pivot
```

---

## Pro Tips

💡 **Modular**: 50+ modules for AWS exploitation
💡 **Session Management**: Saves progress between runs
💡 **Comprehensive**: Enum, privesc, persist, lateral movement
💡 **AWS Focus**: Specialized for AWS (not Azure)
💡 **Post-Exploitation**: Assumes you have AWS credentials

Note: This is an AWS tool, included in Azure offensive tooling repo for cloud coverage

---

## Resources

- GitHub: https://github.com/RhinoSecurityLabs/pacu
- Company: Rhino Security Labs
