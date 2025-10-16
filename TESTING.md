# 🧪 Testing Guide

Comprehensive testing guide for the Skill Assignment MVP.

## 📋 Table of Contents
- [Backend Testing](#backend-testing)
- [Frontend Testing](#frontend-testing)
- [ML Model Testing](#ml-model-testing)
- [Integration Testing](#integration-testing)
- [Performance Testing](#performance-testing)

## 🔙 Backend Testing

### Setup Test Environment

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python init_db.py  # Initialize with sample data
uvicorn main:app --reload
```

### Manual API Testing

#### 1. Health Check
```bash
curl http://localhost:8000/health
# Expected: {"status": "healthy"}
```

#### 2. Test Worker CRUD

**Create Worker:**
```bash
curl -X POST http://localhost:8000/worker/add \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Worker",
    "age": 28,
    "experience": 3.5,
    "skills": ["welding", "assembly"],
    "fatigue_level": 0.3,
    "performance_score": 0.8
  }'
# Expected: 201 Created with worker object
```

**Get All Workers:**
```bash
curl http://localhost:8000/worker/all
# Expected: Array of workers
```

**Update Worker:**
```bash
curl -X PUT http://localhost:8000/worker/1 \
  -H "Content-Type: application/json" \
  -d '{"fatigue_level": 0.2}'
# Expected: Updated worker object
```

**Delete Worker:**
```bash
curl -X DELETE http://localhost:8000/worker/11
# Expected: 204 No Content
```

#### 3. Test Role CRUD

**Create Role:**
```bash
curl -X POST http://localhost:8000/role/add \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Role",
    "required_skills": ["welding", "safety"],
    "difficulty_level": 0.7
  }'
# Expected: 201 Created with role object
```

**Get All Roles:**
```bash
curl http://localhost:8000/role/all
# Expected: Array of roles
```

#### 4. Test ML Predictions

**Get Recommendations:**
```bash
curl -X POST http://localhost:8000/predict-fit \
  -H "Content-Type: application/json" \
  -d '{"role_id": 1, "top_n": 3}'
# Expected: Recommendations with fit scores
```

**Train Model:**
```bash
curl -X POST http://localhost:8000/train-model
# Expected: Training metrics (MSE, R2, samples)
```

#### 5. Test Assignments

**Create Assignment:**
```bash
curl -X POST http://localhost:8000/assignment/create \
  -H "Content-Type: application/json" \
  -d '{
    "worker_id": 1,
    "role_id": 1,
    "fit_score": 0.85
  }'
# Expected: Assignment object
```

**Add Feedback:**
```bash
curl -X PUT http://localhost:8000/assignment/1/feedback \
  -H "Content-Type: application/json" \
  -d '{"success": true, "feedback": "Great work"}'
# Expected: Success message
```

#### 6. Test Analytics

```bash
curl http://localhost:8000/analytics/overview
# Expected: Analytics object with metrics
```

### Validation Testing

#### Test Invalid Data

**Invalid Age:**
```bash
curl -X POST http://localhost:8000/worker/add \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Invalid Worker",
    "age": -5,
    "experience": 3,
    "skills": ["welding"]
  }'
# Expected: 422 Validation Error
```

**Missing Required Fields:**
```bash
curl -X POST http://localhost:8000/worker/add \
  -H "Content-Type: application/json" \
  -d '{"name": "Incomplete"}'
# Expected: 422 Validation Error
```

**Duplicate Role Name:**
```bash
curl -X POST http://localhost:8000/role/add \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Assembly Line Operator",
    "required_skills": ["assembly"],
    "difficulty_level": 0.5
  }'
# Expected: 400 Bad Request (role exists)
```

### Edge Cases

**Non-existent Worker:**
```bash
curl http://localhost:8000/worker/9999
# Expected: 404 Not Found
```

**Train Model with Insufficient Data:**
```bash
# Delete most assignments first
curl -X POST http://localhost:8000/train-model
# Expected: 400 Bad Request (insufficient data)
```

**Predict for Non-existent Role:**
```bash
curl -X POST http://localhost:8000/predict-fit \
  -H "Content-Type: application/json" \
  -d '{"role_id": 9999, "top_n": 3}'
