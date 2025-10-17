"""
Fix database schema - Add missing task_id column to assignments
"""
import sqlite3
import os

db_path = 'skill_assign.db'

if not os.path.exists(db_path):
    print("❌ Database file not found!")
    exit(1)

print("\n🔧 Fixing database schema...\n")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Check if task_id column exists
    cursor.execute("PRAGMA table_info(assignments)")
    columns = [row[1] for row in cursor.fetchall()]
    
    if 'task_id' not in columns:
        print("Adding task_id column to assignments table...")
        cursor.execute("ALTER TABLE assignments ADD COLUMN task_id INTEGER")
        conn.commit()
        print("✅ Added task_id column\n")
    else:
        print("✅ task_id column already exists\n")
    
    # Verify
    cursor.execute("PRAGMA table_info(assignments)")
    print("Current assignments table schema:")
    for row in cursor.fetchall():
        print(f"   {row[1]} ({row[2]})")
    
    print("\n✅ Database schema fixed!\n")
    
except Exception as e:
    print(f"❌ Error: {e}\n")
    conn.rollback()
finally:
    conn.close()

print("🔄 Now restart your backend server:\n")
print("   1. Stop the backend (Ctrl+C)")
print("   2. Start it again: uvicorn main:app --reload")
print("   3. Refresh your web browser\n")
