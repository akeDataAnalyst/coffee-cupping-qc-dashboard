
"""
Configuration for Specialty Coffee Cupping QC Dashboard
"""

from pathlib import Path
import sys

# Add root to path
BASE_DIR = Path(__file__).parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# Data paths
DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"

MOCK_CUPPING_CSV = DATA_DIR / "mock_cupping_data.csv"
PROCESSED_PICKLE = PROCESSED_DIR / "cupping_data.pkl"

# Industry Constants
SPECIALTY_THRESHOLD = 80.0
EXCELLENT_THRESHOLD = 88.0

# SCA Attributes
SCA_ATTRIBUTES = ['aroma', 'flavor', 'aftertaste', 'acidity', 'body', 
                 'balance', 'uniformity', 'clean_cup', 'sweetness', 'overall']

print("Cupping QC Config loaded successfully!")
print(f"Project Root: {BASE_DIR}")
