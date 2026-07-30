from pydantic import BaseModel


class OverallEvaluation(BaseModel):
  score: float
  summary: str
  strengths: list[str]
  issues: list[str]


class DimensionEvaluation(BaseModel):
  score: int
  summary: str
  strengths: list[str]
  issues: list[str]


class Recommendation(BaseModel):
  category: str
  recommendation: str
  

class AxeSummary(BaseModel):
  violations: int
  passes: int
  incomplete: int


class VisualAccessibility(BaseModel):
  summary: str
  strengths: list[str]
  issues: list[str]


class TechnicalAccessibility(BaseModel):
  summary: str
  axe_summary: AxeSummary
  strengths: list[str]
  issues: list[str]
  


class AccessibilityEvaluation(BaseModel):
  score: int
  summary: str
  strengths: list[str]
  issues: list[str]
  visual_accessibility: VisualAccessibility
  technical_accessibility: TechnicalAccessibility


class Dimensions(BaseModel):
  visual_hierarchy: DimensionEvaluation
  navigation: DimensionEvaluation
  aesthetic_design: DimensionEvaluation
  consistency_and_standards: DimensionEvaluation
  clarity_and_familiarity: DimensionEvaluation
  accessibility: AccessibilityEvaluation


class UXEvaluation(BaseModel):
  overall: OverallEvaluation
  dimensions: Dimensions
  recommendations: list[Recommendation]

