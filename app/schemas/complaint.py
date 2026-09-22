from pydantic import BaseModel, Field
from typing import Optional


class ComplaintInput(BaseModel):
    topic: str = Field(..., min_length=1)
    severity: int = Field(..., ge=0, le=5)
    sentiment: float = Field(..., ge=-1.0, le=1.0)
    volume: int = Field(..., ge=0)
    trend: float = Field(..., ge=-1.0, le=1.0)
    regulatory_risk: float = Field(..., ge=0.0, le=1.0)
    business_impact: float = Field(..., ge=0.0, le=1.0)


class MetricWeights(BaseModel):
    severity: float = 0.30
    sentiment: float = 0.25
    volume: float = 0.15
    trend: float = 0.10
    regulatory_risk: float = 0.10
    business_impact: float = 0.10


class RankRequest(BaseModel):
    complaints: list[ComplaintInput]
    metric_weights: Optional[MetricWeights] = None


class RankedComplaint(ComplaintInput):
    priority_score: float
