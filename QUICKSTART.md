# 快速启动指南

## 第一次运行（完整步骤）

### 1. 准备环境

确保已安装：
- Docker Desktop
- Python 3.9+
- Node.js 18+

### 2. 配置 API Key

**本项目已配置使用 OpenRouter**

`backend/.env` 文件已创建并配置好 OpenRouter API。如需修改：

```bash
cd backend
vi .env  # 或使用其他编辑器
```

当前配置：
```env
OPENROUTER_API_KEY=sk-or-v1-your-key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
AI_MODEL=qwen/qwen-max
```

详细配置说明请查看 [OPENROUTER_SETUP.md](./OPENROUTER_SETUP.md)

### 3. 一键启动（推荐）

```bash
# 在项目根目录
./start.sh
```

### 4. 手动启动（备选）

如果一键启动脚本不工作，可以手动启动：

#### 启动数据库
```bash
docker-compose up -d
```

#### 启动后端
```bash
cd backend
pip install -r requirements.txt
python main.py
```

在新终端窗口启动前端：
```bash
cd frontend
npm install
npm run dev
```

### 5. 访问应用

打开浏览器访问：`http://localhost:5173`

## 验证服务状态

### 检查数据库
```bash
docker-compose ps
# 应该看到 postgres 容器状态为 Up
```

### 检查后端
访问：`http://localhost:8089/docs`
应该能看到 API 文档页面

### 检查前端
访问：`http://localhost:5173`
应该能看到黑白像素风格的游戏界面

## 常见问题

### Q: 数据库连接失败
A: 运行 `docker-compose down -v` 然后 `docker-compose up -d` 重新启动

### Q: 后端启动失败
A: 检查是否正确配置了 `.env` 文件和 OPENROUTER_API_KEY (或 OPENAI_API_KEY)

### Q: 前端白屏
A: 打开浏览器控制台查看错误，通常是后端未启动或 API 调用失败

### Q: AI 生成失败
A: 
1. 检查 OpenRouter API Key 是否有效（访问 https://openrouter.ai/keys）
2. 检查 API 账户是否有余额
3. 尝试切换模型（在 .env 中修改 AI_MODEL）
4. 查看后端日志获取详细错误信息

## 停止服务

按 `Ctrl+C` 停止前后端服务

停止数据库：
```bash
docker-compose down
```

如果要删除数据库数据：
```bash
docker-compose down -v
```

## 下一步

阅读 [README.md](./README.md) 了解更多功能和开发信息。

