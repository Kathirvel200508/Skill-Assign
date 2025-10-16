# 🚀 Skill-Based Role Assignment & Workforce Intelligence for Smart Factories

A complete **mobile-first MVP** for automotive factories to intelligently assign factory workers to suitable roles based on their skills, fatigue level, and past performance using machine learning.

## 📋 Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [API Documentation](#api-documentation)
- [ML Model Details](#ml-model-details)
- [Testing](#testing)
- [Deployment](#deployment)

## ✨ Features

### 1. Worker Management
- Add, update, and delete workers
- Track worker attributes: name, age, experience, skills, fatigue level, current role, performance score
- View worker performance trends

### 2. Role Management
- Add factory roles with skill requirements and difficulty level
- View available roles, current assignees, and skill gaps
- Track role assignments

### 3. ML-Powered Skill-Based Assignment
- **XGBoost** machine learning model predicts "fit score" between workers and roles
- Features: worker skill vector, fatigue, experience, performance
- Output: Top 3-5 recommended workers per role with confidence scores
- Heuristic fallback when model is not trained

### 4. Dashboard & Analytics
- Role-wise recommendation list
- Worker performance metrics
- Fatigue distribution tracking
- Success rate analytics
- Manual override: Supervisors can accept/override model recommendations

### 5. Feedback Loop
- Supervisors mark assignment success
- System retrains ML model with new data
- Continuous improvement of predictions

## 🛠️ Tech Stack

### Backend
- **Framework:** FastAPI (Python)
- **Database:** PostgreSQL (with SQLite fallback)
- **ML Libraries:** XGBoost, Scikit-learn, Pandas, NumPy
- **ORM:** SQLAlchemy
- **API Docs:** Automatic Swagger/OpenAPI docs

### Frontend
- **Framework:** React Native (Expo)
- **UI Library:** React Native Paper
- **Navigation:** React Navigation
- **Charts:** React Native Chart Kit
- **HTTP Client:** Axios

## 📁 Project Structure

```
Skill-Assign/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── models.py               # SQLAlchemy database models
│   ├── schemas.py              # Pydantic schemas
│   ├── database.py             # Database configuration
│   ├── config.py               # Environment configuration
│   ├── ml_model.py             # ML model implementation
│   ├── init_db.py              # Database initialization script
│   ├── requirements.txt        # Python dependencies
│   ├── sample_data.csv         # Sample training data
│   └── .env.example            # Environment variables template
├── mobile/
│   ├── screens/
│   │   ├── DashboardScreen.js          # Main dashboard
│   │   ├── WorkerManagementScreen.js   # Worker CRUD
│   │   └── RoleManagementScreen.js     # Role CRUD
│   ├── api/
│   │   └── client.js           # API client
│   ├── App.js                  # Main app component
│   ├── config.js               # API configuration
│   ├── package.json            # Node dependencies
│   └── app.json                # Expo configuration
└── README.md                   # This file
```

## 🚀 Setup Instructions

### Prerequisites
- **Python 3.9+**
- **Node.js 16+** and npm
- **PostgreSQL 12+** (or use SQLite fallback)
- **Expo CLI** (for React Native)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database:**
   
   **Option A: PostgreSQL (Recommended)**
   ```bash
   # Create database
   psql -U postgres
   CREATE DATABASE skill_assign;
   \q
   
   # Copy and configure .env
   copy .env.example .env
   # Edit .env and set DATABASE_URL
   ```
   
   **Option B: SQLite (Quick Start)**
   ```bash
   # Copy and configure .env
   copy .env.example .env
   # Edit .env and set: USE_SQLITE_FALLBACK=true
   ```

5. **Initialize database with sample data:**
   ```bash
   python init_db.py
   ```

6. **Start the backend server:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

7. **Verify backend is running:**
   - Open browser: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Frontend Setup

1. **Navigate to mobile directory:**
   ```bash
   cd mobile
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Configure API endpoint:**
   
   Edit `mobile/config.js`:
   ```javascript
   // For Android Emulator
   const API_BASE_URL = 'http://10.0.2.2:8000';
   
   // For iOS Simulator
   const API_BASE_URL = 'http://localhost:8000';
   
   // For Physical Device (replace with your computer's IP)
   const API_BASE_URL = 'http://192.168.1.XXX:8000';
   ```

4. **Start Expo:**
   ```bash
   npx expo start
   ```

5. **Run on device/emulator:**
   - Press `a` for Android emulator
   - Press `i` for iOS simulator
   - Scan QR code with Expo Go app for physical device

## 📚 API Documentation

### Worker Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/worker/add` | Add new worker |
| `GET` | `/worker/all` | List all workers |
| `GET` | `/worker/{id}` | Get worker by ID |
| `PUT` | `/worker/{id}` | Update worker |
| `DELETE` | `/worker/{id}` | Delete worker |

### Role Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/role/add` | Add new role |
| `GET` | `/role/all` | List all roles |
| `GET` | `/role/{id}` | Get role by ID |
| `PUT` | `/role/{id}` | Update role |
| `DELETE` | `/role/{id}` | Delete role |

### ML Prediction Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/predict-fit` | Get worker recommendations for a role |
| `POST` | `/train-model` | Train/update ML model |

**Example Request:**
```json
POST /predict-fit
{
  "role_id": 1,
  "top_n": 3
}
```

**Example Response:**
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
    }
  ]
}
```

### Assignment Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/assignment/create` | Create new assignment |
| `PUT` | `/assignment/{id}/feedback` | Add feedback to assignment |
| `GET` | `/assignment/all` | List all assignments |

