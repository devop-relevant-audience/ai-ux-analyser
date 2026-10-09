import json
import platform
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor


def load_report(report_path):
    with open(report_path, "r", encoding="utf-8") as file:
        return json.load(file)


def parse_report(report):

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


def run_lighthouse_command(command):
    for attempt in range(2):
        try:
            subprocess.run(
                command,
                check=True,
            )
            return
        except subprocess.CalledProcessError:
            if attempt == 1:
                raise


def run_timed_lighthouse_command(command, label):
    import time

    start = time.perf_counter()
    run_lighthouse_command(command)
    print(f"Lighthouse {label}: {time.perf_counter() - start:.2f}s")


def run_lighthouse(url):
    lighthouse_cmd = (
        "lighthouse.cmd" if platform.system() == "Windows" else "lighthouse"
    )

    desktop_output_path = Path("runtime/lighthouse-desktop-report.json")
    mobile_output_path = Path("runtime/lighthouse-mobile-report.json")

    mobile_output_path.parent.mkdir(exist_ok=True, parents=True)

    mobile_command = [
        lighthouse_cmd,
        url,
        "--output=json",
        f"--output-path={mobile_output_path}",
        "--quiet",
        "--chrome-flags=--headless --no-sandbox",
        "--form-factor=mobile",
        "--only-categories=performance",
    ]

    desktop_command = [
        lighthouse_cmd,
        url,
        "--output=json",
        f"--output-path={desktop_output_path}",
        "--quiet",
        "--chrome-flags=--headless --no-sandbox",
        "--preset=desktop",
        "--only-categories=performance",
    ]

    with ThreadPoolExecutor(max_workers=2) as executor:
        mobile_future = executor.submit(
            run_timed_lighthouse_command, mobile_command, "mobile"
        )
        desktop_future = executor.submit(
            run_timed_lighthouse_command, desktop_command, "desktop"
        )

        mobile_future.result()
        desktop_future.result()

    mobile_report = load_report(mobile_output_path)
    mobile_results = parse_report(mobile_report)

    desktop_report = load_report(desktop_output_path)
    desktop_results = parse_report(desktop_report)

    return {
        "mobile": mobile_results,
        "desktop": desktop_results,
    }
