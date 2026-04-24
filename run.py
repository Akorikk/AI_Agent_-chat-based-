from agent.agent import Agent

agent = Agent()

print(agent.next("hi")["message"])

while True:
    user_input = input("You: ")
    response = agent.next(user_input)
    print("Agent:", response["message"])