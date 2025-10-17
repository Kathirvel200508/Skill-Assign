# 🏥 WEARABLE DEVICE INTEGRATION GUIDE

## ✅ Features Implemented

The system now integrates with **wearable devices** (smartwatches, fitness trackers) to monitor:

1. **Worker Health Metrics**
   - Heart rate (BPM)
   - Blood pressure (systolic/diastolic)
   - Oxygen level (SpO2 %)
   - Body temperature (°C)
   - Stress level (0-100)
   - Fatigue score (0-100)
   - Steps count
   - Calories burned

2. **Work Hours Tracking**
   - Clock in/out times
   - Total hours worked
   - Break duration
   - Daily, weekly, monthly reports
   - Overtime detection
   - Work location tracking

---

## 🔧 Backend API Endpoints

### **Health Metrics Endpoints**

#### 1. **Receive Health Data from Wearable**
```http
POST /health/metric
```

**Request Body:**
```json
{
  "worker_id": 1,
  "heart_rate": 75,
  "blood_pressure_systolic": 120,
  "blood_pressure_diastolic": 80,
  "oxygen_level": 98.5,
  "body_temperature": 36.8,
  "stress_level": 35.0,
  "fatigue_score": 25.0,
  "steps_count": 5000,
  "calories_burned": 350.0,
  "hours_worked_today": 6.5,
  "device_id": "WATCH_001"
}
```

**Response:** `201 Created`

---

#### 2. **Get Worker Health History**
```http
GET /health/worker/{worker_id}?limit=10
```

Returns recent health metrics for a worker.

---

#### 3. **Get Latest Health Reading**
```http
GET /health/worker/{worker_id}/latest
```

Returns the most recent health metric.

---

#### 4. **Get Worker Health Summary**
```http
GET /health/worker/{worker_id}/summary
```

**Response:**
```json
{
  "worker_id": 1,
  "worker_name": "Rajesh Kumar",
  "latest_heart_rate": 75,
  "latest_oxygen_level": 98.5,
  "latest_stress_level": 35.0,
  "latest_fatigue_score": 25.0,
  "hours_worked_today": 6.5,
  "hours_worked_this_week": 38.0,
  "total_steps_today": 5000,
  "health_status": "Good",  // "Good", "Warning", or "Critical"
  "alerts": [
    "Elevated heart rate: 105 bpm"
  ],
  "last_updated": "2025-10-17T01:15:00Z"
}
```

**Health Status Logic:**
- **Good:** All metrics within normal range
- **Warning:** 
  - Heart rate > 100 bpm
  - Oxygen level < 95%
  - Stress level > 70
  - Fatigue score > 70
  - Hours today > 8
  - Hours this week > 45
- **Critical:**
  - Body temperature > 38°C or < 36°C

---

#### 5. **Health Dashboard (All Workers)**
```http
GET /health/dashboard
```

**Response:**
```json
{
  "workers": [...],  // Array of worker health summaries
  "statistics": {
    "total_workers": 20,
    "workers_critical": 0,
    "workers_warning": 3,
    "workers_good": 17,
    "workers_with_alerts": 3,
    "average_hours_today": 6.8,
    "average_hours_this_week": 38.5
  }
}
```

---

### **Work Session Endpoints**

#### 1. **Clock In**
```http
POST /session/clock-in
```

**Request Body:**
```json
{
  "worker_id": 1,
  "clock_in": "2025-10-17T08:00:00Z",
  "location": "Assembly Line A",
  "task_id": 5,  // Optional
  "device_id": "WATCH_001"
}
```

**Response:** `201 Created`

---

#### 2. **Clock Out**
```http
PUT /session/{session_id}/clock-out
```

**Request Body:**
```json
{
  "clock_out": "2025-10-17T17:00:00Z",
  "break_duration": 1.0,  // hours
  "location": "Assembly Line A"
}
```

The system automatically calculates `total_hours` = (clock_out - clock_in) - break_duration

---

#### 3. **Get Worker Sessions**
```http
GET /session/worker/{worker_id}?limit=10
```

Returns recent work sessions.

---

#### 4. **Get Active Session**
```http
GET /session/worker/{worker_id}/active
```

Returns the current active session (if worker is clocked in).

---

#### 5. **Get Hours Report**
```http
GET /session/worker/{worker_id}/hours
```

**Response:**
```json
{
  "worker_id": 1,
  "worker_name": "Rajesh Kumar",
  "today_hours": 7.5,
  "week_hours": 38.0,
  "month_hours": 165.5,
  "overtime_hours": 0.0,
  "sessions_today": 1,
  "average_session_length": 7.5,
  "longest_shift": 8.5,
  "status": "Normal"  // "Normal", "Approaching Limit", "Overtime"
}
```

---

#### 6. **Hours Dashboard (All Workers)**
```http
GET /session/all/hours
```

Returns hours worked report for all workers.

---

## 📊 Supervisor Dashboard Features

### **What Supervisors Can See:**

1. **Real-Time Health Monitoring**
   - Heart rate, oxygen level, temperature
   - Stress and fatigue levels
   - Health status indicators (Good/Warning/Critical)
   - Instant alerts for concerning metrics

