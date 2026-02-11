# Bittensor Validator APY Alert Bot

Automated tool that monitors your staked validators across Bittensor subnets and emails you when a better APY validator takes the #1 spot.

---

## What it does

- Checks every subnet you're staked on daily
- Compares your validator's 30-day APY against the current #1
- Sends you ONE summary email if any validator is outperforming yours by 1%+
- Rate limit safe (13 second delay between API calls)

---

## Requirements

- Python 3
- A VPS or server running 24/7 (recommended: RackNerd ~$15/year)
- A Gmail account
- A free TaoStats API key

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/RadoTSC/validator-apy-alerts.git
cd bittensor-validator-alerts
```

### 2. Install dependencies

```bash
pip install requests
```

### 3. Get your TaoStats API key

1. Go to https://dash.taostats.io/api-keys
2. Click "Add an API Key"
3. Copy your key

### 4. Set up Gmail App Password

1. Go to https://myaccount.google.com
2. Security
3. Enable 2-Step Verification (if not already on)
4. Search "App passwords"
5. Select app: Mail, Device: Other (type "VPS")
6. Click Generate
7. Copy the 16-character password

### 5. Configure the bot

```bash
cp validator_config_template.py validator_config.py
nano validator_config.py
```

Fill in your details:

```python
GMAIL_ADDRESS = "youremail@gmail.com"
GMAIL_APP_PASSWORD = "xxxx xxxx xxxx xxxx"

EMAIL_RECIPIENTS = ["youremail@gmail.com"]

TAOSTATS_API_KEY = "your-taostats-key-here"

MY_VALIDATORS = {
    93: "your_validator_hotkey_here",
    # add more subnets below:
    # 21: "your_hotkey_here",
    # 45: "your_hotkey_here",
}

APY_THRESHOLD_PERCENT = 1.0
```

To find your validator hotkey: go to https://taostats.io, find your validator on each subnet, copy the SS58 hotkey.

### 6. Test it manually

```bash
python3 check_validators.py
```

You should see each subnet checked and receive an email if any validator is outperforming yours.

### 7. Automate with cron (runs daily at 9 AM server time)

```bash
crontab -e
```

Add this line:

```
0 9 * * * cd /path/to/bittensor-validator-alerts && /usr/bin/python3 check_validators.py >> vali-alerts.log 2>&1
```

---

## File structure

```
check_validators.py          # Main script (run this)
validator_tracker.py         # Handles API calls to TaoStats
validator_config_template.py # Config template (copy and fill in)
validator_config.py          # Your config (NOT pushed to GitHub)
.gitignore                   # Keeps your config private
```

---

## Built by

Rado from Trend Setter Capital
YouTube: https://www.youtube.com/@RadoTSC
Twitter/X: https://x.com/RadoTsc
