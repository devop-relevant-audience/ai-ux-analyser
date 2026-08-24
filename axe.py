from axe_playwright_python.sync_playwright import Axe
from playwright.sync_api import sync_playwright


def normalize_violation(rule, include_nodes=True):
    normalized = {
        "id": rule["id"],
        "impact": rule["impact"],
        "description": rule["description"],
        "help": rule["help"],
        "help_url": rule.get("helpUrl"),
        "occurrences": len(rule.get("nodes", [])),
    }

    if include_nodes:
        normalized["nodes"] = [
            {
                "target": node.get("target", []),
                "html": node.get("html", ""),
                "failure_summary": node.get("failureSummary", ""),
            }
            for node in rule.get("nodes", [])
        ]

    return normalized


def normalize_pass(rule):
    return {
        "id": rule["id"],
        "description": rule["description"],
        "help": rule["help"],
        "occurrences": len(rule.get("nodes", [])),
    }


def run_axe(url):
    axe = Axe()

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url, wait_until="load")

        results = axe.run(page)

        axe_results = results.response

        browser.close()

        return {
            "summary": {
                "violations_count": len(axe_results.get("violations", [])),
                "passes_count": len(axe_results.get("passes", [])),
                "incomplete_count": len(axe_results.get("incomplete", [])),
                "inapplicable_count": len(axe_results.get("inapplicable", [])),
            },
            "violations": [
                normalize_violation(rule) for rule in axe_results.get("violations", [])
            ],
            "passes": [normalize_pass(rule) for rule in axe_results.get("passes", [])],
            "incomplete": [
                normalize_violation(rule) for rule in axe_results.get("incomplete", [])
            ],
        }