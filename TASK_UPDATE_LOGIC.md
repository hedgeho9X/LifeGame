# 任务修改功能 - 完整实现逻辑

## 📊 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                        用户界面                              │
│  ┌──────────────────────┐  ┌──────────────────────┐        │
│  │   对话区（左侧）      │  │  任务列表（右侧）     │        │
│  │  - Markdown渲染      │  │  - 实时显示          │        │
│  │  - 对话历史          │  │  - 任务详情          │        │
│  └──────────────────────┘  └──────────────────────┘        │
│              ↓                        ↓                      │
│  ┌────────────────────────────────────────────┐            │
│  │     "应用修改到任务列表" 按钮               │            │
│  └────────────────────────────────────────────┘            │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                      API 层                                  │
│  POST /api/conversations  →  对话                           │
│  POST /api/goals/{id}/apply-updates  →  应用修改            │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                    AI Agent 层                               │
│  refine_tasks()  →  对话回复                                │
│  update_tasks_from_conversation()  →  生成新任务列表        │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                    数据库层                                  │
│  conversations 表  →  存储对话历史                          │
│  tasks 表  →  存储任务（可更新）                            │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 完整工作流程

### 阶段1: 对话交互

#### 步骤1.1: 用户发起对话
```typescript
// frontend/src/components/ConversationPanel.tsx
const handleSendMessage = async (e: React.FormEvent) => {
  const userMessage = inputMessage.trim();
  
  // 1. 添加用户消息到界面
  setMessages([...messages, { role: 'user', content: userMessage }]);
  
  // 2. 调用API
  const response = await api.sendMessage(goalId, userMessage);
  
  // 3. 显示AI回复（Markdown格式）
  setMessages([...messages, response.message]);
};
```

#### 步骤1.2: 后端处理对话
```python
# backend/main.py
@app.post("/api/conversations")
async def create_conversation(conversation: ConversationCreate, db: Session):
    # 1. 获取对话历史
    history = db.query(Conversation).filter(
        Conversation.goal_id == conversation.goal_id
    ).all()
    
    # 2. 获取当前任务
    current_tasks = [...]
    
    # 3. 调用AI生成回复
    ai_response = agent.refine_tasks(
        goal.goal_text,
        current_tasks,
        conversation.user_message,
        history
    )
    
    # 4. 保存对话记录
    user_msg = Conversation(role="user", content=user_message)
    ai_msg = Conversation(role="assistant", content=ai_response)
    db.add(user_msg)
    db.add(ai_msg)
    db.commit()
    
    return ai_msg
```

#### 步骤1.3: AI生成对话回复
```python
# backend/agent.py
def refine_tasks(self, goal_text, current_tasks, user_message, history):
    # 1. 构建对话上下文
    messages = [
        {"role": "system", "content": "你是生活游戏化AI助手..."},
        *history,  # 历史对话
        {"role": "system", "content": f"当前任务: {current_tasks}"},
        {"role": "user", "content": user_message}
    ]
    
    # 2. 调用LLM生成回复（使用Markdown格式）
    response = self.llm.invoke(messages)
    
    return response.content  # 返回Markdown文本
```

**此时**：
- ✅ 对话已保存到数据库
- ✅ AI已给出建议（Markdown格式）
- ❌ 任务列表**还没有**真正修改

---

### 阶段2: 应用修改（关键！）

#### 步骤2.1: 用户点击"应用修改"按钮
```typescript
// frontend/src/components/ConversationPanel.tsx
const handleApplyUpdates = async () => {
  // 1. 调用应用更新API
  const result = await api.applyTaskUpdates(goalId);
  
  // 2. 更新前端任务列表
  onTasksUpdated(result.tasks, result.summary);
  
  // 3. 显示成功消息
  alert(`✅ 任务已更新！\n\n${result.summary}`);
};
```

