from fastapi import FastAPI
from pydantic import BaseModel
from agent import ask_with_tools
from db import init_db, load_messages, save_message

app = FastAPI()
init_db()
DEFAULT_PERSONA = "你是一个猫娘，回答问题时最后一个字要带上喵。"


class ChatIn(BaseModel):
    message: str        #用来校验，别人传来的的json格式必须为{"message":"str"}
    session_id: str = "default"

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/chat")
def chat_api(body: ChatIn):
    history =  load_messages(body.session_id)
    if not history:
        history.append({"role": "system", "content": DEFAULT_PERSONA})
        save_message(body.session_id, "system", DEFAULT_PERSONA)
    answer = ask_with_tools(body.message, history)
    save_message(body.session_id, "user", body.message)
    save_message(body.session_id, "assistant", answer)
    return{"reply":answer}

    