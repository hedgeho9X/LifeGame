# 故障排除指南

## 常见问题和解决方案

### 1. 数据库问题

#### 问题：数据库启动失败
```
Error: Cannot connect to database
```

**解决方案**：
```bash
# 检查 Docker 是否运行
docker info

# 查看容器状态
docker-compose ps

# 查看数据库日志
docker-compose logs postgres

# 重启数据库
docker-compose restart postgres

# 如果还不行，删除并重建
docker-compose down -v
docker-compose up -d
```

#### 问题：端口 5432 被占用
```
Error: port is already allocated
```

**解决方案**：
```bash
# 查找占用端口的进程
lsof -i :5432

# 停止其他 PostgreSQL 服务
brew services stop postgresql  # macOS
# 或
sudo systemctl stop postgresql  # Linux

# 或者修改 docker-compose.yml 中的端口映射
```

### 2. 后端问题

#### 问题：后端启动失败 - 缺少依赖
```
ModuleNotFoundError: No module named 'xxx'
```

**解决方案**：
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

#### 问题：OpenAI API 错误
```
Error: Invalid API key
```

**解决方案**：
1. 检查 `backend/.env` 文件是否存在
2. 确认 API Key 格式正确（sk-...）
3. 验证 API Key 是否有效：https://platform.openai.com/api-keys
4. 确认账户有余额

```bash
# 测试 API Key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### 问题：数据库连接超时
```
Error: could not connect to server
```

**解决方案**：
```bash
# 等待数据库完全启动
sleep 10

# 检查数据库是否就绪
docker-compose exec postgres pg_isready -U gameuser

# 检查连接字符串
cat backend/.env | grep DATABASE_URL
```

#### 问题：导入错误
```
ImportError: attempted relative import with no known parent package
```

**解决方案**：
```bash
# 确保从正确的目录启动
cd backend
python main.py

# 或使用
python -m uvicorn main:app --reload
```

### 3. 前端问题

#### 问题：前端白屏
```
页面显示空白
```

**解决方案**：
1. 打开浏览器开发者工具（F12）
2. 查看 Console 标签中的错误
3. 检查 Network 标签中的请求

常见原因：
- 后端未启动
- API 请求失败
- JavaScript 错误

```bash
# 检查后端是否运行
curl http://localhost:8000/

# 重启前端
cd frontend
npm run dev
```

#### 问题：CORS 错误
```
Access to XMLHttpRequest has been blocked by CORS policy
```

**解决方案**：
检查 `backend/main.py` 中的 CORS 配置：
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 确保包含前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 问题：npm install 失败
```
Error: EACCES: permission denied
```

**解决方案**：
```bash
# 清理缓存
npm cache clean --force

# 删除 node_modules 重新安装
rm -rf node_modules package-lock.json
npm install

# 如果还不行，检查 npm 权限
sudo chown -R $USER:$(id -gn $USER) ~/.npm
```

### 4. Docker 问题

#### 问题：Docker 未运行
```
Cannot connect to the Docker daemon
```

**解决方案**：
- macOS: 启动 Docker Desktop 应用
- Linux: `sudo systemctl start docker`
- Windows: 启动 Docker Desktop

#### 问题：容器启动失败
```
Error response from daemon: driver failed
```

**解决方案**：
```bash
# 查看详细错误
docker-compose logs

# 完全清理并重启
docker-compose down -v
docker system prune -a  # 谨慎使用
docker-compose up -d
```

### 5. 性能问题

#### 问题：AI 生成太慢（超过 30 秒）
**可能原因**：
- OpenAI API 响应慢
- 网络延迟
- 模型选择（GPT-4 比 GPT-3.5 慢）

**解决方案**：
```python
# 在 backend/agent.py 中调整：
self.llm = ChatOpenAI(
    model="gpt-3.5-turbo",  # 使用更快的模型
    temperature=0.7,
    timeout=30  # 添加超时
)
```

#### 问题：页面加载慢
**解决方案**：
```bash
# 检查是否在生产模式
cd frontend
npm run build
npm run preview

# 检查网络请求
# 在浏览器开发者工具 Network 标签查看慢请求
```

### 6. 数据问题

#### 问题：任务完成但数值没更新
**解决方案**：
```bash
# 检查数据库数据
docker-compose exec postgres psql -U gameuser -d life_game_db

# 在 psql 中：
SELECT * FROM user_stats;
SELECT * FROM tasks WHERE id = YOUR_TASK_ID;
```

#### 问题：想要重置所有数据
**解决方案**：
```bash
# 完全重置数据库
docker-compose down -v
docker-compose up -d

# 前端清除 localStorage
# 在浏览器控制台运行：
localStorage.clear()
```

### 7. 开发问题

#### 问题：修改代码后不生效
**后端**：
```bash
# 确保使用了 --reload 参数
uvicorn main:app --reload
```

**前端**：
```bash
# Vite 应该自动热重载
# 如果不行，手动刷新页面
# 或重启 dev server
```

#### 问题：TypeScript 类型错误
**解决方案**：
```bash
cd frontend
npm run build  # 查看所有类型错误

# 或在 VSCode 中查看 Problems 面板
```

### 8. 环境问题

#### 问题：Python 版本太低
```
Error: Python 3.9 or higher is required
```

**解决方案**：
```bash
# 检查版本
python3 --version

# 安装新版本
# macOS
brew install python@3.11

# Ubuntu
sudo apt install python3.11
```

#### 问题：Node.js 版本太低
```
Error: Node.js 18 or higher is required
```

**解决方案**：
```bash
# 使用 nvm 安装（推荐）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18
nvm use 18

# 或从官网下载：https://nodejs.org/
```

## 调试技巧

### 查看日志

**数据库日志**：
```bash
docker-compose logs -f postgres
```

**后端日志**：
后端会在终端直接输出日志，包括：
- API 请求
- 错误堆栈
- SQL 查询（如果启用）

**前端日志**：
- 浏览器开发者工具 Console
- Network 标签查看 API 请求

### 测试 API

```bash
# 测试创建用户
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"测试","background":"背景"}'

# 测试创建目标（需要先获取 user_id）
curl -X POST http://localhost:8000/api/goals \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"goal_text":"学习 Python"}'
```

### 数据库查询

```bash
# 进入数据库 shell
docker-compose exec postgres psql -U gameuser -d life_game_db

# 常用查询
\dt                    # 列出所有表
SELECT * FROM users;   # 查看所有用户
SELECT * FROM goals;   # 查看所有目标
SELECT * FROM tasks;   # 查看所有任务

# 退出
\q
```

## 还是解决不了？

1. 查看 [GitHub Issues](链接)
2. 查看项目文档：`README.md`, `QUICKSTART.md`
3. 检查是否有更新：`git pull`
4. 完全重置项目：`make reset` 然后 `make setup`

## 获取帮助

如果以上方法都不能解决问题：

1. **收集信息**：
   - 错误信息完整输出
   - 操作系统和版本
   - Python/Node.js 版本
   - 重现步骤

2. **提交 Issue**：
   - 在 GitHub 上创建 Issue
   - 包含上述信息
   - 描述期望的行为和实际行为

3. **社区求助**：
   - Stack Overflow
   - 相关技术社区

