import json
import platform
import statistics
import subprocess
import tempfile
import time

# from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


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


def run_lighthouse_repeatedly(command, output_path, label):
    def run_single(run_number):
        with tempfile.NamedTemporaryFile(
            suffix=".json",
            delete=False,
            dir=output_path.parent,
        ) as report_file:
            temporary_path = Path(report_file.name)

        run_command = command.copy()

        output_index = next(
            index
            for index, argument in enumerate(run_command)
            if argument.startswith("--output-path=")
        )

        run_command[output_index] = f"--output-path={temporary_path}"

        start = time.perf_counter()

        try:
            run_lighthouse_command(run_command)
            report = load_report(temporary_path)

            score = round(report["categories"]["performance"]["score"] * 100)

            print(
                f"Lighthouse {label} run {run_number}: "
                f"{time.perf_counter() - start:.2f}s "
                f"(score: {score})"
            )

            return report, score, parse_report(report)

        finally:
            temporary_path.unlink(missing_ok=True)

    results = [run_single(run_number) for run_number in range(1, 6)]

    scores = [result[1] for result in results]

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(results[0][0], file)

    score_summary = {
        "lowest": min(scores),
        "median": statistics.median(scores),
        "highest": max(scores),
    }

    parsed_results = results[0][2]
    parsed_results["performance_score"] = score_summary["median"]

    print(f"Lighthouse {label} scores: {scores}")
    print(f"Lighthouse {label} score summary: {score_summary}")

    return score_summary, parsed_results


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

    mobile_score_summary, mobile_results = run_lighthouse_repeatedly(
        mobile_command,
        mobile_output_path,
        "mobile",
    )

    desktop_score_summary, desktop_results = run_lighthouse_repeatedly(
        desktop_command,
        desktop_output_path,
        "desktop",
    )

    mobile_results["performance_score_summary"] = mobile_score_summary
    desktop_results["performance_score_summary"] = desktop_score_summary

    return {
        "mobile": mobile_results,
        "desktop": desktop_results,
    }
