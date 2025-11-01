# 生活游戏化人生管理系统 MVP

将你的生活目标游戏化，通过 AI 智能拆解任务，获得即时反馈和成就感。

## 功能特点

- 🎮 **游戏化体验**：将现实目标转化为游戏任务
- 🤖 **AI 驱动**：使用 LangChain + GPT-4 智能生成故事和任务
- 📊 **数值系统**：经验值、等级、金币等即时反馈
- 🎨 **黑白像素风格**：复古游戏界面设计
- 💾 **数据持久化**：PostgreSQL 数据库存储

## 技术栈

### 后端
- Python FastAPI
- LangChain
- PostgreSQL
- SQLAlchemy

### 前端
- React + TypeScript
- Vite
- Tailwind CSS
- Zustand (状态管理)

## 快速开始

### 方式 1: 一键启动（推荐）

```bash
# 首次设置（安装所有依赖并启动数据库）
./setup.sh

# 之后每次启动
./start.sh  # 或使用下面的方式 2
```

### 方式 2: 分别启动（便于调试）

**推荐用于开发调试，可以在不同终端窗口查看日志**

```bash
# 首次设置
./setup.sh

# 终端 1 - 启动后端
./start-backend.sh

# 终端 2 - 启动前端（新开一个终端窗口）
./start-frontend.sh
```

### 方式 3: 手动启动

#### 1. 环境要求

- Python 3.10-3.12 (推荐 3.12)
- Node.js 18+
- Docker (用于 PostgreSQL)

#### 2. 启动数据库

```bash
docker-compose up -d
```

#### 3. 配置后端

```bash
cd backend

# 创建虚拟环境（使用 Python 3.10-3.12）
python3.12 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
# 编辑 .env 文件，添加你的 OpenAI API Key
```

#### 4. 启动后端

```bash
cd backend
source venv/bin/activate
python main.py
```

后端将在 `http://localhost:8089` 启动

#### 5. 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端将在 `http://localhost:5173` 启动

### 访问应用

- 🎮 应用主界面：http://localhost:5173
- 📚 API 文档：http://localhost:8089/docs
- 🗄️ 数据库：localhost:5432

## 使用方法

1. **输入目标**：在输入框中描述你的目标，例如："完成简历并海投 20 家公司"
2. **添加背景**（可选）：点击展开背景信息输入框，添加个人信息以获得更个性化的建议
3. **获得故事**：AI 会生成一个游戏化的故事背景
4. **完成任务**：勾选完成的任务，获得经验值和奖励
5. **升级成长**：随着任务完成，角色会升级，数值会增长

## 项目结构

```
person_game/
├── backend/                # 后端 Python 代码
│   ├── main.py            # FastAPI 主应用
│   ├── agent.py           # LangChain AI Agent
│   ├── models.py          # 数据库模型
│   ├── schemas.py         # Pydantic schemas
│   ├── database.py        # 数据库连接
│   └── requirements.txt   # Python 依赖
├── frontend/              # 前端 React 代码
│   ├── src/
│   │   ├── components/    # React 组件
│   │   ├── store/         # Zustand 状态管理
│   │   ├── api/           # API 客户端
│   │   ├── types.ts       # TypeScript 类型定义
│   │   └── App.tsx        # 主应用组件
│   └── package.json       # Node 依赖
├── setup.sh               # 一键安装脚本
├── start.sh               # 启动所有服务
├── start-backend.sh       # 单独启动后端（便于调试）
├── start-frontend.sh      # 单独启动前端（便于调试）
└── docker-compose.yml     # Docker 配置
```

## 开发笔记

### 数据库迁移

如果修改了数据库模型，删除并重新创建数据库：

```bash
# 停止并删除容器和数据
docker-compose down -v

# 重新启动
docker-compose up -d
```

### 环境变量

后端 `.env` 文件配置：

```env
# 使用 OpenRouter (推荐)
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
AI_MODEL=qwen/qwen-max

# 或使用 OpenAI
# OPENAI_API_KEY=your_openai_api_key
# AI_MODEL=gpt-4

DATABASE_URL=postgresql://gameuser:gamepass@localhost:5432/life_game_db
```

### 自定义数值系统

AI Agent 会自动根据目标生成合适的数值类型。你可以在 `backend/agent.py` 中修改提示词来自定义数值系统的行为。

## 故障排除

### 数据库连接失败

确保 PostgreSQL 容器正在运行：
```bash
docker-compose ps
docker-compose logs postgres
```

### 前端无法连接后端

检查后端是否在 8000 端口运行，前端代理配置在 `frontend/vite.config.ts` 中。

### AI 生成失败

确保 `.env` 文件中配置了有效的 OpenAI API Key。

## 后续改进计划

- [ ] 用户认证系统
- [ ] 更丰富的角色动画
- [ ] 成就系统
- [ ] 社交功能（排行榜）
- [ ] 更多游戏元素（技能树、装备系统）
- [ ] 移动端适配
- [ ] 智能眼镜集成

## License

MIT

## 贡献

欢迎提交 Issue 和 Pull Request！

