import pytest
from pydantic import ValidationError

from evaluation_schema import UXEvaluation


def test_valid_ux_evaluation():
    data = {
        "overall": {
            "summary": "The website provides a clear and usable experience.",
            "strengths": [
                "Clear visual hierarchy",
                "Consistent navigation",
            ],
            "issues": [
                "Some content could be easier to scan",
            ],
            "recommendations": [
                {
                    "priority": "High",
                    "issue": "Some content is difficult to scan.",
                    "recommendation": "Improve content hierarchy and spacing.",
                }
            ],
        },
        "dimensions": {
            "visual_hierarchy": {
                "score": 4,
                "summary": "The visual hierarchy is clear.",
                "considerations": ["Some sections are dense."],
                "strengths": ["Clear headings"],
                "issues": ["Dense content in some areas"],
            },
            "navigation": {
                "score": 4,
                "summary": "Navigation is straightforward.",
                "considerations": ["Some navigation labels could be clearer."],
                "strengths": ["Consistent navigation"],
                "issues": ["Some labels are ambiguous"],
            },
            "aesthetic_design": {
                "score": 4,
                "summary": "The design is visually consistent.",
                "considerations": ["Some areas could use more visual variety."],
                "strengths": ["Consistent styling"],
                "issues": ["Some sections feel repetitive"],
            },
            "consistency_and_standards": {
                "score": 4,
                "summary": "The interface follows common conventions.",
                "considerations": ["Minor inconsistencies exist."],
                "strengths": ["Consistent components"],
                "issues": ["Some spacing differs"],
            },
            "clarity_and_familiarity": {
                "score": 4,
                "summary": "The content is generally easy to understand.",
                "considerations": ["Some terminology could be clearer."],
                "strengths": ["Clear messaging"],
                "issues": ["Some wording is unclear"],
            },
            "accessibility": {
                "score": 4,
                "calculated_score": 4.0,
                "summary": "The website is reasonably accessible.",
                "considerations": ["Some accessibility improvements are possible."],
                "strengths": ["Good basic accessibility"],
                "issues": ["Some elements need improvement"],
                "visual_accessibility": {
                    "score": 4,
                    "summary": "Visual accessibility is generally good.",
                    "considerations": ["Some contrast could be improved."],
                    "strengths": ["Readable typography"],
                    "issues": ["Some contrast issues"],
                },
                "technical_accessibility": {
                    "score": 4,
                    "summary": "Technical accessibility is generally good.",
                    "considerations": ["Some technical issues remain."],
                    "strengths": ["Good semantic structure"],
                    "issues": ["Some elements need attention"],
                },
            },
            "performance": {
                "score": 4,
                "summary": "The website performs reasonably well.",
                "considerations": ["Some optimisation is possible."],
                "strengths": ["Good loading performance"],
                "issues": ["Some resources could be optimised"],
            },
        },
    }

    result = UXEvaluation.model_validate(data)

    assert isinstance(result, UXEvaluation)
    assert result.dimensions.visual_hierarchy.score == 4
    assert result.overall.recommendations[0].priority == "High"


def test_invalid_score_is_rejected():
    data = {
        "overall": {
            "summary": "Test",
            "strengths": [],
            "issues": [],
            "recommendations": [],
        },
        "dimensions": {
            "visual_hierarchy": {
                "score": 6,
                "summary": "Test",
                "considerations": [],
                "strengths": [],
                "issues": [],
            }
        },
    }

    with pytest.raises(ValidationError):
        UXEvaluation.model_validate(data)


def test_unexpected_field_is_rejected():
    data = {
        "overall": {
            "summary": "Test",
            "strengths": [],
            "issues": [],
            "recommendations": [],
            "unexpected_field": "This should not be allowed",
        },
        "dimensions": {},
    }

    with pytest.raises(ValidationError):
        UXEvaluation.model_validate(data)