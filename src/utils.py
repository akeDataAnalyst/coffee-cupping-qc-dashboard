
"""
Utility functions for cupping analysis
"""
import pandas as pd

def get_score_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Summary by quality tier"""
    return df.groupby('quality_tier').agg({
        'total_score': ['count', 'mean', 'min', 'max'],
        'defects_per_300g': 'mean',
        'sample_id': 'count'
    }).round(2)

def get_region_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Performance by region"""
    return df.groupby('region').agg({
        'total_score': ['mean', 'max', 'count'],
        'defects_per_300g': 'mean'
    }).round(2)

def filter_high_quality(df: pd.DataFrame, min_score: float = 85.0):
    """Filter excellent and above"""
    return df[df['total_score'] >= min_score]
