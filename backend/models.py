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
    task_id = Column(Integer, nullable=True)  # linked task for this assignment

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, nullable=False)
    role_id = Column(Integer, nullable=True)  # Optional role assignment
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    priority = Column(String, default="medium")  # low, medium, high
    status = Column(String, default="pending")  # pending, in_progress, completed
    assigned_by = Column(String, default="Supervisor")
    due_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

class HealthMetric(Base):
    __tablename__ = "health_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, nullable=False)
    heart_rate = Column(Integer, nullable=True)  # bpm
    blood_pressure_systolic = Column(Integer, nullable=True)  # mmHg
    blood_pressure_diastolic = Column(Integer, nullable=True)  # mmHg
    oxygen_level = Column(Float, nullable=True)  # SpO2 percentage
    body_temperature = Column(Float, nullable=True)  # Celsius
    stress_level = Column(Float, nullable=True)  # 0-100 scale
    fatigue_score = Column(Float, nullable=True)  # 0-100 scale
    steps_count = Column(Integer, default=0)  # daily steps
    calories_burned = Column(Float, default=0.0)  # kcal
    hours_worked_today = Column(Float, default=0.0)  # hours
    device_id = Column(String, nullable=True)  # wearable device identifier
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
    
class WorkSession(Base):
    __tablename__ = "work_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, nullable=False)
    clock_in = Column(DateTime(timezone=True), nullable=False)
    clock_out = Column(DateTime(timezone=True), nullable=True)
    total_hours = Column(Float, nullable=True)  # calculated on clock_out
    break_duration = Column(Float, default=0.0)  # hours
    location = Column(String, nullable=True)  # work location/station
    task_id = Column(Integer, nullable=True)  # linked task if any
    recorded_by = Column(String, default="Wearable Device")  # device or manual
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
