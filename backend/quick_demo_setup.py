"""
Quick Demo Setup - Populate with impressive synthetic data
"""
import requests
import random
from datetime import datetime, timedelta

API = "http://localhost:8000"

print("\n" + "="*60)
print("🎬 QUICK DEMO SETUP - Making Your App Presentation-Ready!")
print("="*60 + "\n")

# Generate realistic health data for existing workers
print("📊 Adding realistic health & work data...")

try:
    workers_response = requests.get(f"{API}/worker/all")
    workers = workers_response.json()
    print(f"✅ Found {len(workers)} workers\n")
    
    health_added = 0
    sessions_added = 0
    tasks_added = 0
    
    # Add health metrics for all workers
    print("💓 Generating health metrics...")
    for worker in workers:
        worker_id = worker['id']
        
        # Create 3 health readings per worker
        for i in range(3):
            health = {
                "worker_id": worker_id,
                "heart_rate": random.randint(65, 95),
                "blood_pressure_systolic": random.randint(115, 130),
                "blood_pressure_diastolic": random.randint(75, 85),
                "oxygen_level": round(random.uniform(96.0, 100.0), 1),
                "body_temperature": round(random.uniform(36.4, 37.1), 1),
                "stress_level": round(random.uniform(20, 60), 1),
                "fatigue_score": round(random.uniform(15, 50), 1),
                "steps_count": random.randint(3000, 12000),
                "calories_burned": round(random.uniform(300, 900), 1),
                "hours_worked_today": round(random.uniform(4, 8.5), 1),
                "device_id": f"WATCH_{worker_id:03d}"
            }
            
            try:
                r = requests.post(f"{API}/health/metric", json=health)
                if r.status_code == 201:
                    health_added += 1
            except:
                pass
    
    print(f"   ✅ Added {health_added} health readings")
    
    # Add work sessions
    print("\n⏰ Generating work sessions...")
    for worker in workers[:12]:  # Sessions for 12 workers
        worker_id = worker['id']
        
        # Create sessions for past 5 days
        for day in range(5):
            date = datetime.utcnow() - timedelta(days=day)
            clock_in = date.replace(hour=random.randint(7, 9), minute=random.randint(0, 59))
            clock_out = clock_in + timedelta(hours=random.uniform(7.5, 8.5))
            
            session = {
                "worker_id": worker_id,
                "clock_in": clock_in.isoformat() + "Z",
                "location": random.choice(["Assembly Line A", "Welding Station", "Quality Control", "CNC Department"]),
                "device_id": f"WATCH_{worker_id:03d}"
            }
            
            try:
                r = requests.post(f"{API}/session/clock-in", json=session)
                if r.status_code == 201:
                    session_id = r.json()['id']
                    
                    # Clock out
                    requests.put(f"{API}/session/{session_id}/clock-out", json={
                        "clock_out": clock_out.isoformat() + "Z",
                        "break_duration": round(random.uniform(0.5, 1.0), 2)
                    })
                    sessions_added += 1
            except:
                pass
    
    print(f"   ✅ Added {sessions_added} work sessions")
    
    # Add diverse tasks
    print("\n📋 Generating diverse tasks...")
    
    task_templates = [
        "Assemble engine components for Model-{model}",
        "Inspect batch #{batch} for quality defects",
        "Perform preventive maintenance on Machine-{id}",
        "Manufacture {qty} units of Part-{part}",
        "Conduct safety inspection of work area",
        "Install wiring harness in chassis {id}",
        "Test functionality of assembled units",
        "Package completed products for shipment",
        "Calibrate measuring instruments",
        "Update maintenance and safety logs"
    ]
    
    for worker in workers:
        # 2-4 tasks per worker
        for _ in range(random.randint(2, 4)):
            template = random.choice(task_templates)
            title = template.format(
                model=random.choice(["TX200", "MX500"]),
                batch=random.randint(1000, 9999),
                id=random.randint(100, 999),
                qty=random.randint(50, 500),
                part=random.choice(["A123", "B456", "C789"])
            )
            
            task = {
                "worker_id": worker['id'],
                "title": title,
                "description": "Complete this task following standard operating procedures.",
                "priority": random.choice(["low", "medium", "high"]),
                "assigned_by": random.choice(["Production Manager", "Shift Supervisor", "Quality Lead"]),
                "due_date": (datetime.utcnow() + timedelta(days=random.randint(1, 7))).isoformat() + "Z"
            }
            
            try:
                r = requests.post(f"{API}/task/create", json=task)
                if r.status_code == 201:
                    tasks_added += 1
            except:
                pass
    
    print(f"   ✅ Added {tasks_added} diverse tasks")
    
    # Show dashboard stats
    print("\n" + "="*60)
    print("📊 DASHBOARD STATISTICS")
    print("="*60)
    
    try:
        health_dash = requests.get(f"{API}/health/dashboard").json()
        stats = health_dash['statistics']
        print(f"\n🏥 Health Monitoring:")
        print(f"   Workers Monitored: {stats['total_workers']}")
        print(f"   🟢 Good Health: {stats['workers_good']}")
        print(f"   🟡 Warnings: {stats['workers_warning']}")
        print(f"   🔴 Critical: {stats['workers_critical']}")
    except:
        pass
    
    try:
        hours_dash = requests.get(f"{API}/session/all/hours").json()
        print(f"\n⏰ Work Hours:")
        print(f"   Workers Tracked: {hours_dash['total_workers']}")
        if hours_dash['workers']:
            total_week = sum(w['week_hours'] for w in hours_dash['workers'])
            print(f"   Total Hours This Week: {total_week:.1f}h")
    except:
        pass
    
    try:
        analytics = requests.get(f"{API}/analytics/overview").json()
        print(f"\n🎯 System Overview:")
        print(f"   Total Workers: {analytics['total_workers']}")
        print(f"   Total Roles: {analytics['total_roles']}")
        print(f"   Total Assignments: {analytics['total_assignments']}")
    except:
        pass
    
    print("\n" + "="*60)
    print("✅ DEMO SETUP COMPLETE!")
    print("="*60)
    print("\n🎬 Your app is ready for presentation!")
    print("\n📱 Access your app:")
    print(f"   Web: http://localhost:3000")
    print(f"   Mobile: http://localhost:8082")
    print(f"   API Docs: http://localhost:8000/docs")
    print("\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("Make sure the backend server is running!")
