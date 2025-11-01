from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    name: str
    background: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# UserStats Schemas
class UserStatsResponse(BaseModel):
    id: int
    user_id: int
    stats_data: Dict[str, int]
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Task Schemas
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    estimated_time: Optional[str] = None

class TaskResponse(TaskBase):
    id: int
    goal_id: int
    order: int
    completed: bool
    completed_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Goal Schemas
class GoalCreate(BaseModel):
    user_id: int
    goal_text: str
    user_background: Optional[str] = None  # 可选的用户背景信息

class GoalResponse(BaseModel):
    id: int
    user_id: int
    goal_text: str
    story: str
    tasks: List[TaskResponse]
    stats_data: Dict[str, int]  # 初始化的数值系统
    created_at: datetime
    completed: bool
    
    class Config:
        from_attributes = True

# Task Complete Schema
class TaskCompleteResponse(BaseModel):
    task_id: int
    completed: bool
    rewards: Dict[str, int]  # 获得的奖励
    updated_stats: Dict[str, int]  # 更新后的数值
    character_state: str  # 角色状态: celebrating, idle

