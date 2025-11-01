from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import engine, get_db
from agent import agent
from datetime import datetime

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Life Game API")

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite 和 React 默认端口
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Life Game API is running"}

# 用户相关接口
@app.post("/api/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """创建新用户并初始化数值系统"""
    db_user = models.User(name=user.name, background=user.background)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # 初始化用户数值系统
    user_stats = models.UserStats(
        user_id=db_user.id,
        stats_data={"等级": 1, "经验值": 0}
    )
    db.add(user_stats)
    db.commit()
    
    return db_user

@app.get("/api/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """获取用户信息"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/api/users/{user_id}/stats", response_model=schemas.UserStatsResponse)
def get_user_stats(user_id: int, db: Session = Depends(get_db)):
    """获取用户数值数据"""
    stats = db.query(models.UserStats).filter(models.UserStats.user_id == user_id).first()
    if not stats:
        raise HTTPException(status_code=404, detail="User stats not found")
    return stats

# 目标相关接口
@app.post("/api/goals", response_model=schemas.GoalResponse)
async def create_goal(goal: schemas.GoalCreate, db: Session = Depends(get_db)):
    """创建新目标，AI 生成故事和任务"""
    
    # 验证用户是否存在
    user = db.query(models.User).filter(models.User.id == goal.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 使用用户背景信息（如果提供）或者从数据库获取
    user_background = goal.user_background or user.background
    
    try:
        # 调用 AI Agent 生成游戏计划
        print(f"🎯 Creating game plan for goal: {goal.goal_text}")
        print(f"👤 User background: {user_background[:100] if user_background else 'None'}...")
        game_plan = agent.create_game_plan(goal.goal_text, user_background)
        print(f"✅ Game plan created successfully with {len(game_plan.tasks)} tasks")
        
        # 创建目标
        db_goal = models.Goal(
            user_id=goal.user_id,
            goal_text=goal.goal_text,
            story=game_plan.story,
            praise_messages=game_plan.praise_messages
        )
        db.add(db_goal)
        db.commit()
        db.refresh(db_goal)
        
        # 创建任务列表
        for idx, task in enumerate(game_plan.tasks):
            db_task = models.Task(
                goal_id=db_goal.id,
                title=task.title,
                description=task.description,
                estimated_time=task.estimated_time,
                order=idx,
                skill_rewards=task.skill_rewards
            )
            db.add(db_task)
        
        # 更新用户数值系统（合并新的数值类型）
        user_stats = db.query(models.UserStats).filter(
            models.UserStats.user_id == goal.user_id
        ).first()
        
        if user_stats:
            # 合并现有数值和新数值
            current_stats = user_stats.stats_data or {}
            for key, value in game_plan.stats.items():
                if key not in current_stats:
                    current_stats[key] = value
            user_stats.stats_data = current_stats
            user_stats.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(db_goal)
        
        # 构造响应
        response = schemas.GoalResponse(
            id=db_goal.id,
            user_id=db_goal.user_id,
            goal_text=db_goal.goal_text,
            story=db_goal.story,
            tasks=[schemas.TaskResponse(
                id=t.id,
                goal_id=t.goal_id,
                title=t.title,
                description=t.description,
                estimated_time=t.estimated_time,
                order=t.order,
                completed=t.completed,
                completed_at=t.completed_at,
                created_at=t.created_at,
                skill_rewards=t.skill_rewards or {}
            ) for t in db_goal.tasks],
            stats_data=user_stats.stats_data,
            praise_messages=db_goal.praise_messages or [],
            created_at=db_goal.created_at,
            completed=db_goal.completed
        )
        
        return response
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating goal: {str(e)}")
        print(f"❌ Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to create goal: {str(e)}")

@app.get("/api/goals/{goal_id}", response_model=schemas.GoalResponse)
def get_goal(goal_id: int, db: Session = Depends(get_db)):
    """获取目标详情"""
    goal = db.query(models.Goal).filter(models.Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    user_stats = db.query(models.UserStats).filter(
        models.UserStats.user_id == goal.user_id
    ).first()
    
    return schemas.GoalResponse(
        id=goal.id,
        user_id=goal.user_id,
        goal_text=goal.goal_text,
        story=goal.story,
        tasks=[schemas.TaskResponse(
            id=t.id,
            goal_id=t.goal_id,
            title=t.title,
            description=t.description,
            estimated_time=t.estimated_time,
            order=t.order,
            completed=t.completed,
            completed_at=t.completed_at,
            created_at=t.created_at,
            skill_rewards=t.skill_rewards or {}
        ) for t in goal.tasks],
        stats_data=user_stats.stats_data if user_stats else {},
        praise_messages=goal.praise_messages or [],
        created_at=goal.created_at,
        completed=goal.completed
    )

# 任务相关接口
@app.post("/api/tasks/{task_id}/complete", response_model=schemas.TaskCompleteResponse)
def complete_task(task_id: int, db: Session = Depends(get_db)):
    """完成任务，计算奖励并更新数值"""
    
    # 获取任务
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.completed:
        raise HTTPException(status_code=400, detail="Task already completed")
    
    # 获取用户数值
    goal = db.query(models.Goal).filter(models.Goal.id == task.goal_id).first()
    user_stats = db.query(models.UserStats).filter(
        models.UserStats.user_id == goal.user_id
    ).first()
    
    if not user_stats:
        raise HTTPException(status_code=404, detail="User stats not found")
    
    # 计算奖励（使用任务的skill_rewards）
    current_stats = user_stats.stats_data
    skill_rewards = task.skill_rewards or {}
    rewards = agent.calculate_rewards(skill_rewards, current_stats)
    
    # 更新数值
    updated_stats = current_stats.copy()
    for key, value in rewards.items():
        updated_stats[key] = updated_stats.get(key, 0) + value
    
    # 保存更新
    task.completed = True
    task.completed_at = datetime.utcnow()
    user_stats.stats_data = updated_stats
    user_stats.updated_at = datetime.utcnow()
    
    db.commit()
    
    # 检查目标是否完成
    goal_tasks = db.query(models.Task).filter(models.Task.goal_id == goal.id).all()
    therapy_ticket_awarded = False
    
    if all(t.completed for t in goal_tasks):
        goal.completed = True
        
        # 🎁 发放话疗券！
        therapy_ticket = models.TherapyTicket(
            user_id=goal.user_id,
            goal_id=goal.id
        )
        db.add(therapy_ticket)
        therapy_ticket_awarded = True
        print(f"🎁 Awarded therapy ticket for goal {goal.id}")
        
        db.commit()
    
    return schemas.TaskCompleteResponse(
        task_id=task.id,
        completed=True,
        rewards=rewards,
        updated_stats=updated_stats,
        character_state="celebrating",
        therapy_ticket_awarded=therapy_ticket_awarded
    )

@app.get("/api/users/{user_id}/goals", response_model=List[schemas.GoalResponse])
def get_user_goals(user_id: int, db: Session = Depends(get_db)):
    """获取用户所有目标"""
    goals = db.query(models.Goal).filter(models.Goal.user_id == user_id).all()
    user_stats = db.query(models.UserStats).filter(
        models.UserStats.user_id == user_id
    ).first()
    
    return [
        schemas.GoalResponse(
            id=goal.id,
            user_id=goal.user_id,
            goal_text=goal.goal_text,
            story=goal.story,
            tasks=[schemas.TaskResponse(
                id=t.id,
                goal_id=t.goal_id,
                title=t.title,
                description=t.description,
                estimated_time=t.estimated_time,
                order=t.order,
                completed=t.completed,
                completed_at=t.completed_at,
                created_at=t.created_at,
                skill_rewards=t.skill_rewards or {}
            ) for t in goal.tasks],
            stats_data=user_stats.stats_data if user_stats else {},
            created_at=goal.created_at,
            completed=goal.completed
        )
        for goal in goals
    ]

# 对话相关接口
@app.post("/api/conversations", response_model=schemas.ConversationResponse)
async def create_conversation(conversation: schemas.ConversationCreate, db: Session = Depends(get_db)):
    """创建对话，允许用户与AI讨论和细化任务"""
    
    # 获取目标
    goal = db.query(models.Goal).filter(models.Goal.id == conversation.goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    # 获取对话历史
    conversation_history = db.query(models.Conversation).filter(
        models.Conversation.goal_id == conversation.goal_id
    ).all()
    
    history = [{"role": msg.role, "content": msg.content} for msg in conversation_history]
    
    # 获取当前任务
    current_tasks = [
        {
            "title": t.title,
            "description": t.description,
            "estimated_time": t.estimated_time
        }
        for t in goal.tasks
    ]
    
    try:
        # 调用AI生成回复
        ai_response = agent.refine_tasks(
            goal.goal_text,
            current_tasks,
            conversation.user_message,
            history
        )
        
        # 保存用户消息
        user_msg = models.Conversation(
            goal_id=conversation.goal_id,
            role="user",
            content=conversation.user_message
        )
        db.add(user_msg)
        
        # 保存AI回复
        ai_msg = models.Conversation(
            goal_id=conversation.goal_id,
            role="assistant",
            content=ai_response
        )
        db.add(ai_msg)
        
        db.commit()
        db.refresh(ai_msg)
        
        return schemas.ConversationResponse(
            message=schemas.ConversationMessage(
                role=ai_msg.role,
                content=ai_msg.content,
                created_at=ai_msg.created_at
            )
        )
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error in conversation: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to process conversation: {str(e)}")

@app.get("/api/goals/{goal_id}/conversations", response_model=List[schemas.ConversationMessage])
def get_goal_conversations(goal_id: int, db: Session = Depends(get_db)):
    """获取目标的对话历史"""
    conversations = db.query(models.Conversation).filter(
        models.Conversation.goal_id == goal_id
    ).all()
    
    return [
        schemas.ConversationMessage(
            role=msg.role,
            content=msg.content,
            created_at=msg.created_at
        )
        for msg in conversations
    ]

@app.post("/api/goals/{goal_id}/apply-updates", response_model=schemas.ApplyTaskUpdatesResponse)
async def apply_task_updates(goal_id: int, db: Session = Depends(get_db)):
    """根据对话历史应用任务更新"""
    
    # 获取目标
    goal = db.query(models.Goal).filter(models.Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    # 获取对话历史
    conversation_history = db.query(models.Conversation).filter(
        models.Conversation.goal_id == goal_id
    ).all()
    
    if not conversation_history:
        raise HTTPException(status_code=400, detail="No conversation history found")
    
    history = [{"role": msg.role, "content": msg.content} for msg in conversation_history]
    
    # 获取当前任务
    current_tasks = [
        {
            "title": t.title,
            "description": t.description,
            "estimated_time": t.estimated_time,
            "skill_rewards": t.skill_rewards or {}
        }
        for t in goal.tasks
    ]
    
    # 获取用户数值
    user_stats = db.query(models.UserStats).filter(
        models.UserStats.user_id == goal.user_id
    ).first()
    
    if not user_stats:
        raise HTTPException(status_code=404, detail="User stats not found")
    
    try:
        # 调用AI生成更新后的任务
        update_result = agent.update_tasks_from_conversation(
            goal.goal_text,
            current_tasks,
            history,
            user_stats.stats_data
        )
        
        # 删除旧任务（只删除未完成的）
        db.query(models.Task).filter(
            models.Task.goal_id == goal_id,
            models.Task.completed == False
        ).delete()
        
        # 添加新任务
        new_tasks = []
        for idx, task in enumerate(update_result.tasks):
            db_task = models.Task(
                goal_id=goal_id,
                title=task.title,
                description=task.description,
                estimated_time=task.estimated_time,
                order=idx,
                skill_rewards=task.skill_rewards
            )
            db.add(db_task)
            db.flush()  # 获取新任务的ID
            new_tasks.append(db_task)
        
        db.commit()
        
        # 刷新以获取所有字段
        for task in new_tasks:
            db.refresh(task)
        
        return schemas.ApplyTaskUpdatesResponse(
            success=True,
            summary=update_result.summary,
            tasks=[schemas.TaskResponse(
                id=t.id,
                goal_id=t.goal_id,
                title=t.title,
                description=t.description,
                estimated_time=t.estimated_time,
                order=t.order,
                completed=t.completed,
                completed_at=t.completed_at,
                created_at=t.created_at,
                skill_rewards=t.skill_rewards or {}
            ) for t in new_tasks]
        )
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error applying task updates: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to apply updates: {str(e)}")

# 话疗券相关接口
@app.get("/api/users/{user_id}/therapy-tickets", response_model=List[schemas.TherapyTicketResponse])
def get_user_therapy_tickets(user_id: int, db: Session = Depends(get_db)):
    """获取用户的话疗券列表"""
    tickets = db.query(models.TherapyTicket).filter(
        models.TherapyTicket.user_id == user_id
    ).order_by(models.TherapyTicket.created_at.desc()).all()
    
    return [
        schemas.TherapyTicketResponse(
            id=ticket.id,
            user_id=ticket.user_id,
            goal_id=ticket.goal_id,
            used=ticket.used,
            created_at=ticket.created_at,
            used_at=ticket.used_at,
            goal_text=ticket.goal.goal_text
        )
        for ticket in tickets
    ]

@app.post("/api/therapy/chat", response_model=schemas.TherapyChatResponse)
async def therapy_chat(request: schemas.TherapyChatRequest, db: Session = Depends(get_db)):
    """使用话疗券与AI话疗师对话"""
    
    # 获取话疗券
    ticket = db.query(models.TherapyTicket).filter(
        models.TherapyTicket.id == request.ticket_id
    ).first()
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Therapy ticket not found")
    
    # 获取用户和目标信息
    user = db.query(models.User).filter(models.User.id == ticket.user_id).first()
    goal = db.query(models.Goal).filter(models.Goal.id == ticket.goal_id).first()
    user_stats = db.query(models.UserStats).filter(
        models.UserStats.user_id == ticket.user_id
    ).first()
    
    # 获取完成的任务
    completed_tasks = [
        {
            "title": t.title,
            "description": t.description
        }
        for t in goal.tasks if t.completed
    ]
    
    # 获取对话历史
    conversation_history = db.query(models.TherapyConversation).filter(
        models.TherapyConversation.ticket_id == request.ticket_id
    ).all()
    
    history = [{"role": msg.role, "content": msg.content} for msg in conversation_history]
    is_opening = len(history) == 0
    
    try:
        # 调用AI话疗师
        ai_response = agent.therapy_chat(
            user_name=user.name,
            user_background=user.background or "",
            goal_text=goal.goal_text,
            completed_tasks=completed_tasks,
            user_stats=user_stats.stats_data,
            user_message=request.user_message or "",
            conversation_history=history
        )
        
        # 保存对话记录
        if request.user_message:
            user_msg = models.TherapyConversation(
                ticket_id=request.ticket_id,
                role="user",
                content=request.user_message
            )
            db.add(user_msg)
        
        ai_msg = models.TherapyConversation(
            ticket_id=request.ticket_id,
            role="assistant",
            content=ai_response
        )
        db.add(ai_msg)
        
        # 标记话疗券为已使用
        if not ticket.used:
            ticket.used = True
            ticket.used_at = datetime.utcnow()
        
        db.commit()
        
        return schemas.TherapyChatResponse(
            message=ai_response,
            is_opening=is_opening
        )
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error in therapy chat: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to process therapy chat: {str(e)}")

# 重置数值系统
@app.post("/api/users/{user_id}/reset-stats", response_model=schemas.ResetStatsResponse)
def reset_user_stats(user_id: int, db: Session = Depends(get_db)):
    """重置用户的数值系统"""
    
    user_stats = db.query(models.UserStats).filter(
        models.UserStats.user_id == user_id
    ).first()
    
    if not user_stats:
        raise HTTPException(status_code=404, detail="User stats not found")
    
    # 重置为初始状态
    user_stats.stats_data = {"等级": 1}
    user_stats.updated_at = datetime.utcnow()
    
    db.commit()
    
    return schemas.ResetStatsResponse(
        success=True,
        message="数值系统已重置"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8089)