#### 步骤2.2: 后端应用更新（核心逻辑）
```python
# backend/main.py
@app.post("/api/goals/{goal_id}/apply-updates")
async def apply_task_updates(goal_id: int, db: Session):
    """根据对话历史应用任务更新"""
    
    # 1. 获取目标和对话历史
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    conversation_history = db.query(Conversation).filter(
        Conversation.goal_id == goal_id
    ).all()
    
    # 2. 获取当前任务列表
    current_tasks = [
        {
            "title": t.title,
            "description": t.description,
            "estimated_time": t.estimated_time,
            "skill_rewards": t.skill_rewards
        }
        for t in goal.tasks
    ]
    
    # 3. 获取用户技能系统
    user_stats = db.query(UserStats).filter(
        UserStats.user_id == goal.user_id
    ).first()
    
    # 4. 🔥 调用AI生成新任务列表
    update_result = agent.update_tasks_from_conversation(
        goal.goal_text,
        current_tasks,
        history,
        user_stats.stats_data
    )
    # update_result = {
    #     tasks: [...],  # 新任务列表
    #     summary: "更新总结"
    # }
    
    # 5. 🗑️ 删除旧任务（只删除未完成的）
    db.query(Task).filter(
        Task.goal_id == goal_id,
        Task.completed == False
    ).delete()
    
    # 6. ✨ 插入新任务
    new_tasks = []
    for idx, task in enumerate(update_result.tasks):
        db_task = Task(
            goal_id=goal_id,
            title=task.title,
            description=task.description,
            estimated_time=task.estimated_time,
            order=idx,
            skill_rewards=task.skill_rewards  # 保持技能一致性
        )
        db.add(db_task)
        new_tasks.append(db_task)
    
    db.commit()
    
    # 7. 返回结果
    return {
        "success": True,
        "summary": update_result.summary,
        "tasks": new_tasks
    }
```

#### 步骤2.3: AI分析对话并生成新任务
```python
# backend/agent.py
def update_tasks_from_conversation(
    self, 
    goal_text: str, 
    current_tasks: List[Dict], 
    conversation_history: List[Dict],
    current_stats: Dict[str, int]
) -> TaskUpdateResponse:
    """根据对话历史更新任务规划"""
    
    # 1. 构建对话上下文
    conversation_text = "\n".join([
        f"{msg['role']}: {msg['content']}" 
        for msg in conversation_history
    ])
    
    # 2. 构建当前任务列表文本
    current_tasks_text = "\n".join([
        f"{i}. {task['title']} - {task['description']}"
        for i, task in enumerate(current_tasks, 1)
    ])
    
    # 3. 构建提示词
    prompt = f"""
    你是生活游戏化系统的AI助手。
    根据用户与AI的对话历史，更新任务规划。
    
    用户目标：{goal_text}
    
    当前技能系统：{current_stats}
    
    对话历史：
    {conversation_text}
    
    当前任务列表：
    {current_tasks_text}
    
    任务：
    1. 分析对话中用户提出的所有修改需求
    2. 保留未提及的任务（如果合理）
    3. 添加、删除或修改任务以满足用户需求
    4. 确保每个任务都有 title、description、estimated_time 和 skill_rewards
    5. skill_rewards 必须使用当前技能系统中的技能名称
    6. 写一个简短的更新总结（summary）
    
    返回格式：
    {{
      "tasks": [
        {{
          "title": "...",
          "description": "...",
          "estimated_time": "...",
          "skill_rewards": {{"技能1": 5, "技能2": 3}}
        }}
      ],
      "summary": "更新总结：添加了XX，修改了YY，删除了ZZ"
    }}
    """
    
    # 4. 调用LLM（使用PydanticOutputParser确保格式正确）
    result = self.llm.invoke(prompt)
    
    # 5. 解析并返回
    return TaskUpdateResponse(
        tasks=result.tasks,
        summary=result.summary
    )
```

---

## 🎯 关键点说明

### 1. 为什么需要两个步骤？

**对话阶段**：
- 目的：让用户和AI充分沟通
- 特点：可以多轮对话，AI给建议但不修改
- 优势：用户可以反复确认，避免误操作

**应用阶段**：
- 目的：真正修改数据库中的任务
- 特点：一次性操作，AI分析完整对话历史
- 优势：所有修改一起应用，保持一致性

### 2. 为什么要分析"整个对话历史"？

```python
# 示例对话：
用户: "第一个任务太复杂了"
AI: "好的，我建议拆成两个任务"
用户: "另外我还想加一个关于面试的任务"
AI: "好主意！"
用户: "等等，第二个任务的时间应该是2小时"

# 应用修改时，AI会分析所有5条消息：
# - 拆分第一个任务 ✓
# - 添加面试任务 ✓
# - 修改第二个任务时间 ✓
```

