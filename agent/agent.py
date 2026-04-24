from utils.state import State
from api.client import lookup_account, process_payment
import re


class Agent:
    def __init__(self, debug=False):
        self.state = State.START
        self.debug = debug
        self.context = {
            "account": None,
            "verified": False,
            "retries": 0,
            "amount": None,
            "card": {}
        }
        self.max_retries = 3

    # ---------- ENTITY EXTRACTION ----------
    def _extract_entities(self, text):
        data = {}

        match = re.search(r'ACC\d+', text.upper())
        if match:
            data["account_id"] = match.group()

        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
            data["dob"] = text

        if re.fullmatch(r"\d{4}", text):
            data["aadhaar"] = text

        if re.fullmatch(r"\d{6}", text):
            data["pincode"] = text

        try:
            data["amount"] = float(text)
        except:
            pass

        return data

    # ---------- RESPONSE ----------
    def _response(self, message):
        return {
            "message": message,
            "state": self.state.value
        }

    # ---------- MAIN ----------
    def next(self, user_input: str) -> dict:
        user_input = user_input.strip()

        # Debug logging (OFF by default)
        if self.debug:
            print(f"[STATE] {self.state}")

        # Retry guard
        if self.context["retries"] >= self.max_retries:
            self.state = State.END
            return self._response("Too many failed attempts. Session ended.")

        # Extract entities
        entities = self._extract_entities(user_input)

        # Out-of-order account handling
        if entities.get("account_id") and not self.context["account"]:
            return self._handle_account(entities["account_id"])

        if self.state == State.START:
            return self._handle_start()

        elif self.state == State.ASK_ACCOUNT_ID:
            return self._handle_account(user_input)

        elif self.state == State.VERIFY_NAME:
            return self._handle_name(user_input)

        elif self.state == State.VERIFY_SECONDARY:
            return self._handle_secondary(user_input)

        elif self.state == State.SHOW_BALANCE:
            return self._handle_amount(user_input, entities)

        elif self.state == State.CARD_NUMBER:
            return self._handle_card_number(user_input)

        elif self.state == State.CARD_NAME:
            return self._handle_card_name(user_input)

        elif self.state == State.CARD_CVV:
            return self._handle_card_cvv(user_input)

        elif self.state == State.CARD_EXPIRY:
            return self._handle_card_expiry(user_input)

        return self._response("Session ended.")

    # ---------- STATES ----------

    def _handle_start(self):
        self.state = State.ASK_ACCOUNT_ID
        return self._response("Hello! Please share your account ID.")

    def _handle_account(self, user_input):
        match = re.search(r'ACC\d+', user_input.upper())

        if not match:
            return self._response("Please provide a valid account ID (e.g., ACC1001).")

        account_id = match.group()

        data, status = lookup_account(account_id)

        if status == 200:
            self.context["account"] = data
            self.context["retries"] = 0
            self.state = State.VERIFY_NAME
            return self._response("Got it. Please confirm your full name.")
        else:
            return self._response("Account not found. Try again.")

    def _handle_name(self, user_input):
        account = self.context["account"]

        if user_input == account["full_name"]:
            self.context["retries"] = 0
            self.state = State.VERIFY_SECONDARY
            return self._response("Name verified. Provide DOB (YYYY-MM-DD) OR Aadhaar last 4 OR pincode.")
        else:
            self.context["retries"] += 1
            if self.context["retries"] >= self.max_retries:
                self.state = State.END
                return self._response("Too many failed attempts. Session ended.")
            return self._response("Name mismatch. Try again.")

    def _handle_secondary(self, user_input):
        account = self.context["account"]

        if user_input in [
            account["dob"],
            account["aadhaar_last4"],
            account["pincode"]
        ]:
            self.context["verified"] = True
            self.context["retries"] = 0

            if account["balance"] == 0:
                self.state = State.END
                return self._response("Your balance is ₹0. No payment required.")

            self.state = State.SHOW_BALANCE
            return self._response(f"Verification successful. Balance ₹{account['balance']}. Enter amount.")
        else:
            self.context["retries"] += 1
            if self.context["retries"] >= self.max_retries:
                self.state = State.END
                return self._response("Too many failed attempts. Session ended.")
            return self._response("Verification failed. Try again.")

    def _handle_amount(self, user_input, entities):
        if entities.get("amount"):
            amount = float(entities["amount"])
        else:
            try:
                amount = float(user_input)
            except:
                return self._response("Invalid amount.")

        if amount <= 0:
            return self._response("Amount must be greater than zero.")

        if amount > self.context["account"]["balance"]:
            return self._response("Amount exceeds balance.")

        self.context["amount"] = amount
        self.state = State.CARD_NUMBER

        return self._response("Enter card number:")

    def _handle_card_number(self, user_input):
        if not user_input.isdigit() or len(user_input) not in [13, 15, 16]:
            return self._response("Invalid card number.")

        self.context["card"]["card_number"] = user_input
        self.state = State.CARD_NAME

        return self._response("Enter cardholder name:")

    def _handle_card_name(self, user_input):
        self.context["card"]["cardholder_name"] = user_input
        self.state = State.CARD_CVV

        return self._response("Enter CVV:")

    def _handle_card_cvv(self, user_input):
        if not re.fullmatch(r"\d{3,4}", user_input):
            return self._response("Invalid CVV.")

        self.context["card"]["cvv"] = user_input
        self.state = State.CARD_EXPIRY

        return self._response("Enter expiry (MM YYYY):")

    def _handle_card_expiry(self, user_input):
        try:
            month, year = user_input.split()
            month = int(month)
            year = int(year)

            if month < 1 or month > 12:
                return self._response("Invalid month.")
        except:
            return self._response("Invalid expiry format.")

        self.context["card"]["expiry_month"] = month
        self.context["card"]["expiry_year"] = year

        result = process_payment(
            self.context["account"]["account_id"],
            self.context["amount"],
            self.context["card"]
        )

        if result.get("success"):
            self.state = State.END
            return self._response(f"Payment successful! Txn: {result['transaction_id']}")

        elif result.get("error_code") == "invalid_card":
            self.state = State.CARD_NUMBER
            return self._response("Invalid card. Please re-enter your card number.")

        else:
            return self._response(f"Payment failed: {result.get('error_code')}")