from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import engine, get_db
from ml_model import ml_model
import random
from datetime import datetime

# Create tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Skill-Based Role Assignment API",
    description="ML-powered workforce intelligence for smart factories",
    version="1.0.0"
)

# CORS middleware for React Native
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load ML model on startup
@app.on_event("startup")
async def startup_event():
    ml_model.load()
    print("ML model loaded (if available)")

# ==================== WORKER ENDPOINTS ====================

@app.post("/worker/add", response_model=schemas.WorkerResponse, status_code=status.HTTP_201_CREATED)
def add_worker(worker: schemas.WorkerCreate, db: Session = Depends(get_db)):
    """Add a new worker to the system"""
    db_worker = models.Worker(**worker.dict())
    db.add(db_worker)
    db.commit()
    db.refresh(db_worker)
    return db_worker

@app.get("/worker/all", response_model=List[schemas.WorkerResponse])
def get_all_workers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all workers"""
    workers = db.query(models.Worker).offset(skip).limit(limit).all()
    return workers

@app.get("/worker/{worker_id}", response_model=schemas.WorkerResponse)
def get_worker(worker_id: int, db: Session = Depends(get_db)):
    """Get a specific worker by ID"""
    worker = db.query(models.Worker).filter(models.Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    return worker

@app.put("/worker/{worker_id}", response_model=schemas.WorkerResponse)
def update_worker(worker_id: int, worker_update: schemas.WorkerUpdate, db: Session = Depends(get_db)):
    """Update worker information"""
    worker = db.query(models.Worker).filter(models.Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    
    update_data = worker_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(worker, key, value)
    
    db.commit()
    db.refresh(worker)
    return worker

@app.delete("/worker/{worker_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_worker(worker_id: int, db: Session = Depends(get_db)):
    """Delete a worker"""
    worker = db.query(models.Worker).filter(models.Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    
    db.delete(worker)
    db.commit()
    return None

# ==================== ROLE ENDPOINTS ====================

@app.post("/role/add", response_model=schemas.RoleResponse, status_code=status.HTTP_201_CREATED)
def add_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    """Add a new role to the system"""
    existing_role = db.query(models.Role).filter(models.Role.name == role.name).first()
    if existing_role:
        raise HTTPException(status_code=400, detail="Role with this name already exists")
    
    db_role = models.Role(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

@app.get("/role/all", response_model=List[schemas.RoleResponse])
def get_all_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all roles"""
    roles = db.query(models.Role).offset(skip).limit(limit).all()
    return roles

@app.get("/role/{role_id}", response_model=schemas.RoleResponse)
def get_role(role_id: int, db: Session = Depends(get_db)):
    """Get a specific role by ID"""
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@app.put("/role/{role_id}", response_model=schemas.RoleResponse)
def update_role(role_id: int, role_update: schemas.RoleUpdate, db: Session = Depends(get_db)):
    """Update role information"""
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    update_data = role_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(role, key, value)
    
    db.commit()
    db.refresh(role)
    return role

