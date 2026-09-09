import json
import requests
from datetime import datetime
from config import URL, MODEL, headers

def get_time():
    """返回当前时间字符串"""
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "获取当前日期和时间",
            "parameters": {"type": "object", "properties":{}}
        }
    }
]

TOOL_FUNCS = {"get_time":get_time}

def ask_with_tools(user_text,messages):
    messages.append({"role":"user","content":user_text})

    while True:
        data = {
            "model": MODEL,
            "messages": messages,
            "tools": TOOLS 
        }

        resp = requests.post(URL, headers=headers, json=data)

        if resp.status_code != 200:
            print("请求失败：", resp.status_code, resp.text[:200])
            return ("请求出错")

        msg = resp.json()["choices"][0]["message"]

        if not msg.get("tool_calls"): return msg["content"]

        """因为我们的tool只有一个，所以这个循环其实是个假的，实际上就一次循环"""
        for tc in msg["tool_calls"]:
            name = tc["function"]["name"]
            args = json.loads(tc["function"]["arguments"])
            result = TOOL_FUNCS[name]() #name就在45行，别忘了
            messages.append({"role": "tool", "tool_call_id": tc["id"], "content": str(result)})

if __name__ == "__main__":
    messages = [{"role": "system", "content": "你是一个猫娘，回答问题时最后一个字要带上喵。"}]
    print(ask_with_tools("现在几点",messages))
    print(ask_with_tools("你好呀",messages))
