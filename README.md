# 从零手写的 LLM 聊天程序 + Agent 工具调用

一个**不用任何 Agent 框架**（没用 LangChain / LangGraph）的大模型应用练习项目。

从最基础的 API 调用开始，一步步加功能，每一步都跑通、都能讲清楚：

```
调通 API → 多轮对话 → 人设(system prompt) → 函数封装 → 环境变量管理
   → 异常处理 → 拆成多文件 → HTTP 接口(FastAPI) → 工具调用循环(Agent)
```

## 这是什么

三个入口，共用一套核心逻辑（`config.py` + `llm.py`）：

| 入口 | 用途 | 怎么跑 |
|---|---|---|
| `chat.py` | 终端聊天：多轮记忆、切换人设、清空记忆 | `python chat.py` |
| `api.py` | HTTP 接口：把聊天能力变成可被任何程序调用的服务 | `uvicorn api:app --reload` |
| `agent.py` | 工具调用：模型自己决定何时调用本地函数 | `python agent.py` |

## 文件结构

```
project1/
├── config.py    # 配置层：API 地址、模型名、从环境变量读 key、请求头
├── llm.py       # 模型层：ask(user_text, messages) —— 只管跟模型说话
├── chat.py      # 终端入口：messages、人设、命令、主循环
├── api.py       # HTTP 入口：GET /health、POST /chat
└── agent.py     # Agent 入口：工具清单 + 工具调用循环
```

**依赖方向是单向的**：`入口文件 → llm.py → config.py`。上层只管调用，不关心 key 从哪来、连哪个地址。

## 快速开始

**1. 装依赖**

```bash
pip install requests fastapi uvicorn
```

**2. 设置 API key（从环境变量读，不写进代码）**

```powershell
# Windows PowerShell
$env:ZHIPU_API_KEY="你的智谱APIKey"

# 或永久设置
setx ZHIPU_API_KEY "你的智谱APIKey"
```

**3. 运行**

```bash
# 终端聊天
python chat.py

# HTTP 服务（然后浏览器打开 http://127.0.0.1:8000/docs 试用）
uvicorn api:app --reload

# 工具调用
python agent.py
```

## 换成其他模型（不限于智谱）

默认使用智谱的 `glm-4-flash`，但**代码没有绑定任何厂商**。只要目标服务的接口兼容 OpenAI 的 `/chat/completions` 格式（目前绝大多数大模型服务都兼容），改 `config.py` 两行就能切换：

```python
# config.py
URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"  # ← 改这里：服务商地址
MODEL = "glm-4-flash"                                           # ← 改这里：模型名
```

例如：

| 服务商 | URL | MODEL |
|---|---|---|
| 智谱（默认） | `https://open.bigmodel.cn/api/paas/v4/chat/completions` | `glm-4-flash` |
| OpenAI | `https://api.openai.com/v1/chat/completions` | `gpt-4o-mini` |
| DeepSeek | `https://api.deepseek.com/chat/completions` | `deepseek-chat` |
| 阿里通义 | `https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions` | `qwen-plus` |
| 本地 Ollama | `http://localhost:11434/v1/chat/completions` | `qwen2.5` |

同时把环境变量名和读取的 key 一起改掉即可：

```python
MY_KEY = os.environ["你的环境变量名"]
```

**为什么能这样**：`llm.py` 里发请求的格式（`messages`、`tools`、`tool_calls`）就是 OpenAI 定的通用协议，各家基本都照抄。所以换服务商 = 换地址和名字，业务代码一行不用动。

## 技术点

- **手写 tool calling 循环**：`模型返回 tool_calls → 查表执行本地函数 → 结果写回 messages → 再请求模型`，完整闭环没有依赖框架
- **消息历史管理**：`messages` 作为参数传递，让 `llm.py` 保持无状态、可复用
- **分层设计**：配置 / 模型通信 / 交互逻辑分离，加新入口不用改核心
- **失败说人话**：`status_code` 检查和 `try/except`，错误时给中文提示而不是抛 Traceback
- **key 不进源码**：只从环境变量读取

## 已知局限

- 记忆存在内存里，**重启服务就丢**
- HTTP 服务的所有请求**共用一份对话记忆**（多人会串台）
- 目前只有一个工具（`get_time`）

## 下一步计划

- [ ] 加第二个带参数的工具（如 `get_weather(city)`）
- [ ] 用 SQLite 持久化对话，按 `session_id` 隔离会话
- [ ] 接 RAG（检索增强）

## 说明

这是一个**学习项目**，记录我从零开始学大模型应用开发的过程。代码是一行一行自己写的，每个概念都要求能讲清楚才往下走。
