import pytest
from pydantic import ValidationError

from visual_schema import VisualEvidence


def create_valid_visual_evidence():
    observation = {"observation": "The page has a clear visual hierarchy."}

    dimension = {
        "mobile": [observation],
        "tablet": [observation],
        "desktop": [observation],
        "summary": [observation],
    }

    return {
        "page_context": {
            "page_type": "Business website",
            "primary_purpose": "Provide information about the business",
            "primary_content": "Information about the company's services",
            "prominent_actions": ["Learn more", "Contact us"],
        },
        "visual_observations": {
            "visual_hierarchy": dimension,
            "navigation": dimension,
            "aesthetic_design": dimension,
            "consistency_and_standards": dimension,
            "clarity_and_familiarity": dimension,
            "accessibility": dimension,
        },
        "viewport_summaries": {
            "mobile": "The mobile layout is clear and readable.",
            "tablet": "The tablet layout is well structured.",
            "desktop": "The desktop layout provides a clear presentation.",
        },
        "screenshot_integrity": {
            "mobile": [observation],
            "tablet": [observation],
            "desktop": [observation],
            "summary": [observation],
        },
    }


def test_valid_visual_evidence():
    data = create_valid_visual_evidence()

    result = VisualEvidence.model_validate(data)

    assert isinstance(result, VisualEvidence)
    assert result.page_context.page_type == "Business website"
    assert result.viewport_summaries.mobile == (
        "The mobile layout is clear and readable."
    )


def test_too_many_mobile_observations_are_rejected():
    data = create_valid_visual_evidence()

    data["visual_observations"]["visual_hierarchy"]["mobile"] = [
        {"observation": "Observation 1"},
        {"observation": "Observation 2"},
    ]

    with pytest.raises(ValidationError):
        VisualEvidence.model_validate(data)


def test_unexpected_field_is_rejected():
    data = create_valid_visual_evidence()

    data["page_context"]["unexpected_field"] = "This should not be allowed"

    with pytest.raises(ValidationError):
        VisualEvidence.model_validate(data)