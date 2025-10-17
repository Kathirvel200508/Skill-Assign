"""
Populate ALL data for Dashboard and Assignments pages
Creates: Workers, Roles, Assignments, Tasks
"""
import requests
import random
from datetime import datetime, timedelta

API = "http://localhost:8000"

print("\n" + "="*70)
print("🎬 POPULATING COMPLETE DATA FOR DEMO")
print("="*70 + "\n")

# ========== WORKERS ==========
print("📊 Step 1: Adding Workers...")

WORKERS = [
    {
        "name": "Rajesh Kumar",
        "age": 28,
        "experience": 5.5,
        "skills": ["Welding", "CNC Operation", "Quality Control", "Blueprint Reading", "Safety Protocols"],
        "fatigue_level": 0.25,
        "hours_per_day": 7.5,
        "hours_per_week": 37.5,
        "performance_score": 0.88
    },
    {
        "name": "Priya Sharma",
        "age": 32,
        "experience": 8.0,
        "skills": ["Machine Operation", "Quality Inspection", "Manual Assembly", "Testing", "Documentation"],
        "fatigue_level": 0.20,
        "hours_per_day": 8.0,
        "hours_per_week": 40.0,
        "performance_score": 0.92
    },
    {
        "name": "Amit Patel",
        "age": 35,
        "experience": 10.0,
        "skills": ["CNC Programming", "Lathe Operation", "Milling", "CAD Design", "Training"],
        "fatigue_level": 0.30,
        "hours_per_day": 8.5,
        "hours_per_week": 42.5,
        "performance_score": 0.85
    },
    {
        "name": "Sunita Reddy",
        "age": 26,
        "experience": 3.5,
        "skills": ["Manual Assembly", "Quality Control", "Packaging", "Inventory", "Communication"],
        "fatigue_level": 0.15,
        "hours_per_day": 7.0,
        "hours_per_week": 35.0,
        "performance_score": 0.90
    },
    {
        "name": "Vikram Singh",
        "age": 40,
        "experience": 15.0,
        "skills": ["Welding", "Supervision", "Team Leadership", "Safety Training", "Quality Standards"],
        "fatigue_level": 0.35,
        "hours_per_day": 8.0,
        "hours_per_week": 40.0,
        "performance_score": 0.87
    },
    {
        "name": "Anjali Desai",
        "age": 29,
        "experience": 6.0,
        "skills": ["Electrical Wiring", "Testing", "Troubleshooting", "Circuit Design", "Documentation"],
        "fatigue_level": 0.22,
        "hours_per_day": 7.5,
        "hours_per_week": 37.5,
        "performance_score": 0.89
    },
    {
        "name": "Karthik Iyer",
        "age": 31,
        "experience": 7.5,
        "skills": ["CNC Operation", "Programming", "Maintenance", "Quality Check", "Problem Solving"],
        "fatigue_level": 0.28,
        "hours_per_day": 8.0,
        "hours_per_week": 40.0,
        "performance_score": 0.86
    },
    {
        "name": "Neha Gupta",
        "age": 27,
        "experience": 4.5,
        "skills": ["Quality Inspection", "Testing", "Documentation", "ISO Standards", "Training"],
        "fatigue_level": 0.18,
        "hours_per_day": 7.0,
        "hours_per_week": 35.0,
        "performance_score": 0.91
    },
    {
        "name": "Ravi Menon",
        "age": 38,
        "experience": 12.0,
        "skills": ["Machine Maintenance", "Hydraulics", "Pneumatics", "Troubleshooting", "Safety"],
        "fatigue_level": 0.32,
        "hours_per_day": 8.5,
        "hours_per_week": 42.5,
        "performance_score": 0.84
    },
    {
        "name": "Deepa Nair",
        "age": 30,
        "experience": 6.5,
        "skills": ["Manual Assembly", "Power Tools", "Quality Control", "Team Work", "Precision"],
        "fatigue_level": 0.24,
        "hours_per_day": 7.5,
        "hours_per_week": 37.5,
        "performance_score": 0.88
    }
]

created_workers = []
for worker in WORKERS:
    try:
        response = requests.post(f"{API}/worker/add", json=worker)
        if response.status_code == 201:
            worker_data = response.json()
            created_workers.append(worker_data)
            print(f"✅ {worker['name']} (ID: {worker_data['id']}) - {len(worker['skills'])} skills")
    except Exception as e:
        print(f"⚠️  {worker['name']}: {str(e)[:50]}")

print(f"\n✅ Created {len(created_workers)} workers\n")

# ========== ROLES ==========
print("🎯 Step 2: Adding Roles...")

