from __future__ import annotations

from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    high = "High"
    medium = "Medium"
    low = "Low"


class ConfidenceLevel(str, Enum):
    high = "High"
    medium = "Medium"
    low = "Low"


class InsightCategory(str, Enum):
    permit = "Permit"
    agency = "Agency"
    coordination = "Coordination"
    environmental = "Environmental"
    utility_conflict = "Utility Conflict"
    schedule = "Schedule"


class Insight(BaseModel):
    category: InsightCategory
    insight: str
    risk_level: RiskLevel
    why_it_matters: str
    recommended_next_step: str
    confidence: ConfidenceLevel
    assumptions: List[str] = Field(default_factory=list)


class PermitAnalysis(BaseModel):
    project_summary: str
    overall_risk_level: RiskLevel
    insights: List[Insight]
    missing_information: List[str] = Field(default_factory=list)
    disclaimer: str = (
        "This is a planning-support analysis, not legal or permitting advice."
    )
