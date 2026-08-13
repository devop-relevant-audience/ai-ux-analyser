from datetime import datetime


def build_report(lighthouse_report, axe_report):
    return {
        "timestamp": datetime.now().isoformat(),
        "lighthouse": lighthouse_report,
        "axe": axe_report,
    }
