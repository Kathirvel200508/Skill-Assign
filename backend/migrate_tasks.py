"""
Migration script to add tasks table to existing database
"""
from database import engine
from models import Base, Task

def migrate():
    print("Creating tasks table...")
    # Create only the tasks table
    Task.__table__.create(bind=engine, checkfirst=True)
    print("✓ Tasks table created successfully!")

if __name__ == "__main__":
    migrate()
