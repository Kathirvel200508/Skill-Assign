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
