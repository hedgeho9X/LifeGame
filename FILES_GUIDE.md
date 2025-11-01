# 📁 项目文件说明

## 项目结构一览

```
person_game/
├── 📄 文档文件
│   ├── README.md                   # 项目主文档
│   ├── QUICKSTART.md              # 快速启动指南  
│   ├── PROJECT_OVERVIEW.md        # 项目详细概览
│   ├── PROJECT_COMPLETE.md        # 项目完成总结 ⭐
│   ├── OPENROUTER_SETUP.md        # OpenRouter 配置指南
│   ├── TROUBLESHOOTING.md         # 故障排除指南
│   ├── DEMO.md                    # 演示场景示例
│   └── FILES_GUIDE.md             # 本文件
│
├── 🔧 配置和脚本
│   ├── docker-compose.yml         # Docker 数据库配置
│   ├── .gitignore                 # Git 忽略文件
│   ├── Makefile                   # Make 命令集合
│   ├── setup.sh                   # 环境设置脚本 ⭐
│   ├── start.sh                   # 启动脚本 ⭐
│   └── test_system.sh            # 系统测试脚本
│
├── 🐍 backend/ (后端)
│   ├── main.py                    # FastAPI 主应用 ⭐
│   ├── agent.py                   # AI Agent (LangChain) ⭐
│   ├── models.py                  # 数据库模型
│   ├── schemas.py                 # Pydantic Schemas
│   ├── database.py                # 数据库连接配置
│   ├── requirements.txt           # Python 依赖
│   ├── .env                       # 环境变量（已配置 OpenRouter）
│   └── __init__.py               
│
└── ⚛️ frontend/ (前端)
    ├── package.json               # Node 依赖
    ├── vite.config.ts            # Vite 配置
    ├── tsconfig.json             # TypeScript 配置
    ├── tailwind.config.js        # Tailwind CSS 配置
    ├── postcss.config.js         # PostCSS 配置
    ├── index.html                # HTML 入口
    │
    └── src/
        ├── main.tsx              # React 入口
        ├── App.tsx               # 主应用组件 ⭐
        ├── index.css             # 全局样式（像素风格）
        ├── types.ts              # TypeScript 类型定义
        │
        ├── api/
        │   └── client.ts         # API 客户端
        │
        ├── store/
        │   └── gameStore.ts      # Zustand 状态管理
        │
        └── components/
            ├── Character.tsx      # 角色组件（ASCII 艺术）
            ├── GoalInput.tsx      # 目标输入组件
            ├── TaskList.tsx       # 任务列表组件
            ├── StatsDisplay.tsx   # 数值显示组件
            ├── StoryDisplay.tsx   # 故事展示组件
            └── RewardAnimation.tsx # 奖励动画组件
```

## 核心文件详解

### 🌟 必读文件

1. **PROJECT_COMPLETE.md** - 项目完成总结
   - 已完成功能列表
   - 技术栈说明
   - 使用指南
   - **建议首先阅读**

2. **QUICKSTART.md** - 快速启动
   - 3 步启动系统
   - 常见问题解答
   - **开始使用前必读**

3. **OPENROUTER_SETUP.md** - AI 配置
   - OpenRouter 说明
   - 模型选择指南
   - 价格参考
   - **了解 AI 配置必读**

### 🔑 关键代码文件

#### 后端核心

**backend/main.py** (272 行)
```python
# FastAPI 应用主入口
# 包含所有 API 端点：
# - POST /api/users - 创建用户
# - POST /api/goals - 创建目标（调用 AI）
# - POST /api/tasks/{id}/complete - 完成任务
# - GET /api/users/{id}/stats - 获取数值
```

**backend/agent.py** (109 行)
```python
# AI Agent 核心逻辑
# - LifeGameAgent 类
# - create_game_plan() - 生成故事和任务
# - calculate_rewards() - 计算奖励
# - 支持 OpenRouter 配置
```

**backend/models.py** (55 行)
```python
# SQLAlchemy 数据库模型
# - User - 用户表
# - UserStats - 用户数值表  
# - Goal - 目标表
# - Task - 任务表
```

#### 前端核心

**frontend/src/App.tsx** (200+ 行)
```typescript
// React 主应用组件
// - 用户初始化
// - 目标提交处理
// - 任务完成处理
// - 页面布局和路由
```

