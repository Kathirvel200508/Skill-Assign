"""
Script to reset the tasks table
"""
from database import engine
from models import Task
from sqlalchemy import text

def reset_tasks_table():
    print("Dropping existing tasks table...")
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS tasks"))
        conn.commit()
    
    print("Creating new tasks table...")
    Task.__table__.create(bind=engine, checkfirst=True)
    print("✓ Tasks table reset successfully!")

if __name__ == "__main__":
    reset_tasks_table()
