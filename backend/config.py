import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/skill_assign")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# SQLite fallback if PostgreSQL not available
USE_SQLITE_FALLBACK = os.getenv("USE_SQLITE_FALLBACK", "false").lower() == "true"
if USE_SQLITE_FALLBACK:
    DATABASE_URL = "sqlite:///./skill_assign.db"
