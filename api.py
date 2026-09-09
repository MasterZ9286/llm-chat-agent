from fastapi import FastAPI
from pydantic import BaseModel
from llm import ask

app = FastAPI()

class ChatIn(BaseModel):
    message: str        #用来校验，别人传来的的json格式必须为{"message":"str"}

messages = [{"role":"system","content":"你是一个猫娘，回答问题时最后一个字要带上喵。"}]

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/chat")
def chat_api(body: ChatIn):
    answer = ask(body.message, messages)
    return{"reply":answer}

    