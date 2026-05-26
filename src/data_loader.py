
"""
Data loading and processing for Cupping QC System
"""
import pandas as pd
from .config import MOCK_CUPPING_CSV, PROCESSED_PICKLE

def load_cupping_data() -> pd.DataFrame:
    """Load cupping data"""
    if PROCESSED_PICKLE.exists():
        df = pd.read_pickle(PROCESSED_PICKLE)
        print(f"Loaded {len(df)} cupping records from pickle")
    elif MOCK_CUPPING_CSV.exists():
        df = pd.read_csv(MOCK_CUPPING_CSV)
        # Convert date columns
        for col in ['roast_date', 'cupping_date', 'last_updated']:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col])
        print(f"Loaded {len(df)} cupping records from CSV")
    else:
        raise FileNotFoundError("Cupping data not found. Run Phase 1 first.")

    return df

def validate_cupping_data(df: pd.DataFrame) -> pd.DataFrame:
    """Validate and enrich cupping data"""
    df = df.copy()

    # Ensure total score is calculated correctly
    sca_cols = ['aroma', 'flavor', 'aftertaste', 'acidity', 'body', 
                'balance', 'uniformity', 'clean_cup', 'sweetness', 'overall']

    df['total_score'] = df[sca_cols].sum(axis=1).round(1)

    # Quality Tier
    df['quality_tier'] = pd.cut(
        df['total_score'],
        bins=[0, 82, 85, 88, 100],
        labels=['Good', 'Very Good', 'Excellent', 'Outstanding']
    )

    return df