# Expected: 404 Not Found
```

## 📱 Frontend Testing

### Setup

```bash
cd mobile
npm install
npx expo start
```

### Manual Testing Checklist

#### Dashboard Screen

- [ ] Analytics cards display correctly
- [ ] All roles are listed
- [ ] "Find Best Workers" button works
- [ ] Recommendations modal opens
- [ ] Recommendations show correct data
- [ ] Fit scores are displayed (0-100%)
- [ ] Fatigue levels show correct colors
- [ ] "Assign Role" button creates assignment
- [ ] Success message appears after assignment
- [ ] Pull-to-refresh works
- [ ] Loading states display correctly
- [ ] Error handling works (backend offline)

#### Worker Management Screen

- [ ] All workers are listed
- [ ] Worker cards show all information
- [ ] Performance and fatigue chips display
- [ ] Skills are shown correctly
- [ ] "Add Worker" FAB opens modal
- [ ] Add form validates input
- [ ] New worker is created successfully
- [ ] Edit button opens pre-filled form
- [ ] Worker updates save correctly
- [ ] Delete confirmation dialog appears
- [ ] Worker deletion works
- [ ] Pull-to-refresh works
- [ ] Empty state handles no workers

#### Role Management Screen

- [ ] All roles are listed
- [ ] Required skills display correctly
- [ ] Difficulty bar shows correct level
- [ ] Current assignment shows if assigned
- [ ] Skill gap analysis displays
- [ ] Missing skills are highlighted
- [ ] "Add Role" FAB opens modal
- [ ] Add form validates input
- [ ] New role is created successfully
- [ ] Edit button opens pre-filled form
- [ ] Role updates save correctly
- [ ] Delete confirmation dialog appears
- [ ] Role deletion works
- [ ] Pull-to-refresh works

### Device Testing

#### Android Emulator
```bash
npx expo start --android
```

**Test:**
- [ ] App launches successfully
- [ ] Navigation works
- [ ] API calls succeed (use 10.0.2.2:8000)
- [ ] Forms work correctly
- [ ] Modals display properly
- [ ] Back button behavior correct

#### iOS Simulator (Mac only)
```bash
npx expo start --ios
```

**Test:**
- [ ] App launches successfully
- [ ] Navigation works
- [ ] API calls succeed
- [ ] Forms work correctly
- [ ] Modals display properly
- [ ] Safe area insets correct

#### Physical Device

**Setup:**
1. Install Expo Go app
2. Update `mobile/config.js` with computer's IP
3. Scan QR code

**Test:**
- [ ] App loads on same WiFi network
- [ ] All features work as on emulator
- [ ] Performance is acceptable
- [ ] Touch interactions smooth
- [ ] Keyboard behavior correct

### Error Handling Testing

**Backend Offline:**
1. Stop backend server
2. Try to load data in app
3. Verify error message displays
4. Verify app doesn't crash

**Network Timeout:**
1. Simulate slow network
2. Verify loading indicators
3. Verify timeout handling

**Invalid Data:**
1. Try to add worker with age 0
2. Verify validation message
3. Try to add role with empty name
4. Verify error handling

## 🧠 ML Model Testing

### Test Heuristic Scoring

**Before Training (< 10 samples):**

```bash
# Should use heuristic scoring
curl -X POST http://localhost:8000/predict-fit \
  -H "Content-Type: application/json" \
  -d '{"role_id": 1, "top_n": 3}'

# Verify:
# - Fit scores are between 0-1
# - Workers with matching skills score higher
# - Low fatigue workers score higher
# - High performance workers score higher
```

### Test Model Training

**Add Training Data:**

```bash
# Create 10+ assignments with feedback
for i in {1..10}; do
  curl -X POST http://localhost:8000/assignment/create \
    -H "Content-Type: application/json" \
    -d "{\"worker_id\": $((i % 10 + 1)), \"role_id\": $((i % 6 + 1)), \"fit_score\": 0.8}"
  
  curl -X PUT http://localhost:8000/assignment/$i/feedback \
    -H "Content-Type: application/json" \
    -d '{"success": true}'
done
```

**Train Model:**

```bash
curl -X POST http://localhost:8000/train-model

# Verify response includes:
# - status: "success"
# - metrics.mse (should be < 0.2)
# - metrics.r2 (should be > 0.5)
# - training_samples >= 10
```

### Test Model Predictions

**After Training:**

```bash
curl -X POST http://localhost:8000/predict-fit \
  -H "Content-Type: application/json" \
  -d '{"role_id": 1, "top_n": 5}'

# Verify:
# - Predictions use trained model
# - Fit scores are reasonable (0-1)
# - Confidence scores are present
# - Top workers have higher scores
```

### Test Model Persistence

**Restart Backend:**

```bash
# Stop and restart backend
# Model should auto-load from models/fit_model.pkl

curl -X POST http://localhost:8000/predict-fit \
  -H "Content-Type: application/json" \
  -d '{"role_id": 1, "top_n": 3}'

# Verify predictions still work
```

### Feature Extraction Testing

**Test Edge Cases:**

1. **Worker with no skills:**
   - Create worker with empty skills array
   - Get predictions
   - Verify low fit scores

2. **Role with no required skills:**
   - Create role with empty required_skills
   - Get predictions
   - Verify handling

3. **High fatigue worker:**
   - Create worker with fatigue_level = 0.9
   - Get predictions
   - Verify lower fit scores

4. **Perfect skill match:**
   - Create worker with exact skills as role
   - Get predictions
   - Verify high fit score

## 🔗 Integration Testing

### End-to-End Workflow 1: New Worker Assignment

```bash
# 1. Add new worker
WORKER_ID=$(curl -X POST http://localhost:8000/worker/add \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Integration Test Worker",
    "age": 30,
    "experience": 5,
    "skills": ["welding", "assembly"],
    "fatigue_level": 0.2,
    "performance_score": 0.85
  }' | jq -r '.id')

