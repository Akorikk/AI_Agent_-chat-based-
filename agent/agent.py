from utils.state import State
from api.client import lookup_account, process_payment
import re


class Agent:
    def __init__(self):
        self.state = State.START
        self.context = {
            "account": None,
            "verified": False,
            "retries": 0,
            "amount": None,
            "card": {}
        }
        self.max_retries = 3

    def next(self, user_input: str) -> dict:
        user_input = user_input.strip()

        # Retry limit
        if self.context["retries"] >= self.max_retries:
            self.state = State.END
            return {"message": "Too many failed attempts. Session ended."}

        if self.state == State.START:
            return self._handle_start()

        elif self.state == State.ASK_ACCOUNT_ID:
            return self._handle_account(user_input)

        elif self.state == State.VERIFY_NAME:
            return self._handle_name(user_input)

        elif self.state == State.VERIFY_SECONDARY:
            return self._handle_secondary(user_input)

        elif self.state == State.SHOW_BALANCE:
            return self._handle_amount(user_input)

        elif self.state == State.CARD_NUMBER:
            return self._handle_card_number(user_input)

        elif self.state == State.CARD_NAME:
            return self._handle_card_name(user_input)

        elif self.state == State.CARD_CVV:
            return self._handle_card_cvv(user_input)

        elif self.state == State.CARD_EXPIRY:
            return self._handle_card_expiry(user_input)

        return {"message": "Session ended."}
    
    

    def _handle_start(self):
        self.state = State.ASK_ACCOUNT_ID
        return {"message": "Hello! Please share your account ID."}

    def _handle_account(self, user_input):
        data, status = lookup_account(user_input.upper())

        if status == 200:
            self.context["account"] = data
            self.state = State.VERIFY_NAME
            return {"message": "Got it. Please confirm your full name."}
        else:
            return {"message": "Account not found. Try again."}

    def _handle_name(self, user_input):
        account = self.context["account"]

        if user_input == account["full_name"]:
            self.state = State.VERIFY_SECONDARY
            return {
                "message": "Name verified. Provide DOB (YYYY-MM-DD) OR Aadhaar last 4 OR pincode."
            }
        else:
            self.context["retries"] += 1
            return {"message": "Name mismatch. Try again."}

    def _handle_secondary(self, user_input):
        account = self.context["account"]

        if user_input in [
            account["dob"],
            account["aadhaar_last4"],
            account["pincode"]
        ]:
            self.context["verified"] = True
            self.state = State.SHOW_BALANCE

            return {
                "message": f"Verification successful. Your balance is ₹{account['balance']}. Enter amount to pay."
            }
        else:
            self.context["retries"] += 1
            return {"message": "Verification failed. Try again."}

    def _handle_amount(self, user_input):
        try:
            amount = float(user_input)
        except:
            return {"message": "Invalid amount. Enter a number."}

        if amount <= 0:
            return {"message": "Amount must be greater than zero."}

        if amount > self.context["account"]["balance"]:
            return {"message": "Amount exceeds outstanding balance."}

        self.context["amount"] = amount
        self.state = State.CARD_NUMBER

        return {"message": "Enter card number:"}

    def _handle_card_number(self, user_input):
        if not user_input.isdigit() or len(user_input) < 13:
            return {"message": "Invalid card number."}

        self.context["card"]["card_number"] = user_input
        self.state = State.CARD_NAME

        return {"message": "Enter cardholder name:"}

    def _handle_card_name(self, user_input):
        self.context["card"]["cardholder_name"] = user_input
        self.state = State.CARD_CVV

        return {"message": "Enter CVV:"}

    def _handle_card_cvv(self, user_input):
        if not re.fullmatch(r"\d{3,4}", user_input):
            return {"message": "Invalid CVV."}

        self.context["card"]["cvv"] = user_input
        self.state = State.CARD_EXPIRY

        return {"message": "Enter expiry (MM YYYY):"}

    def _handle_card_expiry(self, user_input):
        try:
            month, year = user_input.split()
            month = int(month)
            year = int(year)
        except:
            return {"message": "Invalid expiry format. Use MM YYYY."}

        self.context["card"]["expiry_month"] = month
        self.context["card"]["expiry_year"] = year

        result = process_payment(
            self.context["account"]["account_id"],
            self.context["amount"],
            self.context["card"]
        )

        if result.get("success"):
            self.state = State.END
            return {
                "message": f"Payment successful! Transaction ID: {result['transaction_id']}"
            }
        else:
            return {
                "message": f"Payment failed: {result.get('error_code', 'unknown error')}"
            }