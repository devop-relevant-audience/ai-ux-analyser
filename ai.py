import base64
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from schema import UXEvaluation

load_dotenv()

def load_rubric():
    rubric_path = Path("docs/ux_rubric_spec.md")

    with open(rubric_path, "r", encoding="utf-8") as file:
        rubric = file.read()

    return rubric


def build_prompt(
    rubric,
    lighthouse_report,
    axe_report,
):
    schema = json.dumps(
        UXEvaluation.model_json_schema(),
        indent=2,
    )

    role = """
You are an expert UX evaluator.
"""
    task = """
Evaluate the supplied webpage using the UX rubric below 

The evaluation must be evidence-based and follow the rubric consistently.
"""
    instructions = """
- When assigning scores, follow the scoring methodology and evidence defined in the UX rubric.
  If objective evidence conflicts with subjective visual impressions, prioritize the objective evidence where applicable.
- Assign a score from 1 to 5 for each UX dimension.
- Base visual observations on the provided screenshots.
- Use Axe as the primary source of technical accessibility evidence.
- Use Lighthouse metrics where they are relevant to the evaluation.
- Do not invent information that is not supported by the provided evidence.
- Do not make assumptions about interactions or functionality that cannot be observed from the screenshots or reports. 
- Provide concise summaries, strengths, issues, and actionable recommendations based on evidence.
- Return ONLY a valid JSON object.
- Do not include any introductory text, explanations, markdown formatting, or code fences.
- Ensure all scores given for each dimension are supported by evidence rather than subjective opinion.
"""
    evidence = f"""
Screenshots
The webpage screenshots will be supplied together with this prompt.

UX Rubric
{rubric}

Lighthouse Report
{lighthouse_report}

Axe Report
{axe_report}
"""
    prompt = f"""
# Role

{role}

# Task

{task}

# Instructions

{instructions}

# Evidence

{evidence}

# Expected Output

Return ONLY a valid JSON object.

The JSON MUST conform exactly to the following JSON Schema.

Do not omit required fields.
Do not add extra fields.
Do not rename fields.

JSON Schema:

{schema}
"""
    return prompt


def encode_image(image_path):
    """
    Read an image file and encode it as Base64 string.
    """
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    encoded_image = base64.b64encode(image_bytes)

    return encoded_image.decode("utf-8")


def call_ai(
    prompt,
    screenshots,
):

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

    return response.output_text

def validate_response(response):
    return UXEvaluation.model_validate_json(response)


def generate_ux_report(
    screenshots,
    lighthouse_report,
    axe_report,
):

    rubric = load_rubric()

    prompt = build_prompt(
        rubric,
        lighthouse_report,
        axe_report,
    )

    response = call_ai(
        prompt,
        screenshots,
    )

    report = validate_response(response)

    return report
