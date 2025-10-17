# 🔧 Debugging Guide - Task Assignment Not Working

## 🎯 Problem
Tasks assigned from supervisor dashboard are not appearing in the worker mobile app.

## ✅ Step-by-Step Debugging

### **Step 1: Verify Backend is Running**

Open browser and go to:
```
http://localhost:8000/health
```

**Expected:** `{"status":"healthy"}`

**If not working:**
- Backend server is not running
- Restart it: `cd backend && python -m uvicorn main:app --reload`

---

### **Step 2: Test Task Creation**

I've created a test tool for you. Open this file in your browser:
```
file:///C:/Users/kavin/Skill-Assign/test_connection.html
```

Or just double-click: `test_connection.html`

**Use the test tool to:**
1. ✅ Check Backend Connection
2. ✅ Get Rajesh's current tasks
3. ✅ Create a test task
4. ✅ Get notifications

---

### **Step 3: Check Mobile App Configuration**

The mobile app needs to connect to the backend. Check what device you're using:

#### **If using Web Browser (Expo Web):**
- ✅ Config is correct: `http://localhost:8000`
- Should work out of the box

#### **If using Android Emulator:**
- ❌ Need to change config to: `http://10.0.2.2:8000`
- Edit: `mobile/config.js`
- Change line 5 to: `const API_BASE_URL = 'http://10.0.2.2:8000';`

#### **If using Physical Device:**
- ❌ Need your computer's IP address
- Find your IP: Run `ipconfig` in terminal
- Look for "IPv4 Address" (e.g., 192.168.1.100)
- Edit: `mobile/config.js`
- Change line 5 to: `const API_BASE_URL = 'http://YOUR_IP:8000';`

---

### **Step 4: Check Mobile App Logs**

Open the mobile app and check the browser console (F12):

**Look for:**
```
[TasksScreen] Loading tasks for worker 1...
[TasksScreen] API URL: http://localhost:8000/task/worker/1
[TasksScreen] Response status: 200
[TasksScreen] Tasks received: 2
```

**If you see errors:**
- Network error → Backend not accessible
- 404 error → Wrong URL
- 500 error → Backend error (check backend logs)

---

### **Step 5: Manual Test**

**From Supervisor Dashboard:**
1. Go to: http://localhost:3000/tasks
2. Click "Assign New Task"
3. Select "Rajesh Kumar"
4. Title: "URGENT TEST TASK"
5. Priority: High
6. Click "Assign Task"
7. You should see success message

**Check Backend:**
```
http://localhost:8000/task/worker/1
```
Should show the new task in JSON format

**Check Mobile App:**
1. Open mobile app
2. Pull down to refresh (important!)
3. Check "Tasks" tab
4. Should see "URGENT TEST TASK"

---

## 🔍 Common Issues & Solutions

### **Issue 1: "No tasks assigned yet" in mobile app**

**Possible causes:**
1. Mobile app not connecting to backend
2. Wrong worker ID
3. Tasks not being created
4. Mobile app not refreshing

**Solutions:**
- Check browser console for errors
- Pull down to manually refresh
- Use test tool to verify tasks exist
- Check API URL in mobile app header

---

### **Issue 2: Tasks created but not showing**

**Cause:** Mobile app caching or not refreshing

**Solution:**
1. Pull down to refresh
2. Close and reopen mobile app
3. Check if auto-refresh is working (every 30 seconds)
4. Look at console logs

---

### **Issue 3: "Connection Error" alert**

**Cause:** Backend not accessible from mobile app

**Solution:**
1. Verify backend is running: `http://localhost:8000/health`
2. Check mobile app config matches your setup:
   - Web browser → `localhost:8000`
   - Android emulator → `10.0.2.2:8000`
   - Physical device → `YOUR_IP:8000`
3. Restart mobile app after config change

---

### **Issue 4: Wrong worker showing**

**Cause:** Worker ID mismatch

**Solution:**
- Mobile app is hardcoded to Worker ID 1 (Rajesh Kumar)
- Verify Rajesh is ID 1: Run `python backend/check_workers.py`
- If different, update mobile app code

---

## 🧪 Quick Test Commands

**Check if tasks exist:**
```bash
cd backend
python check_workers.py
python test_tasks.py
```

**Create test task:**
```bash
cd backend
python assign_task_to_rajesh.py
```

**Check API directly:**
```
http://localhost:8000/task/worker/1
http://localhost:8000/task/worker/1/notifications
```

---

## 📱 Mobile App Debug Info

The mobile app now shows:
- Worker name: "Rajesh Kumar"
- Worker ID: 1
- Total tasks count
- API URL being used

**Look at the header** in the mobile app to verify:
- Correct worker ID
- Correct API URL
- Task count updating

---

## ✅ Verification Checklist

- [ ] Backend running on port 8000
- [ ] Can access http://localhost:8000/health
- [ ] Test tool shows tasks exist
- [ ] Mobile app config matches your device type
- [ ] Mobile app shows correct API URL in header
- [ ] Pulled down to refresh in mobile app
- [ ] Checked browser console for errors
- [ ] Task appears in http://localhost:8000/task/worker/1

---

## 🆘 Still Not Working?

1. **Open test tool** (`test_connection.html`)
2. **Click all 4 test buttons**
3. **Take screenshot** of results
4. **Check mobile app** browser console (F12)
5. **Take screenshot** of console logs

This will show exactly where the problem is!

---

## 📞 Quick Fix

**Try this right now:**

1. Open test tool: Double-click `test_connection.html`
2. Click "Create Task"
3. Open mobile app
4. **Pull down to refresh** (this is important!)
5. Check if task appears

If task appears in test tool but not mobile app:
- Problem is mobile app configuration
- Check API URL in mobile app header
- Make sure it matches backend URL

If task doesn't appear in test tool:
- Problem is backend
- Check backend is running
- Check backend logs for errors