# 2. Get recommendations for a role
curl -X POST http://localhost:8000/predict-fit \
  -H "Content-Type: application/json" \
  -d '{"role_id": 1, "top_n": 5}'

# 3. Create assignment
ASSIGNMENT_ID=$(curl -X POST http://localhost:8000/assignment/create \
  -H "Content-Type: application/json" \
  -d "{
    \"worker_id\": $WORKER_ID,
    \"role_id\": 1,
    \"fit_score\": 0.85
  }" | jq -r '.id')

# 4. Add feedback
curl -X PUT http://localhost:8000/assignment/$ASSIGNMENT_ID/feedback \
  -H "Content-Type: application/json" \
  -d '{"success": true, "feedback": "Excellent performance"}'

# 5. Verify analytics updated
curl http://localhost:8000/analytics/overview

# 6. Cleanup
curl -X DELETE http://localhost:8000/worker/$WORKER_ID
```

### End-to-End Workflow 2: Model Retraining

```bash
# 1. Get initial predictions
curl -X POST http://localhost:8000/predict-fit \
  -H "Content-Type: application/json" \
  -d '{"role_id": 1, "top_n": 3}' > before.json

# 2. Add multiple assignments with feedback
# (Add 5+ new assignments)

# 3. Retrain model
curl -X POST http://localhost:8000/train-model

# 4. Get new predictions
curl -X POST http://localhost:8000/predict-fit \
  -H "Content-Type: application/json" \
  -d '{"role_id": 1, "top_n": 3}' > after.json

# 5. Compare predictions
diff before.json after.json
```

## ⚡ Performance Testing

### Load Testing

**Test Concurrent Requests:**

```bash
# Install Apache Bench
# Windows: Download from Apache website
# Mac: brew install httpd
# Linux: sudo apt-get install apache2-utils

# Test worker endpoint
ab -n 100 -c 10 http://localhost:8000/worker/all

# Test prediction endpoint
ab -n 50 -c 5 -p predict.json -T application/json \
  http://localhost:8000/predict-fit

# Verify:
# - Requests per second > 50
# - No failed requests
# - Average response time < 200ms
```

### Database Performance

```bash
# Test with large dataset
# Add 100 workers
for i in {1..100}; do
  curl -X POST http://localhost:8000/worker/add \
    -H "Content-Type: application/json" \
    -d "{
      \"name\": \"Worker $i\",
      \"age\": $((20 + i % 40)),
      \"experience\": $((i % 15)),
      \"skills\": [\"skill1\", \"skill2\"],
      \"fatigue_level\": 0.3,
      \"performance_score\": 0.75
    }"
done

# Test query performance
time curl http://localhost:8000/worker/all
# Should complete in < 1 second
```

### ML Model Performance

```bash
# Test prediction speed
time curl -X POST http://localhost:8000/predict-fit \
  -H "Content-Type: application/json" \
  -d '{"role_id": 1, "top_n": 10}'

# With 100 workers, should complete in < 2 seconds
```

## 📊 Test Results Documentation

### Create Test Report

```markdown
## Test Report - [Date]

### Backend API Tests
- Total Endpoints Tested: 15
- Passed: 15
- Failed: 0
- Coverage: 100%

### Frontend Tests
- Screens Tested: 3
- Features Tested: 25
- Passed: 25
- Failed: 0

### ML Model Tests
- Heuristic Scoring: ✅ Pass
- Model Training: ✅ Pass
- Predictions: ✅ Pass
- Persistence: ✅ Pass

### Performance Tests
- API Response Time: 150ms avg
- Concurrent Users: 10 (no failures)
- Database Queries: < 100ms
- ML Predictions: < 500ms

### Issues Found
None

### Recommendations
- Add automated test suite
- Implement CI/CD pipeline
- Add monitoring and alerting
```

## 🤖 Automated Testing (Future)

### Backend Unit Tests (pytest)

```python
# test_api.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_create_worker():
    response = client.post("/worker/add", json={
        "name": "Test Worker",
        "age": 30,
        "experience": 5,
        "skills": ["welding"],
        "fatigue_level": 0.3,
        "performance_score": 0.8
    })
    assert response.status_code == 201
    assert response.json()["name"] == "Test Worker"
```

### Frontend Tests (Jest + React Native Testing Library)

```javascript
// DashboardScreen.test.js
import { render, fireEvent, waitFor } from '@testing-library/react-native';
import DashboardScreen from '../screens/DashboardScreen';

test('loads and displays roles', async () => {
  const { getByText } = render(<DashboardScreen />);
  
  await waitFor(() => {
    expect(getByText('Assembly Line Operator')).toBeTruthy();
  });
});
```

## ✅ Testing Checklist

### Before Each Release

- [ ] All API endpoints tested manually
- [ ] All frontend screens tested on Android
- [ ] All frontend screens tested on iOS
- [ ] ML model training tested
- [ ] ML predictions tested
- [ ] Database migrations tested
- [ ] Error handling verified
- [ ] Performance benchmarks met
- [ ] Security checks completed
- [ ] Documentation updated

---

**Thorough testing ensures a reliable MVP! 🎯**
