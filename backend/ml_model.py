import numpy as np
import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import xgboost as xgb
from typing import List, Tuple, Dict
import json

MODEL_PATH = "models/fit_model.pkl"
SCALER_PATH = "models/scaler.pkl"

class SkillAssignmentModel:
    def __init__(self):
        self.model = None
        self.feature_names = None
        self.all_skills = set()
        
    def _extract_features(self, worker_data: dict, role_data: dict, all_skills: set) -> np.ndarray:
        """
        Extract features from worker and role data
        Features:
        - Worker experience
        - Worker fatigue level
        - Worker performance score
        - Worker age (normalized)
        - Role difficulty level
        - Skill match count
        - Skill match percentage
        - One-hot encoded skills
        """
        features = []
        
        # Basic features
        features.append(worker_data.get('experience', 0))
        features.append(worker_data.get('fatigue_level', 0))
        features.append(worker_data.get('performance_score', 0.5))
        features.append(worker_data.get('age', 25) / 100.0)  # normalize age
        features.append(role_data.get('difficulty_level', 0.5))
        
        # Skill matching features
        worker_skills = set(worker_data.get('skills', []))
        required_skills = set(role_data.get('required_skills', []))
        
        skill_match_count = len(worker_skills.intersection(required_skills))
        skill_match_percentage = skill_match_count / len(required_skills) if required_skills else 0
        
        features.append(skill_match_count)
        features.append(skill_match_percentage)
        
        # One-hot encode skills (top skills only to avoid explosion)
        for skill in sorted(all_skills):
            features.append(1 if skill in worker_skills else 0)
        
        return np.array(features)
    
    def prepare_training_data(self, assignments_data: List[dict], workers_data: List[dict], 
                             roles_data: List[dict]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepare training data from historical assignments
        """
        # Build lookup dictionaries
        workers_dict = {w['id']: w for w in workers_data}
        roles_dict = {r['id']: r for r in roles_data}
        
        # Collect all skills
        self.all_skills = set()
        for worker in workers_data:
            self.all_skills.update(worker.get('skills', []))
        for role in roles_data:
            self.all_skills.update(role.get('required_skills', []))
        
        # Limit to top 20 skills to avoid feature explosion
        skill_counts = {}
        for worker in workers_data:
            for skill in worker.get('skills', []):
                skill_counts[skill] = skill_counts.get(skill, 0) + 1
        
        self.all_skills = set(sorted(skill_counts.keys(), key=lambda x: skill_counts[x], reverse=True)[:20])
        
        X = []
        y = []
        
        for assignment in assignments_data:
            worker_id = assignment.get('worker_id')
            role_id = assignment.get('role_id')
            success = assignment.get('success')
            
            if worker_id in workers_dict and role_id in roles_dict and success is not None:
                worker = workers_dict[worker_id]
                role = roles_dict[role_id]
                
                features = self._extract_features(worker, role, self.all_skills)
                X.append(features)
                y.append(1.0 if success else 0.0)
        
        return np.array(X), np.array(y)
    
    def train(self, X: np.ndarray, y: np.ndarray, incremental: bool = False) -> Dict:
        """
        Train the XGBoost model (supports incremental training)
        """
        if len(X) == 0:
            raise ValueError("No training data available")
        
        if incremental and self.model is not None:
            # Incremental training - warm start with existing model
            print("[ML] Incremental training with new data...")
            self.model.fit(X, y, xgb_model=self.model.get_booster())
            
            return {
                'mode': 'incremental',
                'new_samples': len(X),
                'message': 'Model updated with new data'
            }
        else:
            # Full training
            print("[ML] Full model training...")
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Train XGBoost model
            self.model = xgb.XGBRegressor(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.1,
                random_state=42,
                objective='reg:squarederror'
            )
            
            self.model.fit(X_train, y_train)
            
            # Evaluate
            y_pred = self.model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            return {
                'mode': 'full',
                'mse': float(mse),
                'r2': float(r2),
                'train_samples': len(X_train),
                'test_samples': len(X_test)
            }
    
    def predict(self, worker_data: dict, role_data: dict) -> Tuple[float, float]:
        """
        Predict fit score for a worker-role pair
        Returns: (fit_score, confidence)
        """
        if self.model is None:
            # Return heuristic-based score if model not trained
            return self._heuristic_score(worker_data, role_data)
        
        features = self._extract_features(worker_data, role_data, self.all_skills)
        features = features.reshape(1, -1)
        
        fit_score = float(self.model.predict(features)[0])
        
        # Clip to [0, 1] range
        fit_score = max(0.0, min(1.0, fit_score))
        
        # Calculate confidence based on feature quality
        confidence = self._calculate_confidence(worker_data, role_data)
        
        return fit_score, confidence
    
    def _heuristic_score(self, worker_data: dict, role_data: dict) -> Tuple[float, float]:
        """
        Calculate heuristic-based fit score when model is not available
        """
        worker_skills = set(worker_data.get('skills', []))
        required_skills = set(role_data.get('required_skills', []))
        
        # Skill match component (40%)
        skill_match = len(worker_skills.intersection(required_skills)) / len(required_skills) if required_skills else 0
        
        # Performance component (30%)
        performance = worker_data.get('performance_score', 0.5)
        
        # Fatigue penalty (20%)
        fatigue_penalty = 1.0 - worker_data.get('fatigue_level', 0)
        
        # Experience component (10%)
        experience = min(worker_data.get('experience', 0) / 10.0, 1.0)
        
        fit_score = (skill_match * 0.4 + performance * 0.3 + fatigue_penalty * 0.2 + experience * 0.1)
        
        confidence = 0.7  # Lower confidence for heuristic
        
        return fit_score, confidence
    
    def _calculate_confidence(self, worker_data: dict, role_data: dict) -> float:
        """
        Calculate confidence score based on data quality
        """
        confidence = 0.8
        
        # Reduce confidence if worker has high fatigue
        if worker_data.get('fatigue_level', 0) > 0.7:
            confidence -= 0.1
        
        # Reduce confidence if worker is inexperienced
        if worker_data.get('experience', 0) < 1:
            confidence -= 0.1
        
        # Increase confidence if skills match well
        worker_skills = set(worker_data.get('skills', []))
        required_skills = set(role_data.get('required_skills', []))
        skill_match = len(worker_skills.intersection(required_skills)) / len(required_skills) if required_skills else 0
        
        if skill_match > 0.8:
            confidence += 0.1
        
        return max(0.5, min(1.0, confidence))
    
    def save(self, path: str = MODEL_PATH):
        """Save model to disk"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        model_data = {
            'model': self.model,
            'all_skills': list(self.all_skills)
        }
        joblib.dump(model_data, path)
    
    def load(self, path: str = MODEL_PATH):
        """Load model from disk"""
        if os.path.exists(path):
            model_data = joblib.load(path)
            self.model = model_data['model']
            self.all_skills = set(model_data['all_skills'])
            return True
        return False

# Global model instance
ml_model = SkillAssignmentModel()
