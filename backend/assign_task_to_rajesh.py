"""
Test script to assign a task to Rajesh Kumar
"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

def assign_task_to_rajesh():
    print("=" * 60)
    print("ASSIGNING TASK TO RAJESH KUMAR")
    print("=" * 60)
    
    # Get Rajesh Kumar's worker ID
    print("\n1. Finding Rajesh Kumar...")
    response = requests.get(f"{BASE_URL}/worker/all")
    workers = response.json()
    rajesh = next((w for w in workers if "Rajesh" in w['name']), None)
    
    if not rajesh:
        print("   ✗ Rajesh Kumar not found!")
        return
    
    print(f"   ✓ Found: {rajesh['name']} (ID: {rajesh['id']})")
    print(f"   Current Role: {rajesh.get('current_role', 'None')}")
    
    # Get available roles
    print("\n2. Getting available roles...")
    response = requests.get(f"{BASE_URL}/role/all")
    roles = response.json()
    print(f"   ✓ Found {len(roles)} roles")
    
    # Select a role (use first one if available)
    role_id = roles[0]['id'] if roles else None
    role_name = roles[0]['name'] if roles else "No specific role"
    
    # Create task for Rajesh Kumar
    print(f"\n3. Creating task for Rajesh Kumar...")
    due_date = (datetime.now() + timedelta(days=2)).isoformat()
    
    task_data = {
        "worker_id": rajesh['id'],
        "role_id": role_id,
        "title": "Complete Machine Maintenance",
        "description": "Perform routine maintenance on Assembly Line 3. Check all safety mechanisms and lubrication points.",
        "priority": "high",
        "due_date": due_date,
        "assigned_by": "Supervisor Dashboard"
    }
    
    response = requests.post(f"{BASE_URL}/task/create", json=task_data)
    
    if response.status_code == 201:
        task = response.json()
        print(f"   ✓ Task created successfully!")
        print(f"   Task ID: {task['id']}")
        print(f"   Title: {task['title']}")
        print(f"   Priority: {task['priority']}")
        print(f"   Role: {role_name}")
        
        # Verify task appears in worker's task list
        print(f"\n4. Verifying task in Rajesh's task list...")
        response = requests.get(f"{BASE_URL}/task/worker/{rajesh['id']}")
        tasks = response.json()
        print(f"   ✓ Rajesh now has {len(tasks)} task(s)")
        
        # Check notifications
        print(f"\n5. Checking Rajesh's notifications...")
        response = requests.get(f"{BASE_URL}/task/worker/{rajesh['id']}/notifications")
        notifications = response.json()
        print(f"   ✓ {notifications['count']} active notification(s)")
        
        if notifications['notifications']:
            latest = notifications['notifications'][0]
            print(f"\n   📱 MOBILE APP WILL SHOW:")
            print(f"   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print(f"   🔔 {latest['title']}")
            print(f"   👤 Worker: {latest['worker_name']}")
            print(f"   💼 Role: {latest['role_name']}")
            print(f"   ⚠️  Priority: {latest['priority'].upper()}")
            print(f"   📊 Status: {latest['status'].replace('_', ' ').title()}")
            print(f"   👔 Assigned by: {latest['assigned_by']}")
            print(f"   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        print(f"\n✅ SUCCESS! Task assigned to Rajesh Kumar")
        print(f"📱 Open the mobile app to see the task in:")
        print(f"   • Tasks tab (to manage the task)")
        print(f"   • Notifications tab (to see details)")
        print(f"\n🔄 Mobile app auto-refreshes every 30 seconds")
        print(f"   or pull down to refresh manually")
        
    else:
        print(f"   ✗ Error: {response.status_code}")
        print(f"   {response.text}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    assign_task_to_rajesh()
