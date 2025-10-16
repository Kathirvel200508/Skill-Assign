from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, Boolean
from sqlalchemy.sql import func
from database import Base

class Worker(Base):
    __tablename__ = "workers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    experience = Column(Float, nullable=False)  # years
    skills = Column(JSON, nullable=False)  # list of skills
    fatigue_level = Column(Float, default=0.0)  # 0-1 scale (calculated from hours)
    hours_per_day = Column(Float, default=8.0)  # hours worked per day (max 8.5)
    hours_per_week = Column(Float, default=40.0)  # hours worked per week (max 52)
    current_role = Column(String, nullable=True)
    performance_score = Column(Float, default=0.5)  # 0-1 scale
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)  # role description
    required_skills = Column(JSON, nullable=False)  # list of required skills
    difficulty_level = Column(Float, nullable=False)  # 0-1 scale
    typical_tasks = Column(JSON, nullable=True)  # list of typical tasks
    success_criteria = Column(String, nullable=True)  # what defines success
    current_assignee_id = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Assignment(Base):
    __tablename__ = "assignments"
    
    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, nullable=False)
    role_id = Column(Integer, nullable=False)
    fit_score = Column(Float, nullable=False)  # predicted fit score
    success = Column(Boolean, nullable=True)  # actual outcome (for training)
    assigned_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    feedback = Column(String, nullable=True)
