import requests
from validator_config import TAOSTATS_API_KEY


def get_validators_for_subnet(netuid):
    """
    Fetch all validators for a specific subnet from TaoStats API.
    Returns list of validators sorted by 30-day APY (highest first).
    """
    
    # TaoStats API endpoint
    url = f"https://api.taostats.io/api/dtao/validator/yield/latest/v1?netuid={netuid}"
    
    headers = {
        "accept": "application/json",
        "Authorization": TAOSTATS_API_KEY
    }
    
    try:
        # Make API call
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()  # Raise error if request failed
        
        data = response.json()
        
        # Filter validators for this specific subnet
        subnet_validators = []
        for validator in data["data"]:
            if validator["netuid"] == netuid:
                subnet_validators.append(validator)
        
        # Sort by 30-day APY (highest first)
        # Convert APY string to float for sorting
        subnet_validators.sort(
            key=lambda v: float(v["thirty_day_apy"]), 
            reverse=True
        )
        
        return subnet_validators
    
    except requests.exceptions.RequestException as e:
        print(f"ERROR fetching data for subnet {netuid}: {e}")
        return []
    except Exception as e:
        print(f"ERROR processing data for subnet {netuid}: {e}")
        return []


# Test function (you can run this to verify it works)
if __name__ == "__main__":
    # Test with subnet 93
    validators = get_validators_for_subnet(93)
    
    if validators:
        print(f"Found {len(validators)} validators on subnet 93")
        print(f"\nTop 3 validators by 30-day APY:")
        for i, val in enumerate(validators[:3], 1):
            name = val.get("name") or "Unknown"
            apy = float(val["thirty_day_apy"]) * 100  # Convert to percentage
            hotkey = val["hotkey"]["ss58"][:10]  # First 10 chars
            print(f"{i}. {name} ({hotkey}...) - {apy:.2f}%")
    else:
        print("No validators found or API error")
