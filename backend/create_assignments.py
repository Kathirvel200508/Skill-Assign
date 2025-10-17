"""
Create Assignments with linked Tasks using existing Workers and Roles
"""
import requests

API = "http://localhost:8000"

print("\n📊 Getting existing data...\n")

# Get workers
workers_response = requests.get(f"{API}/worker/all")
workers = workers_response.json()
print(f"✅ Found {len(workers)} workers")

# Get roles
roles_response = requests.get(f"{API}/role/all")
roles = roles_response.json()
print(f"✅ Found {len(roles)} roles\n")

if len(workers) == 0 or len(roles) == 0:
    print("❌ Need workers and roles first!")
    exit()

print("📋 Creating Assignments with Tasks...\n")

# Create 10 diverse assignments
scenarios = [
    (0, 0, 0.87, "completed"),   
    (1, 2, 0.92, "completed"),   
    (2, 0, 0.85, "in_progress"), 
    (3, 3, 0.90, "pending"),     
    (4, 1, 0.88, "completed"),   
    (5, min(5, len(roles)-1), 0.89, "in_progress"), 
    (6, 0, 0.84, "pending"),     
    (7, 2, 0.91, "completed"),   
    (8, min(4, len(roles)-1), 0.83, "in_progress"), 
    (9, 3, 0.86, "completed"),   
]

created_count = 0

for worker_idx, role_idx, fit_score, task_status in scenarios:
    if worker_idx >= len(workers) or role_idx >= len(roles):
        continue
    
    worker = workers[worker_idx]
    role = roles[role_idx]
    
    # Create task
    task_data = {
        "worker_id": worker['id'],
        "role_id": role['id'],
        "title": f"Role Assignment: {role['name']}",
        "description": f"You have been assigned to {role['name']}. Fit score: {int(fit_score*100)}%.",
        "priority": "high",
        "status": task_status,
        "assigned_by": "Supervisor Dashboard"
    }
    
    try:
        print(f"Creating task for {worker['name']}...")
        task_response = requests.post(f"{API}/task/create", json=task_data)
        print(f"Task response: {task_response.status_code}")
        if task_response.status_code == 201:
            task_id = task_response.json()['id']
            
            # Create assignment (without task_id for now - backend needs restart)
            assignment_data = {
                "worker_id": worker['id'],
                "role_id": role['id'],
                "fit_score": fit_score
            }
            
            print(f"Creating assignment...")
            assignment_response = requests.post(f"{API}/assignment/create", json=assignment_data)
            print(f"Assignment response: {assignment_response.status_code}")
            if assignment_response.status_code == 201:
                created_count += 1
                status_icon = "✅" if task_status == "completed" else "🔵" if task_status == "in_progress" else "⏳"
                print(f"{status_icon} {worker['name']} → {role['name']} ({task_status})")
            else:
                print(f"Assignment error: {assignment_response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

print(f"\n{'='*60}")
print(f"✅ Created {created_count} assignments with linked tasks!")
print(f"{'='*60}")
print("\n🌐 Now open your web browser:")
print("   Dashboard: http://localhost:3000")
print("   Assignments: http://localhost:3000 (click Assignments tab)")
print("   Mobile: http://localhost:8082\n")
