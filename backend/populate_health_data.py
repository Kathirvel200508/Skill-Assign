"""
Populate sample health metrics and work sessions from wearable devices
This simulates data coming from smartwatches/fitness trackers
"""
import requests
import random
from datetime import datetime, timedelta

API_BASE_URL = "http://localhost:8000"

def generate_health_metrics(worker_id, count=5):
    """Generate sample health metrics for a worker"""
    metrics = []
    
    for i in range(count):
        # Realistic health values
        heart_rate = random.randint(60, 100)
        oxygen_level = round(random.uniform(95.0, 100.0), 1)
        body_temp = round(random.uniform(36.2, 37.2), 1)
        stress_level = round(random.uniform(20, 60), 1)
        fatigue_score = round(random.uniform(10, 50), 1)
        steps = random.randint(1000, 10000)
        calories = round(random.uniform(100, 800), 1)
        hours_worked = round(random.uniform(0, 8.5), 1)
        
        metric = {
            "worker_id": worker_id,
            "heart_rate": heart_rate,
            "blood_pressure_systolic": random.randint(110, 135),
            "blood_pressure_diastolic": random.randint(70, 90),
            "oxygen_level": oxygen_level,
            "body_temperature": body_temp,
            "stress_level": stress_level,
            "fatigue_score": fatigue_score,
            "steps_count": steps,
            "calories_burned": calories,
            "hours_worked_today": hours_worked,
            "device_id": f"WATCH_{worker_id:03d}"
        }
        
        metrics.append(metric)
    
    return metrics

def generate_work_session(worker_id, hours_ago=8):
    """Generate a work session for a worker"""
    clock_in_time = datetime.utcnow() - timedelta(hours=hours_ago)
    clock_out_time = clock_in_time + timedelta(hours=random.uniform(6, 8.5))
    
    session = {
        "worker_id": worker_id,
        "clock_in": clock_in_time.isoformat() + "Z",
        "location": random.choice(["Assembly Line A", "Assembly Line B", "Welding Station", "Quality Control", "Maintenance Bay"]),
        "device_id": f"WATCH_{worker_id:03d}"
    }
    
    return session, clock_out_time

def main():
    print("=" * 60)
    print("POPULATING WEARABLE DEVICE DATA")
    print("=" * 60)
    
    # Get all workers
    print("\n[1] Fetching workers...")
    try:
        response = requests.get(f"{API_BASE_URL}/worker/all")
        workers = response.json()
        print(f"✅ Found {len(workers)} workers")
    except Exception as e:
        print(f"❌ Error fetching workers: {e}")
        return
    
    # Populate health metrics for each worker
    print("\n[2] Creating health metrics...")
    health_count = 0
    for worker in workers[:10]:  # First 10 workers
        worker_id = worker['id']
        worker_name = worker['name']
        
        metrics = generate_health_metrics(worker_id, count=3)
        
        for metric in metrics:
            try:
                response = requests.post(f"{API_BASE_URL}/health/metric", json=metric)
                if response.status_code == 201:
                    health_count += 1
                    print(f"   ✅ {worker_name}: HR={metric['heart_rate']} bpm, O2={metric['oxygen_level']}%, Stress={metric['stress_level']}%")
            except Exception as e:
                print(f"   ❌ Error for {worker_name}: {e}")
    
    print(f"\n✅ Created {health_count} health metric records")
    
    # Create work sessions
    print("\n[3] Creating work sessions...")
    session_count = 0
    for worker in workers[:10]:
        worker_id = worker['id']
        worker_name = worker['name']
        
        # Create 2 sessions (today and yesterday)
        for days_ago in [0, 1]:
            session_data, clock_out_time = generate_work_session(worker_id, hours_ago=(days_ago * 24 + 8))
            
            try:
                # Clock in
                response = requests.post(f"{API_BASE_URL}/session/clock-in", json=session_data)
                if response.status_code == 201:
                    session_id = response.json()['id']
                    session_count += 1
                    
                    # Clock out
                    clock_out_data = {
                        "clock_out": clock_out_time.isoformat() + "Z",
                        "break_duration": round(random.uniform(0.5, 1.0), 2)
                    }
                    
                    requests.put(f"{API_BASE_URL}/session/{session_id}/clock-out", json=clock_out_data)
                    print(f"   ✅ {worker_name}: Session recorded ({days_ago} days ago)")
            except Exception as e:
                print(f"   ❌ Error for {worker_name}: {e}")
    
    print(f"\n✅ Created {session_count} work sessions")
    
    # Test dashboard endpoints
    print("\n[4] Testing dashboard endpoints...")
    
    # Health Dashboard
    try:
        response = requests.get(f"{API_BASE_URL}/health/dashboard")
        if response.status_code == 200:
            data = response.json()
            stats = data['statistics']
            print(f"\n📊 Health Dashboard Statistics:")
            print(f"   Total Workers: {stats['total_workers']}")
            print(f"   Workers Good: {stats['workers_good']}")
            print(f"   Workers Warning: {stats['workers_warning']}")
            print(f"   Workers Critical: {stats['workers_critical']}")
            print(f"   Workers with Alerts: {stats['workers_with_alerts']}")
            print(f"   Avg Hours Today: {stats['average_hours_today']}")
            print(f"   Avg Hours This Week: {stats['average_hours_this_week']}")
    except Exception as e:
        print(f"   ❌ Error fetching health dashboard: {e}")
    
    # Hours Dashboard
    try:
        response = requests.get(f"{API_BASE_URL}/session/all/hours")
        if response.status_code == 200:
            data = response.json()
            print(f"\n⏰ Hours Dashboard:")
            print(f"   Workers Tracked: {data['total_workers']}")
            if data['workers']:
                print(f"\n   Sample Worker Hours:")
                for worker in data['workers'][:3]:
                    print(f"   - {worker['worker_name']}: {worker['today_hours']}h today, {worker['week_hours']}h this week ({worker['status']})")
    except Exception as e:
        print(f"   ❌ Error fetching hours dashboard: {e}")
    
    print("\n" + "=" * 60)
    print("✅ DATA POPULATION COMPLETE!")
    print("=" * 60)
    print("\n📱 Access the dashboards:")
    print(f"   Health Dashboard: {API_BASE_URL}/health/dashboard")
    print(f"   Hours Dashboard: {API_BASE_URL}/session/all/hours")
    print(f"   API Docs: {API_BASE_URL}/docs")
    print("\n")

if __name__ == "__main__":
    main()
