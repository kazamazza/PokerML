import os
from dotenv import load_dotenv
from project_root import PROJECT_ROOT

# Detect environment
# Dynamically select the correct .env file path
env_file_name = ".env.docker" if os.getenv("INSIDE_DOCKER") == "1" else ".env.local"
env_file_path = os.path.join(PROJECT_ROOT, env_file_name)

# Load environment variables
load_dotenv(dotenv_path=env_file_path)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "postgres")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)