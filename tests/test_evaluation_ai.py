import json
from pathlib import Path

from evaluation_ai import generate_ux_report
from lighthouse import load_report, parse_report


TEST_DIR = Path("tests/Discord")


# -------------------------
# Luna visual observations
# -------------------------

with open(
    TEST_DIR / "luna_observations.json",
    "r",
    encoding="utf-8",
) as file:
    visual_observations = json.load(file)["visual_observations"]


# -------------------------
# Lighthouse
# -------------------------

mobile_raw = load_report(TEST_DIR / "lighthouse-mobile-report.json")

desktop_raw = load_report(TEST_DIR / "lighthouse-desktop-report.json")

lighthouse_report = {
    "mobile": parse_report(mobile_raw),
    "desktop": parse_report(desktop_raw),
}


# -------------------------
# Axe
# -------------------------

axe_path = TEST_DIR / "axe.json"

print("Looking for Axe report at:", axe_path.resolve())
print("File exists:", axe_path.exists())

with open(
    axe_path,
    "r",
    encoding="utf-8",
) as file:
    axe_report = json.load(file)


# -------------------------
# Generate UX report
# -------------------------

report = generate_ux_report(
    visual_observations,
    lighthouse_report,
    axe_report,
)


# -------------------------
# Print result
# -------------------------

print(report.model_dump_json(indent=2))