### Analytics Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/analytics/overview` | Get overall metrics |

## 🧠 ML Model Details

### Model Architecture
- **Algorithm:** XGBoost Regressor
- **Target:** Fit score (0-1) predicting worker-role compatibility
- **Features:**
  - Worker experience (years)
  - Worker fatigue level (0-1)
  - Worker performance score (0-1)
  - Worker age (normalized)
  - Role difficulty level (0-1)
  - Skill match count
  - Skill match percentage
  - One-hot encoded skills (top 20)

### Training Process
1. Collect historical assignment data with success labels
2. Extract features from worker and role data
3. Train XGBoost model with 80/20 train-test split
4. Save trained model to `models/fit_model.pkl`
5. Model automatically loads on backend startup

### Heuristic Fallback
When insufficient training data exists (<10 samples), the system uses a heuristic scoring:
- **40%** Skill match percentage
- **30%** Performance score
- **20%** Fatigue penalty (inverse)
- **10%** Experience

### Retraining
- Add feedback to assignments via `/assignment/{id}/feedback`
- Call `/train-model` endpoint when sufficient new data available
- Model automatically updates and improves predictions

## 🧪 Testing

### Backend Testing

1. **Test with Postman/Thunder Client:**
   - Import API from: http://localhost:8000/docs
   - Test all CRUD operations

2. **Sample Test Flow:**
   ```bash
   # 1. Get all workers
   GET http://localhost:8000/worker/all
   
   # 2. Get all roles
   GET http://localhost:8000/role/all
   
   # 3. Get recommendations for role ID 1
   POST http://localhost:8000/predict-fit
   {
     "role_id": 1,
     "top_n": 3
   }
   
   # 4. Create assignment
   POST http://localhost:8000/assignment/create
   {
     "worker_id": 2,
     "role_id": 1,
     "fit_score": 0.92
   }
   
   # 5. Add feedback
   PUT http://localhost:8000/assignment/1/feedback
   {
     "success": true,
     "feedback": "Excellent performance"
   }
   
   # 6. Train model
   POST http://localhost:8000/train-model
   ```

### Frontend Testing

1. **Android Emulator:**
   ```bash
   npx expo start --android
   ```

2. **iOS Simulator:**
   ```bash
   npx expo start --ios
   ```

3. **Physical Device:**
   - Install Expo Go app
   - Scan QR code from terminal
   - Ensure device is on same network as backend

## 🌐 Deployment

### Backend Deployment (Render/Heroku)

**Render:**
1. Create `render.yaml`:
   ```yaml
   services:
     - type: web
       name: skill-assign-api
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

2. Connect GitHub repo to Render
3. Add environment variables in Render dashboard

**Heroku:**
```bash
# Create Procfile
echo "web: uvicorn main:app --host 0.0.0.0 --port $PORT" > Procfile

# Deploy
heroku create skill-assign-api
git push heroku main
```

### Frontend Deployment

**Build for Production:**
```bash
# Android APK
eas build --platform android

# iOS IPA
eas build --platform ios
```

## 📊 Sample Data

The system comes preloaded with:
- **10 workers** with diverse skills and experience levels
- **6 factory roles** (Assembly, Welding, Quality, Automation, Machine Operation, Supervision)
- **13 sample assignments** for ML training

## 🔧 Troubleshooting

### Backend Issues

**Database connection error:**
- Verify PostgreSQL is running
- Check DATABASE_URL in .env
- Try SQLite fallback: `USE_SQLITE_FALLBACK=true`

**Module not found:**
```bash
pip install -r requirements.txt
```

**Port already in use:**
```bash
# Change port
uvicorn main:app --reload --port 8001
```

### Frontend Issues

**Cannot connect to backend:**
- Check API_BASE_URL in `mobile/config.js`
- For Android emulator, use `10.0.2.2:8000`
- For physical device, use computer's IP address
- Ensure backend is running

**Expo start fails:**
```bash
# Clear cache
npx expo start -c
```

**Module not found:**
```bash
npm install
```

## 📝 License

MIT License - feel free to use this project for your factory automation needs!

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open a GitHub issue or contact the development team.

---

**Built with ❤️ for Smart Factory Automation**
