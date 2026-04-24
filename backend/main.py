from fastapi import FastAPI
from pydantic import BaseModel
from agent.agent import Agent

app = FastAPI()

agent = Agent(debug=False)


class UserInput(BaseModel):
    message: str


@app.post("/chat")
def chat(input: UserInput):
    response = agent.next(input.message)
    return response