**frontend/src/components/Character.tsx**
```typescript
// ASCII 艺术角色组件
// 三种状态：idle、thinking、celebrating
```

**frontend/src/components/TaskList.tsx**
```typescript
// 任务列表组件
// - 显示任务清单
// - 复选框交互
// - 进度条展示
```

**frontend/src/store/gameStore.ts**
```typescript
// Zustand 全局状态管理
// - user、stats、currentGoal
// - 状态更新方法
```

### 🔧 配置文件

**docker-compose.yml**
```yaml
# PostgreSQL 数据库容器配置
# 端口：5432
# 用户：gameuser
# 密码：gamepass
```

**backend/.env** ⚠️ 敏感文件
```env
# OpenRouter API 配置
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
AI_MODEL=qwen/qwen-max
DATABASE_URL=postgresql://...
```

**frontend/vite.config.ts**
```typescript
// Vite 构建配置
// 代理设置：/api -> http://localhost:8089
```

### 📜 脚本文件

**setup.sh** - 环境设置
```bash
# 检查环境（Docker、Python、Node.js）
# 安装依赖
# 创建虚拟环境
# 启动数据库
```

**start.sh** - 启动服务
```bash
# 启动数据库
# 启动后端（port 8089）
# 启动前端（port 5173）
```

**test_system.sh** - 系统测试
```bash
# 测试数据库连接
# 测试后端 API
# 测试前端服务
# 测试 API 功能
```

## 📝 文档阅读顺序

### 新手上路
1. **PROJECT_COMPLETE.md** - 了解项目
2. **QUICKSTART.md** - 快速启动
3. **DEMO.md** - 查看示例

### 开发者
1. **PROJECT_OVERVIEW.md** - 技术架构
2. **README.md** - 详细说明
3. 阅读核心代码文件

### 运维/部署
1. **QUICKSTART.md** - 启动流程
2. **OPENROUTER_SETUP.md** - AI 配置
3. **TROUBLESHOOTING.md** - 问题排查

## 🔍 代码导航

### 查找特定功能

**AI 任务拆解**
- `backend/agent.py` - `create_game_plan()`
- Prompt 模板在同一文件中

**任务完成奖励**
- `backend/agent.py` - `calculate_rewards()`
- `backend/main.py` - `/api/tasks/{id}/complete` 端点

**前端状态管理**
- `frontend/src/store/gameStore.ts`
- 使用 Zustand hooks

**UI 组件样式**
- `frontend/src/index.css` - 全局样式
- 各组件文件中使用 Tailwind classes

**数据库操作**
- `backend/main.py` - 使用 SQLAlchemy ORM
- `backend/models.py` - 模型定义

## 🚫 忽略文件

以下文件/文件夹被 `.gitignore` 忽略：

```
# Python
__pycache__/
venv/
*.pyc

# Node
node_modules/
dist/

# 敏感文件
.env
.env.local

# 数据库
postgres_data/

# IDE
.vscode/
.idea/
```

## 📊 代码统计

```
后端 Python 代码：~500 行
前端 TypeScript 代码：~800 行
配置文件：~200 行
文档：~2000 行
总计：~3500 行
```

## 🔗 重要链接

### API 相关
- Swagger 文档：http://localhost:8089/docs
- Redoc 文档：http://localhost:8089/redoc

### 外部服务
- OpenRouter：https://openrouter.ai
- Qwen 模型：https://tongyi.aliyun.com

### 技术文档
- FastAPI：https://fastapi.tiangolo.com
- React：https://react.dev
- LangChain：https://python.langchain.com
- Tailwind CSS：https://tailwindcss.com

## 💡 快速参考

### 启动命令
```bash
./setup.sh          # 首次运行
./start.sh          # 启动所有服务
./test_system.sh    # 测试系统
```

### Make 命令
```bash
make setup          # 设置环境
make start          # 启动服务
make stop           # 停止服务
make test           # 运行测试
make clean          # 清理
make db-shell       # 打开数据库 shell
```

### 访问地址
- 应用：http://localhost:5173
- API：http://localhost:8089
- API 文档：http://localhost:8089/docs

## 🎯 下一步

1. 阅读 **PROJECT_COMPLETE.md**
2. 运行 `./setup.sh` 设置环境
3. 运行 `./start.sh` 启动系统
4. 访问 http://localhost:5173 开始使用
5. 查看 **DEMO.md** 了解使用场景

祝使用愉快！🎮

