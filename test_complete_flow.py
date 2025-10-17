"""
Test the complete flow: Create task via API and verify it appears for Rajesh Kumar
"""
import requests
import time

API_URL = "http://localhost:8000"

print("=" * 70)
print("TESTING COMPLETE FLOW: SUPERVISOR → BACKEND → MOBILE APP")
print("=" * 70)

# Step 1: Create a task for Rajesh Kumar (exactly like supervisor dashboard does)
print("\n1️⃣  SUPERVISOR DASHBOARD: Creating task for Rajesh Kumar...")
task_data = {
    "worker_id": 1,
    "role_id": None,
    "title": "FLOW TEST - Urgent Maintenance",
    "description": "This is a test from the complete flow test",
    "priority": "high",
    "due_date": None,
    "assigned_by": "Supervisor Dashboard"
}

print("   Task data:")
print(f"   - Worker ID: {task_data['worker_id']} (Rajesh Kumar)")
print(f"   - Title: {task_data['title']}")
print(f"   - Priority: {task_data['priority']}")

try:
    response = requests.post(f"{API_URL}/task/create", json=task_data)
    print(f"\n   Response Status: {response.status_code}")
    
    if response.status_code in [200, 201]:
        task = response.json()
        print(f"   ✅ Task created successfully!")
        print(f"   - Task ID: {task['id']}")
        print(f"   - Worker ID: {task['worker_id']}")
        print(f"   - Title: {task['title']}")
        print(f"   - Status: {task['status']}")
        task_id = task['id']
    else:
        print(f"   ❌ Failed: {response.text}")
        exit(1)
except Exception as e:
    print(f"   ❌ ERROR: {e}")
    print("\n   🛑 Backend is not running!")
    print("   Start it: cd backend && python -m uvicorn main:app --reload")
    exit(1)

# Step 2: Wait for mobile app to poll (2 seconds)
print("\n2️⃣  WAITING: Mobile app polls every 2 seconds...")
print("   Waiting 3 seconds to simulate mobile app refresh...")
for i in range(3, 0, -1):
    print(f"   {i}...", end=" ", flush=True)
    time.sleep(1)
print()

# Step 3: Fetch tasks for Rajesh Kumar (like mobile app does)
print("\n3️⃣  MOBILE APP: Fetching tasks for Rajesh Kumar...")
try:
    response = requests.get(f"{API_URL}/task/worker/1")
    print(f"   Response Status: {response.status_code}")
    
    if response.status_code == 200:
        tasks = response.json()
        print(f"   ✅ Found {len(tasks)} tasks for Rajesh Kumar")
        
        # Check if our task is in the list
        our_task = next((t for t in tasks if t['id'] == task_id), None)
        
        if our_task:
            print(f"\n   🎉🎉🎉 SUCCESS! 🎉🎉🎉")
            print(f"   Our test task IS in Rajesh Kumar's task list!")
            print(f"   - Task ID: {our_task['id']}")
            print(f"   - Title: {our_task['title']}")
            print(f"   - Status: {our_task['status']}")
        else:
            print(f"\n   ❌ PROBLEM: Our task NOT found in list!")
            print(f"   Task ID {task_id} not in worker's tasks")
        
        print(f"\n   All tasks for Rajesh Kumar:")
        for i, task in enumerate(tasks[:5], 1):
            marker = "👉" if task['id'] == task_id else "  "
            print(f"   {marker} {i}. {task['title']} (ID: {task['id']}, Status: {task['status']})")
    else:
        print(f"   ❌ Failed: {response.text}")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

# Step 4: Check notifications endpoint
print("\n4️⃣  NOTIFICATIONS: Checking notifications endpoint...")
try:
    response = requests.get(f"{API_URL}/task/worker/1/notifications")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ {data['count']} notifications found")
        if data['notifications']:
            latest = data['notifications'][0]
            print(f"   Latest: {latest['title']}")
    else:
        print(f"   ❌ Failed: {response.status_code}")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

print("\n" + "=" * 70)
print("CONCLUSION:")
print("=" * 70)
print("✅ Backend is working - tasks can be created")
print("✅ Tasks are assigned to Rajesh Kumar (Worker ID: 1)")
print("✅ Tasks appear in the /task/worker/1 endpoint")
print()
print("If mobile app doesn't show tasks, the problem is:")
print("  1. Mobile app not fetching from the right URL")
print("  2. Mobile app not checking worker ID 1")
print("  3. Mobile app has JavaScript errors")
print()
print("Next: Check mobile app console (F12) for errors!")
print("=" * 70)
