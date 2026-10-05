from normalize import build_report


def test_build_report_combines_analysis_results():
    lighthouse_report = {
        "mobile": {
            "performance_score": 90,
        },
        "desktop": {
            "performance_score": 95,
        },
    }

    axe_report = {
        "summary": {
            "violations_count": 2,
            "passes_count": 10,
            "incomplete_count": 1,
            "inapplicable_count": 5,
        }
    }

    ai_report = {
        "overall": {
            "summary": "The website provides a clear user experience."
        }
    }

    report = build_report(
        lighthouse_report,
        axe_report,
        ai_report,
    )

    assert "timestamp" in report
    assert report["lighthouse"] == lighthouse_report
    assert report["axe"] == axe_report
    assert report["ai"] == ai_report


def test_build_report_preserves_analysis_data():
    lighthouse_report = {"mobile": {"performance_score": 90}}
    axe_report = {"summary": {"violations_count": 2}}
    ai_report = {"overall_score": 4.0}

    report = build_report(
        lighthouse_report,
        axe_report,
        ai_report,
    )

    assert report["lighthouse"]["mobile"]["performance_score"] == 90
    assert report["axe"]["summary"]["violations_count"] == 2
    assert report["ai"]["overall_score"] == 4.0