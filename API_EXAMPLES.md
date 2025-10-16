# 📡 API Examples & Testing Guide

Complete examples for testing all API endpoints using curl, Postman, or any HTTP client.

## Base URL
```
http://localhost:8000
```

## 🧑 Worker Management

### 1. Add New Worker
```bash
curl -X POST http://localhost:8000/worker/add \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "age": 30,
    "experience": 5.5,
    "skills": ["welding", "assembly", "quality_check"],
    "fatigue_level": 0.3,
    "performance_score": 0.85
  }'
```

**Response:**
```json
{
  "id": 11,
  "name": "John Doe",
  "age": 30,
  "experience": 5.5,
  "skills": ["welding", "assembly", "quality_check"],
  "fatigue_level": 0.3,
  "current_role": null,
  "performance_score": 0.85,
  "created_at": "2024-10-16T05:30:00Z"
}
```

### 2. Get All Workers
```bash
curl http://localhost:8000/worker/all
```

### 3. Get Worker by ID
```bash
curl http://localhost:8000/worker/1
```

### 4. Update Worker
```bash
curl -X PUT http://localhost:8000/worker/1 \
  -H "Content-Type: application/json" \
  -d '{
    "fatigue_level": 0.2,
    "performance_score": 0.90
  }'
```

### 5. Delete Worker
```bash
curl -X DELETE http://localhost:8000/worker/1
```

## 🎯 Role Management

### 1. Add New Role
```bash
curl -X POST http://localhost:8000/role/add \
  -H "Content-Type: application/json" \
  -d '{
    "name": "CNC Operator",
    "required_skills": ["machine_operation", "programming", "maintenance"],
    "difficulty_level": 0.75
  }'
```

**Response:**
```json
{
  "id": 7,
  "name": "CNC Operator",
  "required_skills": ["machine_operation", "programming", "maintenance"],
  "difficulty_level": 0.75,
  "current_assignee_id": null,
  "created_at": "2024-10-16T05:30:00Z"
}
```

### 2. Get All Roles
```bash
curl http://localhost:8000/role/all
```

### 3. Get Role by ID
```bash
curl http://localhost:8000/role/1
```

### 4. Update Role
```bash
curl -X PUT http://localhost:8000/role/1 \
  -H "Content-Type: application/json" \
  -d '{
    "difficulty_level": 0.65
  }'
```

### 5. Delete Role
```bash
curl -X DELETE http://localhost:8000/role/1
```

## 🤖 ML Prediction

### 1. Get Worker Recommendations for Role
```bash
curl -X POST http://localhost:8000/predict-fit \
  -H "Content-Type: application/json" \
  -d '{
    "role_id": 1,
    "top_n": 5
  }'
```

**Response:**
```json
{
  "role_id": 1,
  "role_name": "Assembly Line Operator",
  "recommendations": [
    {
      "worker_id": 2,
      "worker_name": "Priya Sharma",
      "fit_score": 0.92,
      "confidence": 0.85,
      "skills": ["welding", "machine_operation", "maintenance"],
      "fatigue_level": 0.1,
      "performance_score": 0.92,
      "skill_match_percentage": 100.0
    },
    {
      "worker_id": 1,
      "worker_name": "Rajesh Kumar",
      "fit_score": 0.85,
      "confidence": 0.80,
      "skills": ["welding", "assembly", "quality_check"],
      "fatigue_level": 0.2,
      "performance_score": 0.85,
      "skill_match_percentage": 66.67
    }
  ]
}
```

### 2. Train ML Model
```bash
curl -X POST http://localhost:8000/train-model
```

**Response:**
```json
{
  "status": "success",
  "message": "Model trained successfully",
  "metrics": {
    "mse": 0.045,
    "r2": 0.87,
    "train_samples": 10,
    "test_samples": 3
  },
  "training_samples": 13
}
```

**Note:** Requires at least 10 assignments with feedback (success field set).

## 📋 Assignment Management

### 1. Create Assignment
```bash
curl -X POST http://localhost:8000/assignment/create \
  -H "Content-Type: application/json" \
  -d '{
    "worker_id": 2,
    "role_id": 1,
    "fit_score": 0.92
  }'
```

