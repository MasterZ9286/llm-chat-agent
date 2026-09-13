import json
from datetime import datetime
from llm import call_model

def get_time():
    """返回当前时间字符串"""
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def get_weather(city):
    """假装查天气"""
    return f"{city}今天晴，30°"

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "获取当前日期和时间",
            "parameters": {"type": "object", "properties":{}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询指定城市的天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名称，如 “武汉”"}
                },
                "required": ["city"]
            }
        }
    }
]

TOOL_FUNCS = {"get_time":get_time, "get_weather": get_weather}

def ask_with_tools(user_text,messages):
    messages.append({"role":"user","content":user_text})

    max_rounds = 5
    round_count = 0

    while True:
        round_count += 1
        if round_count > max_rounds:
            return "(工具调用太多次，已停止)"

        msg = call_model(messages, tools=TOOLS)       
        if msg is None:
            return "(请求出错，请看上方错误信息)"
        if not msg.get("tool_calls"): return msg["content"]
        messages.append(msg)
        #找工具用
        for tc in msg["tool_calls"]:
            name = tc["function"]["name"]
            args = json.loads(tc["function"]["arguments"])
            result = TOOL_FUNCS[name](**args) #name就在45行，别忘了
            messages.append({"role": "tool", "tool_call_id": tc["id"], "content": str(result)})

if __name__ == "__main__":
    messages = [{"role": "system", "content": "你是一个猫娘，回答问题时最后一个字要带上喵。"}]
    print("输入/exit退出")
    while True:
        text = input("你：")
        if not text.strip():
            continue
        if text == "/exit":
            break
        print(f"AI:", ask_with_tools(text, messages))
