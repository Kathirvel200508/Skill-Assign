from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Worker Schemas
class WorkerCreate(BaseModel):
    name: str
    age: int = Field(gt=0, le=100)
    experience: float = Field(ge=0)
    skills: List[str]
    fatigue_level: float = Field(default=0.0, ge=0, le=1)
    hours_per_day: float = Field(default=8.0, ge=0, le=8.5)
    hours_per_week: float = Field(default=40.0, ge=0, le=52)
    current_role: Optional[str] = None
    performance_score: float = Field(default=0.5, ge=0, le=1)

class WorkerUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    experience: Optional[float] = None
    skills: Optional[List[str]] = None
    fatigue_level: Optional[float] = None
    hours_per_day: Optional[float] = None
    hours_per_week: Optional[float] = None
    current_role: Optional[str] = None
    performance_score: Optional[float] = None

class WorkerResponse(BaseModel):
    id: int
    name: str
    age: int
    experience: float
    skills: List[str]
    fatigue_level: float
    hours_per_day: float
    hours_per_week: float
    current_role: Optional[str]
    performance_score: float
    created_at: datetime
    
    class Config:
        from_attributes = True

# Role Schemas
class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None
    required_skills: List[str]
    difficulty_level: float = Field(ge=0, le=1)
    typical_tasks: Optional[List[str]] = None
    success_criteria: Optional[str] = None

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    required_skills: Optional[List[str]] = None
    difficulty_level: Optional[float] = None
    typical_tasks: Optional[List[str]] = None
    success_criteria: Optional[str] = None
    current_assignee_id: Optional[int] = None

class RoleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    required_skills: List[str]
    difficulty_level: float
    typical_tasks: Optional[List[str]]
    success_criteria: Optional[str]
    current_assignee_id: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Assignment Schemas
class AssignmentCreate(BaseModel):
    worker_id: int
    role_id: int
    fit_score: float
    task_id: Optional[int] = None

class AssignmentFeedback(BaseModel):
    success: bool
    feedback: Optional[str] = None

class AssignmentResponse(BaseModel):
    id: int
    worker_id: int
    role_id: int
    fit_score: float
    success: Optional[bool]
    assigned_at: datetime
    completed_at: Optional[datetime]
    task_id: Optional[int]
    
    class Config:
        from_attributes = True

# Prediction Schemas
class PredictFitRequest(BaseModel):
    role_id: int
    top_n: int = Field(default=3, ge=1, le=10)

class WorkerRecommendation(BaseModel):
    worker_id: int
    worker_name: str
    fit_score: float
    confidence: float
    skills: List[str]
    fatigue_level: float
    hours_per_day: float
    hours_per_week: float
    performance_score: float
    skill_match_percentage: float

class PredictFitResponse(BaseModel):
    role_id: int
    role_name: str
    recommendations: List[WorkerRecommendation]

# Analytics Schemas
class AnalyticsOverview(BaseModel):
    total_workers: int
    total_roles: int
    total_assignments: int
    average_fit_score: float
    success_rate: float
    workers_by_fatigue: dict
    top_performers: List[dict]
    skills_distribution: dict  # skill -> count of workers
    average_hours_per_week: dict  # worker_id -> avg hours

class SkillRecommendation(BaseModel):
    worker_id: int
    worker_name: str
    current_skills: List[str]
    recommended_skills: List[str]
    reason: str
    priority: str  # "High", "Medium", "Low"

class SkillGapAnalysis(BaseModel):
    workers_needing_training: List[SkillRecommendation]
    most_demanded_skills: List[dict]  # skill -> demand count

class RoleDescriptionResponse(BaseModel):
    role_id: int
    role_name: str
    description: str
    required_skills: List[str]
    difficulty_level: float
    typical_tasks: List[str]
    success_criteria: str

# Task Schemas
class TaskCreate(BaseModel):
    worker_id: int
    role_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")
    due_date: Optional[datetime] = None
    assigned_by: str = "Supervisor"

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(pending|in_progress|completed)$")
    due_date: Optional[datetime] = None

class TaskResponse(BaseModel):
    id: int
    worker_id: int
    role_id: Optional[int]
    title: str
    description: Optional[str]
    priority: str
    status: str
    assigned_by: str
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# Health Metric Schemas
class HealthMetricCreate(BaseModel):
    worker_id: int
    heart_rate: Optional[int] = None
    blood_pressure_systolic: Optional[int] = None
    blood_pressure_diastolic: Optional[int] = None
    oxygen_level: Optional[float] = None
    body_temperature: Optional[float] = None
    stress_level: Optional[float] = Field(None, ge=0, le=100)
    fatigue_score: Optional[float] = Field(None, ge=0, le=100)
    steps_count: int = 0
    calories_burned: float = 0.0
    hours_worked_today: float = 0.0
    device_id: Optional[str] = None

class HealthMetricResponse(BaseModel):
    id: int
    worker_id: int
    heart_rate: Optional[int]
    blood_pressure_systolic: Optional[int]
    blood_pressure_diastolic: Optional[int]
    oxygen_level: Optional[float]
    body_temperature: Optional[float]
    stress_level: Optional[float]
    fatigue_score: Optional[float]
    steps_count: int
    calories_burned: float
    hours_worked_today: float
    device_id: Optional[str]
    recorded_at: datetime
    
    class Config:
        from_attributes = True

class WorkerHealthSummary(BaseModel):
    worker_id: int
    worker_name: str
    latest_heart_rate: Optional[int]
    latest_oxygen_level: Optional[float]
    latest_stress_level: Optional[float]
    latest_fatigue_score: Optional[float]
    hours_worked_today: float
    hours_worked_this_week: float
    total_steps_today: int
    health_status: str  # "Good", "Warning", "Critical"
    alerts: List[str]  # Health alerts
    last_updated: datetime

# Work Session Schemas
class WorkSessionCreate(BaseModel):
    worker_id: int
    clock_in: datetime
    location: Optional[str] = None
    task_id: Optional[int] = None
    device_id: Optional[str] = None

class WorkSessionUpdate(BaseModel):
    clock_out: Optional[datetime] = None
    break_duration: Optional[float] = None
    location: Optional[str] = None

class WorkSessionResponse(BaseModel):
    id: int
    worker_id: int
    clock_in: datetime
    clock_out: Optional[datetime]
    total_hours: Optional[float]
    break_duration: float
    location: Optional[str]
    task_id: Optional[int]
    recorded_by: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class WorkerHoursReport(BaseModel):
    worker_id: int
    worker_name: str
    today_hours: float
    week_hours: float
    month_hours: float
    overtime_hours: float
    sessions_today: int
    average_session_length: float
    longest_shift: float
    status: str  # "Normal", "Approaching Limit", "Overtime"
