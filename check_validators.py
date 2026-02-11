import time
import smtplib
from email.message import EmailMessage
from validator_config import (
    GMAIL_ADDRESS, GMAIL_APP_PASSWORD,
    EMAIL_RECIPIENTS, MY_VALIDATORS, APY_THRESHOLD_PERCENT
)
from validator_tracker import get_validators_for_subnet


def send_summary_email(alerts):
    """Send ONE email with all subnets where you dropped from #1"""
    
    subject = f"Validator Alert: {len(alerts)} subnet(s) need attention"
    
    body = "The following subnets have a new #1 validator:\n\n"
    body += "=" * 40 + "\n\n"
    
    for alert in alerts:
        body += f"Subnet {alert['netuid']}\n"
        body += f"Your validator: {alert['your_name']}\n"
        body += f"Your 1M APY: {alert['your_apy']:.2f}%\n"
        body += f"New #1: {alert['new_name']}\n"
        body += f"New #1 hotkey: {alert['new_hotkey']}\n"
        body += f"New #1 APY: {alert['new_apy']:.2f}%\n"
        body += f"Difference: {alert['difference']:.2f}%\n"
        body += "\n" + "=" * 40 + "\n\n"
    
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = ", ".join(EMAIL_RECIPIENTS)
    msg.set_content(body)
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        smtp.send_message(msg)
    
    print(f"Summary email sent for {len(alerts)} subnet(s)")


def check_subnet(netuid, your_hotkey):
    """Check if your validator is still #1. Returns alert dict or None."""
    
    validators = get_validators_for_subnet(netuid)
    
    if not validators:
        print(f"Subnet {netuid}: No validators found")
        return None
    
    # #1 validator
    number_one = validators[0]
    
    # Find YOUR validator
    your_validator = None
    for v in validators:
        if v["hotkey"]["ss58"] == your_hotkey:
            your_validator = v
            break
    
    if not your_validator:
        print(f"Subnet {netuid}: Your validator not found")
        return None
    
    your_apy = float(your_validator["thirty_day_apy"]) * 100
    top_apy = float(number_one["thirty_day_apy"]) * 100
    difference = top_apy - your_apy
    
    print(f"Subnet {netuid}: Your APY={your_apy:.2f}% | #1 APY={top_apy:.2f}% | Diff={difference:.2f}%")
    
    # Return alert if you're not #1 AND difference is above threshold
    if number_one["hotkey"]["ss58"] != your_hotkey and difference >= APY_THRESHOLD_PERCENT:
        return {
            "netuid": netuid,
            "your_name": your_validator.get("name") or your_hotkey,
            "your_apy": your_apy,
            "new_name": number_one.get("name") or number_one["hotkey"]["ss58"],
            "new_hotkey": number_one["hotkey"]["ss58"],
            "new_apy": top_apy,
            "difference": difference
        }
    
    return None


def main():
    print("Checking validator positions...\n")
    
    alerts = []  # Collect all alerts here
    subnets = list(MY_VALIDATORS.items())
    
    for i, (netuid, your_hotkey) in enumerate(subnets):
        try:
            alert = check_subnet(netuid, your_hotkey)
            if alert:
                alerts.append(alert)
        except Exception as e:
            print(f"ERROR on subnet {netuid}: {e}")
        
        # Wait 13 seconds between calls EXCEPT after last one
        if i < len(subnets) - 1:
            print(f"Waiting 13 seconds (API rate limit)...")
            time.sleep(13)
    
    # Send ONE email with everything
    if alerts:
        send_summary_email(alerts)
    else:
        print("\nAll validators are #1 or within threshold. No email sent.")
    
    print("\nDone.")


if __name__ == "__main__":
    main()
