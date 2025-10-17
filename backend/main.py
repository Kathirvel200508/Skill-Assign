from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import engine, get_db
from ml_model import ml_model
from chatbot import chatbot
import random
from datetime import datetime, timedelta
from sqlalchemy import func

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

# Load ML model and chatbot on startup
@app.on_event("startup")
async def startup_event():
    ml_model.load()
    print("ML model loaded (if available)")
    
    # Load chatbot (optional, can be lazy-loaded)
    # chatbot.load_model()  # Uncomment to load on startup
    print("Chatbot ready (will load on first use)")

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

# ==================== TASK ENDPOINTS ====================

@app.post("/task/create", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    """Create a new task and assign it to a worker"""
    # Verify worker exists
    worker = db.query(models.Worker).filter(models.Worker.id == task.worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/task/worker/{worker_id}", response_model=List[schemas.TaskResponse])
def get_worker_tasks(worker_id: int, status: str = None, db: Session = Depends(get_db)):
    """Get all tasks for a specific worker"""
    query = db.query(models.Task).filter(models.Task.worker_id == worker_id)
    
    if status:
        query = query.filter(models.Task.status == status)
    
    tasks = query.order_by(models.Task.created_at.desc()).all()
    return tasks

@app.get("/task/worker/{worker_id}/notifications")
def get_worker_task_notifications(worker_id: int, db: Session = Depends(get_db)):
    """Get task notifications with worker and role details for mobile app"""
    tasks = db.query(models.Task).filter(
        models.Task.worker_id == worker_id,
        models.Task.status.in_(['pending', 'in_progress'])
    ).order_by(models.Task.created_at.desc()).all()
    
    notifications = []
    for task in tasks:
        # Get worker details
        worker = db.query(models.Worker).filter(models.Worker.id == task.worker_id).first()
        
        # Get role details if role_id exists
        role_name = None
        if task.role_id:
            role = db.query(models.Role).filter(models.Role.id == task.role_id).first()
            role_name = role.name if role else None
        
        notification = {
            "id": task.id,
            "task_id": task.id,
            "worker_id": task.worker_id,
            "worker_name": worker.name if worker else f"Worker {task.worker_id}",
            "role_id": task.role_id,
            "role_name": role_name or "No specific role",
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "status": task.status,
            "assigned_by": task.assigned_by,
            "due_date": task.due_date,
            "created_at": task.created_at,
            "is_new": (datetime.utcnow() - task.created_at).total_seconds() < 3600  # New if less than 1 hour old
        }
        notifications.append(notification)
    
    return {"notifications": notifications, "count": len(notifications)}

@app.get("/task/all", response_model=List[schemas.TaskResponse])
def get_all_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all tasks"""
    tasks = db.query(models.Task).order_by(models.Task.created_at.desc()).offset(skip).limit(limit).all()
    return tasks

@app.get("/task/{task_id}", response_model=schemas.TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get a specific task by ID"""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/task/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(get_db)):
    """Update task information (for workers to update status)"""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task_update.dict(exclude_unset=True)
    
    # If status is being updated to completed, set completed_at
    if update_data.get('status') == 'completed' and task.status != 'completed':
        update_data['completed_at'] = datetime.utcnow()
    
    for key, value in update_data.items():
        setattr(task, key, value)
    
    db.commit()
    db.refresh(task)
    return task

@app.delete("/task/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task"""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return None

# ==================== WEARABLE DEVICE / HEALTH ENDPOINTS ====================

@app.post("/health/metric", response_model=schemas.HealthMetricResponse, status_code=status.HTTP_201_CREATED)
def create_health_metric(metric: schemas.HealthMetricCreate, db: Session = Depends(get_db)):
    """Receive health data from wearable device"""
    # Verify worker exists
    worker = db.query(models.Worker).filter(models.Worker.id == metric.worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    
    db_metric = models.HealthMetric(**metric.dict())
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric

@app.get("/health/worker/{worker_id}", response_model=List[schemas.HealthMetricResponse])
def get_worker_health_metrics(worker_id: int, limit: int = 10, db: Session = Depends(get_db)):
    """Get recent health metrics for a specific worker"""
    metrics = db.query(models.HealthMetric).filter(
        models.HealthMetric.worker_id == worker_id
    ).order_by(models.HealthMetric.recorded_at.desc()).limit(limit).all()
    return metrics

@app.get("/health/worker/{worker_id}/latest", response_model=schemas.HealthMetricResponse)
def get_worker_latest_health(worker_id: int, db: Session = Depends(get_db)):
    """Get latest health metric for a worker"""
    metric = db.query(models.HealthMetric).filter(
        models.HealthMetric.worker_id == worker_id
    ).order_by(models.HealthMetric.recorded_at.desc()).first()
    
    if not metric:
        raise HTTPException(status_code=404, detail="No health data found for this worker")
    return metric

@app.get("/health/worker/{worker_id}/summary", response_model=schemas.WorkerHealthSummary)
def get_worker_health_summary(worker_id: int, db: Session = Depends(get_db)):
    """Get comprehensive health summary for a worker"""
    worker = db.query(models.Worker).filter(models.Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    
    # Get latest health metric
    latest_metric = db.query(models.HealthMetric).filter(
        models.HealthMetric.worker_id == worker_id
    ).order_by(models.HealthMetric.recorded_at.desc()).first()
    
    # Calculate hours worked today and this week
    today = datetime.utcnow().date()
    week_start = today - timedelta(days=today.weekday())
    
    today_sessions = db.query(models.WorkSession).filter(
        models.WorkSession.worker_id == worker_id,
        func.date(models.WorkSession.clock_in) == today
    ).all()
    
    week_sessions = db.query(models.WorkSession).filter(
        models.WorkSession.worker_id == worker_id,
        func.date(models.WorkSession.clock_in) >= week_start
    ).all()
    
    hours_today = sum(s.total_hours or 0 for s in today_sessions)
    hours_week = sum(s.total_hours or 0 for s in week_sessions)
    
    # Determine health status and alerts
    health_status = "Good"
    alerts = []
    
    if latest_metric:
        if latest_metric.heart_rate and latest_metric.heart_rate > 100:
            health_status = "Warning"
            alerts.append(f"Elevated heart rate: {latest_metric.heart_rate} bpm")
        
        if latest_metric.oxygen_level and latest_metric.oxygen_level < 95:
            health_status = "Warning"
            alerts.append(f"Low oxygen level: {latest_metric.oxygen_level}%")
        
        if latest_metric.stress_level and latest_metric.stress_level > 70:
            health_status = "Warning"
            alerts.append(f"High stress level: {latest_metric.stress_level}%")
        
        if latest_metric.fatigue_score and latest_metric.fatigue_score > 70:
            health_status = "Warning"
            alerts.append(f"High fatigue: {latest_metric.fatigue_score}%")
        
        if latest_metric.body_temperature and (latest_metric.body_temperature > 38.0 or latest_metric.body_temperature < 36.0):
            health_status = "Critical"
            alerts.append(f"Abnormal temperature: {latest_metric.body_temperature}°C")
    
    if hours_today > 8:
        alerts.append(f"Overtime today: {hours_today:.1f} hours")
    
    if hours_week > 45:
        alerts.append(f"High weekly hours: {hours_week:.1f} hours")
    
    return schemas.WorkerHealthSummary(
        worker_id=worker_id,
        worker_name=worker.name,
        latest_heart_rate=latest_metric.heart_rate if latest_metric else None,
        latest_oxygen_level=latest_metric.oxygen_level if latest_metric else None,
        latest_stress_level=latest_metric.stress_level if latest_metric else None,
        latest_fatigue_score=latest_metric.fatigue_score if latest_metric else None,
        hours_worked_today=hours_today,
        hours_worked_this_week=hours_week,
        total_steps_today=latest_metric.steps_count if latest_metric else 0,
        health_status=health_status,
        alerts=alerts,
        last_updated=latest_metric.recorded_at if latest_metric else datetime.utcnow()
    )

@app.get("/health/dashboard")
def get_health_dashboard(db: Session = Depends(get_db)):
    """Get health dashboard for all workers (for supervisor)"""
    workers = db.query(models.Worker).all()
    worker_summaries = []
    
    for worker in workers:
        try:
            summary = get_worker_health_summary(worker.id, db)
            worker_summaries.append(summary.dict())
        except:
            # Skip workers with no data
            pass
    
    # Calculate overall statistics
    total_workers = len(worker_summaries)
    workers_with_alerts = len([w for w in worker_summaries if w['alerts']])
    workers_critical = len([w for w in worker_summaries if w['health_status'] == 'Critical'])
    workers_warning = len([w for w in worker_summaries if w['health_status'] == 'Warning'])
    workers_good = len([w for w in worker_summaries if w['health_status'] == 'Good'])
    
    avg_hours_today = sum(w['hours_worked_today'] for w in worker_summaries) / total_workers if total_workers > 0 else 0
    avg_hours_week = sum(w['hours_worked_this_week'] for w in worker_summaries) / total_workers if total_workers > 0 else 0
    
    return {
        "workers": worker_summaries,
        "statistics": {
            "total_workers": total_workers,
            "workers_critical": workers_critical,
            "workers_warning": workers_warning,
            "workers_good": workers_good,
            "workers_with_alerts": workers_with_alerts,
            "average_hours_today": round(avg_hours_today, 2),
            "average_hours_this_week": round(avg_hours_week, 2)
        }
    }

# ==================== WORK SESSION ENDPOINTS ====================

@app.post("/session/clock-in", response_model=schemas.WorkSessionResponse, status_code=status.HTTP_201_CREATED)
def clock_in(session_data: schemas.WorkSessionCreate, db: Session = Depends(get_db)):
    """Worker clocks in (from wearable device)"""
    # Verify worker exists
    worker = db.query(models.Worker).filter(models.Worker.id == session_data.worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    
    # Check if there's an active session
    active_session = db.query(models.WorkSession).filter(
        models.WorkSession.worker_id == session_data.worker_id,
        models.WorkSession.clock_out == None
    ).first()
    
    if active_session:
        raise HTTPException(status_code=400, detail="Worker already clocked in. Please clock out first.")
    
    db_session = models.WorkSession(**session_data.dict())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

@app.put("/session/{session_id}/clock-out", response_model=schemas.WorkSessionResponse)
def clock_out(session_id: int, session_update: schemas.WorkSessionUpdate, db: Session = Depends(get_db)):
    """Worker clocks out"""
    session = db.query(models.WorkSession).filter(models.WorkSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session.clock_out:
        raise HTTPException(status_code=400, detail="Session already closed")
    
    # Set clock out time
    clock_out_time = session_update.clock_out or datetime.utcnow()
    session.clock_out = clock_out_time
    
    # Calculate total hours
    time_diff = clock_out_time - session.clock_in
    total_hours = time_diff.total_seconds() / 3600  # Convert to hours
    session.total_hours = round(total_hours - (session_update.break_duration or 0), 2)
    
    if session_update.break_duration:
        session.break_duration = session_update.break_duration
    
    if session_update.location:
        session.location = session_update.location
    
    db.commit()
    db.refresh(session)
    return session

@app.get("/session/worker/{worker_id}", response_model=List[schemas.WorkSessionResponse])
def get_worker_sessions(worker_id: int, limit: int = 10, db: Session = Depends(get_db)):
    """Get work sessions for a specific worker"""
    sessions = db.query(models.WorkSession).filter(
        models.WorkSession.worker_id == worker_id
    ).order_by(models.WorkSession.clock_in.desc()).limit(limit).all()
    return sessions

@app.get("/session/worker/{worker_id}/active", response_model=schemas.WorkSessionResponse)
def get_active_session(worker_id: int, db: Session = Depends(get_db)):
    """Get current active session for a worker"""
    session = db.query(models.WorkSession).filter(
        models.WorkSession.worker_id == worker_id,
        models.WorkSession.clock_out == None
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="No active session found")
    return session

@app.get("/session/worker/{worker_id}/hours", response_model=schemas.WorkerHoursReport)
def get_worker_hours_report(worker_id: int, db: Session = Depends(get_db)):
    """Get detailed hours worked report for a worker"""
    worker = db.query(models.Worker).filter(models.Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    
    today = datetime.utcnow().date()
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)
    
    # Query sessions
    today_sessions = db.query(models.WorkSession).filter(
        models.WorkSession.worker_id == worker_id,
        func.date(models.WorkSession.clock_in) == today,
        models.WorkSession.clock_out != None
    ).all()
    
    week_sessions = db.query(models.WorkSession).filter(
        models.WorkSession.worker_id == worker_id,
        func.date(models.WorkSession.clock_in) >= week_start,
        models.WorkSession.clock_out != None
    ).all()
    
    month_sessions = db.query(models.WorkSession).filter(
        models.WorkSession.worker_id == worker_id,
        func.date(models.WorkSession.clock_in) >= month_start,
        models.WorkSession.clock_out != None
    ).all()
    
    # Calculate hours
    today_hours = sum(s.total_hours or 0 for s in today_sessions)
    week_hours = sum(s.total_hours or 0 for s in week_sessions)
    month_hours = sum(s.total_hours or 0 for s in month_sessions)
    
    # Calculate overtime (over 8 hours/day or 40 hours/week)
    overtime_hours = max(0, week_hours - 40)
    
    # Other statistics
    sessions_today = len(today_sessions)
    avg_session = (today_hours / sessions_today) if sessions_today > 0 else 0
    longest_shift = max([s.total_hours for s in today_sessions], default=0)
    
    # Determine status
    status_text = "Normal"
    if week_hours > 45:
        status_text = "Overtime"
    elif week_hours > 40:
        status_text = "Approaching Limit"
    
    return schemas.WorkerHoursReport(
        worker_id=worker_id,
        worker_name=worker.name,
        today_hours=round(today_hours, 2),
        week_hours=round(week_hours, 2),
        month_hours=round(month_hours, 2),
        overtime_hours=round(overtime_hours, 2),
        sessions_today=sessions_today,
        average_session_length=round(avg_session, 2),
        longest_shift=round(longest_shift, 2),
        status=status_text
    )

@app.get("/session/all/hours")
def get_all_workers_hours(db: Session = Depends(get_db)):
    """Get hours worked report for all workers (for supervisor dashboard)"""
    workers = db.query(models.Worker).all()
    reports = []
    
    for worker in workers:
        try:
            report = get_worker_hours_report(worker.id, db)
            reports.append(report.dict())
        except:
            pass
    
    return {"workers": reports, "total_workers": len(reports)}

# ==================== AI CHATBOT ENDPOINTS ====================

@app.post("/chatbot/message")
def chat_with_assistant(message: str, db: Session = Depends(get_db)):
    """Chat with AI assistant about workforce data"""
    try:
        response = chatbot.generate_response(message, db)
        
        return {
            "response": response,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chatbot error: {str(e)}")

@app.get("/chatbot/status")
def get_chatbot_status():
    """Check chatbot status"""
    return {
        "loaded": chatbot.model is not None,
        "model": chatbot.model_name,
        "status": "ready" if chatbot.model else "rule-based (LLM not loaded)"
    }

@app.post("/chatbot/load")
def load_chatbot_model():
    """Load the UserLM-8b model"""
    try:
        print("[API] Loading chatbot model...")
        success = chatbot.load_model()
        if success:
            return {
                "success": True,
                "message": "UserLM-8b model loaded successfully!",
                "device": chatbot.device
            }
        else:
            return {
                "success": False,
                "message": "Failed to load model. Will use rule-based responses."
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading model: {str(e)}")

# ==================== DYNAMIC ML TRAINING ENDPOINTS ====================

@app.post("/ml/train")
def train_ml_model(incremental: bool = True, db: Session = Depends(get_db)):
    """Train or update ML model with latest data"""
    try:
        # Get all data
        workers = db.query(models.Worker).all()
        roles = db.query(models.Role).all()
        assignments = db.query(models.Assignment).filter(
            models.Assignment.success != None
        ).all()
        
        if len(assignments) < 5:
            raise HTTPException(
                status_code=400, 
                detail="Need at least 5 completed assignments to train model"
            )
        
        # Convert to dicts
        workers_data = [
            {
                'id': w.id, 
                'skills': w.skills, 
                'experience': w.experience,
                'performance_score': w.performance_score,
                'fatigue_level': w.fatigue_level,
                'age': w.age
            } for w in workers
        ]
        
        roles_data = [
            {
                'id': r.id,
                'required_skills': r.required_skills,
                'difficulty_level': r.difficulty_level
            } for r in roles
        ]
        
        assignments_data = [
            {
                'worker_id': a.worker_id,
                'role_id': a.role_id,
                'success': a.success
            } for a in assignments
        ]
        
        # Prepare training data
        X, y = ml_model.prepare_training_data(assignments_data, workers_data, roles_data)
        
        # Train
        results = ml_model.train(X, y, incremental=incremental)
        
        # Save model
        ml_model.save()
        
        return {
            "success": True,
            "details": results,
            "message": f"Model trained successfully with {len(assignments)} assignments"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training error: {str(e)}")

@app.get("/ml/status")
def get_ml_status(db: Session = Depends(get_db)):
    """Get ML model status"""
    assignment_count = db.query(models.Assignment).filter(
        models.Assignment.success != None
    ).count()
    
    return {
        "model_loaded": ml_model.model is not None,
        "training_data_available": assignment_count,
        "can_train": assignment_count >= 5,
        "skills_tracked": len(ml_model.all_skills) if ml_model.all_skills else 0
    }
