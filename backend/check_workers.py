"""
Check workers in database
"""
from database import get_db
from models import Worker

db = next(get_db())
workers = db.query(Worker).all()

print("Workers in database:")
print("-" * 50)
for w in workers:
    print(f"ID: {w.id:2d} | Name: {w.name}")
print("-" * 50)

# Find Rajesh Kumar
rajesh = db.query(Worker).filter(Worker.name.like('%Rajesh%')).first()
if rajesh:
    print(f"\n✓ Found Rajesh Kumar!")
    print(f"  Worker ID: {rajesh.id}")
    print(f"  Full Name: {rajesh.name}")
    print(f"  Current Role: {rajesh.current_role or 'None'}")
else:
    print("\n✗ Rajesh Kumar not found in database")
