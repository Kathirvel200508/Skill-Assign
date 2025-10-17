"""
Chatbot and Dynamic ML Training Endpoints
Add these to main.py
"""

# Add to schemas.py first:
"""
from pydantic import BaseModel

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    context: str = None

class TrainRequest(BaseModel):
    incremental: bool = True

class TrainResponse(BaseModel):
    success: bool
    details: dict
    message: str
"""

# Add these endpoints to main.py:

ENDPOINTS_CODE = """

# ==================== AI CHATBOT ENDPOINTS ====================

@app.post("/chatbot/message")
def chat_with_assistant(chat_msg: schemas.ChatMessage, db: Session = Depends(get_db)):
    \"\"\"Chat with AI assistant about workforce data\"\"\"
    try:
        response = chatbot.generate_response(chat_msg.message, db)
        
        return {
            "response": response,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chatbot error: {str(e)}")

@app.get("/chatbot/status")
def get_chatbot_status():
    \"\"\"Check chatbot status\"\"\"
    return {
        "loaded": chatbot.model is not None,
        "model": chatbot.model_name,
        "status": "ready" if chatbot.model else "not loaded"
    }

@app.post("/chatbot/load")
def load_chatbot():
    \"\"\"Load chatbot model\"\"\"
    try:
        success = chatbot.load_model()
        return {
            "success": success,
            "message": "Chatbot loaded successfully" if success else "Failed to load chatbot"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== DYNAMIC ML TRAINING ENDPOINTS ====================

@app.post("/ml/train")
def train_ml_model(train_req: schemas.TrainRequest, db: Session = Depends(get_db)):
    \"\"\"Train or update ML model with latest data\"\"\"
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
        results = ml_model.train(X, y, incremental=train_req.incremental)
        
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
    \"\"\"Get ML model status\"\"\"
    assignment_count = db.query(models.Assignment).filter(
        models.Assignment.success != None
    ).count()
    
    return {
        "model_loaded": ml_model.model is not None,
        "training_data_available": assignment_count,
        "can_train": assignment_count >= 5,
        "skills_tracked": len(ml_model.all_skills) if ml_model.all_skills else 0
    }

@app.post("/ml/retrain-on-new-data")
def auto_retrain(db: Session = Depends(get_db)):
    \"\"\"Automatically retrain when new successful assignments are added\"\"\"
    try:
        # Get recent successful assignments (last hour)
        recent_time = datetime.utcnow() - timedelta(hours=1)
        new_assignments = db.query(models.Assignment).filter(
            models.Assignment.success != None,
            models.Assignment.assigned_at >= recent_time
        ).all()
        
        if len(new_assignments) == 0:
            return {
                "trained": False,
                "message": "No new data to train on"
            }
        
        # Get all data for incremental training
        workers = db.query(models.Worker).all()
        roles = db.query(models.Role).all()
        
        workers_data = [
            {
                'id': w.id, 'skills': w.skills, 'experience': w.experience,
                'performance_score': w.performance_score, 'fatigue_level': w.fatigue_level,
                'age': w.age
            } for w in workers
        ]
        
        roles_data = [
            {'id': r.id, 'required_skills': r.required_skills, 
             'difficulty_level': r.difficulty_level} for r in roles
        ]
        
        assignments_data = [
            {'worker_id': a.worker_id, 'role_id': a.role_id, 'success': a.success} 
            for a in new_assignments
        ]
        
        # Prepare and train incrementally
        X, y = ml_model.prepare_training_data(assignments_data, workers_data, roles_data)
        results = ml_model.train(X, y, incremental=True)
        
        # Save
        ml_model.save()
        
        return {
            "trained": True,
            "new_samples": len(new_assignments),
            "details": results,
            "message": f"Model updated with {len(new_assignments)} new assignments"
        }
        
    except Exception as e:
        return {
            "trained": False,
            "error": str(e)
        }
"""

print(ENDPOINTS_CODE)
