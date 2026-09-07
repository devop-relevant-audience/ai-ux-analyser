from typing import Literal
from pydantic import BaseModel, Field


class Recommendation(BaseModel):
    model_config = {"extra": "forbid"}

    priority: Literal["Low", "Medium", "High"]
    issue: str
    recommendation: str

class OverallEvaluation(BaseModel):
    model_config = {"extra": "forbid"}

    summary: str
    strengths: list[str]
    issues: list[str]
    recommendations: list[Recommendation]


class DimensionEvaluation(BaseModel):
    model_config = {"extra": "forbid"}

    score: int = Field(ge=1, le=5)
    summary: str
    considerations: list[str] = Field(max_length=3)
    strengths: list[str] = Field(max_length=2)
    issues: list[str] = Field(max_length=2)


class VisualAccessibility(BaseModel):
    model_config = {"extra": "forbid"}

    score: int = Field(ge=1, le=5)
    summary: str
    considerations: list[str] = Field(max_length=3)
    strengths: list[str] = Field(max_length=2)
    issues: list[str] = Field(max_length=2)


class TechnicalAccessibility(BaseModel):
    model_config = {"extra": "forbid"}

    score: int = Field(ge=1, le=5)
    summary: str
    considerations: list[str] = Field(max_length=3)
    strengths: list[str] = Field(max_length=2)
    issues: list[str] = Field(max_length=2)

class AccessibilityEvaluation(BaseModel):
    model_config = {"extra": "forbid"}

    score: int = Field(ge=1, le=5)
    calculated_score: float = Field(ge=1, le=5)
    summary: str
    considerations: list[str] = Field(max_length=3)
    strengths: list[str] = Field(max_length=2)
    issues: list[str] = Field(max_length=2)
    visual_accessibility: VisualAccessibility
    technical_accessibility: TechnicalAccessibility


class Dimensions(BaseModel):
    model_config = {"extra": "forbid"}

    visual_hierarchy: DimensionEvaluation
    navigation: DimensionEvaluation
    aesthetic_design: DimensionEvaluation
    consistency_and_standards: DimensionEvaluation
    clarity_and_familiarity: DimensionEvaluation
    accessibility: AccessibilityEvaluation
    performance: DimensionEvaluation

class UXEvaluation(BaseModel):
    model_config = {"extra": "forbid"}
    
    overall: OverallEvaluation
    dimensions: Dimensions
