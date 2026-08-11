import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from evaluation_schema import UXEvaluation

load_dotenv()

def load_rubric():
    rubric_path = Path("docs/ux_rubric_spec.md")

    with open(rubric_path, "r", encoding="utf-8") as file:
        rubric = file.read()

    return rubric


def build_prompt(
    rubric,
    visual_observations,
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
General Principles

- Evaluate each UX dimension independently.
- Follow the scoring methodology defined in the supplied UX rubric.
- Do not allow strengths or weaknesses from one UX dimension to influence the score of another dimension.
- Base every conclusion only on the supplied evidence.
- Do not invent information that is not supported by the evidence.
- Do not make assumptions about interactions, animations, hidden menus, hover states, or functionality that cannot be directly observed.

Evidence Priority

Use the evidence source that is most directly relevant to the dimension being evaluated.

- Lighthouse metrics
- Axe accessibility findings
- Visual observations provide evidence about observable visual characteristics of the webpage.

When multiple evidence sources are relevant to the same dimension, incorporate each relevant source according to the criteria defined in the UX rubric.

If objective evidence conflicts with subjective visual impressions, always prioritise the objective evidence.

Objective Evidence

- Copy Lighthouse metrics exactly as provided.
- Copy Axe findings exactly as provided.
- Do not estimate, reinterpret, modify, or round objective values differently.
- Objective measurements must never be contradicted.
- Do not treat the absence of a Lighthouse or Axe finding as proof that a visual characteristic is satisfactory unless the relevant metric or finding directly supports that conclusion.
- When Lighthouse and Axe report different findings for related accessibility checks, report both findings accurately rather than assuming one invalidates the other.
- Do not merge, reconcile, or override conflicting findings unless the supplied evidence explicitly establishes why they differ.

Evaluation Process

For EACH UX dimension:

1. Read only the corresponding evaluation criteria and score guidance from the UX rubric.
2. Compare the collected evidence against every score level defined in the rubric.
3. Select the highest score whose criteria are substantially satisfied.
4. If the evidence falls between two score levels, assign the lower score unless the higher score is clearly and consistently supported.
5. Generate the dimension summary using only the supporting evidence.
6. List strengths that are directly supported and justified by the evidence and relevant to the assigned score
7. List issues that are directly supported and justified by the evidence and relevant to the assigned score
8. Do not use evidence from another dimension to justify the score.
9. Identify the relevant supporting evidence from the supplied visual observations, Lighthouse report, and Axe report.

Complete this process independently for all six UX dimensions before generating the final report.

Visual Evidence

- Use Luna's visual observations as the visual evidence source.
- Treat Luna's observations as factual visual evidence, not as UX judgements, scores, or recommendations.
- Treat observations under mobile, tablet, and desktop as viewport-specific evidence.
- Treat summary observations as cross-viewport visual evidence.
- Do not reinterpret a visual observation as a technical accessibility finding.
- Do not invent visual characteristics that are not present in the supplied visual observations.
- Do not assume that a visual characteristic satisfies an accessibility or usability requirement unless the UX rubric explicitly supports that conclusion.
- Do not treat Luna's observations as judgments about the quality of the interface.

Scoring

- Every assigned score must be directly supported by the identified evidence.
- Do not infer evidence that is not explicitly observable.
- Minor isolated issues should not significantly reduce an otherwise strong dimension.
- Multiple moderate issues may justify assigning a lower score, consistent with the rubric.
- Do not assign a lower score solely because evidence is unavailable.
- Do not assign a higher score solely because no issue was reported.

Recommendations

- Recommendations must directly address issues identified in the evaluation.
- Do not introduce new issues that were not previously identified.
- Prioritise recommendations according to their likely impact on user experience.
- Each recommendation should address a specific identified issue.
- Recommendations must be understandable to a non-technical reader where possible.
- Do not turn an audit recommendation to check or verify something into a claim that the issue definitely exists.
- Only recommend fixing an issue when the supplied evidence establishes that the issue is present.

Writing Style

- Use concise, factual, and objective language.
- Avoid unnecessary descriptive or promotional language.
- Avoid unsupported subjective opinions.
- Use clear, concise, user-friendly language that can be understood by a non-technical reader.
- Avoid unnecessary UX, design, accessibility, or technical terminology when a simpler alternative is available.
- When a technical or UX-specific term is necessary, explain it briefly in plain language.
- When reporting technical findings, explain what the finding means for the user rather than only repeating the technical rule name or audit terminology.
- Do not expose internal field names, variable names, or implementation terminology in user-facing summaries, strengths, issues, or recommendations.
- Preserve important objective information, such as severity, occurrence counts, and audit results, when reporting technical findings.

Overall Score

- Do not independently calculate the overall score.
- The application calculates the overall score from the six dimension scores after the AI evaluation is complete.

Output Requirements

- Return ONLY a valid JSON object.
- Do not include any content outside the JSON object.
- Do not include markdown formatting.
- Do not include code fences.
- Do not include introductory or concluding text.
- Do not omit required fields.
- Do not add additional fields.
- The JSON must conform exactly to the supplied schema.
"""
    evidence = f"""
Visual Observations from Luna
{visual_observations}

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


def call_terra(
    prompt,
):

    api_key = os.getenv("OPENROUTER_API_KEY")

    if api_key is None:
        raise ValueError("OPENROUTER_API_KEY was not found.")

    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
    )


    response = client.responses.create(
        model="openai/gpt-5.6-terra",
        input=[
            {
                "type": "message",
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": prompt,
                    },
                ],
            },
        ],
        reasoning={
          "effort": "high",
        },
        temperature=0,
    )

    Path("last_response.json").write_text(
    response.output_text,
    encoding="utf-8",
    )

    return response.output_text

def validate_response(response):
    return UXEvaluation.model_validate_json(response)


def generate_ux_report(
    visual_observations,
    lighthouse_report,
    axe_report,
):

    rubric = load_rubric()

    prompt = build_prompt(
        rubric,
        visual_observations,
        lighthouse_report,
        axe_report,
    )

    response = call_terra(prompt)

    report = validate_response(response)

    return report