ROLES = [
    {
        "name": "CNC Machine Operator",
        "description": "Operate CNC machines for precision manufacturing",
        "required_skills": ["CNC Operation", "Blueprint Reading", "Quality Control", "Precision Measurement"],
        "difficulty_level": 7.5,
        "typical_tasks": ["Set up CNC machines", "Load programs", "Monitor production", "Quality inspection"]
    },
    {
        "name": "Welding Specialist",
        "description": "Perform various welding operations",
        "required_skills": ["Welding", "Safety Protocols", "Blueprint Reading", "Quality Control"],
        "difficulty_level": 8.0,
        "typical_tasks": ["MIG/TIG welding", "Joint preparation", "Weld inspection", "Equipment maintenance"]
    },
    {
        "name": "Quality Inspector",
        "description": "Ensure product quality standards",
        "required_skills": ["Quality Inspection", "Testing", "Documentation", "ISO Standards", "Measurement"],
        "difficulty_level": 6.5,
        "typical_tasks": ["Inspect products", "Document findings", "Use measuring tools", "Report defects"]
    },
    {
        "name": "Assembly Line Worker",
        "description": "Assemble components on production line",
        "required_skills": ["Manual Assembly", "Power Tools", "Team Work", "Quality Control"],
        "difficulty_level": 5.0,
        "typical_tasks": ["Assemble parts", "Use hand tools", "Follow work instructions", "Quality check"]
    },
    {
        "name": "Maintenance Technician",
        "description": "Maintain and repair machinery",
        "required_skills": ["Machine Maintenance", "Troubleshooting", "Hydraulics", "Pneumatics", "Safety"],
        "difficulty_level": 8.5,
        "typical_tasks": ["Preventive maintenance", "Repair equipment", "Diagnose issues", "Update logs"]
    },
    {
        "name": "Electrical Technician",
        "description": "Handle electrical systems and wiring",
        "required_skills": ["Electrical Wiring", "Testing", "Troubleshooting", "Safety Protocols"],
        "difficulty_level": 7.0,
        "typical_tasks": ["Install wiring", "Test circuits", "Repair electrical systems", "Safety checks"]
    }
]

created_roles = []
for role in ROLES:
    try:
        response = requests.post(f"{API}/role/add", json=role)
        if response.status_code == 201:
            role_data = response.json()
            created_roles.append(role_data)
            print(f"✅ {role['name']} (ID: {role_data['id']}) - Difficulty: {role['difficulty_level']}/10")
    except Exception as e:
        print(f"⚠️  {role['name']}: {str(e)[:50]}")

print(f"\n✅ Created {len(created_roles)} roles\n")

# ========== ASSIGNMENTS & TASKS ==========
print("📋 Step 3: Creating Assignments with Tasks...")

assignments_created = 0
tasks_created = 0

# Create 8 assignments with linked tasks
assignment_scenarios = [
    (0, 0, 0.87, "completed"),   # Rajesh → CNC Operator (completed)
    (1, 2, 0.92, "completed"),   # Priya → Quality Inspector (completed)
    (2, 0, 0.85, "in_progress"), # Amit → CNC Operator (in progress)
    (3, 3, 0.90, "completed"),   # Sunita → Assembly (completed)
    (4, 1, 0.88, "pending"),     # Vikram → Welding (pending)
    (5, 5, 0.89, "in_progress"), # Anjali → Electrical (in progress)
    (6, 0, 0.84, "pending"),     # Karthik → CNC Operator (pending)
    (7, 2, 0.91, "completed"),   # Neha → Quality Inspector (completed)
]

for worker_idx, role_idx, fit_score, task_status in assignment_scenarios:
    if worker_idx >= len(created_workers) or role_idx >= len(created_roles):
        continue
    
    worker = created_workers[worker_idx]
    role = created_roles[role_idx]
    
    try:
        # Create task first
        task_data = {
            "worker_id": worker['id'],
            "role_id": role['id'],
            "title": f"Role Assignment: {role['name']}",
            "description": f"You have been assigned to {role['name']}. Fit score: {int(fit_score*100)}%.",
            "priority": "high",
            "status": task_status,
            "assigned_by": "Supervisor Dashboard"
        }
        
        task_response = requests.post(f"{API}/task/create", json=task_data)
        
        if task_response.status_code == 201:
            task_id = task_response.json()['id']
            tasks_created += 1
            
            # Create assignment linked to task
            assignment_data = {
                "worker_id": worker['id'],
                "role_id": role['id'],
                "fit_score": fit_score,
                "task_id": task_id
            }
            
            assignment_response = requests.post(f"{API}/assignment/create", json=assignment_data)
            
            if assignment_response.status_code == 201:
                assignments_created += 1
                status_icon = "✅" if task_status == "completed" else "🔵" if task_status == "in_progress" else "⏳"
                print(f"{status_icon} {worker['name']} → {role['name']} ({task_status})")
    
    except Exception as e:
        print(f"⚠️  Error: {str(e)[:50]}")

print(f"\n✅ Created {assignments_created} assignments")
print(f"✅ Created {tasks_created} linked tasks\n")

# ========== SUMMARY ==========
print("="*70)
print("📊 DATA POPULATION COMPLETE!")
print("="*70)
print(f"\n✅ {len(created_workers)} Workers")
print(f"✅ {len(created_roles)} Roles")
print(f"✅ {assignments_created} Assignments")
print(f"✅ {tasks_created} Tasks")

print(f"\n📱 Status Breakdown:")
completed_count = sum(1 for _, _, _, s in assignment_scenarios if s == "completed")
in_progress_count = sum(1 for _, _, _, s in assignment_scenarios if s == "in_progress")
pending_count = sum(1 for _, _, _, s in assignment_scenarios if s == "pending")

print(f"   ✅ Completed: {completed_count}")
print(f"   🔵 In Progress: {in_progress_count}")
print(f"   ⏳ Pending: {pending_count}")

print(f"\n🌐 Now visit:")
print(f"   Dashboard: http://localhost:3000")
print(f"   Assignments: http://localhost:3000 (Assignments tab)")
print(f"   Mobile: http://localhost:8082")

print("\n" + "="*70)
print("🎉 Your app is now fully populated and ready!")
print("="*70 + "\n")
