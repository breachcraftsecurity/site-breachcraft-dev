# username-anarchy

**Type:** Ruby Script
**Purpose:** Generate username variations from names for enumeration
**Platform:** Linux, macOS, Windows (with Ruby)
**Tags:** #osint #username-generation #enumeration #wordlist

---

## Installation

```bash
# Clone repository
git clone https://github.com/urbanadventurer/username-anarchy.git
cd username-anarchy

# Requires Ruby (usually pre-installed on Linux/macOS)
ruby -v
```

---

## Quick Reference

```bash
# From full name
./username-anarchy John Smith

# From file of names
./username-anarchy --input-file names.txt

# Specific format
./username-anarchy --select-format first.last John Smith

# Save to file
./username-anarchy John Smith > usernames.txt
```

---

## Username Generation

```bash
# Single name
./username-anarchy John Smith
# Outputs:
# john
# smith
# jsmith
# smithj
# john.smith
# j.smith
# johns
# etc.

# Multiple names from file
cat > names.txt << EOF
John Smith
Jane Doe
Bob Johnson
EOF

./username-anarchy --input-file names.txt > potential-usernames.txt
```

---

## Format Selection

```bash
# Common O365 format (first.last)
./username-anarchy --select-format first.last John Smith
# Output: john.smith

# FirstLast format
./username-anarchy --select-format firstlast John Smith
# Output: johnsmith

# First initial + last name
./username-anarchy --select-format flast John Smith
# Output: jsmith

# List all available formats
./username-anarchy --list-formats
```

---

## Common Use Cases

### O365 Enumeration Preparation
```bash
# Generate usernames from LinkedIn names
./username-anarchy --input-file linkedin-names.txt > usernames.txt

# Use with o365spray
o365spray --enum -U usernames.txt --domain company.com

# Or Oh365UserFinder
python3 oh365userfinder.py -r usernames.txt -w valid-users.txt
```

### Password Spraying Lists
```bash
# Generate variations
./username-anarchy --input-file employees.txt > all-variations.txt

# Filter to company format (e.g., first.last)
./username-anarchy --select-format first.last --input-file employees.txt > formatted-users.txt

# Spray
o365spray --spray -U formatted-users.txt -p 'Password123!' --domain company.com
```

---

## Integration

```bash
# Chain with enumeration tools
./username-anarchy John Smith Jane Doe > users.txt
o365spray --enum -U users.txt --domain company.com --output ./results/
```

---

## Pro Tips

💡 **LinkedIn Mining**: Extract names from LinkedIn, feed to username-anarchy
💡 **Format Discovery**: Test different formats to find company standard
💡 **Fuzzing**: Generates many variations - reduces manual work
💡 **Dedupe**: Use `sort -u` to remove duplicates from output
💡 **Common Formats**: first.last, flast, first_last most common in enterprises

---

## Resources

- GitHub: https://github.com/urbanadventurer/username-anarchy
- Author: @urbanadventurer
