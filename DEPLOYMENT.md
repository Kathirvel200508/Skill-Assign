# 🚀 Deployment Guide

Complete guide for deploying the Skill Assignment MVP to production.

## 📋 Table of Contents
- [Prerequisites](#prerequisites)
- [Backend Deployment](#backend-deployment)
- [Database Setup](#database-setup)
- [Frontend Deployment](#frontend-deployment)
- [Environment Configuration](#environment-configuration)

## 🔧 Prerequisites

### Required Accounts
- GitHub account (for code repository)
- Render.com account (backend hosting) OR Heroku
- Railway.app account (database hosting) OR Render
- Expo account (mobile app deployment)

### Required Tools
- Git
- Python 3.9+
- Node.js 16+
- Expo CLI: `npm install -g expo-cli`
- EAS CLI: `npm install -g eas-cli`

## 🗄️ Database Setup

### Option 1: Render PostgreSQL (Recommended)

1. **Create PostgreSQL Database**
   - Go to https://render.com
   - Click "New +" → "PostgreSQL"
   - Name: `skill-assign-db`
   - Region: Choose closest to your users
   - Plan: Free tier for testing, Starter for production

2. **Get Connection Details**
   - Internal Database URL: `postgresql://user:pass@host/db`
   - External Database URL: `postgresql://user:pass@host:5432/db`

3. **Initialize Database**
   - Database will be auto-initialized by backend on first run

### Option 2: Railway PostgreSQL

1. **Create Project**
   - Go to https://railway.app
   - Click "New Project" → "Provision PostgreSQL"

2. **Get Connection String**
   - Click on PostgreSQL service
   - Copy "DATABASE_URL" from Variables tab

## 🔙 Backend Deployment

### Option 1: Render

1. **Create Web Service**
   - Go to Render Dashboard
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Root Directory: `backend`
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

2. **Environment Variables**
   Add in Render dashboard:
   ```
   DATABASE_URL=<your_postgres_url>
   ENVIRONMENT=production
   USE_SQLITE_FALLBACK=false
   ```

3. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Note your service URL: `https://skill-assign-api.onrender.com`

### Option 2: Heroku

1. **Create Heroku App**
   ```bash
   cd backend
   heroku create skill-assign-api
   ```

2. **Add PostgreSQL**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

3. **Create Procfile**
   ```bash
   echo "web: uvicorn main:app --host 0.0.0.0 --port $PORT" > Procfile
   ```

4. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

5. **Initialize Database**
   ```bash
   heroku run python init_db.py
   ```

### Option 3: Railway

1. **Create New Project**
   - Go to Railway dashboard
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository

2. **Configure Service**
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Add Environment Variables**
   ```
   DATABASE_URL=${{Postgres.DATABASE_URL}}
   ENVIRONMENT=production
   ```

## 📱 Frontend Deployment

### Build Android APK

1. **Configure EAS**
   ```bash
   cd mobile
   eas login
   eas build:configure
   ```

2. **Update API URL**
   Edit `mobile/config.js`:
   ```javascript
   const API_BASE_URL = 'https://your-backend-url.onrender.com';
   ```

3. **Build APK**
   ```bash
   eas build --platform android --profile preview
   ```

4. **Download APK**
   - Build will complete in 10-20 minutes
   - Download APK from Expo dashboard
   - Distribute to users via direct download or Play Store

### Build iOS App

1. **Requirements**
   - Apple Developer Account ($99/year)
   - Mac computer with Xcode

2. **Build IPA**
   ```bash
   eas build --platform ios --profile preview
   ```

3. **Distribute**
   - TestFlight for beta testing
   - App Store for production

### Publish OTA Updates

For quick updates without rebuilding:

```bash
eas update --branch production --message "Bug fixes"
```

## 🌐 Environment Configuration

### Backend (.env)

**Development:**
```env
DATABASE_URL=sqlite:///./skill_assign.db
ENVIRONMENT=development
USE_SQLITE_FALLBACK=true
```

**Production:**
```env
DATABASE_URL=postgresql://user:pass@host:5432/db
ENVIRONMENT=production
USE_SQLITE_FALLBACK=false
```

### Frontend (config.js)

**Development:**
```javascript
const API_BASE_URL = 'http://localhost:8000';
// or 'http://10.0.2.2:8000' for Android emulator
```

**Production:**
```javascript
const API_BASE_URL = 'https://skill-assign-api.onrender.com';
```

## 🔒 Security Checklist

Before going to production:

- [ ] Change default database passwords
- [ ] Restrict CORS to specific origins
- [ ] Add rate limiting
- [ ] Enable HTTPS only
- [ ] Add authentication (JWT)
- [ ] Set up database backups
- [ ] Configure logging and monitoring
- [ ] Add error tracking (Sentry)
- [ ] Review and minimize exposed endpoints
- [ ] Add input validation and sanitization

## 📊 Post-Deployment

### 1. Initialize Database

```bash
# SSH into your backend server or use Heroku CLI
python init_db.py
```

### 2. Verify API

```bash
curl https://your-backend-url.com/health
# Should return: {"status": "healthy"}

curl https://your-backend-url.com/worker/all
# Should return list of workers
```

### 3. Test Mobile App

- Open app on device
- Verify data loads from production API
- Test all CRUD operations
- Test ML predictions
- Check analytics dashboard

### 4. Train ML Model

```bash
curl -X POST https://your-backend-url.com/train-model
```

## 🔧 Troubleshooting

### Backend Issues

**Error: Database connection failed**
- Verify DATABASE_URL is correct
- Check database is running
- Verify network connectivity

**Error: Module not found**
- Ensure all dependencies in requirements.txt
- Rebuild and redeploy

**Error: Port binding failed**
- Ensure using $PORT environment variable
- Check start command uses `--port $PORT`

### Frontend Issues

**Error: Network request failed**
- Verify API_BASE_URL is correct
- Check backend is running
- Test API endpoint in browser

**Error: Build failed**
- Check all dependencies are installed
- Verify app.json configuration
- Check for syntax errors

## 📈 Scaling Recommendations

### Database
- Upgrade to paid tier for better performance
- Enable connection pooling
- Add read replicas for analytics
- Set up automated backups

### Backend
- Scale to multiple instances
- Add Redis for caching
- Use CDN for static assets
- Implement queue system for ML training

### Frontend
- Use CodePush for instant updates
- Implement offline mode
- Add analytics tracking
- Optimize bundle size

## 💰 Cost Estimates

### Free Tier (Testing)
- Render PostgreSQL: Free (expires after 90 days)
- Render Web Service: Free (spins down after inactivity)
- Expo: Free
- **Total: $0/month**

### Production (Small Scale)
- Render PostgreSQL: $7/month
- Render Web Service: $7/month
- Expo: Free
- **Total: $14/month**

### Production (Medium Scale)
- Railway PostgreSQL: $10/month
- Render Web Service (2 instances): $14/month
- Redis: $10/month
- Expo: Free
- **Total: $34/month**

## 📝 Deployment Checklist

- [ ] Database created and accessible
- [ ] Backend deployed and running
- [ ] Environment variables configured
- [ ] Database initialized with schema
- [ ] API endpoints tested
- [ ] Frontend built with production API URL
- [ ] Mobile app tested on devices
- [ ] ML model trained with sample data
- [ ] Documentation updated
- [ ] Monitoring and logging configured

## 🆘 Support

For deployment issues:
1. Check service logs (Render/Heroku dashboard)
2. Verify environment variables
3. Test API endpoints manually
4. Check database connectivity
5. Review error messages in logs

---

**Your MVP is now ready for production! 🎉**
