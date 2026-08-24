from binascii import Incomplete

from pydantic import BaseModel, Field


class OverallEvaluation(BaseModel):
    summary: str
    strengths: list[str]
    issues: list[str]


class DimensionEvaluation(BaseModel):
    score: int = Field(ge=1, le=5)
    summary: str
    considerations: list[str] = Field(default_factory=list, max_length=2)
    strengths: list[str] = Field(default_factory=list, max_length=2)
    issues: list[str] = Field(default_factory=list, max_length=2)


class Recommendation(BaseModel):
    category: str
    recommendation: str


class AxeSummary(BaseModel):
    violations_count: int
    passes_count: int
    incomplete_count: int
    inapplicable_count: int

class VisualAccessibility(BaseModel):
    score: int = Field(ge=1, le=5)
    summary: str
    considerations: list[str] = Field(default_factory=list, max_length=2)
    strengths: list[str] = Field(default_factory=list, max_length=2)
    issues: list[str] = Field(default_factory=list, max_length=2)


class TechnicalAccessibility(BaseModel):
    score: int = Field(ge=1, le=5)
    summary: str
    considerations: list[str] = Field(default_factory=list, max_length=2)
    axe_summary: AxeSummary
    strengths: list[str] = Field(default_factory=list, max_length=2)
    issues: list[str] = Field(default_factory=list, max_length=2)


class AccessibilityEvaluation(BaseModel):
    score: int = Field(ge=1, le=5)
    summary: str
    considerations: list[str] = Field(default_factory=list, max_length=2)
    strengths: list[str] = Field(default_factory=list, max_length=2)
    issues: list[str] = Field(default_factory=list, max_length=2)
    visual_accessibility: VisualAccessibility
    technical_accessibility: TechnicalAccessibility


class Dimensions(BaseModel):
    visual_hierarchy: DimensionEvaluation
    navigation: DimensionEvaluation
    aesthetic_design: DimensionEvaluation
    consistency_and_standards: DimensionEvaluation
    clarity_and_familiarity: DimensionEvaluation
    accessibility: AccessibilityEvaluation
    performance: DimensionEvaluation

class UXEvaluation(BaseModel):
    overall: OverallEvaluation
    dimensions: Dimensions
    recommendations: list[Recommendation]
