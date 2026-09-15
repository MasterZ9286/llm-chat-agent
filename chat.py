from llm import ask
from db import init_db, load_messages, save_message, clear_messages

DEFAULT_PERSONA = "你是一个猫娘，回答问题时最后一个字要带上喵。"
SESSION_ID = "ZK"


def main():
    init_db()
    messages = load_messages(SESSION_ID)
    if not messages:
        messages.append({"role": "system", "content": DEFAULT_PERSONA})
        save_message(SESSION_ID, "system", DEFAULT_PERSONA)
    print("输入/exit以退出程序\n输入/clear以清除记忆\n输入/persona后面接新内容以更换人格")
    while True:
        text = input("你：")
        if not text.strip():
            continue
        if text == "/exit":
            break
        elif text == "/clear":
            messages = [{"role": "system", "content": DEFAULT_PERSONA}]
            clear_messages(SESSION_ID)
            save_message(SESSION_ID, "system", DEFAULT_PERSONA)
            print("记忆已清空。")
        elif text.startswith("/persona"):
            new_persona = text[len("/persona"):]
            messages = [{"role": "system", "content": new_persona}]
            print("人格已切换。")

        else:
            answer = ask(text,messages)
            save_message(SESSION_ID, "user", text)
            save_message(SESSION_ID, "assistant", answer)
            print(f"AI:{answer}")

if __name__ == "__main__":
    main()