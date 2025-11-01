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
    created_at = Column(DateTime, default=datetime.utcnow)
    completed = Column(Boolean, default=False)
    
    # 关联
    user = relationship("User", back_populates="goals")
    tasks = relationship("Task", back_populates="goal")

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
    
    # 关联
    goal = relationship("Goal", back_populates="tasks")

