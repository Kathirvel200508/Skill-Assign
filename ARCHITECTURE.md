# 🏗️ System Architecture

## Overview

The Skill-Based Role Assignment system follows a **client-server architecture** with a React Native mobile frontend, FastAPI backend, PostgreSQL database, and XGBoost ML model.

```
┌─────────────────────────────────────────────────────────────┐
│                     MOBILE APP (React Native)                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Dashboard   │  │   Workers    │  │    Roles     │      │
│  │   Screen     │  │   Screen     │  │   Screen     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         │                  │                  │              │
│         └──────────────────┴──────────────────┘              │
│                            │                                 │
│                     Axios HTTP Client                        │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              │ REST API (JSON)
                              │
┌─────────────────────────────▼───────────────────────────────┐
│                    BACKEND (FastAPI)                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                  API Endpoints                        │   │
│  │  /worker/*  /role/*  /predict-fit  /train-model     │   │
│  └────────────┬─────────────────────────┬────────────────┘   │
│               │                         │                    │
│  ┌────────────▼──────────┐  ┌──────────▼─────────────┐     │
│  │   Business Logic      │  │    ML Model Engine     │     │
│  │   (CRUD Operations)   │  │   (XGBoost Predictor)  │     │
│  └────────────┬──────────┘  └──────────┬─────────────┘     │
│               │                         │                    │
│  ┌────────────▼─────────────────────────▼─────────────┐     │
│  │              SQLAlchemy ORM                         │     │
│  └────────────┬────────────────────────────────────────┘     │
└───────────────┼──────────────────────────────────────────────┘
                │
┌───────────────▼────────────────────────────────────────┐
│              DATABASE (PostgreSQL/SQLite)              │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐        │
│  │ Workers  │  │  Roles   │  │ Assignments  │        │
│  └──────────┘  └──────────┘  └──────────────┘        │
└────────────────────────────────────────────────────────┘
```

## 📱 Frontend Architecture (React Native)

### Technology Stack
- **Framework**: React Native (Expo)
- **UI Library**: React Native Paper (Material Design)
- **Navigation**: React Navigation (Bottom Tabs)
- **HTTP Client**: Axios
- **State Management**: React Hooks (useState, useEffect)

### Screen Components

#### 1. Dashboard Screen
**Purpose**: Main hub for role assignments and analytics

**Features**:
- Analytics overview cards
- Role list with skill requirements
- ML-powered worker recommendations
- Assignment creation

**Key Functions**:
```javascript
loadData()              // Fetch roles and analytics
handleGetRecommendations(role)  // Get ML predictions
handleAssignWorker(workerId, roleId, fitScore)  // Create assignment
```

#### 2. Worker Management Screen
**Purpose**: CRUD operations for workers

**Features**:
- Worker list with performance metrics
- Add/Edit/Delete workers
- Skill and fatigue tracking
- Performance visualization

**Key Functions**:
```javascript
loadWorkers()           // Fetch all workers
handleAddWorker()       // Open add modal
handleEditWorker(worker)  // Open edit modal
handleDeleteWorker(worker)  // Delete with confirmation
handleSaveWorker()      // Create or update worker
```

#### 3. Role Management Screen
**Purpose**: CRUD operations for roles

**Features**:
- Role list with difficulty levels
- Required skills display
- Current assignment tracking
- Skill gap analysis

**Key Functions**:
```javascript
loadData()              // Fetch roles and workers
handleAddRole()         // Open add modal
handleEditRole(role)    // Open edit modal
handleDeleteRole(role)  // Delete with confirmation
handleSaveRole()        // Create or update role
getSkillGap(role)       // Calculate skill match
```

### API Client Structure

```javascript
// api/client.js
const api = axios.create({
  baseURL: config.API_BASE_URL,
  timeout: 10000,
});

// Organized by domain
workerAPI = { getAll, getById, add, update, delete }
roleAPI = { getAll, getById, add, update, delete }
predictionAPI = { predictFit, trainModel }
assignmentAPI = { create, addFeedback, getAll }
analyticsAPI = { getOverview }
```

## 🔧 Backend Architecture (FastAPI)

### Technology Stack
- **Framework**: FastAPI (async Python web framework)
- **ORM**: SQLAlchemy 2.0
- **Validation**: Pydantic v2
- **ML**: XGBoost, Scikit-learn
- **Database**: PostgreSQL (production) / SQLite (development)

### Layer Architecture

#### 1. API Layer (`main.py`)
**Responsibilities**:
- HTTP endpoint definitions
- Request/response handling
- CORS middleware
- Error handling

**Endpoint Groups**:
```python
# Worker endpoints
POST   /worker/add
GET    /worker/all
GET    /worker/{id}
PUT    /worker/{id}
DELETE /worker/{id}

# Role endpoints
POST   /role/add
GET    /role/all
GET    /role/{id}
PUT    /role/{id}
DELETE /role/{id}

# ML endpoints
POST   /predict-fit
POST   /train-model

# Assignment endpoints
POST   /assignment/create
PUT    /assignment/{id}/feedback
GET    /assignment/all

# Analytics endpoints
GET    /analytics/overview
```

