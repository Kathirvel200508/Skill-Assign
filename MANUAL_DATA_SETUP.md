# 📝 MANUAL DATA POPULATION GUIDE

If the automated scripts don't work, here's how to manually add impressive demo data:

---

## 🎯 **METHOD 1: Using API Docs (Easiest)**

### **Step 1: Open API Documentation**
```
http://localhost:8000/docs
```

### **Step 2: Add Health Metrics**

1. Find **"POST /health/metric"** endpoint
2. Click **"Try it out"**
3. Paste this JSON:

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
  "steps_count": 8500,
  "calories_burned": 450.0,
  "hours_worked_today": 7.5,
  "device_id": "WATCH_001"
}
```

4. Click **"Execute"**
5. Repeat for worker_id 2, 3, 4, etc. (change worker_id and vary the numbers)

**Quick Variations:**
- worker_id: 1-10
- heart_rate: 65-95
- oxygen_level: 96.0-100.0
- stress_level: 20-60
- fatigue_score: 15-50

---

### **Step 3: Add Work Sessions**

1. Find **"POST /session/clock-in"** endpoint
2. Click **"Try it out"**
3. Paste this JSON:

```json
{
  "worker_id": 1,
  "clock_in": "2025-10-17T08:00:00Z",
  "location": "Assembly Line A",
  "device_id": "WATCH_001"
}
```

4. Click **"Execute"** - note the session **"id"** in response
5. Find **"PUT /session/{session_id}/clock-out"**
6. Enter the session id
7. Paste:

```json
{
  "clock_out": "2025-10-17T16:30:00Z",
  "break_duration": 0.5
}
```

8. Click **"Execute"**

**Repeat for more workers with different times and locations**

---

### **Step 4: Add Diverse Tasks**

1. Find **"POST /task/create"** endpoint
2. Click **"Try it out"**
3. Use these sample tasks:

**Task 1:**
```json
{
  "worker_id": 1,
  "title": "Assemble engine components for Model-TX200",
  "description": "Complete assembly following standard procedures.",
  "priority": "high",
  "assigned_by": "Production Manager",
  "due_date": "2025-10-20T17:00:00Z"
}
```

**Task 2:**
```json
{
  "worker_id": 2,
  "title": "Inspect batch #5678 for quality defects",
  "description": "Perform thorough quality inspection.",
  "priority": "medium",
  "assigned_by": "Quality Lead",
  "due_date": "2025-10-18T17:00:00Z"
}
```

**Task 3:**
```json
{
  "worker_id": 1,
  "title": "Perform preventive maintenance on Machine-305",
  "description": "Complete maintenance checklist and update logs.",
  "priority": "high",
  "assigned_by": "Maintenance Head",
  "due_date": "2025-10-19T17:00:00Z"
}
```

**More Task Ideas:**
- "Install wiring harness in chassis 742"
- "Test functionality of assembled units"
- "Package completed products for shipment"
- "Conduct safety inspection of work area"
- "Calibrate measuring instruments"
- "Update maintenance and safety logs"

---

## 🎯 **METHOD 2: Using cURL Commands**

Copy-paste these commands in PowerShell:

### **Add Health Metric:**
```powershell
$body = @{
    worker_id = 1
    heart_rate = 75
    oxygen_level = 98.5
    body_temperature = 36.8
    stress_level = 35
    fatigue_score = 25
    steps_count = 8500
    calories_burned = 450
    hours_worked_today = 7.5
    device_id = "WATCH_001"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/health/metric" -Method Post -Body $body -ContentType "application/json"
```

### **Add Task:**
```powershell
$task = @{
    worker_id = 1
    title = "Assemble engine components for Model-TX200"
    description = "Complete assembly following standard procedures"
    priority = "high"
    assigned_by = "Production Manager"
    due_date = "2025-10-20T17:00:00Z"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/task/create" -Method Post -Body $task -ContentType "application/json"
```

---

## 🎯 **METHOD 3: Using Python Script**

Create a file `add_sample_data.py`:

```python
import requests

API = "http://localhost:8000"

# Add 5 health metrics
for i in range(1, 6):
    health = {
        "worker_id": i,
        "heart_rate": 70 + (i * 5),
        "oxygen_level": 97.0 + i,
        "stress_level": 30.0 + (i * 5),
        "fatigue_score": 20.0 + (i * 3),
        "steps_count": 5000 + (i * 1000),
        "device_id": f"WATCH_{i:03d}"
    }
    r = requests.post(f"{API}/health/metric", json=health)
    print(f"Added health for worker {i}: {r.status_code}")

# Add 10 tasks
tasks = [
    "Assemble engine components",
    "Inspect quality defects",
    "Perform maintenance",
    "Install wiring harness",
    "Test assembled units",
    "Package products",
    "Safety inspection",
    "Calibrate instruments",
    "Update logs",
    "Train new workers"
]

for i, title in enumerate(tasks, 1):
    task = {
        "worker_id": (i % 10) + 1,
        "title": title,
        "priority": "high" if i % 3 == 0 else "medium",
        "assigned_by": "Supervisor"
    }
    r = requests.post(f"{API}/task/create", json=task)
    print(f"Added task: {title} - {r.status_code}")

print("\n✅ Sample data added!")
```

Run: `python add_sample_data.py`

---

## 📊 **VERIFY DATA WAS ADDED**

### **Check Health Data:**
```
http://localhost:8000/health/dashboard
```
Should show workers with health metrics

### **Check Work Hours:**
```
http://localhost:8000/session/all/hours
```
Should show workers with work sessions

### **Check Tasks:**
```
http://localhost:8000/task/all
```
Should show all tasks

### **Check in Mobile App:**
```
http://localhost:8082
```
Go to Tasks tab - should see tasks for Worker ID 1

---

## 🎬 **MINIMUM DATA FOR DEMO**

To make your demo look good, you need AT LEAST:

✅ **5 workers with health metrics** (heart rate, oxygen, stress)
✅ **3 workers with work sessions** (clock-in/out times)  
✅ **10 tasks** (mix of priorities, assigned to different workers)
✅ **2-3 role assignments** (from Dashboard → Find Best Workers)

---

## 💡 **QUICK TIP**

**If you're short on time**, just add:
1. 3 health metrics for Worker 1, 2, 3
2. 5 diverse tasks
3. Test the task assignment from Dashboard

This is enough to demonstrate all key features!

---

## 🆘 **TROUBLESHOOTING**

**"Worker not found" error:**
- Workers need to exist first
- Go to http://localhost:8000/worker/all to see worker IDs
- Use existing worker IDs (1-20)

**"Already clocked in" error:**
- Worker can only have one active session
- Clock out the previous session first
- Or use a different worker_id

**Data not showing in mobile app:**
- Make sure you're adding tasks for worker_id: 1 (Rajesh Kumar)
- Mobile app is hardcoded to show Worker ID 1's tasks
- Stay on the "Tasks" tab for auto-refresh

---

**Good luck! You've got this! 🚀**
