from utils.state import State

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

        # Retry guard
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

        return {"message": "Unhandled state."}