#### 2. Data Models Layer (`models.py`)
**SQLAlchemy Models**:

```python
Worker
├── id: Integer (PK)
├── name: String
├── age: Integer
├── experience: Float
├── skills: JSON (list)
├── fatigue_level: Float
├── current_role: String
├── performance_score: Float
├── created_at: DateTime
└── updated_at: DateTime

Role
├── id: Integer (PK)
├── name: String (unique)
├── required_skills: JSON (list)
├── difficulty_level: Float
├── current_assignee_id: Integer
├── created_at: DateTime
└── updated_at: DateTime

Assignment
├── id: Integer (PK)
├── worker_id: Integer (FK)
├── role_id: Integer (FK)
├── fit_score: Float
├── success: Boolean (nullable)
├── assigned_at: DateTime
├── completed_at: DateTime (nullable)
└── feedback: String (nullable)
```

#### 3. Schema Layer (`schemas.py`)
**Pydantic Models for Validation**:

```python
# Request schemas
WorkerCreate, WorkerUpdate
RoleCreate, RoleUpdate
AssignmentCreate, AssignmentFeedback
PredictFitRequest

# Response schemas
WorkerResponse, RoleResponse
AssignmentResponse, PredictFitResponse
WorkerRecommendation, AnalyticsOverview
```

#### 4. Database Layer (`database.py`)
**Responsibilities**:
- Database connection management
- Session handling
- Connection pooling

```python
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    # Dependency injection for database sessions
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

#### 5. ML Model Layer (`ml_model.py`)
**Class**: `SkillAssignmentModel`

**Key Methods**:
```python
_extract_features(worker_data, role_data, all_skills)
    # Extract feature vector from worker and role

prepare_training_data(assignments, workers, roles)
    # Prepare X, y for training

train(X, y)
    # Train XGBoost model

predict(worker_data, role_data)
    # Predict fit score and confidence

_heuristic_score(worker_data, role_data)
    # Fallback scoring when model not trained

save(path) / load(path)
    # Model persistence
```

## 🧠 Machine Learning Pipeline

### Feature Engineering

**Input Features (per worker-role pair)**:
1. Worker experience (years)
2. Worker fatigue level (0-1)
3. Worker performance score (0-1)
4. Worker age (normalized by 100)
5. Role difficulty level (0-1)
6. Skill match count (integer)
7. Skill match percentage (0-1)
8. One-hot encoded skills (top 20 skills)

**Total Features**: 7 + 20 = 27 features

### Model Training Flow

```
┌─────────────────────────────────────────────────────┐
│  Historical Assignments (with success labels)       │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│  Feature Extraction                                  │
│  - Join worker and role data                        │
│  - Extract 27 features per assignment               │
│  - Create X (features) and y (success) matrices     │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│  Train/Test Split (80/20)                           │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│  XGBoost Training                                    │
│  - n_estimators: 100                                │
│  - max_depth: 5                                     │
│  - learning_rate: 0.1                               │
│  - objective: reg:squarederror                      │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│  Model Evaluation                                    │
│  - MSE (Mean Squared Error)                         │
│  - R² Score                                         │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│  Save Model (models/fit_model.pkl)                  │
└─────────────────────────────────────────────────────┘
```

### Prediction Flow

```
┌─────────────────────────────────────────────────────┐
│  Input: Role ID                                      │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│  Fetch all workers and role details                 │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│  For each worker:                                    │
│  1. Extract features                                │
│  2. Predict fit score (0-1)                         │
│  3. Calculate confidence                            │
│  4. Calculate skill match percentage                │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│  Sort by fit score (descending)                     │
│  Return top N recommendations                       │
└─────────────────────────────────────────────────────┘
```

### Heuristic Scoring (Fallback)

When model is not trained (< 10 samples):

```python
fit_score = (
    skill_match_percentage * 0.4 +    # 40% weight
    performance_score * 0.3 +          # 30% weight
    (1 - fatigue_level) * 0.2 +       # 20% weight
    min(experience / 10, 1.0) * 0.1   # 10% weight
)
```

## 🗄️ Database Schema

### Entity Relationship Diagram

```
┌─────────────────┐
│     Worker      │
│─────────────────│
│ id (PK)         │
│ name            │
│ age             │
│ experience      │
│ skills          │
│ fatigue_level   │
│ current_role    │
│ performance     │
└────────┬────────┘
         │
         │ 1:N
         │
         ▼
