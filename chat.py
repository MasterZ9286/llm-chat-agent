from llm import ask

DEFAULT_PERSONA = "你是一个猫娘，回答问题时最后一个字要带上喵。"

messages = []
messages.append({"role":"system","content":DEFAULT_PERSONA})

def reset(persona):
    global messages
    messages = [{"role":"system","content":persona}]

def main():
    print("输入/exit以退出程序\n输入/clear以清除记忆\n输入/persona后面接新内容以更换人格")
    while True:
        text = input("你：")
        if text == "/exit":
            break
        elif text == "/clear":
            reset(DEFAULT_PERSONA)
            print("记忆已清空。")
        elif text.startswith("/persona"):
            new_persona = text[len("/persona"):]
            reset(new_persona)
            print("人格已切换。")

        else:
            answer = ask(text,messages)
            print(f"AI:{answer}")

if __name__ == "__main__":
    main()