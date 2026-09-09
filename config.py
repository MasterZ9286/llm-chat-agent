import os

URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
MODEL = "glm-4-flash"

try:
    MY_KEY = os.environ["ZHIPU_API_KEY"]
except KeyError:
    print("没找到ZHIPU_API_KEY,请设置环境变量")
    raise SystemExit(1)

headers = {
    "Authorization":f"Bearer {MY_KEY}",
    "Content-Type":"application/json"
}