2. **Work Hours Tracking**
   - Current day hours
   - Weekly hours
   - Monthly totals
   - Overtime alerts
   - Break compliance

3. **Worker Status Overview**
   - Total workers monitored
   - Workers with health alerts
   - Workers in overtime
   - Average work hours

4. **Individual Worker Details**
   - Complete health history
   - Work session logs
   - Performance trends
   - Alert history

---

## 🔗 Integration with Mobile App

The mobile app will display:

1. **Worker's Own Health Data**
   - Current heart rate, oxygen, stress levels
   - Daily steps and calories
   - Health status and alerts

2. **Work Hours**
   - Hours worked today
   - Hours this week
   - Overtime warnings
   - Clock in/out buttons

3. **Smart Notifications**
   - "Take a break" when fatigue is high
   - "Hydrate" reminders
   - Overtime warnings
   - Health alerts

---

## 🧪 Testing the Features

### **1. Populate Sample Data**

```bash
cd backend
python populate_health_data.py
```

This creates:
- Health metrics for 10 workers
- Realistic vital signs
- Work session records

---

### **2. Test Health Dashboard**

Open browser: http://localhost:8000/health/dashboard

You'll see:
- List of all workers with their health status
- Statistics summary
- Workers with alerts highlighted

---

### **3. Test Hours Dashboard**

Open browser: http://localhost:8000/session/all/hours

You'll see:
- Hours worked by each worker
- Overtime status
- Session summaries

---

### **4. Test Individual Worker**

```bash
# Get health summary
curl http://localhost:8000/health/worker/1/summary

# Get hours report
curl http://localhost:8000/session/worker/1/hours
```

---

## 📱 Wearable Device Simulation

To simulate a wearable device sending data:

```python
import requests
import time
import random

API_URL = "http://localhost:8000"
WORKER_ID = 1
DEVICE_ID = "WATCH_001"

while True:
    # Send health metric every 60 seconds
    health_data = {
        "worker_id": WORKER_ID,
        "heart_rate": random.randint(60, 100),
        "oxygen_level": round(random.uniform(95.0, 100.0), 1),
        "body_temperature": round(random.uniform(36.2, 37.2), 1),
        "stress_level": round(random.uniform(20, 60), 1),
        "fatigue_score": round(random.uniform(10, 50), 1),
        "steps_count": random.randint(0, 100),
        "calories_burned": round(random.uniform(0, 10), 1),
        "device_id": DEVICE_ID
    }
    
    response = requests.post(f"{API_URL}/health/metric", json=health_data)
    print(f"Sent health data: HR={health_data['heart_rate']} bpm, O2={health_data['oxygen_level']}%")
    
    time.sleep(60)  # Send every minute
```

---

## 🎯 Use Cases

### **Use Case 1: Preventing Worker Burnout**

Supervisor sees Worker X has:
- Fatigue score: 85%
- Hours today: 9.5
- Stress level: 78%

**Action:** System sends alert, supervisor assigns break or shorter task.

---

### **Use Case 2: Health Emergency Detection**

Worker Y's wearable detects:
- Heart rate: 140 bpm (sudden spike)
- Oxygen level: 92% (low)
- Temperature: 38.5°C (fever)

**Action:** 
- Immediate alert to supervisor
- Worker's task status updated
- Emergency protocol initiated

---

### **Use Case 3: Overtime Management**

Worker Z has worked:
- 8.5 hours today
- 47 hours this week

**Action:**
- System flags as "Overtime"
- Supervisor notified
- Shift scheduling adjusted

---

### **Use Case 4: Performance Optimization**

ML system correlates:
- Workers with fatigue < 30% have 25% higher productivity
- Workers with > 45 hours/week show 15% more errors

**Action:**
- Shift schedules optimized
- Break times adjusted
- Task assignments balanced

---

## 📈 Dashboard Metrics

### **Health Dashboard Cards:**

1. **Total Workers Monitored**
2. **Critical Health Alerts**
3. **Workers Needing Break**
4. **Average Heart Rate**
5. **Average Stress Level**
6. **Workers in Good Health**

### **Hours Dashboard Cards:**

1. **Total Hours Today**
2. **Workers in Overtime**
3. **Average Work Hours**
4. **Workers Clocked In**
5. **Total Sessions Today**
6. **Compliance Rate**

---

## 🔐 Security & Privacy

- Health data is encrypted
- Access controlled by worker ID
- Supervisors see aggregated data
- Workers can view own detailed metrics
- HIPAA/GDPR compliant structure

---

## 🚀 Next Steps

1. ✅ **Backend Implemented**
2. ⏳ **Frontend Dashboard** (Next)
3. ⏳ **Mobile App Integration** (Next)
4. ⏳ **Real Wearable Device Integration**
5. ⏳ **Alert Notifications**

---

## 📝 API Documentation

Full interactive API docs available at:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

**Last Updated:** Oct 17, 2025, 1:15 AM
**Status:** ✅ Backend fully implemented and tested!
