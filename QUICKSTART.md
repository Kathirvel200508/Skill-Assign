# ⚡ Quick Start Guide

Get the Skill Assignment MVP running in **5 minutes**!

## 🎯 Prerequisites Check

```bash
# Check Python version (need 3.9+)
python --version

# Check Node.js version (need 16+)
node --version

# Check if PostgreSQL is installed (optional - can use SQLite)
psql --version
```

## 🚀 Fast Setup (SQLite Mode)

### Step 1: Backend Setup (2 minutes)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file for SQLite
echo DATABASE_URL=sqlite:///./skill_assign.db > .env
echo USE_SQLITE_FALLBACK=true >> .env

# Initialize database with sample data
python init_db.py

# Start backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**✅ Backend should now be running at http://localhost:8000**

Open http://localhost:8000/docs to see API documentation!

### Step 2: Frontend Setup (2 minutes)

Open a **NEW terminal window**:

```bash
# Navigate to mobile directory
cd mobile

# Install dependencies
npm install

# Start Expo
npx expo start
```

### Step 3: Run Mobile App (1 minute)

**Option A: Android Emulator**
- Press `a` in the terminal
- App will open in Android emulator

**Option B: iOS Simulator (Mac only)**
- Press `i` in the terminal
- App will open in iOS simulator

**Option C: Physical Device**
1. Install "Expo Go" app from App Store/Play Store
2. Scan QR code shown in terminal
3. App will open on your device

**⚠️ For Physical Device:**
Edit `mobile/config.js` and replace `localhost` with your computer's IP:
```javascript
const API_BASE_URL = 'http://YOUR_IP_ADDRESS:8000';
```

Find your IP:
```bash
# Windows
ipconfig

# Mac/Linux
ifconfig
```

## 🎮 Test the App

### 1. Dashboard Screen
- View analytics overview
- See available roles
- Click "Find Best Workers" on any role
- View AI-powered recommendations
- Click "Assign Role" to assign a worker

### 2. Workers Screen
- View all workers with their skills and performance
- Click ➕ to add new worker
- Click ✏️ to edit worker
- Click 🗑️ to delete worker

### 3. Roles Screen
- View all roles with required skills
- See current assignments and skill gaps
- Click ➕ to add new role
- Click ✏️ to edit role
- Click 🗑️ to delete role

## 🧪 Test ML Model

### Train the Model

1. Make sure you have at least 10 assignments with feedback
2. Use Postman or curl:

```bash
curl -X POST http://localhost:8000/train-model
```

3. You should see training metrics:
```json
{
  "status": "success",
  "message": "Model trained successfully",
  "metrics": {
    "mse": 0.05,
    "r2": 0.85,
    "train_samples": 10,
    "test_samples": 3
  }
}
```

### Get Predictions

```bash
curl -X POST http://localhost:8000/predict-fit \
  -H "Content-Type: application/json" \
  -d '{"role_id": 1, "top_n": 3}'
```

## 📊 Sample Data Included

The system comes preloaded with:
- ✅ 10 workers with diverse skills
- ✅ 6 factory roles
- ✅ 13 sample assignments for ML training

## 🔧 Common Issues

### Backend won't start

**Error: "Address already in use"**
```bash
# Use different port
uvicorn main:app --reload --port 8001
```

**Error: "Module not found"**
```bash
# Make sure virtual environment is activated
pip install -r requirements.txt
```

### Frontend can't connect

**Error: "Network request failed"**

1. Check backend is running: http://localhost:8000
2. For Android emulator, edit `mobile/config.js`:
   ```javascript
   const API_BASE_URL = 'http://10.0.2.2:8000';
   ```
3. For physical device, use your computer's IP address

### Expo issues

**Error: "Metro bundler failed"**
```bash
# Clear cache
npx expo start -c
```

## 🎯 Next Steps

1. ✅ Explore the dashboard and test recommendations
2. ✅ Add your own workers and roles
3. ✅ Create assignments and add feedback
4. ✅ Train the ML model with real data
5. ✅ Check API documentation at http://localhost:8000/docs

## 📚 Full Documentation

See [README.md](README.md) for complete documentation including:
- Detailed API reference
- ML model architecture
- Deployment instructions
- PostgreSQL setup
- Advanced configuration

## 💡 Tips

- **Use SQLite for quick testing** - No database setup required!
- **Switch to PostgreSQL for production** - Better performance and scalability
- **Train model regularly** - More data = better predictions
- **Monitor fatigue levels** - System automatically factors in worker fatigue
- **Review skill gaps** - Check role assignments for missing skills

---

**Need help?** Check the [README.md](README.md) or open an issue on GitHub!