@app.delete("/role/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(role_id: int, db: Session = Depends(get_db)):
    """Delete a role"""
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    db.delete(role)
    db.commit()
    return None

# ==================== ML PREDICTION ENDPOINTS ====================

@app.post("/predict-fit", response_model=schemas.PredictFitResponse)
def predict_fit(request: schemas.PredictFitRequest, db: Session = Depends(get_db)):
    """Predict best workers for a given role using ML model"""
    role = db.query(models.Role).filter(models.Role.id == request.role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    workers = db.query(models.Worker).all()
    if not workers:
        raise HTTPException(status_code=404, detail="No workers available")
    
    recommendations = []
    
    for worker in workers:
        worker_data = {
            'id': worker.id,
            'name': worker.name,
            'age': worker.age,
            'experience': worker.experience,
            'skills': worker.skills,
            'fatigue_level': worker.fatigue_level,
            'performance_score': worker.performance_score
        }
        
        role_data = {
            'id': role.id,
            'name': role.name,
            'required_skills': role.required_skills,
            'difficulty_level': role.difficulty_level
        }
        
        fit_score, confidence = ml_model.predict(worker_data, role_data)
        
        worker_skills = set(worker.skills)
        required_skills = set(role.required_skills)
        skill_match_percentage = len(worker_skills.intersection(required_skills)) / len(required_skills) * 100 if required_skills else 0
        
        recommendations.append(schemas.WorkerRecommendation(
            worker_id=worker.id,
            worker_name=worker.name,
            fit_score=fit_score,
            confidence=confidence,
            skills=worker.skills,
            fatigue_level=worker.fatigue_level,
            hours_per_day=worker.hours_per_day,
            hours_per_week=worker.hours_per_week,
            performance_score=worker.performance_score,
            skill_match_percentage=skill_match_percentage
        ))
    
    recommendations.sort(key=lambda x: x.fit_score, reverse=True)
    top_recommendations = recommendations[:request.top_n]
    
    return schemas.PredictFitResponse(
        role_id=role.id,
        role_name=role.name,
        recommendations=top_recommendations
    )

@app.post("/train-model")
def train_model(db: Session = Depends(get_db)):
    """Train/Update ML model with historical assignment data"""
    assignments = db.query(models.Assignment).filter(models.Assignment.success.isnot(None)).all()
    
    if len(assignments) < 10:
        raise HTTPException(
            status_code=400, 
            detail=f"Insufficient training data. Need at least 10 labeled assignments, found {len(assignments)}"
        )
    
    workers = db.query(models.Worker).all()
    roles = db.query(models.Role).all()
    
    assignments_data = [
        {
            'worker_id': a.worker_id,
            'role_id': a.role_id,
            'success': a.success
        }
        for a in assignments
    ]
    
    workers_data = [
        {
            'id': w.id,
            'age': w.age,
            'experience': w.experience,
            'skills': w.skills,
            'fatigue_level': w.fatigue_level,
            'performance_score': w.performance_score
        }
        for w in workers
    ]
    
    roles_data = [
        {
            'id': r.id,
            'required_skills': r.required_skills,
            'difficulty_level': r.difficulty_level
        }
        for r in roles
    ]
    
    try:
        X, y = ml_model.prepare_training_data(assignments_data, workers_data, roles_data)
        metrics = ml_model.train(X, y)
        ml_model.save()
        
        return {
            "status": "success",
            "message": "Model trained successfully",
            "metrics": metrics,
            "training_samples": len(assignments)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")

# ==================== ASSIGNMENT ENDPOINTS ====================

@app.post("/assignment/create", response_model=schemas.AssignmentResponse, status_code=status.HTTP_201_CREATED)
def create_assignment(assignment: schemas.AssignmentCreate, db: Session = Depends(get_db)):
    """Create a new assignment"""
    worker = db.query(models.Worker).filter(models.Worker.id == assignment.worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    
    role = db.query(models.Role).filter(models.Role.id == assignment.role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    db_assignment = models.Assignment(**assignment.dict())
    db.add(db_assignment)
    
    worker.current_role = role.name
    role.current_assignee_id = worker.id
    
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

@app.put("/assignment/{assignment_id}/feedback")
def add_assignment_feedback(assignment_id: int, feedback: schemas.AssignmentFeedback, db: Session = Depends(get_db)):
    """Add feedback to an assignment (for model retraining)"""
    assignment = db.query(models.Assignment).filter(models.Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    assignment.success = feedback.success
    assignment.feedback = feedback.feedback
    assignment.completed_at = datetime.utcnow()
    
    db.commit()
    
    return {"status": "success", "message": "Feedback recorded"}

@app.get("/assignment/all", response_model=List[schemas.AssignmentResponse])
def get_all_assignments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all assignments"""
    assignments = db.query(models.Assignment).offset(skip).limit(limit).all()
    return assignments

# ==================== ANALYTICS ENDPOINTS ====================

@app.get("/analytics/overview", response_model=schemas.AnalyticsOverview)
def get_analytics_overview(db: Session = Depends(get_db)):
    """Get overall analytics and metrics"""
    total_workers = db.query(models.Worker).count()
    total_roles = db.query(models.Role).count()
    total_assignments = db.query(models.Assignment).count()
    
    assignments = db.query(models.Assignment).all()
    
    if assignments:
        avg_fit_score = sum(a.fit_score for a in assignments) / len(assignments)
        completed_assignments = [a for a in assignments if a.success is not None]
        success_rate = sum(1 for a in completed_assignments if a.success) / len(completed_assignments) if completed_assignments else 0
    else:
        avg_fit_score = 0
        success_rate = 0
    
    workers = db.query(models.Worker).all()
    workers_by_fatigue = {
        "low": sum(1 for w in workers if w.fatigue_level < 0.3),
        "medium": sum(1 for w in workers if 0.3 <= w.fatigue_level < 0.7),
        "high": sum(1 for w in workers if w.fatigue_level >= 0.7)
    }
    
    top_performers = sorted(workers, key=lambda w: w.performance_score, reverse=True)[:5]
    top_performers_list = [
        {"id": w.id, "name": w.name, "performance_score": w.performance_score}
        for w in top_performers
    ]
    
    # Skills distribution
    skills_distribution = {}
    for worker in workers:
        for skill in worker.skills:
            skills_distribution[skill] = skills_distribution.get(skill, 0) + 1
    
    # Average hours per week by worker
    average_hours_per_week = {
        str(w.id): {"name": w.name, "hours": w.hours_per_week}
        for w in workers
    }
    
    return schemas.AnalyticsOverview(
        total_workers=total_workers,
        total_roles=total_roles,
        total_assignments=total_assignments,
        average_fit_score=avg_fit_score,
        success_rate=success_rate,
        workers_by_fatigue=workers_by_fatigue,
        top_performers=top_performers_list,
        skills_distribution=skills_distribution,
        average_hours_per_week=average_hours_per_week
    )

@app.get("/analytics/skill-gap", response_model=schemas.SkillGapAnalysis)
def get_skill_gap_analysis(db: Session = Depends(get_db)):
    """Analyze skill gaps and recommend training"""
    workers = db.query(models.Worker).all()
    roles = db.query(models.Role).all()
    
    # Collect all required skills across roles
    all_required_skills = set()
    skill_demand = {}
    for role in roles:
        for skill in role.required_skills:
            all_required_skills.add(skill)
            skill_demand[skill] = skill_demand.get(skill, 0) + 1
    
    # Find workers who need training
    workers_needing_training = []
    for worker in workers:
        worker_skills = set(worker.skills)
        missing_skills = all_required_skills - worker_skills
        
        if missing_skills:
            # Prioritize based on performance and current workload
            if worker.performance_score > 0.7 and worker.hours_per_week < 48:
                priority = "High"
                reason = "High performer with capacity for growth"
            elif worker.performance_score > 0.5:
                priority = "Medium"
                reason = "Good potential for skill development"
            else:
                priority = "Low"
                reason = "Focus on current role mastery first"
            
            # Recommend top 3 most demanded missing skills
            recommended = sorted(
                [s for s in missing_skills],
                key=lambda s: skill_demand.get(s, 0),
                reverse=True
            )[:3]
            
            workers_needing_training.append(schemas.SkillRecommendation(
                worker_id=worker.id,
                worker_name=worker.name,
                current_skills=worker.skills,
                recommended_skills=recommended,
                reason=reason,
                priority=priority
            ))
    
    # Sort by priority
    priority_order = {"High": 0, "Medium": 1, "Low": 2}
    workers_needing_training.sort(key=lambda x: priority_order[x.priority])
    
    # Most demanded skills
    most_demanded = [
        {"skill": skill, "demand": count}
        for skill, count in sorted(skill_demand.items(), key=lambda x: x[1], reverse=True)
    ]
    
    return schemas.SkillGapAnalysis(
        workers_needing_training=workers_needing_training,
        most_demanded_skills=most_demanded
    )

@app.get("/role/{role_id}/description", response_model=schemas.RoleDescriptionResponse)
def get_role_description(role_id: int, db: Session = Depends(get_db)):
    """Get detailed role description"""
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    return schemas.RoleDescriptionResponse(
        role_id=role.id,
        role_name=role.name,
        description=role.description or "No description available",
        required_skills=role.required_skills,
        difficulty_level=role.difficulty_level,
        typical_tasks=role.typical_tasks or [],
        success_criteria=role.success_criteria or "Complete assigned tasks efficiently"
    )

# ==================== UTILITY ENDPOINTS ====================

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Skill-Based Role Assignment API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
