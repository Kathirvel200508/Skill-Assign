# 🔥 REAL-TIME TASK SYNCHRONIZATION TEST GUIDE

## ✅ Step-by-Step Testing Instructions

### **STEP 1: Open Both Apps Side by Side**

1. **Web Supervisor App**
   - Open: http://localhost:3000
   - Navigate to: **Tasks** section (in sidebar)

2. **Mobile App**  
   - Open: http://localhost:8082
   - Make sure you're on the **"Tasks"** tab (clipboard icon at bottom)
   - You should see: "My Tasks - Rajesh Kumar"

---

### **STEP 2: Verify Mobile App is Polling**

Check the **backend terminal** - you should see these logs repeating every 2 seconds:
```
INFO: 127.0.0.1:XXXXX - "GET /task/worker/1 HTTP/1.1" 200 OK
```

✅ If you see this = Mobile app is successfully polling for tasks!

---

### **STEP 3: Assign a Task from Web App**

In the **Web Supervisor App**:

1. Click **"Assign New Task"** button (top right)
2. Fill in the form:
   - **Worker:** Select "Rajesh Kumar" (or any worker with ID 1)
   - **Title:** "TEST - Check Mobile Now!"
   - **Description:** "Testing real-time sync"
   - **Priority:** High
   - **Due Date:** (optional)
3. Click **"Assign Task"** button

---

### **STEP 4: Watch the Mobile App**

Within **2 seconds**, you should see in the Mobile App:

✅ **Green banner appears:** "🎉 New Task Assigned!"
✅ **New task card appears** in the "📋 Pending Tasks" section
✅ **Task counter updates** (e.g., "8 tasks" → "9 tasks")

---

### **STEP 5: Verify in Backend Logs**

Check backend terminal - you should see:
```
INFO: 127.0.0.1:XXXXX - "POST /task/create HTTP/1.1" 201 Created
INFO: 127.0.0.1:XXXXX - "GET /task/worker/1 HTTP/1.1" 200 OK
```

First line = Task created by web app
Second line = Mobile app fetched the new task

---

## 🐛 TROUBLESHOOTING

### Problem: "Task doesn't appear in mobile app"

**Check #1: Is mobile app on the Tasks screen?**
- Look at bottom navigation tabs
- Tap the **clipboard icon** (Tasks tab)

**Check #2: Is mobile app actually running?**
- Go to http://localhost:8082
- You should see the app interface, not a blank page

**Check #3: Is mobile app polling?**
- Check backend logs for: `GET /task/worker/1`
- Should repeat every 2 seconds

**Check #4: Is the task assigned to Worker ID 1?**
- In web app, make sure you select **Rajesh Kumar** (Worker ID 1)
- Mobile app only shows tasks for Worker ID 1

**Check #5: Check browser console**
- Open mobile app (http://localhost:8082)
- Press F12 to open console
- Look for: `[MOBILE APP] ✅ Tasks loaded`

---

## 🧪 AUTOMATED TEST

Run this command to create a test task:

```bash
python test_task_sync.py
```

This will:
1. Create a task for Worker ID 1
2. Verify it appears in the database
3. Tell you to check the mobile app

---

## 📊 EXPECTED BEHAVIOR

| Action | Web App | Mobile App | Time |
|--------|---------|------------|------|
| Click "Assign Task" | Shows success message | No change yet | 0s |
| Task saved to DB | Task appears in list | No change yet | 0.5s |
| Mobile app polls | N/A | **New task appears!** | 0-2s |
| Mobile detects new task | N/A | **Green banner shows** | 0-2s |

---

## 🎯 CURRENT STATUS

✅ Backend is running (port 8000)
✅ Database is working (SQLite)
✅ Web app is running (port 3000)
✅ Mobile app is running (port 8082)
✅ Mobile app is polling every 2 seconds
✅ API endpoints are working

**The synchronization IS WORKING!**

If you don't see tasks, make sure:
1. Mobile app is on the "Tasks" tab
2. You're assigning tasks to "Rajesh Kumar" (Worker ID 1)
3. Mobile app URL is http://localhost:8082 (not the QR code)

---

## 💡 QUICK TEST

1. **Open:** http://localhost:8082 (mobile app)
2. **Click:** Tasks tab (bottom navigation)
3. **Open:** http://localhost:3000 (web app)
4. **Go to:** Tasks section
5. **Click:** "Assign New Task"
6. **Select:** Rajesh Kumar
7. **Enter title:** "SYNC TEST"
8. **Click:** "Assign Task"
9. **Watch mobile app** - task appears within 2 seconds!

---

Last Updated: Oct 17, 2025
