# OpenRouter 配置指南

本项目已配置使用 [OpenRouter](https://openrouter.ai) 作为 AI Provider。OpenRouter 是一个统一的 AI API 网关，支持访问多种 AI 模型。

## 为什么选择 OpenRouter？

1. **多模型支持**：一个 API 访问 Claude、GPT、Qwen 等多种模型
2. **价格实惠**：按需付费，通常比直接调用官方 API 更便宜
3. **国内友好**：访问速度较好，不需要特殊网络配置
4. **灵活切换**：轻松切换不同模型进行测试

## 已配置的信息

根据您提供的配置，系统已设置为：

```env
OPENROUTER_API_KEY=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
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
AI_MODEL=qwen/qwen-max
```

## 配置文件位置

编辑 `backend/.env` 文件（已创建），内容如下：

```env
# ===== AI Provider 配置 =====
OPENROUTER_API_KEY=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
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
AI_MODEL=qwen/qwen-max

# ===== 数据库配置 =====
DATABASE_URL=postgresql://gameuser:gamepass@localhost:5432/life_game_db
```

## 支持的模型

您可以在 `.env` 文件中修改 `AI_MODEL` 来切换不同模型：

### 推荐模型

**Qwen 系列** (阿里通义千问)：
- `qwen/qwen-max` - 最强版本，推荐使用
- `qwen/qwen-plus` - 平衡性能和成本
- `qwen/qwen-turbo` - 快速响应

**OpenAI 系列**：
- `openai/gpt-4` - 强大但较贵
- `openai/gpt-3.5-turbo` - 快速且便宜

**Anthropic Claude**：
- `anthropic/claude-3-opus` - 最强版本
- `anthropic/claude-3-sonnet` - 推荐性价比
- `anthropic/claude-3-haiku` - 最快最便宜

**Meta Llama**：
- `meta-llama/llama-3-70b-instruct`
- `meta-llama/llama-3-8b-instruct`

完整模型列表：https://openrouter.ai/models

## 价格参考

根据 OpenRouter 官网（截至 2025 年）：

- **qwen/qwen-max**: ~$0.02-0.04 / 1K tokens
- **gpt-3.5-turbo**: ~$0.0015 / 1K tokens  
- **gpt-4**: ~$0.03 / 1K tokens
- **claude-3-sonnet**: ~$0.003 / 1K tokens

每次任务拆解大约消耗 500-1000 tokens，成本约 $0.001-0.04

## 测试配置

启动后端后，可以通过以下方式测试：

```bash
# 启动后端
cd backend
source venv/bin/activate
python main.py

# 在另一个终端测试 API
curl -X POST http://localhost:8089/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"测试用户"}'

# 测试 AI 生成
curl -X POST http://localhost:8089/api/goals \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"goal_text":"学习 Python 编程"}'
```

## 切换到其他 Provider

### 方案 1: 使用 OpenAI 官方

修改 `backend/.env`：
```env
# 注释掉 OpenRouter 配置
# OPENROUTER_API_KEY=...
# OPENROUTER_BASE_URL=...

# 使用 OpenAI
OPENAI_API_KEY=sk-your-openai-key
AI_MODEL=gpt-4
```

### 方案 2: 使用 Anthropic Claude

安装额外依赖：
```bash
pip install langchain-anthropic
```

修改 `backend/agent.py`：
```python
from langchain_anthropic import ChatAnthropic

self.llm = ChatAnthropic(
    model="claude-3-sonnet-20240229",
    api_key=os.getenv("ANTHROPIC_API_KEY")
)
```

## 监控使用情况

1. 访问 [OpenRouter Dashboard](https://openrouter.ai/dashboard)
2. 查看 API 调用次数和消耗
3. 设置预算上限防止超支

## 常见问题

### Q: API Key 无效
A: 
1. 检查 Key 是否以 `sk-or-v1-` 开头
2. 确认账户有余额
3. 访问 https://openrouter.ai/keys 重新生成

### Q: 模型响应慢
A: 
1. 尝试切换到更快的模型（如 qwen-turbo）
2. 检查网络连接
3. 查看 OpenRouter 状态页：https://openrouter.ai/status

### Q: 返回格式错误
A: 
某些模型可能不太擅长生成结构化 JSON，推荐使用：
- qwen/qwen-max
- openai/gpt-4
- anthropic/claude-3-sonnet

### Q: 想要更便宜的方案
A: 
1. 使用 `qwen/qwen-turbo` 或 `openai/gpt-3.5-turbo`
2. 减少 prompt 长度
3. 调整 temperature 参数

## 获取 API Key

如果您还没有 OpenRouter API Key：

1. 访问 https://openrouter.ai
2. 注册账户
3. 进入 [Keys](https://openrouter.ai/keys) 页面
4. 创建新的 API Key
5. 复制并保存到 `backend/.env`

## 安全提示

⚠️ **重要**：
- 不要将 `.env` 文件提交到 Git
- 不要在公开场合分享 API Key
- 定期轮换 API Key
- 设置使用限额

## 参考链接

- [OpenRouter 官网](https://openrouter.ai)
- [OpenRouter 文档](https://openrouter.ai/docs)
- [模型列表](https://openrouter.ai/models)
- [价格计算器](https://openrouter.ai/models)
- [Discord 社区](https://discord.gg/fVyRaUDgxW)

