"""
Add Roles and create Assignments with Tasks
"""
import requests
import json

API = "http://localhost:8000"

print("\n🎯 Adding Roles...\n")

# Add roles
roles_data = [
    {
        "name": "CNC Machine Operator",
        "description": "Operate CNC machines for precision manufacturing",
        "required_skills": ["CNC Operation", "Blueprint Reading", "Quality Control"],
        "difficulty_level": 0.75,
        "typical_tasks": ["Set up CNC machines", "Load programs", "Monitor production"]
    },
    {
        "name": "Welding Specialist",
        "description": "Perform welding operations",
        "required_skills": ["Welding", "Safety Protocols", "Blueprint Reading"],
        "difficulty_level": 0.80,
        "typical_tasks": ["MIG/TIG welding", "Joint preparation", "Weld inspection"]
    },
    {
        "name": "Quality Inspector",
        "description": "Ensure product quality standards",
        "required_skills": ["Quality Inspection", "Testing", "Documentation"],
        "difficulty_level": 0.65,
        "typical_tasks": ["Inspect products", "Document findings", "Use measuring tools"]
    },
    {
        "name": "Assembly Line Worker",
        "description": "Assemble components on production line",
        "required_skills": ["Manual Assembly", "Power Tools", "Team Work"],
        "difficulty_level": 0.50,
        "typical_tasks": ["Assemble parts", "Use hand tools", "Follow instructions"]
    },
    {
        "name": "Maintenance Technician",
        "description": "Maintain and repair machinery",
        "required_skills": ["Machine Maintenance", "Troubleshooting", "Safety"],
        "difficulty_level": 0.85,
        "typical_tasks": ["Preventive maintenance", "Repair equipment", "Diagnose issues"]
    },
    {
        "name": "Electrical Technician",
        "description": "Handle electrical systems",
        "required_skills": ["Electrical Wiring", "Testing", "Troubleshooting"],
        "difficulty_level": 0.70,
        "typical_tasks": ["Install wiring", "Test circuits", "Safety checks"]
    }
]

created_roles = []
for role in roles_data:
    try:
        print(f"Adding: {role['name']}")
        response = requests.post(f"{API}/role/add", json=role)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            role_data = response.json()
            created_roles.append(role_data)
            print(f"✅ {role['name']} (ID: {role_data['id']})\n")
        else:
            print(f"Response: {response.text}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")

print(f"✅ Created {len(created_roles)} roles\n")

# Get all workers
print("📊 Getting workers...\n")
try:
    workers_response = requests.get(f"{API}/worker/all")
    workers = workers_response.json()
    print(f"✅ Found {len(workers)} workers\n")
except:
    print("❌ Could not get workers\n")
    workers = []

# Create assignments with tasks
if len(created_roles) > 0 and len(workers) > 0:
    print("📋 Creating Assignments with Tasks...\n")
    
    scenarios = [
        (0, 0, 0.87, "completed"),   # Worker 0 → Role 0 (completed)
        (1, 2, 0.92, "completed"),   # Worker 1 → Role 2 (completed)
        (2, 0, 0.85, "in_progress"), # Worker 2 → Role 0 (in progress)
        (3, 3, 0.90, "pending"),     # Worker 3 → Role 3 (pending)
        (4, 1, 0.88, "completed"),   # Worker 4 → Role 1 (completed)
        (5, 5, 0.89, "in_progress"), # Worker 5 → Role 5 (in progress)
        (6, 0, 0.84, "pending"),     # Worker 6 → Role 0 (pending)
        (7, 2, 0.91, "completed"),   # Worker 7 → Role 2 (completed)
        (8, 4, 0.83, "in_progress"), # Worker 8 → Role 4 (in progress)
        (9, 3, 0.86, "completed"),   # Worker 9 → Role 3 (completed)
    ]
    
    for worker_idx, role_idx, fit_score, task_status in scenarios:
        if worker_idx >= len(workers) or role_idx >= len(created_roles):
            continue
        
        worker = workers[worker_idx]
        role = created_roles[role_idx]
        
        # Create task
        task_data = {
            "worker_id": worker['id'],
            "role_id": role['id'],
            "title": f"Role Assignment: {role['name']}",
            "description": f"Assigned to {role['name']}. Fit: {int(fit_score*100)}%",
            "priority": "high",
            "status": task_status,
            "assigned_by": "Supervisor"
        }
        
        try:
            task_response = requests.post(f"{API}/task/create", json=task_data)
            if task_response.status_code == 201:
                task_id = task_response.json()['id']
                
                # Create assignment
                assignment_data = {
                    "worker_id": worker['id'],
                    "role_id": role['id'],
                    "fit_score": fit_score,
                    "task_id": task_id
                }
                
                assignment_response = requests.post(f"{API}/assignment/create", json=assignment_data)
                if assignment_response.status_code == 201:
                    status_icon = "✅" if task_status == "completed" else "🔵" if task_status == "in_progress" else "⏳"
                    print(f"{status_icon} {worker['name']} → {role['name']} ({task_status})")
        except Exception as e:
            print(f"❌ Error: {e}")

print("\n" + "="*60)
print("✅ DONE! Refresh your Dashboard and Assignments pages")
print("="*60 + "\n")