**Response:**
```json
{
  "id": 14,
  "worker_id": 2,
  "role_id": 1,
  "fit_score": 0.92,
  "success": null,
  "assigned_at": "2024-10-16T05:30:00Z",
  "completed_at": null
}
```

### 2. Add Feedback to Assignment
```bash
curl -X PUT http://localhost:8000/assignment/14/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "success": true,
    "feedback": "Worker performed excellently. Completed all tasks ahead of schedule."
  }'
```

**Response:**
```json
{
  "status": "success",
  "message": "Feedback recorded"
}
```

### 3. Get All Assignments
```bash
curl http://localhost:8000/assignment/all
```

## 📊 Analytics

### Get Analytics Overview
```bash
curl http://localhost:8000/analytics/overview
```

**Response:**
```json
{
  "total_workers": 10,
  "total_roles": 6,
  "total_assignments": 14,
  "average_fit_score": 0.82,
  "success_rate": 0.92,
  "workers_by_fatigue": {
    "low": 6,
    "medium": 3,
    "high": 1
  },
  "top_performers": [
    {
      "id": 7,
      "name": "Karthik Iyer",
      "performance_score": 0.95
    },
    {
      "id": 2,
      "name": "Priya Sharma",
      "performance_score": 0.92
    }
  ]
}
```

## 🔍 Health Check

### Check API Health
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy"
}
```

## 📝 Complete Workflow Example

### Scenario: Assign best worker to a new role

```bash
# Step 1: Add a new role
curl -X POST http://localhost:8000/role/add \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Paint Shop Operator",
    "required_skills": ["painting", "quality_check", "safety"],
    "difficulty_level": 0.6
  }'
# Returns: role_id = 7

# Step 2: Get recommendations for this role
curl -X POST http://localhost:8000/predict-fit \
  -H "Content-Type: application/json" \
  -d '{
    "role_id": 7,
    "top_n": 3
  }'
# Returns: Top 3 workers with fit scores

# Step 3: Assign the best worker (e.g., worker_id = 5, fit_score = 0.88)
curl -X POST http://localhost:8000/assignment/create \
  -H "Content-Type: application/json" \
  -d '{
    "worker_id": 5,
    "role_id": 7,
    "fit_score": 0.88
  }'
# Returns: assignment_id = 15

# Step 4: After worker completes the role, add feedback
curl -X PUT http://localhost:8000/assignment/15/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "success": true,
    "feedback": "Excellent work quality"
  }'

# Step 5: Retrain model with new data
curl -X POST http://localhost:8000/train-model
# Model improves with new feedback data
```

## 🧪 Postman Collection

### Import into Postman

1. Create new collection: "Skill Assignment API"
2. Set base URL variable: `{{base_url}}` = `http://localhost:8000`
3. Add requests from examples above

### Example Postman Request

**POST** `{{base_url}}/predict-fit`

**Headers:**
```
Content-Type: application/json
```

**Body (raw JSON):**
```json
{
  "role_id": 1,
  "top_n": 3
}
```

## 🔐 Error Responses

### 404 Not Found
```json
{
  "detail": "Worker not found"
}
```

### 400 Bad Request
```json
{
  "detail": "Role with this name already exists"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "age"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Training failed: Insufficient training data"
}
```

## 💡 Tips

1. **Use the interactive docs**: Visit http://localhost:8000/docs for a web interface to test all endpoints
2. **Check response status codes**: 
   - 200: Success
   - 201: Created
   - 204: No Content (successful deletion)
   - 400: Bad Request
   - 404: Not Found
   - 422: Validation Error
   - 500: Server Error

3. **Model training**: Collect at least 10-15 assignments with feedback before training for best results
4. **Fit scores**: Range from 0-1, where >0.7 is good, >0.8 is excellent
5. **Fatigue levels**: 0-0.3 (low), 0.3-0.7 (medium), 0.7-1.0 (high)

## 📚 Additional Resources

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

**Happy Testing! 🚀**
