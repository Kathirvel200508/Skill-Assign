"""
Test script to verify task endpoints are working
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_endpoints():
    print("Testing Task Endpoints...\n")
    
    # Test 1: Get all tasks
    print("1. Testing GET /task/all")
    response = requests.get(f"{BASE_URL}/task/all")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        tasks = response.json()
        print(f"   Found {len(tasks)} tasks")
    else:
        print(f"   Error: {response.text}")
    
    # Test 2: Get all workers
    print("\n2. Getting workers...")
    response = requests.get(f"{BASE_URL}/worker/all")
    if response.status_code == 200:
        workers = response.json()
        print(f"   Found {len(workers)} workers")
        if workers:
            worker_id = workers[0]['id']
            print(f"   Using worker ID: {worker_id}")
            
            # Test 3: Create a test task
            print("\n3. Creating test task...")
            task_data = {
                "worker_id": worker_id,
                "role_id": None,
                "title": "Test Task - Safety Check",
                "description": "This is a test task to verify the system is working",
                "priority": "high",
                "assigned_by": "Test Supervisor"
            }
            response = requests.post(f"{BASE_URL}/task/create", json=task_data)
            print(f"   Status: {response.status_code}")
            if response.status_code == 201:
                task = response.json()
                print(f"   ✓ Task created successfully!")
                print(f"   Task ID: {task['id']}")
                print(f"   Title: {task['title']}")
                
                # Test 4: Get worker tasks
                print(f"\n4. Getting tasks for worker {worker_id}...")
                response = requests.get(f"{BASE_URL}/task/worker/{worker_id}")
                if response.status_code == 200:
                    worker_tasks = response.json()
                    print(f"   ✓ Found {len(worker_tasks)} tasks for this worker")
                    
                # Test 5: Get worker notifications
                print(f"\n5. Getting notifications for worker {worker_id}...")
                response = requests.get(f"{BASE_URL}/task/worker/{worker_id}/notifications")
                if response.status_code == 200:
                    notifications = response.json()
                    print(f"   ✓ Found {notifications['count']} notifications")
                    if notifications['notifications']:
                        notif = notifications['notifications'][0]
                        print(f"   Latest: {notif['title']}")
                        print(f"   Role: {notif['role_name']}")
                        print(f"   Status: {notif['status']}")
            else:
                print(f"   Error: {response.text}")
    
    print("\n✓ All tests completed!")

if __name__ == "__main__":
    test_endpoints()
