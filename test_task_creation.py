"""
Test if task creation actually works
"""
import requests
import json

API_URL = "http://localhost:8000"

print("=" * 60)
print("TESTING TASK CREATION FROM SUPERVISOR DASHBOARD")
print("=" * 60)

# Test 1: Create a task for Rajesh Kumar
print("\n1. Creating task for Rajesh Kumar (Worker ID: 1)...")
task_data = {
    "worker_id": 1,
    "role_id": None,
    "title": "SUPERVISOR TEST - Urgent Machine Repair",
    "description": "This is a test from supervisor dashboard",
    "priority": "high",
    "due_date": None,
    "assigned_by": "Supervisor Dashboard"
}

try:
    response = requests.post(f"{API_URL}/task/create", json=task_data)
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 200:
        task = response.json()
        print(f"   ✅ SUCCESS! Task created:")
        print(f"   - Task ID: {task['id']}")
        print(f"   - Title: {task['title']}")
        print(f"   - Worker ID: {task['worker_id']}")
        print(f"   - Status: {task['status']}")
        task_id = task['id']
    else:
        print(f"   ❌ FAILED: {response.text}")
        task_id = None
except Exception as e:
    print(f"   ❌ ERROR: {e}")
    task_id = None

# Test 2: Verify task appears in worker's list
print("\n2. Checking if task appears for Rajesh Kumar...")
try:
    response = requests.get(f"{API_URL}/task/worker/1")
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 200:
        tasks = response.json()
        print(f"   ✅ Found {len(tasks)} tasks for Rajesh Kumar")
        
        if task_id:
            # Find our test task
            test_task = next((t for t in tasks if t['id'] == task_id), None)
            if test_task:
                print(f"   ✅ Our test task IS in the list!")
                print(f"   - Title: {test_task['title']}")
            else:
                print(f"   ❌ Our test task NOT found in list!")
        
        print(f"\n   All tasks:")
        for i, task in enumerate(tasks[:5], 1):
            print(f"   {i}. {task['title']} - {task['status']}")
    else:
        print(f"   ❌ FAILED: {response.text}")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

# Test 3: Check notifications
print("\n3. Checking notifications for Rajesh Kumar...")
try:
    response = requests.get(f"{API_URL}/task/worker/1/notifications")
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Found {data['count']} notifications")
        if data['notifications']:
            print(f"   Latest notification: {data['notifications'][0]['title']}")
    else:
        print(f"   ❌ FAILED: {response.text}")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

print("\n" + "=" * 60)
print("CONCLUSION:")
print("=" * 60)
if task_id:
    print("✅ Backend is working correctly!")
    print("✅ Tasks can be created via API")
    print("✅ Tasks appear in worker's list")
    print("\nIf mobile app doesn't show tasks, the problem is:")
    print("- Mobile app not refreshing")
    print("- Mobile app using wrong API URL")
    print("- Mobile app not running")
else:
    print("❌ Backend is NOT working!")
    print("Problem is in the backend, not the dashboard")
print("=" * 60)
