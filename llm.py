import requests
from config import URL,MODEL,headers

def ask(user_text,messages):
    messages.append({"role":"user","content":user_text})
    data = {
        "model" : MODEL,
        "messages" : messages
    }

    resp = requests.post(URL,headers=headers,json=data)

    if resp.status_code != 200:
        print(f"请求失败，状态码：{resp.status_code}")
        print(f"服务器返回{resp.text}")
        return "(请求出错，请看上方报错信息)"

    result = resp.json()
    answer = result["choices"][0]["message"]["content"]

    messages.append({"role":"assistant","content":answer})

    return answer
