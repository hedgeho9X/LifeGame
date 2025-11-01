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
    skill_rewards: Dict[str, int] = {}
    
    class Config:
        from_attributes = True

# Conversation Schemas
class ConversationCreate(BaseModel):
    goal_id: int
    user_message: str

class ConversationMessage(BaseModel):
    role: str
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class ConversationResponse(BaseModel):
    message: ConversationMessage
    updated_tasks: Optional[List[TaskResponse]] = None

class ApplyTaskUpdatesRequest(BaseModel):
    goal_id: int

class ApplyTaskUpdatesResponse(BaseModel):
    success: bool
    summary: str
    tasks: List[TaskResponse]

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
    praise_messages: List[str] = []  # 夸赞弹幕语句
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
    therapy_ticket_awarded: bool = False  # 是否获得话疗券

# Therapy Ticket Schemas
class TherapyTicketResponse(BaseModel):
    id: int
    user_id: int
    goal_id: int
    used: bool
    created_at: datetime
    used_at: Optional[datetime] = None
    goal_text: str  # 关联的目标文本
    
    class Config:
        from_attributes = True

class TherapyChatRequest(BaseModel):
    ticket_id: int
    user_message: Optional[str] = None  # 第一次可以为空，AI主动开场

class TherapyChatResponse(BaseModel):
    message: str  # AI回复
    is_opening: bool  # 是否是开场白

class ResetStatsResponse(BaseModel):
    success: bool
    message: str

