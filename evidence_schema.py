from pydantic import BaseModel, Field

from visual_schema import VisualObservations



class LighthouseMetrics(BaseModel):
    performance_score: int = Field(ge=0, le=100)
    fcp: float
    lcp: float
    speed_index: float
    tbt: float
    cls: float


class LighthouseEvidence(BaseModel):
    mobile: LighthouseMetrics
    desktop: LighthouseMetrics


class LighthouseSummary(BaseModel):
    mobile: LighthouseMetrics
    desktop: LighthouseMetrics


class AxeSummary(BaseModel):
    violations_count: int
    passes_count: int
    incomplete_count: int
    inapplicable_count: int

class AxeViolation(BaseModel):
    id: str
    impact: str | None = None
    description: str
    help: str
    occurrences: int
    nodes: list[dict] = Field(default_factory=list)


class AxePass(BaseModel):
    id: str
    description: str
    help: str
    occurrences: int


class AxeEvidence(BaseModel):
    summary: AxeSummary
    violations: list[AxeViolation] = Field(default_factory=list)
    passes: list[AxePass] = Field(default_factory=list)


class EvaluationEvidence(BaseModel):
    visual_observations: VisualObservations
    lighthouse: LighthouseEvidence
    axe: AxeEvidence


class PerformanceEvaluation(BaseModel):
    score: int = Field(ge=1, le=5)
    summary: str
    lighthouse_summary: LighthouseSummary
    considerations: list[str] = Field(default_factory=list, max_length=2)
    strengths: list[str] = Field(default_factory=list, max_length=2)
    issues: list[str] = Field(default_factory=list, max_length=2)