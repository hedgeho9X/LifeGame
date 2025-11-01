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
            story=game_plan.story
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
                order=idx
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
                created_at=t.created_at
            ) for t in db_goal.tasks],
            stats_data=user_stats.stats_data,
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
            created_at=t.created_at
        ) for t in goal.tasks],
        stats_data=user_stats.stats_data if user_stats else {},
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
    
    # 计算奖励
    current_stats = user_stats.stats_data
    rewards = agent.calculate_rewards(task.title, current_stats)
    
    # 更新数值
    updated_stats = current_stats.copy()
    for key, value in rewards.items():
        if key == "经验值" and "等级" in rewards:
            # 经验值已经在 calculate_rewards 中处理过了
            updated_stats[key] = rewards[key]
        else:
            updated_stats[key] = updated_stats.get(key, 0) + value
    
    # 保存更新
    task.completed = True
    task.completed_at = datetime.utcnow()
    user_stats.stats_data = updated_stats
    user_stats.updated_at = datetime.utcnow()
    
    db.commit()
    
    # 检查目标是否完成
    goal_tasks = db.query(models.Task).filter(models.Task.goal_id == goal.id).all()
    if all(t.completed for t in goal_tasks):
        goal.completed = True
        db.commit()
    
    return schemas.TaskCompleteResponse(
        task_id=task.id,
        completed=True,
        rewards=rewards,
        updated_stats=updated_stats,
        character_state="celebrating"
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
                created_at=t.created_at
            ) for t in goal.tasks],
            stats_data=user_stats.stats_data if user_stats else {},
            created_at=goal.created_at,
            completed=goal.completed
        )
        for goal in goals
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8089)

