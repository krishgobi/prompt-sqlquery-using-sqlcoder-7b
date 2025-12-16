from sqlalchemy import create_engine
import sys
from pathlib import Path

# Add parent directory to path to allow app imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
