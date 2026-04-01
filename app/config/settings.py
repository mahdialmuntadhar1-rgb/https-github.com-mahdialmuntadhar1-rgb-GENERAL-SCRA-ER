import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./iraq_edu_data.db")
APP_NAME = os.getenv("APP_NAME", "Iraq Edu Data Control Center")

# UI Settings
THEME = "blue"
APPEARANCE_MODE = "dark"
