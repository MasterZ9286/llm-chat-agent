# llm-chat-agent

一个**不依赖任何 Agent 框架**（无需 LangChain / LangGraph）的大模型应用示例项目。

代码量小、结构清晰、依赖极少，适合用来理解 LLM 应用的三条主线：**多轮对话、HTTP 服务化、工具调用（Agent 循环）**。

## 特性

- **三个入口，共用一套核心**：终端聊天、HTTP 接口、工具调用 Agent
- **手写 tool calling 循环**：模型决定调用哪个本地函数 → 本地执行 → 结果回传 → 生成回答，全流程透明，无黑盒
- **多工具 + 多轮工具调用**：一次请求可触发多个工具，带轮次上限保护
- **分层设计**：配置 / 模型通信 / 交互逻辑彼此独立
- **错误可读**：请求失败返回中文提示而非抛出 Traceback
- **密钥不落源码**：API Key 仅从环境变量读取
- **兼容任意 OpenAI 格式的模型服务**：改两行配置即可切换厂商

## 快速开始

### 1. 安装依赖

```bash
pip install requests fastapi uvicorn
```

### 2. 配置 API Key（环境变量）

```bash
# Linux / macOS
export ZHIPU_API_KEY="your-api-key"

# Windows PowerShell（临时）
$env:ZHIPU_API_KEY="your-api-key"

# Windows（永久，之后需重开终端）
setx ZHIPU_API_KEY "your-api-key"
```

### 3. 运行

```bash
# ① 终端聊天
python chat.py

# ② HTTP 服务（浏览器打开 http://127.0.0.1:8000/docs 可交互试用）
uvicorn api:app --reload

# ③ 工具调用 Agent
python agent.py
```

## 使用示例

**终端聊天 / 工具调用**

```
你：你好
AI：你好喵！有什么可以帮助你的吗？

你：现在几点
AI：现在是2026年9月10日22点37分24秒喵。

你：北京和武汉的天气
AI：北京今天晴，30°，武汉也是晴，30°喵。      ← 一次调用两个工具
```

**HTTP 接口**

```bash
curl http://127.0.0.1:8000/health
# {"status":"ok"}

curl -X POST http://127.0.0.1:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"message":"你好"}'
# {"reply":"你好喵！"}
```

## 工作原理：工具调用循环

```
用户提问
   │
   ▼
发送请求（messages + tools 工具清单）
   │
   ▼
模型返回 tool_calls？ ──否──► 返回文字回答，结束
   │
   是
   ▼
查表执行本地函数（TOOL_FUNCS[name](**args)）
   │
   ▼
把执行结果以 role="tool" 写回 messages
   │
   └──────► 回到顶部，再次请求模型（最多 5 轮）
```

关键点：**模型只负责"决定调用哪个函数"，真正的执行发生在本进程内。** 执行结果必须写回对话历史，模型才知道发生了什么。

## 项目结构

```
.
├── config.py    # 配置层：API 地址、模型名、读取环境变量、请求头
├── llm.py       # 模型层：call_model() 发送请求；ask() 单轮对话
├── chat.py      # 入口：终端交互，多轮记忆、人设切换
├── api.py       # 入口：FastAPI 服务，GET /health、POST /chat
├── agent.py     # 入口：工具清单 + 工具调用循环
└── README.md
```

**依赖方向是单向的**，上层只需知道下层的接口：

```
chat.py / api.py / agent.py  →  llm.py  →  config.py
```

## 配置其他模型

默认使用智谱 `glm-4-flash`。只要目标服务兼容 OpenAI 的 `/chat/completions` 协议，改 `config.py` 两行即可切换：

```python
# config.py
URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"   # 服务商地址
MODEL = "glm-4-flash"                                            # 模型名
```

| 服务商 | URL | MODEL |
|---|---|---|
| 智谱（默认） | `https://open.bigmodel.cn/api/paas/v4/chat/completions` | `glm-4-flash` |
| OpenAI | `https://api.openai.com/v1/chat/completions` | `gpt-4o-mini` |
| DeepSeek | `https://api.deepseek.com/chat/completions` | `deepseek-chat` |
| 阿里通义 | `https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions` | `qwen-plus` |
| 本地 Ollama | `http://localhost:11434/v1/chat/completions` | `qwen2.5` |

## 添加自定义工具

1. 写一个普通 Python 函数（返回值会被转成字符串回传给模型）
2. 在 `TOOLS` 里描述它的名称、用途、参数（**描述写得越清楚，模型判断越准**）
3. 在 `TOOL_FUNCS` 里注册名称到函数的映射

```python
def get_weather(city):
    return f"{city}今天晴，30°"

TOOLS = [..., {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "查询指定城市的天气",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string", "description": "城市名称"}},
            "required": ["city"]
        }
    }
}]

TOOL_FUNCS = {"get_weather": get_weather}
```

## 当前限制

- 对话历史保存在**进程内存**中，重启即丢失
- HTTP 服务的所有请求**共用同一份对话历史**，多用户会相互干扰
- 未实现鉴权、限流、并发处理
- 工具调用轮次上限固定为 5

## Roadmap

- [ ] 用 SQLite 持久化对话，按 `session_id` 隔离会话
- [ ] 接入 RAG（检索增强生成）
- [ ] 补充单元测试

## License

MIT
