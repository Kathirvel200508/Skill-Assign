from database import SessionLocal
from models import Worker
import random

db = SessionLocal()

workers = db.query(Worker).all()

for worker in workers:
    # Set default hours if not already set
    if not hasattr(worker, 'hours_per_day') or worker.hours_per_day is None:
        worker.hours_per_day = random.uniform(7.5, 8.5)
    if not hasattr(worker, 'hours_per_week') or worker.hours_per_week is None:
        worker.hours_per_week = random.uniform(38, 50)
    
    # Recalculate fatigue based on hours
    fatigue = min((worker.hours_per_week / 52) * 0.7 + (worker.hours_per_day / 8.5) * 0.3, 1.0)
    worker.fatigue_level = fatigue

db.commit()
print(f"✅ Updated {len(workers)} workers with hours and recalculated fatigue")
db.close()