### 3. 数据安全保证

```python
# 只删除未完成的任务
db.query(Task).filter(
    Task.goal_id == goal_id,
    Task.completed == False  # 关键！
).delete()

# 已完成的任务不会被删除 ✓
```

### 4. 技能系统一致性

```python
# AI生成新任务时，会确保技能名称匹配
current_stats = {"等级": 1, "专注力": 0, "执行力": 0}

# 新任务的skill_rewards只能用这些技能
new_task.skill_rewards = {"专注力": 5, "执行力": 3}  # ✓
new_task.skill_rewards = {"魔法值": 10}  # ✗ 会被AI自动修正
```

---

## 🐛 当前问题排查

### 问题：404 Not Found

**原因**：
```
后端服务器正在运行旧代码
 ↓
新的API端点 /api/goals/{id}/apply-updates 不存在
 ↓
前端调用时返回 404
```

**解决方案**：
```bash
# 1. 停止旧服务器
pkill -f uvicorn

# 2. 启动新服务器
cd /Users/jerry/Documents/Code/LifeGame
./start-backend.sh
```

**验证方法**：
1. 访问 http://localhost:8089/docs
2. 查找 `POST /api/goals/{goal_id}/apply-updates` 端点
3. 如果看到这个端点，说明更新成功

---

## 📝 使用示例

### 完整流程演示

```
1. 创建目标："海投20家公司"
   ↓ AI生成6个任务

2. 点击"与AI对话"
   ↓ 打开分屏对话界面

3. 用户："第一个任务'唤醒沉睡的简历骨架'太抽象了"
   ↓ AI回复："好的，我建议改为'整理简历基础信息'..."

4. 用户："另外加一个LinkedIn的任务"
   ↓ AI回复："我会添加'优化LinkedIn档案'任务..."

5. 用户："就这样吧"
   ↓ 点击"✅ 应用修改到任务列表"

6. 系统处理：
   ├─ 获取对话历史（3条用户消息+3条AI回复）
   ├─ AI分析：需要修改第1个任务，添加1个新任务
   ├─ 删除未完成的旧任务（假设5个未完成）
   ├─ 插入新任务（6个）
   └─ 返回更新总结

7. 前端显示：
   "✅ 任务已更新！
   
   更新总结：
   - 修改了第1个任务的标题和描述
   - 新增了'优化LinkedIn档案'任务
   - 保留了其他4个任务
   
   共6个任务"
```

---

## 🔒 安全性考虑

### 1. 事务保护
```python
try:
    db.query(Task).delete()
    for task in new_tasks:
        db.add(task)
    db.commit()  # 一次性提交
except Exception as e:
    db.rollback()  # 出错回滚
    raise
```

### 2. 权限检查
```python
# 确保目标属于该用户
goal = db.query(Goal).filter(
    Goal.id == goal_id,
    Goal.user_id == current_user.id  # 权限检查
).first()
```

### 3. 数据验证
```python
# Pydantic自动验证
class TaskItem(BaseModel):
    title: str  # 必填
    description: str  # 必填
    estimated_time: str  # 必填
    skill_rewards: Dict[str, int]  # 必填且格式正确
```

---

## 🚀 性能优化

### 1. 批量操作
```python
# ✓ 批量删除
db.query(Task).filter(...).delete()

# ✓ 批量插入
db.add_all(new_tasks)

# ✗ 避免逐个操作
for task in old_tasks:
    db.delete(task)  # 慢
```

### 2. AI调用优化
```python
# 只在需要时调用AI
if not conversation_history:
    raise HTTPException(400, "No conversation to apply")

# 使用流式输出（未来改进）
# async for chunk in self.llm.stream(prompt):
#     yield chunk
```

---

## 📚 相关文件

### 后端
- `backend/agent.py` - AI逻辑
- `backend/main.py` - API端点
- `backend/schemas.py` - 数据模型
- `backend/models.py` - 数据库模型

### 前端
- `frontend/src/components/ConversationPanel.tsx` - 对话界面
- `frontend/src/api/client.ts` - API调用
- `frontend/src/App.tsx` - 主应用

---

## 更新日期
2025年11月1日