┌─────────────────┐       ┌─────────────────┐
│   Assignment    │   N:1 │      Role       │
│─────────────────│◄──────│─────────────────│
│ id (PK)         │       │ id (PK)         │
│ worker_id (FK)  │       │ name            │
│ role_id (FK)    │       │ required_skills │
│ fit_score       │       │ difficulty      │
│ success         │       │ assignee_id     │
│ assigned_at     │       └─────────────────┘
│ completed_at    │
│ feedback        │
└─────────────────┘
```

### Indexes

```sql
-- Primary keys (auto-indexed)
workers.id
roles.id
assignments.id

-- Unique constraints
roles.name

-- Foreign key indexes
assignments.worker_id
assignments.role_id
```

## 🔄 Data Flow Examples

### Example 1: Get Recommendations

```
User clicks "Find Best Workers" on Dashboard
    │
    ▼
DashboardScreen.handleGetRecommendations(role)
    │
    ▼
predictionAPI.predictFit(roleId, topN=5)
    │
    ▼
POST /predict-fit { role_id: 1, top_n: 5 }
    │
    ▼
FastAPI: predict_fit() endpoint
    │
    ├─► Fetch role from database
    ├─► Fetch all workers from database
    │
    ▼
For each worker:
    ml_model.predict(worker_data, role_data)
        │
        ├─► Extract 27 features
        ├─► Run XGBoost prediction
        └─► Calculate confidence
    │
    ▼
Sort by fit_score, take top 5
    │
    ▼
Return PredictFitResponse
    │
    ▼
Display recommendations in modal
    │
    ▼
User clicks "Assign Role"
    │
    ▼
assignmentAPI.create({ worker_id, role_id, fit_score })
    │
    ▼
POST /assignment/create
    │
    ▼
Create Assignment record
Update Worker.current_role
Update Role.current_assignee_id
    │
    ▼
Return success
    │
    ▼
Refresh dashboard
```

### Example 2: Train Model

```
Supervisor adds feedback to assignments
    │
    ▼
PUT /assignment/{id}/feedback { success: true }
    │
    ▼
Update Assignment.success = true
Update Assignment.completed_at
    │
    ▼
(Repeat for multiple assignments)
    │
    ▼
User/System triggers model training
    │
    ▼
POST /train-model
    │
    ▼
FastAPI: train_model() endpoint
    │
    ├─► Fetch assignments with success != null
    ├─► Fetch all workers
    ├─► Fetch all roles
    │
    ▼
ml_model.prepare_training_data()
    │
    ├─► Join data by worker_id and role_id
    ├─► Extract features for each assignment
    └─► Create X (features), y (success) matrices
    │
    ▼
ml_model.train(X, y)
    │
    ├─► Split train/test (80/20)
    ├─► Train XGBoost model
    ├─► Evaluate on test set
    └─► Calculate MSE and R²
    │
    ▼
ml_model.save()
    │
    └─► Save to models/fit_model.pkl
    │
    ▼
Return training metrics
```

## 🔒 Security Considerations

### Current Implementation
- CORS enabled for all origins (development)
- No authentication (MVP)
- Input validation via Pydantic
- SQL injection prevention via SQLAlchemy ORM

### Production Recommendations
1. **Authentication**: Add JWT tokens
2. **Authorization**: Role-based access control
3. **CORS**: Restrict to specific origins
4. **Rate Limiting**: Prevent API abuse
5. **HTTPS**: Encrypt data in transit
6. **Database**: Use connection pooling and prepared statements
7. **Input Sanitization**: Additional validation layers

## 📈 Scalability Considerations

### Current Limitations
- Single-server deployment
- Synchronous ML predictions
- In-memory model loading
- No caching layer

### Scaling Strategies

**Horizontal Scaling**:
- Load balancer (Nginx/HAProxy)
- Multiple FastAPI instances
- Shared PostgreSQL database
- Redis for session/cache

**Vertical Scaling**:
- Increase server resources
- Optimize database queries
- Add database indexes
- Use connection pooling

**ML Optimization**:
- Async prediction endpoints
- Model caching in Redis
- Batch predictions
- GPU acceleration for large models

**Database Optimization**:
- Read replicas for analytics
- Partitioning for large tables
- Query optimization
- Connection pooling

## 🔧 Configuration Management

### Environment Variables
```bash
DATABASE_URL          # Database connection string
ENVIRONMENT          # development/production
USE_SQLITE_FALLBACK  # true/false
```

### Frontend Configuration
```javascript
API_BASE_URL         # Backend API endpoint
```

## 📊 Monitoring & Logging

### Recommended Additions
1. **Application Logging**: Structured logs (JSON)
2. **Performance Monitoring**: Response times, error rates
3. **ML Metrics**: Prediction accuracy, model drift
4. **Database Monitoring**: Query performance, connection pool
5. **User Analytics**: Feature usage, success rates

### Tools
- **Backend**: Python logging, Sentry
- **Database**: PostgreSQL logs, pgAdmin
- **Frontend**: React Native Debugger, Sentry
- **Infrastructure**: Prometheus, Grafana

---

**Architecture designed for rapid MVP development with clear paths to production scaling.**
