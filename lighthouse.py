import json
import platform
import subprocess
from pathlib import Path


def load_report(report_path):
    with open(report_path, "r", encoding="utf-8") as file:
        return json.load(file)


def parse_report(report):
    print(
        "RAW TBT:",
        report["audits"]["total-blocking-time"]["numericValue"]
    )

    print(
        "RAW CLS:",
        report["audits"]["cumulative-layout-shift"]["numericValue"]
    )

    return {
        "performance_score": round(report["categories"]["performance"]["score"] * 100),
        "fcp": round(
            report["audits"]["first-contentful-paint"]["numericValue"] / 1000,
            2,
        ),
        "lcp": round(
            report["audits"]["largest-contentful-paint"]["numericValue"] / 1000,
            2,
        ),
        "speed_index": round(
            report["audits"]["speed-index"]["numericValue"] / 1000,
            2,
        ),
        "tbt": round(
            report["audits"]["total-blocking-time"]["numericValue"],
            2,
        ),
        "cls": round(
            report["audits"]["cumulative-layout-shift"]["numericValue"],
            4,
        ),
    }


def run_lighthouse(url):
    lighthouse_cmd = (
        "lighthouse.cmd" if platform.system() == "Windows" else "lighthouse"
    )

    mobile_output_path = Path("runtime/lighthouse-mobile-report.json")
    mobile_output_path.parent.mkdir(exist_ok=True)

    subprocess.run(
        [
            lighthouse_cmd,
            url,
            "--output=json",
            f"--output-path={mobile_output_path}",
            "--quiet",
            "--chrome-flags=--headless --no-sandbox",
            "--form-factor=mobile",
        ],
        check=True,
    )

    mobile_report = load_report(mobile_output_path)
    mobile_results = parse_report(mobile_report)

    desktop_output_path = Path("runtime/lighthouse-desktop-report.json")
    desktop_output_path.parent.mkdir(exist_ok=True)

    subprocess.run(
        [
            lighthouse_cmd,
            url,
            "--output=json",
            f"--output-path={desktop_output_path}",
            "--quiet",
            "--chrome-flags=--headless --no-sandbox",
            "--preset=desktop",
        ],
        check=True,
    )

    desktop_report = load_report(desktop_output_path)
    desktop_results = parse_report(desktop_report)

    return {
        "mobile": mobile_results,
        "desktop": desktop_results,
    }
