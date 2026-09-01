from pydantic import BaseModel, Field


class VisualObservation(BaseModel):
    observation: str


class PageContext(BaseModel):
    page_type: str
    primary_purpose: str
    primary_content: str
    prominent_actions: list[str] = Field(default_factory=list)


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


class ScreenshotIntegrity(BaseModel):
    mobile: list[VisualObservation] = Field(default_factory=list, max_length=2)
    tablet: list[VisualObservation] = Field(default_factory=list, max_length=2)
    desktop: list[VisualObservation] = Field(default_factory=list, max_length=2)
    summary: list[VisualObservation] = Field(default_factory=list, max_length=5)


class VisualEvidence(BaseModel):
    page_context: PageContext
    visual_observations: VisualObservations
    screenshot_integrity: ScreenshotIntegrity = Field(
        default_factory=ScreenshotIntegrity
    )
