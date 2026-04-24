import requests

BASE_URL = "https://se-payment-verification-api.service.external.usea2.aws.prodigaltech.com"


def lookup_account(account_id):
    try:
        response = requests.post(
            f"{BASE_URL}/api/lookup-account",
            json={"account_id": account_id}
        )
        return response.json(), response.status_code
    except:
        return {"error": "network_error"}, 500


def process_payment(account_id, amount, card):
    try:
        response = requests.post(
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
        return response.json()
    except:
        return {"success": False, "error_code": "network_error"}