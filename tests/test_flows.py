from agent.agent import Agent


def run_success_flow():
    print("\n=== SUCCESS FLOW ===")
    agent = Agent()

    print(agent.next("hi"))
    print(agent.next("ACC1001"))
    print(agent.next("Nithin Jain"))
    print(agent.next("1990-05-14"))
    print(agent.next("500"))
    print(agent.next("4532015112830366"))
    print(agent.next("Nithin Jain"))
    print(agent.next("123"))
    print(agent.next("12 2027"))


def run_verification_failure():
    print("\n=== VERIFICATION FAILURE ===")
    agent = Agent()

    print(agent.next("hi"))
    print(agent.next("ACC1001"))
    print(agent.next("Wrong Name"))
    print(agent.next("Wrong Name"))
    print(agent.next("Wrong Name"))


def run_zero_balance():
    print("\n=== ZERO BALANCE ===")
    agent = Agent()

    print(agent.next("hi"))
    print(agent.next("ACC1003"))
    print(agent.next("Priya Agarwal"))
    print(agent.next("1992-08-10"))


def run_payment_failure():
    print("\n=== PAYMENT FAILURE ===")
    agent = Agent()

    print(agent.next("hi"))
    print(agent.next("ACC1001"))
    print(agent.next("Nithin Jain"))
    print(agent.next("1990-05-14"))
    print(agent.next("500"))
    print(agent.next("123"))


if __name__ == "__main__":
    run_success_flow()
    run_verification_failure()
    run_zero_balance()
    run_payment_failure()