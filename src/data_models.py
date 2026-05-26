
"""
Pydantic models for cupping data validation
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CuppingRecord(BaseModel):
    sample_id: str
    lot_id: str
    supplier_name: str
    region: str
    processing_method: str
    roast_date: datetime
    cupping_date: datetime

    # SCA Scores
    aroma: float = Field(ge=6.0, le=10.0)
    flavor: float = Field(ge=6.0, le=10.0)
    aftertaste: float = Field(ge=6.0, le=10.0)
    acidity: float = Field(ge=6.0, le=10.0)
    body: float = Field(ge=6.0, le=10.0)
    balance: float = Field(ge=6.0, le=10.0)
    uniformity: float = Field(ge=6.0, le=10.0)
    clean_cup: float = Field(ge=6.0, le=10.0)
    sweetness: float = Field(ge=6.0, le=10.0)
    overall: float = Field(ge=6.0, le=10.0)

    total_score: float
    quality_tier: str
    defects_per_300g: int = Field(ge=0)
    moisture_pct: float
    grade_ecx: str
    flavor_notes: str
    cupper_name: str
    last_updated: datetime
