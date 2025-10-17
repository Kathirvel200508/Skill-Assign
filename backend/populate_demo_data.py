"""
Comprehensive Synthetic Data Generator for Demo/Jury Presentation
Creates realistic, diverse data to showcase all features
"""
import requests
import random
from datetime import datetime, timedelta
import json

API_BASE_URL = "http://localhost:8000"

# Color codes for output
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
RESET = '\033[0m'

def print_section(title):
    print(f"\n{CYAN}{'='*70}{RESET}")
    print(f"{CYAN}{title.center(70)}{RESET}")
    print(f"{CYAN}{'='*70}{RESET}\n")

def print_success(message):
    print(f"{GREEN}✅ {message}{RESET}")

def print_info(message):
    print(f"{BLUE}ℹ️  {message}{RESET}")

def print_warning(message):
    print(f"{YELLOW}⚠️  {message}{RESET}")

# ========== ENHANCED WORKER DATA ==========
INDIAN_NAMES = [
    "Rajesh Kumar", "Priya Sharma", "Amit Patel", "Sunita Reddy", "Vikram Singh",
    "Anjali Desai", "Karthik Iyer", "Neha Gupta", "Ravi Menon", "Deepa Nair",
    "Suresh Rao", "Lakshmi Pillai", "Arun Krishnan", "Meera Bhat", "Sanjay Joshi",
    "Kavita Saxena", "Arjun Verma", "Pooja Agarwal", "Manoj Kumar", "Divya Singh"
]

SKILL_CATEGORIES = {
    "Technical": ["Welding", "CNC Operation", "Electrical Wiring", "PLC Programming", "Hydraulics", "Pneumatics", "CAD Design"],
    "Assembly": ["Manual Assembly", "Power Tools", "Quality Inspection", "Blueprint Reading", "Precision Measurement"],
    "Machinery": ["Lathe Operation", "Milling", "Grinding", "Drilling", "Turning", "Machine Maintenance"],
    "Quality": ["Quality Control", "Testing", "Calibration", "Documentation", "ISO Standards"],
    "Safety": ["Safety Protocols", "First Aid", "Fire Safety", "Hazard Identification", "PPE Usage"],
    "Soft Skills": ["Team Leadership", "Communication", "Problem Solving", "Time Management", "Training"]
}

def generate_diverse_workers():
    """Generate workers with diverse skill sets and realistic attributes"""
    workers = []
    used_names = set()
    
    for i in range(20):
        name = random.choice([n for n in INDIAN_NAMES if n not in used_names])
        used_names.add(name)
        
        # Generate diverse skill sets
        num_skills = random.randint(3, 8)
        skills = []
        for category in random.sample(list(SKILL_CATEGORIES.keys()), min(3, len(SKILL_CATEGORIES))):
            skills.extend(random.sample(SKILL_CATEGORIES[category], min(2, len(SKILL_CATEGORIES[category]))))
        skills = list(set(skills))[:num_skills]
        
        # Realistic attributes
        age = random.randint(22, 55)
        experience = min(age - 18, random.uniform(1, 25))
        hours_per_day = round(random.uniform(7, 8.5), 1)
        hours_per_week = round(hours_per_day * 5 + random.uniform(-2, 3), 1)
        
        worker = {
            "name": name,
            "age": age,
            "experience": round(experience, 1),
            "skills": skills,
            "fatigue_level": round(random.uniform(0.1, 0.6), 2),
            "hours_per_day": hours_per_day,
            "hours_per_week": min(hours_per_week, 52),
            "performance_score": round(random.uniform(0.5, 0.95), 2)
        }
        workers.append(worker)
    
    return workers

# ========== REALISTIC HEALTH DATA ==========
def generate_health_metric(worker_id, hours_ago=0, status="normal"):
    """Generate realistic health metrics based on status"""
    base_time = datetime.utcnow() - timedelta(hours=hours_ago)
    
    if status == "normal":
        heart_rate = random.randint(65, 85)
        oxygen_level = round(random.uniform(97.0, 100.0), 1)
        stress_level = round(random.uniform(15, 45), 1)
        fatigue_score = round(random.uniform(10, 40), 1)
        body_temp = round(random.uniform(36.4, 37.0), 1)
    elif status == "tired":
        heart_rate = random.randint(85, 100)
        oxygen_level = round(random.uniform(95.5, 98.0), 1)
        stress_level = round(random.uniform(50, 75), 1)
        fatigue_score = round(random.uniform(60, 80), 1)
        body_temp = round(random.uniform(36.8, 37.2), 1)
    elif status == "alert":
        heart_rate = random.randint(100, 120)
        oxygen_level = round(random.uniform(93.0, 96.0), 1)
        stress_level = round(random.uniform(75, 90), 1)
        fatigue_score = round(random.uniform(75, 95), 1)
        body_temp = round(random.uniform(37.2, 37.8), 1)
    
    return {
        "worker_id": worker_id,
        "heart_rate": heart_rate,
        "blood_pressure_systolic": random.randint(110, 135),
        "blood_pressure_diastolic": random.randint(70, 90),
        "oxygen_level": oxygen_level,
        "body_temperature": body_temp,
        "stress_level": stress_level,
        "fatigue_score": fatigue_score,
        "steps_count": random.randint(2000, 15000),
        "calories_burned": round(random.uniform(200, 1200), 1),
        "hours_worked_today": round(random.uniform(0, 8.5), 1),
        "device_id": f"SMARTWATCH_{worker_id:03d}"
    }

