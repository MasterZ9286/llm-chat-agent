import requests
from config import URL,MODEL,headers

"""call_model被ask和ask_with_tool调用"""
def call_model(messages,tools = None):
    data = {
        "model": MODEL,
        "messages":messages,
    }
    if tools is not None:
        data["tools"] = tools

    resp = requests.post(URL, headers=headers, json=data)
    if resp.status_code != 200:
        print(f"状态码:{resp.status_code}\n错误信息:{resp.text}" )
        return None
    result = resp.json()
    return result["choices"][0]["message"]

def ask(user_text,messages):
    messages.append({"role":"user","content":user_text})
   
    msg = call_model(messages)
    if msg is None:
        return "(请求出错，请看上方错误信息)"

    content = msg["content"]

    messages.append({"role":"assistant","content":content})

    return content
