# fb_tool

Personal Facebook utility for Termux. One action per run.

---

## Project Structure

```
fb_tool/
├── main.py        # Entry point
├── actions.py     # Android Intent launchers
├── config.py      # Settings & alias storage
├── logger.py      # Log file
├── config/        # Auto-created (settings.json)
└── logs/          # Auto-created (fb_tool.log)
```

---

## Installation

```bash
# 1. Update Termux
pkg update && pkg upgrade -y

# 2. Install Python
pkg install python -y

# 3. Install Termux:API package
pkg install termux-api -y

# 4. Install Termux:API companion app from F-Droid
#    https://f-droid.org/packages/com.termux.api/

# 5. Extract and run
unzip fb_tool.zip
cd fb_tool
python main.py
```

---

## Usage

```
fb_tool - Personal Facebook Utility
------------------------------------
[1] Switch Account
[2] Open Facebook Post
[3] Rename Account Alias
[4] Exit

Choice:
```

### Switch Account
Opens Facebook and shows manual steps to reach the account switcher.
Only works with accounts already logged in on your device.

### Open Facebook Post
Paste a URL — it launches directly in the Facebook app.
Supports:
- https://www.facebook.com/...
- https://m.facebook.com/...
- https://fb.watch/...

### Rename Account Alias
Labels your account slots locally (e.g. "Main", "Work").
Stored in config/settings.json.

---

## Configuration

Edit config/settings.json:

```json
{
  "accounts": [
    {"id": 1, "alias": "Main"},
    {"id": 2, "alias": "Work"},
    {"id": 3, "alias": "Account 3"}
  ],
  "delays": {
    "after_launch": 3.0,
    "after_switch": 2.0
  },
  "logging_enabled": true
}
```

Increase after_launch if Facebook is slow to open on your device.

---

## Logs

```bash
cat logs/fb_tool.log
> logs/fb_tool.log   # clear logs
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| termux-open not found | pkg install termux-api + install Termux:API from F-Droid |
| Facebook won't open | Confirm Facebook app is installed |
| am: not found | Some devices restrict this; termux-open is the fallback |
| URL rejected | Must start with https://www.facebook.com/ |

---

Press Ctrl+C at any time to exit.
