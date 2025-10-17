"""
Test script to verify task synchronization between web and mobile
"""
import requests
import json
import time

API_BASE_URL = "http://localhost:8000"

print("=" * 60)
print("TESTING TASK SYNCHRONIZATION")
print("=" * 60)

# Test 1: Check if backend is running
print("\n[1] Checking backend connection...")
try:
    response = requests.get(f"{API_BASE_URL}/worker/all")
    print(f"✅ Backend is running (Status: {response.status_code})")
    workers = response.json()
    print(f"   Found {len(workers)} workers")
except Exception as e:
    print(f"❌ Backend connection failed: {e}")
    exit(1)

# Test 2: Get current tasks for Worker ID 1 (Rajesh Kumar)
print("\n[2] Getting current tasks for Worker ID 1...")
try:
    response = requests.get(f"{API_BASE_URL}/task/worker/1")
    current_tasks = response.json()
    print(f"✅ Current tasks: {len(current_tasks)}")
    for task in current_tasks[:3]:  # Show first 3
        print(f"   - {task['title']} (Status: {task['status']})")
except Exception as e:
    print(f"❌ Failed to get tasks: {e}")

# Test 3: Create a new task
print("\n[3] Creating a TEST task from supervisor...")
task_data = {
    "worker_id": 1,
    "title": "🚨 SYNC TEST - Check Mobile App NOW!",
    "description": "This task was created to test real-time sync. Check your mobile app!",
    "priority": "high",
    "assigned_by": "Supervisor Dashboard (Automated Test)"
}

try:
    response = requests.post(
        f"{API_BASE_URL}/task/create",
        json=task_data,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 201:
        created_task = response.json()
        print(f"✅ Task created successfully!")
        print(f"   Task ID: {created_task['id']}")
        print(f"   Title: {created_task['title']}")
        print(f"   Worker ID: {created_task['worker_id']}")
        print(f"   Status: {created_task['status']}")
        
        print("\n" + "=" * 60)
        print("🎉 SUCCESS! Task created in database!")
        print("=" * 60)
        print("\n📱 Now check your MOBILE APP:")
        print("   → The task should appear within 2 seconds")
        print("   → Look for: '🚨 SYNC TEST - Check Mobile App NOW!'")
        print("   → You should see a green banner: '🎉 New Task Assigned!'")
        print("\n⏰ Waiting 5 seconds to verify...")
        
        time.sleep(5)
        
        # Verify task appears
        print("\n[4] Verifying task appears in task list...")
        response = requests.get(f"{API_BASE_URL}/task/worker/1")
        updated_tasks = response.json()
        print(f"✅ Total tasks now: {len(updated_tasks)}")
        
        if len(updated_tasks) > len(current_tasks):
            print(f"✅ NEW TASK CONFIRMED! (+{len(updated_tasks) - len(current_tasks)} task)")
        
    else:
        print(f"❌ Failed to create task: {response.status_code}")
        print(f"   Response: {response.text}")
        
except Exception as e:
    print(f"❌ Error creating task: {e}")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
