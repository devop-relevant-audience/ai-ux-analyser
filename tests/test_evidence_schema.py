import pytest
from pydantic import ValidationError

from evidence_schema import EvaluationEvidence


def create_visual_observations():
    observation = {"observation": "The page has a clear visual hierarchy."}

    dimension = {
        "mobile": [observation],
        "tablet": [observation],
        "desktop": [observation],
        "summary": [observation],
    }

    return {
        "visual_hierarchy": dimension,
        "navigation": dimension,
        "aesthetic_design": dimension,
        "consistency_and_standards": dimension,
        "clarity_and_familiarity": dimension,
        "accessibility": dimension,
    }


def create_valid_evidence():
    lighthouse_metrics = {
        "performance_score": 90,
        "fcp": 1.2,
        "lcp": 2.0,
        "speed_index": 2.5,
        "tbt": 100.0,
        "cls": 0.05,
    }

    return {
        "visual_observations": create_visual_observations(),
        "lighthouse": {
            "mobile": lighthouse_metrics,
            "desktop": lighthouse_metrics,
        },
        "axe": {
            "summary": {
                "violations_count": 2,
                "passes_count": 10,
                "incomplete_count": 1,
                "inapplicable_count": 5,
            },
            "violations": [
                {
                    "id": "color-contrast",
                    "impact": "serious",
                    "description": "Elements must meet minimum color contrast.",
                    "help": "Ensure the contrast ratio is sufficient.",
                    "occurrences": 2,
                    "nodes": [],
                }
            ],
            "passes": [
                {
                    "id": "button-name",
                    "description": "Buttons must have discernible text.",
                    "help": "Ensure buttons have accessible names.",
                    "occurrences": 5,
                }
            ],
        },
    }


def test_valid_evidence_is_accepted():
    data = create_valid_evidence()

    result = EvaluationEvidence.model_validate(data)

    assert isinstance(result, EvaluationEvidence)
    assert result.lighthouse.mobile.performance_score == 90
    assert result.axe.summary.violations_count == 2
    assert (
        result.visual_observations.visual_hierarchy.mobile[0].observation
        == "The page has a clear visual hierarchy."
    )


def test_invalid_lighthouse_score_is_rejected():
    data = create_valid_evidence()

    data["lighthouse"]["mobile"]["performance_score"] = 101

    with pytest.raises(ValidationError):
        EvaluationEvidence.model_validate(data)


def test_missing_required_evidence_is_rejected():
    data = create_valid_evidence()

    del data["axe"]

    with pytest.raises(ValidationError):
        EvaluationEvidence.model_validate(data)