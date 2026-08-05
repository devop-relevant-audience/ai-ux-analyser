from axe_playwright_python.sync_playwright import Axe
from playwright.sync_api import sync_playwright


def run_axe(url):
    axe = Axe()

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url, wait_until="load")

        results = axe.run(page)

        browser.close()

        return {
            "violations_count": results.violations_count,
            "violations": [
                {
                    "id": v["id"],
                    "impact": v["impact"],
                    "description": v["description"],
                    "help": v["help"],
                    "occurrences": len(v["nodes"]),
                }
                for v in results.response["violations"]
            ],
        }


if __name__ == "__main__":
    report = run_axe("https://www.discord.com/")
    print(report)
