import json
import subprocess
import platform

def load_report(report_path):
    with open(report_path, "r") as file:
        data = json.load(file)
    return data


def parse_report(report):
    return {
        "performance_score": round(report["categories"]["performance"]["score"] * 100),
        "accessibility_score": round(report["categories"]["accessibility"]["score"] * 100),
        "best_practices_score": round(report["categories"]["best-practices"]["score"] * 100),
        "seo_score": round(report["categories"]["seo"]["score"] * 100),
        "fcp": round(report["audits"]["first-contentful-paint"]["numericValue"], 2),
        "lcp": round(report["audits"]["largest-contentful-paint"]["numericValue"], 2),
        "speed_index": round(report["audits"]["speed-index"]["numericValue"], 2),
        "tbt": round(report["audits"]["total-blocking-time"]["numericValue"], 2),
        "cls": round(report["audits"]["cumulative-layout-shift"]["numericValue"], 4),
    }


def run_lighthouse(url):
    lighthouse_cmd = (
        "lighthouse.cmd" if platform.system() == "Windows"
        else "lighthouse"
    )

    subprocess.run(
        [
            lighthouse_cmd,
            url,
            "--output=json",
            "--output-path=lighthouse-report.json",
            "--quiet",
            "--chrome-flags=--headless --no-sandbox",
        ],
        check=True,
    )

    report = load_report("lighthouse-report.json")
    return parse_report(report)


if __name__ == "__main__":
    report = run_lighthouse("https://www.discord.com/")
    print(report)
   