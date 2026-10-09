from app import build_final_report


def test_build_final_report_combines_all_results():
    lighthouse_report = {
        "mobile": {"performance_score": 90},
        "desktop": {"performance_score": 95},
    }

    axe_report = {
        "summary": {
            "violations_count": 2,
            "passes_count": 10,
        }
    }

    ai_report = {
        "overall": {"summary": "Good overall user experience."},
        "dimensions": {"navigation": {"score": 4}},
    }

    visual_evidence = {"page_context": {"page_type": "Landing page"}}

    overall_score = 4.2

    report = build_final_report(
        lighthouse_report,
        axe_report,
        ai_report,
        visual_evidence,
        overall_score,
    )

    assert report["lighthouse"] == lighthouse_report
    assert report["axe"] == axe_report
    assert report["ai"] == ai_report
    assert report["visual_evidence"] == visual_evidence
    assert report["ai"]["overall_score"] == overall_score