# ========== WORK SESSIONS WITH PATTERNS ==========
def generate_work_sessions(worker_id, days=7):
    """Generate realistic work sessions over multiple days"""
    sessions = []
    
    for day in range(days):
        # Some workers might have day off
        if random.random() > 0.85:
            continue
        
        date_offset = datetime.utcnow() - timedelta(days=day)
        
        # Morning shift
        clock_in = date_offset.replace(hour=random.randint(7, 9), minute=random.randint(0, 59), second=0)
        work_duration = random.uniform(7.5, 8.5)
        clock_out = clock_in + timedelta(hours=work_duration)
        break_duration = round(random.uniform(0.5, 1.0), 2)
        
        session = {
            "worker_id": worker_id,
            "clock_in": clock_in.isoformat() + "Z",
            "location": random.choice([
                "Assembly Line A", "Assembly Line B", "Welding Station 1", 
                "CNC Department", "Quality Control", "Maintenance Bay",
                "Packaging Unit", "Testing Lab", "Machine Shop", "Tool Room"
            ]),
            "device_id": f"SMARTWATCH_{worker_id:03d}"
        }
        
        sessions.append((session, clock_out.isoformat() + "Z", break_duration))
    
    return sessions

# ========== DIVERSE TASKS ==========
TASK_TEMPLATES = {
    "Assembly": [
        "Assemble engine components for Model-{model}",
        "Install wiring harness in chassis {id}",
        "Mount control panel in Unit-{id}",
        "Fit hydraulic system components",
        "Attach safety covers and guards"
    ],
    "Quality": [
        "Inspect batch #{batch} for defects",
        "Perform quality audit on production line",
        "Calibrate measuring instruments",
        "Document quality metrics for shift",
        "Test functionality of assembled units"
    ],
    "Maintenance": [
        "Perform preventive maintenance on Machine-{id}",
        "Repair hydraulic leak in Station-{id}",
        "Replace worn parts in CNC-{id}",
        "Lubricate and clean machinery",
        "Update maintenance logs"
    ],
    "Production": [
        "Manufacture {qty} units of Part-{part}",
        "Set up machine for new production run",
        "Monitor production line efficiency",
        "Package completed products",
        "Prepare materials for next shift"
    ],
    "Safety": [
        "Conduct safety inspection of work area",
        "Update safety training records",
        "Review incident reports and take action",
        "Ensure PPE compliance",
        "Test emergency equipment"
    ]
}

def generate_diverse_tasks(worker_count=20):
    """Generate realistic tasks for all workers"""
    tasks = []
    
    for worker_id in range(1, worker_count + 1):
        # 2-5 tasks per worker
        num_tasks = random.randint(2, 5)
        
        for _ in range(num_tasks):
            category = random.choice(list(TASK_TEMPLATES.keys()))
            template = random.choice(TASK_TEMPLATES[category])
            
            title = template.format(
                model=random.choice(["TX200", "MX500", "RX750"]),
                id=random.randint(100, 999),
                batch=random.randint(1000, 9999),
                qty=random.randint(50, 500),
                part=random.choice(["A123", "B456", "C789", "D012"])
            )
            
            descriptions = [
                "Complete this task following standard operating procedures. Report any issues immediately.",
                "High priority production requirement. Coordinate with team lead if assistance needed.",
                "Quality critical task. Ensure all measurements are within tolerance.",
                "Time-sensitive assignment. Follow safety protocols at all times.",
                "Part of daily routine maintenance. Document completion in system."
            ]
            
            due_date = datetime.utcnow() + timedelta(days=random.randint(1, 7))
            
            task = {
                "worker_id": worker_id,
                "title": title,
                "description": random.choice(descriptions),
                "priority": random.choices(
                    ["low", "medium", "high"],
                    weights=[20, 50, 30]
                )[0],
                "assigned_by": random.choice([
                    "Production Manager",
                    "Shift Supervisor",
                    "Quality Lead",
                    "Maintenance Head",
                    "Operations Manager"
                ]),
                "due_date": due_date.isoformat() + "Z"
            }
            
            # Some tasks are already completed
            if random.random() > 0.6:
                task["status"] = random.choice(["completed", "in_progress"])
            
            tasks.append(task)
    
    return tasks

