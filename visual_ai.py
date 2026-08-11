import base64
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from visual_schema import VisualEvidence

load_dotenv()


def load_rubric():
    rubric_path = Path("docs/ux_rubric_spec.md")

    with open(rubric_path, "r", encoding="utf-8") as file:
        rubric = file.read()

    return rubric


def encode_image(image_path):
    """
    Read an image file and encode it as Base64 string.
    """
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    encoded_image = base64.b64encode(image_bytes)

    return encoded_image.decode("utf-8")


def build_visual_prompt(rubric):
    prompt = f"""
# Role

You are a visual evidence extraction assistant for a UX evaluation system.

# Task

Analyze the supplied webpage screenshots and extract only observable visual
evidence relevant to the UX evaluation rubric.

Your task is NOT to evaluate the UX, assign scores, identify strengths or
issues, or provide recommendations.

Your task is only to describe what is visibly observable in the screenshots.

# Instructions

- Examine the mobile, tablet, and desktop screenshots.
- Base every observation only on what is visibly observable.
- Do not infer functionality that cannot be observed.
- Do not assume how an interaction behaves.
- Do not assign scores.
- Do not describe an observation as good, bad, strong, weak, effective, or ineffective.
- Do not make recommendations.
- Do not evaluate whether an observation satisfies a rubric score.
- If a characteristic is not visible or cannot be reliably determined from the screenshots, do not report it.
- Distinguish observations between viewport sizes when the visual presentation differs.
- Do not invent information that is not visible in the screenshots.
- Do not repeat the same observation across multiple dimensions unless the observation is directly relevant to each dimension.
- Use clear, factual, user-readable language.

# UX Rubric

{rubric}

# Expected Output

The response MUST use exactly the following JSON structure:


{{
  "visual_observations": {{
    "visual_hierarchy": {{
      "mobile": [],
      "tablet": [],
      "desktop": [],
      "summary": []
    }},
    "navigation": {{
      "mobile": [],
      "tablet": [],
      "desktop": [],
      "summary": []
    }},
    "aesthetic_design": {{
      "mobile": [],
      "tablet": [],
      "desktop": [],
      "summary": []
    }},
    "consistency_and_standards": {{
      "mobile": [],
      "tablet": [],
      "desktop": [],
      "summary": []
    }},
    "clarity_and_familiarity": {{
      "mobile": [],
      "tablet": [],
      "desktop": [],
      "summary": []
    }},
    "accessibility": {{
      "mobile": [],
      "tablet": [],
      "desktop": [],
      "summary": []
    }}
  }}
}}

Each observation must be an object containing:

"observation": a factual description of what is visibly observable
Do not rename any fields.

Do not add additional fields.

Example:

{{
  "visual_observations": {{
    "visual_hierarchy": {{
      "mobile": [
        {{
          "observation": "The hero content is vertically stacked, with the illustration above the centered heading, description, and buttons."
        }}
      ],
      "tablet": [
        {{
          "observation": "The hero illustration appears above the centered hero heading, description, and buttons."
        }}
      ],
      "desktop": [
        {{
          "observation": "The hero heading and description are positioned on the left, with the main illustration on the right."
        }}
      ],
      "summary": [
        {{
          "observation": "Large uppercase headings are used for the hero and feature sections."
        }},
        {{
          "observation": "Feature content is grouped into rounded panels containing headings, supporting text, and related imagery."
        }}
      ]
    }},
    "navigation": {{
      "mobile": [],
      "tablet": [],
      "desktop": [],
      "summary": []
    }},
    "aesthetic_design": {{
      "mobile": [],
      "tablet": [],
      "desktop": [],
      "summary": []
    }},
    "consistency_and_standards": {{
      "mobile": [],
      "tablet": [],
      "desktop": [],
      "summary": []
    }},
    "clarity_and_familiarity": {{
      "mobile": [],
      "tablet": [],
      "desktop": [],
      "summary": []
    }},
    "accessibility": {{
      "mobile": [],
      "tablet": [],
      "desktop": [],
      "summary": []
    }}
  }}
}}

Return observations for the following UX dimensions:

- Visual Hierarchy
- Navigation
- Aesthetic Design
- Consistency and Standards
- Clarity and Familiarity
- Accessibility

For each UX dimension:

- Provide up to 1 observation for mobile.
- Provide up to 1 observation for tablet.
- Provide up to 1 observation for desktop.
- Provide up to 2 cross-viewport observations in summary.

The mobile observation must describe a visual characteristic specifically observable in the mobile screenshot.

The tablet observation must describe a visual characteristic specifically observable in the tablet screenshot.

The desktop observation must describe a visual characteristic specifically observable in the desktop screenshot.

The summary observations must describe visual characteristics that are observable across multiple viewport sizes.

Summary observations must provide cross-viewport evidence rather than repeating the mobile, tablet, or desktop observation.

Do not repeat the same observation between mobile, tablet, desktop, and summary.

Do not invent observations if the relevant characteristic cannot be reliably determined from the screenshots.

Do not invent or repeat observations to reach the maximum.

Return ONLY a valid JSON object.
"""

    return prompt


def call_luna(prompt, screenshots):
    api_key = os.getenv("OPENROUTER_API_KEY")

    if api_key is None:
        raise ValueError("OPENROUTER_API_KEY was not found.")

    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
    )

    mobile_image = encode_image(screenshots["mobile"])
    tablet_image = encode_image(screenshots["tablet"])
    desktop_image = encode_image(screenshots["desktop"])

    response = client.responses.create(
        model="openai/gpt-5.6-luna",
        input=[
            {
                "type": "message",
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": prompt,
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{mobile_image}",
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{tablet_image}",
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{desktop_image}",
                    },
                ],
            },
        ],
        reasoning={
            "effort": "high",
        },
        temperature=0,
    )


    report = VisualEvidence.model_validate_json(response.output_text)


    output_path = Path("tests/Discord/luna_observations.json")

    output_path.write_text(
        report.model_dump_json(indent=2),
        encoding="utf-8",
    )

    return report


def extract_visual_evidence(screenshots):
    rubric = load_rubric()

    prompt = build_visual_prompt(rubric)

    response = call_luna(
        prompt,
        screenshots,
    )

    return response


if __name__ == "__main__":
    TEST_DIR = Path("tests/Discord")

    screenshots = {
        "mobile": str(TEST_DIR / "mobile.png"),
        "tablet": str(TEST_DIR / "tablet.png"),
        "desktop": str(TEST_DIR / "desktop.png"),
    }

    result = extract_visual_evidence(screenshots)

    print(result.model_dump_json(indent=2))
