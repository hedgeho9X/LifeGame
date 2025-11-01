from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    background = Column(Text)  # 个人背景信息
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关联
    goals = relationship("Goal", back_populates="user")
    stats = relationship("UserStats", back_populates="user", uselist=False)
    therapy_tickets = relationship("TherapyTicket", back_populates="user")

class UserStats(Base):
    __tablename__ = "user_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    stats_data = Column(JSON, default={})  # 存储数值系统 {key: value}
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联
    user = relationship("User", back_populates="stats")

class Goal(Base):
    __tablename__ = "goals"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    goal_text = Column(Text, nullable=False)
    story = Column(Text)  # AI 生成的游戏故事
    praise_messages = Column(JSON, default=[])  # AI生成的夸赞语句列表
    created_at = Column(DateTime, default=datetime.utcnow)
    completed = Column(Boolean, default=False)
    
    # 关联
    user = relationship("User", back_populates="goals")
    tasks = relationship("Task", back_populates="goal")
    conversations = relationship("Conversation", back_populates="goal", order_by="Conversation.created_at")
    therapy_tickets = relationship("TherapyTicket", back_populates="goal")

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    goal_id = Column(Integer, ForeignKey("goals.id"))
    title = Column(String(200), nullable=False)
    description = Column(Text)
    estimated_time = Column(String(50))
    order = Column(Integer)  # 任务顺序
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    skill_rewards = Column(JSON, default={})  # 每个任务的技能奖励
    
    # 关联
    goal = relationship("Goal", back_populates="tasks")

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    goal_id = Column(Integer, ForeignKey("goals.id"))
    role = Column(String(50), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关联
    goal = relationship("Goal", back_populates="conversations")

class TherapyTicket(Base):
    __tablename__ = "therapy_tickets"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    goal_id = Column(Integer, ForeignKey("goals.id"))  # 关联到完成的目标
    used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    used_at = Column(DateTime, nullable=True)
    
    # 关联
    user = relationship("User", back_populates="therapy_tickets")
    goal = relationship("Goal", back_populates="therapy_tickets")
    conversations = relationship("TherapyConversation", back_populates="ticket", order_by="TherapyConversation.created_at")

class TherapyConversation(Base):
    __tablename__ = "therapy_conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("therapy_tickets.id"))
    role = Column(String(50), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关联
    ticket = relationship("TherapyTicket", back_populates="conversations")
