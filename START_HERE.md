# 🎮 开始使用生活游戏化系统

## ⚡ 3 步快速启动

### 1️⃣ 设置环境
```bash
./setup.sh
```
这会自动安装所有依赖并配置数据库。

### 2️⃣ 启动系统
```bash
./start.sh
```
这会启动数据库、后端和前端服务。

### 3️⃣ 开始使用
打开浏览器访问：**http://localhost:5173**

---

## 📚 重要文档

- **[PROJECT_COMPLETE.md](./PROJECT_COMPLETE.md)** ⭐ - 项目完成总结（推荐首读）
- **[QUICKSTART.md](./QUICKSTART.md)** - 详细启动指南
- **[OPENROUTER_SETUP.md](./OPENROUTER_SETUP.md)** - AI 配置说明
- **[DEMO.md](./DEMO.md)** - 使用示例
- **[FILES_GUIDE.md](./FILES_GUIDE.md)** - 文件说明

---

## 🔧 已配置的服务

✅ **AI Provider**: OpenRouter (qwen/qwen-max)  
✅ **数据库**: PostgreSQL (Docker)  
✅ **后端**: FastAPI (端口 8089)  
✅ **前端**: React + Vite (端口 5173)

---

## 🌐 访问地址

- **应用界面**: http://localhost:5173
- **API 文档**: http://localhost:8089/docs
- **后端 API**: http://localhost:8089

---

## 🎯 快速测试

1. 在界面中输入目标，例如：
   ```
   完成简历并海投 20 家公司
   ```

2. （可选）添加个人背景：
   ```
   我是计算机专业大四学生，擅长 Python 和前端开发
   ```

3. 点击"开始冒险"

4. AI 会生成：
   - 🎭 游戏化故事
   - ✅ 任务清单（3-8 个）
   - 📊 数值系统

5. 勾选完成的任务，获得奖励和升级！

---

## ❓ 遇到问题？

1. 查看 **[TROUBLESHOOTING.md](./TROUBLESHOOTING.md)**
2. 运行测试脚本：`./test_system.sh`
3. 检查服务状态：`docker-compose ps`

---

## 🛠️ 常用命令

```bash
# Make 命令（推荐）
make setup          # 设置环境
make start          # 启动服务
make stop           # 停止服务
make test           # 测试系统
make clean          # 清理
make db-shell       # 数据库 shell

# 或使用脚本
./setup.sh          # 设置
./start.sh          # 启动
./test_system.sh    # 测试
```

---

## 🎉 功能特点

✨ **AI 驱动**: 智能任务拆解和故事生成  
🎨 **像素风格**: 黑白复古游戏界面  
📊 **即时反馈**: 完成任务立即获得奖励  
🎮 **游戏化**: 等级、经验值、成就系统  
💾 **数据持久化**: PostgreSQL 存储

---

## 💡 技术栈

- **前端**: React + TypeScript + Tailwind CSS
- **后端**: Python + FastAPI + LangChain
- **AI**: OpenRouter API (Qwen Max)
- **数据库**: PostgreSQL

---

## 📖 了解更多

- [项目完成总结](./PROJECT_COMPLETE.md) - 详细功能说明
- [项目概览](./PROJECT_OVERVIEW.md) - 架构设计
- [README](./README.md) - 完整文档

---

**祝你使用愉快！开始你的游戏化人生之旅吧！** 🚀🎮

