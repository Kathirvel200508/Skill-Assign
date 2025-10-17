"""
Setup and verify backend database
"""
import os
import sys

print("\n" + "="*70)
print("🔧 BACKEND & DATABASE SETUP")
print("="*70 + "\n")

# Step 1: Ensure .env file exists
env_path = '.env'
if not os.path.exists(env_path):
    print("📝 Creating .env file...")
    with open(env_path, 'w') as f:
        f.write("USE_SQLITE_FALLBACK=true\n")
        f.write("ENVIRONMENT=development\n")
    print("✅ Created .env file with SQLite configuration\n")
else:
    print("✅ .env file exists\n")

# Step 2: Create database tables
print("📊 Creating database tables...")
try:
    from database import engine, Base
    import models
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created\n")
except Exception as e:
    print(f"❌ Error creating tables: {e}\n")
    sys.exit(1)

# Step 3: Verify data exists
print("🔍 Checking existing data...")
try:
    from sqlalchemy.orm import Session
    from database import SessionLocal
    
    db = SessionLocal()
    
    worker_count = db.query(models.Worker).count()
    role_count = db.query(models.Role).count()
    task_count = db.query(models.Task).count()
    assignment_count = db.query(models.Assignment).count()
    
    print(f"   Workers: {worker_count}")
    print(f"   Roles: {role_count}")
    print(f"   Tasks: {task_count}")
    print(f"   Assignments: {assignment_count}\n")
    
    db.close()
    
    if worker_count == 0 or role_count == 0:
        print("⚠️  Database is empty! Run populate scripts to add data.\n")
    else:
        print("✅ Database has data!\n")
        
except Exception as e:
    print(f"❌ Error checking data: {e}\n")

# Step 4: Test backend endpoints
print("🧪 Testing backend server...")
try:
    import requests
    
    response = requests.get('http://localhost:8000/docs', timeout=2)
    if response.status_code == 200:
        print("✅ Backend is running on http://localhost:8000\n")
    else:
        print("⚠️  Backend responded but with status:", response.status_code, "\n")
except requests.exceptions.ConnectionError:
    print("❌ Backend is NOT running!")
    print("   Start it with: uvicorn main:app --reload\n")
except Exception as e:
    print(f"❌ Error testing backend: {e}\n")

print("="*70)
print("📋 NEXT STEPS:")
print("="*70 + "\n")
print("1. If backend is not running:")
print("   cd backend")
print("   uvicorn main:app --reload")
print()
print("2. If database is empty:")
print("   python create_assignments.py")
print()
print("3. Then start web app:")
print("   cd web")
print("   npm run dev")
print()
print("4. Access:")
print("   Dashboard: http://localhost:3000")
print("   API Docs: http://localhost:8000/docs")
print("\n" + "="*70 + "\n")
