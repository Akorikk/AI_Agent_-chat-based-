import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Use env variable, fallback to default
BASE_URL = os.getenv("BASE_URL")

if not BASE_URL:
    BASE_URL = "https://se-payment-verification-api.service.external.usea2.aws.prodigaltech.com"


def lookup_account(account_id):
    try:
        res = requests.post(
            f"{BASE_URL}/api/lookup-account",
            json={"account_id": account_id}
        )
        return res.json(), res.status_code
    except Exception:
        return {"error": "network_error"}, 500


def process_payment(account_id, amount, card):
    try:
        res = requests.post(
            f"{BASE_URL}/api/process-payment",
            json={
                "account_id": account_id,
                "amount": amount,
                "payment_method": {
                    "type": "card",
                    "card": card
                }
            }
        )
        return res.json()
    except Exception:
        return {"success": False, "error_code": "network_error"}