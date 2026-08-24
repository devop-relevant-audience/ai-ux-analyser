from pydantic import BaseModel, Field

class VisualObservation(BaseModel):
    observation: str

class VisualDimensionEvidence(BaseModel):
    mobile: list[VisualObservation] = Field(default_factory=list, max_length=1)
    tablet: list[VisualObservation] = Field(default_factory=list, max_length=1)
    desktop: list[VisualObservation] = Field(default_factory=list, max_length=1)
    summary: list[VisualObservation] = Field(default_factory=list, max_length=2)

class VisualObservations(BaseModel):
    visual_hierarchy: VisualDimensionEvidence
    navigation: VisualDimensionEvidence
    aesthetic_design: VisualDimensionEvidence
    consistency_and_standards: VisualDimensionEvidence
    clarity_and_familiarity: VisualDimensionEvidence
    accessibility: VisualDimensionEvidence

class VisualEvidence(BaseModel):
    visual_observations: VisualObservations