# ========== MAIN POPULATION FUNCTION ==========
def main():
    print_section("🎬 DEMO DATA GENERATOR - JURY PRESENTATION MODE")
    print_info("Creating realistic synthetic data for all features...")
    print_info("This will make your app look production-ready! 🚀\n")
    
    # Step 1: Clear existing data (optional)
    print_section("📊 STEP 1: GENERATING WORKERS")
    workers = generate_diverse_workers()
    
    created_workers = []
    for worker in workers:
        try:
            response = requests.post(f"{API_BASE_URL}/worker/add", json=worker)
            if response.status_code == 201:
                worker_data = response.json()
                created_workers.append(worker_data)
                skills_str = ", ".join(worker['skills'][:3])
                print_success(f"{worker['name']} - {len(worker['skills'])} skills: {skills_str}...")
        except Exception as e:
            print_warning(f"Skipping {worker['name']}: {str(e)[:50]}")
    
    print_info(f"\n✨ Created {len(created_workers)} workers with diverse skill sets")
    
    # Step 2: Generate Health Metrics
    print_section("🏥 STEP 2: GENERATING HEALTH METRICS")
    health_count = 0
    
    for worker in created_workers[:15]:  # Health data for 15 workers
        worker_id = worker['id']
        
        # Create varied health patterns
        if worker_id % 5 == 0:
            status = "alert"  # Some workers are tired/stressed
        elif worker_id % 3 == 0:
            status = "tired"
        else:
            status = "normal"
        
        # Generate metrics over the past 24 hours
        for hours_ago in [0, 4, 8, 12, 16, 20]:
            metric = generate_health_metric(worker_id, hours_ago, status)
            
            try:
                response = requests.post(f"{API_BASE_URL}/health/metric", json=metric)
                if response.status_code == 201:
                    health_count += 1
            except Exception as e:
                pass
        
        status_emoji = "🟢" if status == "normal" else "🟡" if status == "tired" else "🔴"
        print_success(f"{worker['name']}: {status_emoji} {status.upper()} - HR:{metric['heart_rate']} bpm, Stress:{metric['stress_level']}%")
    
    print_info(f"\n💓 Created {health_count} health metric readings across multiple timepoints")
    
    # Step 3: Generate Work Sessions
    print_section("⏰ STEP 3: GENERATING WORK SESSIONS")
    session_count = 0
    
    for worker in created_workers[:15]:
        worker_id = worker['id']
        sessions = generate_work_sessions(worker_id, days=7)
        
        for session_data, clock_out_time, break_duration in sessions:
            try:
                # Clock in
                response = requests.post(f"{API_BASE_URL}/session/clock-in", json=session_data)
                if response.status_code == 201:
                    session_id = response.json()['id']
                    
                    # Clock out
                    clock_out_data = {
                        "clock_out": clock_out_time,
                        "break_duration": break_duration
                    }
                    requests.put(f"{API_BASE_URL}/session/{session_id}/clock-out", json=clock_out_data)
                    session_count += 1
            except Exception as e:
                pass
        
        print_success(f"{worker['name']}: {len(sessions)} work sessions over 7 days")
    
    print_info(f"\n📅 Created {session_count} work sessions with realistic patterns")
    
    # Step 4: Generate Tasks
    print_section("📋 STEP 4: GENERATING DIVERSE TASKS")
    tasks = generate_diverse_tasks(len(created_workers))
    task_count = 0
    
    for task in tasks:
        try:
            response = requests.post(f"{API_BASE_URL}/task/create", json=task)
            if response.status_code == 201:
                task_count += 1
        except Exception as e:
            pass
    
    print_info(f"Generated {task_count} tasks across categories:")
    for category in TASK_TEMPLATES.keys():
        count = len([t for t in tasks if any(keyword in t['title'] for keyword in [category.lower()])])
        print_success(f"  {category}: ~{count} tasks")
    
    # Step 5: Generate Assignments
    print_section("🎯 STEP 5: GENERATING ROLE ASSIGNMENTS")
    
    try:
        roles_response = requests.get(f"{API_BASE_URL}/role/all")
        roles = roles_response.json()
        assignment_count = 0
        
        for worker in created_workers[:12]:
            role = random.choice(roles)
            
            assignment = {
                "worker_id": worker['id'],
                "role_id": role['id'],
                "fit_score": round(random.uniform(0.65, 0.95), 2)
            }
            
            try:
                response = requests.post(f"{API_BASE_URL}/assignment/create", json=assignment)
                if response.status_code == 201:
                    assignment_count += 1
                    print_success(f"{worker['name']} → {role['name']} (Fit: {assignment['fit_score']*100:.0f}%)")
            except:
                pass
        
        print_info(f"\n🎖️  Created {assignment_count} role assignments")
    except:
        print_warning("Could not generate assignments (roles may not exist)")
    
    # Step 6: Summary Statistics
    print_section("📊 FINAL STATISTICS")
    
    try:
        # Health Dashboard
        health_dash = requests.get(f"{API_BASE_URL}/health/dashboard").json()
        stats = health_dash['statistics']
        
        print(f"{MAGENTA}Health Monitoring:{RESET}")
        print_success(f"  Workers Monitored: {stats['total_workers']}")
        print_success(f"  🟢 Good Health: {stats['workers_good']}")
        print_success(f"  🟡 Warnings: {stats['workers_warning']}")
        print_success(f"  🔴 Critical: {stats['workers_critical']}")
        print_success(f"  Avg Hours Today: {stats['average_hours_today']:.1f}h")
        print_success(f"  Avg Hours/Week: {stats['average_hours_this_week']:.1f}h")
    except:
        pass
    
    try:
        # Hours Dashboard
        hours_dash = requests.get(f"{API_BASE_URL}/session/all/hours").json()
        
        print(f"\n{MAGENTA}Work Hours Tracking:{RESET}")
        print_success(f"  Workers Tracked: {hours_dash['total_workers']}")
        
        if hours_dash['workers']:
            total_today = sum(w['today_hours'] for w in hours_dash['workers'])
            total_week = sum(w['week_hours'] for w in hours_dash['workers'])
            print_success(f"  Total Hours Today: {total_today:.1f}h")
            print_success(f"  Total Hours This Week: {total_week:.1f}h")
    except:
        pass
    
    try:
        # Analytics
        analytics = requests.get(f"{API_BASE_URL}/analytics/overview").json()
        
        print(f"\n{MAGENTA}Overall System:{RESET}")
        print_success(f"  Total Workers: {analytics['total_workers']}")
        print_success(f"  Total Roles: {analytics['total_roles']}")
        print_success(f"  Total Assignments: {analytics['total_assignments']}")
        print_success(f"  Success Rate: {analytics['success_rate']*100:.0f}%")
    except:
        pass
    
    # Final Message
    print_section("🎉 DEMO DATA GENERATION COMPLETE!")
    
    print(f"{GREEN}✨ Your app is now ready for jury presentation!{RESET}\n")
    print(f"{CYAN}📱 Access Points:{RESET}")
    print(f"  🌐 Web App: http://localhost:3000")
    print(f"  📱 Mobile App: http://localhost:8082")
    print(f"  🔧 API Docs: http://localhost:8000/docs")
    print(f"  🏥 Health Dashboard: http://localhost:8000/health/dashboard")
    print(f"  ⏰ Hours Dashboard: http://localhost:8000/session/all/hours")
    
    print(f"\n{MAGENTA}💡 Demo Highlights:{RESET}")
    print(f"  ✅ Diverse worker profiles with realistic skills")
    print(f"  ✅ Real-time health monitoring with alerts")
    print(f"  ✅ Comprehensive work hours tracking")
    print(f"  ✅ Variety of tasks across multiple categories")
    print(f"  ✅ ML-powered role assignments")
    print(f"  ✅ 7 days of historical data")
    print(f"  ✅ Multiple health statuses (normal/tired/alert)")
    
    print(f"\n{YELLOW}🎬 Presentation Tips:{RESET}")
    print(f"  1. Show health dashboard first - live metrics look impressive")
    print(f"  2. Demonstrate mobile app task sync (assign task → appears in mobile)")
    print(f"  3. Show ML recommendations (Dashboard → Find Best Workers)")
    print(f"  4. Highlight workers with alerts (demonstrates monitoring)")
    print(f"  5. Show work hours reports (proves tracking capability)")
    
    print(f"\n{GREEN}Good luck with your presentation! 🚀{RESET}\n")

if __name__ == "__main__":
    main()
