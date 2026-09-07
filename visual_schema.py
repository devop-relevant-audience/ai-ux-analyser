from pydantic import BaseModel, Field


class VisualObservation(BaseModel):
    model_config = {"extra": "forbid"}

    observation: str


class PageContext(BaseModel):
    model_config = {"extra": "forbid"}

    page_type: str
    primary_purpose: str
    primary_content: str
    prominent_actions: list[str]


class VisualDimensionEvidence(BaseModel):
    model_config = {"extra": "forbid"}

    mobile: list[VisualObservation] = Field(max_length=1)
    tablet: list[VisualObservation] = Field(max_length=1)
    desktop: list[VisualObservation] = Field(max_length=1)
    summary: list[VisualObservation] = Field(max_length=2)


class VisualObservations(BaseModel):
    model_config = {"extra": "forbid"}
    
    visual_hierarchy: VisualDimensionEvidence
    navigation: VisualDimensionEvidence
    aesthetic_design: VisualDimensionEvidence
    consistency_and_standards: VisualDimensionEvidence
    clarity_and_familiarity: VisualDimensionEvidence
    accessibility: VisualDimensionEvidence


class ScreenshotIntegrity(BaseModel):
    model_config = {"extra": "forbid"}

    mobile: list[VisualObservation] = Field(max_length=2)
    tablet: list[VisualObservation] = Field(max_length=2)
    desktop: list[VisualObservation] = Field(max_length=2)
    summary: list[VisualObservation] = Field(max_length=5)


class VisualEvidence(BaseModel):
    model_config = {"extra": "forbid"}
    
    page_context: PageContext
    visual_observations: VisualObservations
    screenshot_integrity: ScreenshotIntegrity
    
