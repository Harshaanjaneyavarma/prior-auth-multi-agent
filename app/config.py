import os
from pathlib import Path
BASE_DIR=Path(__file__).resolve().parent.parent
DATA_DIR=Path(os.getenv("DEMO_DATA_DIR",BASE_DIR/"runtime"))
API_KEYS=set(os.getenv("DEMO_API_KEYS","demo-clinician-key").split(","))
