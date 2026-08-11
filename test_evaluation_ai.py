
import json
from pathlib import Path

from evaluation_ai import generate_ux_report

TEST_DIR = Path("tests/Discord")


with open(
    TEST_DIR / "luna_observations.json",
    "r",
    encoding="utf-8",
) as file:
    visual_observations = json.load(file)


with open(
    TEST_DIR / "lighthouse-report.json",
    "r",
    encoding="utf-8",
) as file:
    lighthouse_report = file.read()


with open(
    TEST_DIR / "axe.json",
    "r",
    encoding="utf-8",
) as file:
    axe_report = json.load(file)


report = generate_ux_report(
    visual_observations,
    lighthouse_report,
    axe_report,
)


print(report.model_dump_json(indent=2))