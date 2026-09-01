import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from evaluation_schema import UXEvaluation
from evidence_schema import EvaluationEvidence

load_dotenv()


def load_rubric():
    rubric_path = Path("docs/ux_rubric_spec.md")

    with open(rubric_path, "r", encoding="utf-8") as file:
        rubric = file.read()

    return rubric


def build_prompt(
    rubric,
    evidence,
):
    schema = json.dumps(
        UXEvaluation.model_json_schema(),
        indent=2,
    )

    evidence_json = json.dumps(
        evidence.model_dump(),
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
# 1. General Evaluation Principles

- Evaluate each UX dimension independently.
- Follow the dimension-specific criteria and scoring guidance defined in the supplied UX rubric.
- Do not allow evidence from one UX dimension to influence the score of another dimension unless the rubric explicitly defines the evidence as relevant.
- Base every conclusion only on the supplied evidence.
- Do not invent information that is not supported by the evidence.
- Do not assume interactions, animations, hover states, hidden functionality, or behaviour that cannot be directly observed.
- Do not classify terminology, labels, icons, or design choices as issues solely because they are unfamiliar.
- An issue must be supported by the relevant rubric criteria and supplied evidence.
- Absence of evidence is not evidence of an issue.
- If a characteristic cannot be evaluated from the supplied evidence, do not treat it as a strength or issue.

# 2. Page Context

Use the supplied page context to understand the apparent type and purpose
of the webpage before evaluating the UX dimensions.

Different webpage types may have different primary content, user goals,
and important actions. Do not assume that every webpage has a conventional
marketing or purchase CTA.

When relevant to a dimension, consider whether the visual prominence,
placement, and organization of important content and actions are
appropriate for the apparent purpose of the webpage.

For example, on a news or media webpage, prominent articles and news
content may represent the primary user focus. On an e-commerce webpage,
product discovery, product information, and purchase-related actions may
be more important.

Page context provides interpretive context only. It does not itself prove
that an interface has good or poor UX and must not independently justify
a score.

Evaluate each dimension using the observable evidence and the
dimension-specific scoring criteria.

# 3. Evidence Sources and Their Roles

Use the evidence source that is most directly relevant to the dimension being evaluated.

### Visual Observations

- Luna's visual observations are the evidence source for observable visual characteristics.
- Treat Luna's observations as factual observations, not UX judgements, scores, or recommendations.
- Treat mobile, tablet, and desktop observations as viewport-specific evidence.
- Treat summary observations as cross-viewport visual evidence.
- Do not reinterpret a visual observation as a technical accessibility or performance finding.
- Do not invent visual characteristics that are not present in the observations.

### Advertisements and Secondary Content

When evaluating Aesthetic Design, consider advertisements, promotional
blocks, banners, overlays, repeated calls to action, and other secondary
content when they are identified by the visual evidence.

The presence of an advertisement or secondary content does not
automatically justify a score deduction.

Evaluate its observable impact using:

- Size
- Repetition
- Visual prominence
- Placement
- Amount of visual space occupied
- Interruption of the primary content flow
- Competition with primary content
- Effect on the ability to identify and scan primary content

Repeated or visually prominent secondary content should receive greater
consideration than an isolated, low-impact element.

If the visual evidence identifies a large or repeated block but cannot
reliably determine that it is an advertisement, evaluate its observable
visual effect without assuming its purpose.

If an element appears to be an advertisement or promotional element but
cannot be reliably confirmed, do not identify it as an advertisement as a
fact. Instead, describe the element based on its observable appearance,
placement, size, repetition, or other visible characteristics, and clearly
state that its purpose cannot be determined from the available evidence.

An uncertain classification does not prevent the evaluator from
considering the element's observable visual impact. If the element creates
a noticeable UX weakness, it may be included as an issue and may contribute
to a score deduction even when its exact purpose is unknown.

For example, a large or repeated advertisement may:

- Reduce Visual Hierarchy by competing with a primary heading, CTA, or
  other important content.
- Reduce Aesthetic Design by increasing visual clutter, visual density, or
  interrupting the primary content flow.

Do not deduct points for the mere presence of an advertisement or
secondary element. A deduction must be supported by an observable
negative impact relevant to the specific dimension being evaluated.

Do not require positive identification of an advertisement before
considering its contribution to visual clutter.


### Screenshot Integrity

- Screenshot integrity observations describe the reliability of the captured screenshots, not the quality of the webpage itself.
- Use screenshot integrity observations only to determine whether visual evidence is reliable.
- A reported screenshot or capture artifact must not directly lower any UX dimension score.
- Do not classify a screenshot artifact as a UX strength or issue.
- If a screenshot is partially affected but still contains reliable visual evidence, use only the reliable portions when evaluating the UX.
- If a visual observation is supported by reliable evidence despite a screenshot artifact, it may still be used for scoring.
- If an apparent issue is visible only within a suspected screenshot artifact and is not independently supported by another evidence source, do not use it to lower the score.

If a screenshot appears incomplete, incorrectly rendered, or affected by a loading/capture artifact, 
treat the affected visual observation as uncertain. Do not deduct points solely because of an apparent 
issue that may be caused by the capture process.

When objective evidence is available, use it to support or challenge visual observations. 
Do not claim that an objective result confirms a specific visual issue unless the objective evidence actually identifies that element.

Clearly distinguish between confirmed issues, visual observations, and uncertain observations caused by possible capture artifacts.

### Lighthouse

- Lighthouse provides objective performance evidence and should primarily support the Performance dimension.
- Lighthouse may support another UX dimension only when the finding directly affects a characteristic explicitly defined in that dimension.
- Use the supplied mobile and desktop Lighthouse results.
- Lighthouse results do not directly measure tablet performance.
- Do not infer performance characteristics from screenshots.

### Axe

- Axe provides objective technical accessibility evidence and should support the Technical Accessibility component of Accessibility.
- Use Axe violations and passes when evaluating Technical Accessibility.
- A passing Axe result only supports the specific accessibility rule that passed.
- Do not infer that all accessibility requirements are satisfied because few violations are reported.
- Do not list Axe passes exhaustively. Mention only passes that provide meaningful evidence for the evaluated accessibility characteristics.
- Do not use Axe findings to infer visual accessibility characteristics that cannot be observed from the screenshots.


# 4. Objective Evidence Rules

- Treat Lighthouse and Axe findings as objective evidence.
- Do not alter, estimate, invent, contradict, or reinterpret objective values.
- Interpret objective values only according to the thresholds and scoring guidance defined in the supplied UX rubric.
- Preserve important objective information such as metric values, violation types, severity, and affected-element counts when relevant.
- The absence of a Lighthouse or Axe finding must not be treated as proof that an unrelated characteristic is satisfactory.
- When objective evidence conflicts with subjective visual impressions, prioritise the objective evidence.
- When Lighthouse and Axe report different findings for related accessibility checks, report both accurately rather than assuming one invalidates the other.


# 5. Evaluation Process

For EACH of the seven UX dimensions:

1. Read only the criteria and score guidance relevant to the current dimension.
2. Identify the supplied evidence relevant to that dimension.
3. Compare the relevant evidence against every score level defined in the rubric.
4. Assign a score only after identifying whether any criteria required for the higher score are absent or contradicted by the supplied evidence.
5. A dimension should not receive 5/5 merely because no major problem is present.
6. A score of 5 requires the positive criteria for 5/5 to be clearly and consistently supported by evidence.
7. If a meaningful limitation prevents the highest score from being fully satisfied, assign the next lower score when supported by the rubric.
8. Do not assume that a generally good interface qualifies for 5/5 when the rubric identifies specific characteristics required for that score.
9. If the evidence falls between two score levels, assign the lower score unless the higher score is clearly and consistently supported.
10. Identify directly supported strengths.
11. Identify directly supported issues.
12. Identify notable neutral considerations when appropriate.
13. Do not use evidence from another dimension to justify the score.
14. If a supplied observation directly corresponds to a criterion in the dimension's scoring guidance, explicitly consider it when assigning the score.
15. Generate the summary using only evidence supporting the assigned score.

Complete the evaluation independently for all seven dimensions before generating the overall report.


# 6. Scoring Rules

- Every assigned score must be directly supported by the identified evidence.
- Do not infer evidence that is not explicitly observable or supplied.
- Minor isolated issues should not significantly reduce an otherwise strong dimension.
- Multiple moderate issues may justify a lower score when supported by the rubric.
- Do not assign a lower score solely because evidence is unavailable.
- Do not assign a higher score solely because no issue was reported.
- Do not determine a score by simply counting strengths, issues, Axe violations, or Lighthouse metrics.


# 7. Accessibility Evaluation

Accessibility consists of two independent components:

1. Visual Accessibility
2. Technical Accessibility

The overall Accessibility score must reflect both components with equal importance.

### Visual Accessibility

- Evaluate Visual Accessibility using only the supplied visual observations.
- Do not use Axe findings to create visual accessibility claims.
- Evaluate the visual accessibility characteristics defined in the rubric.

### Technical Accessibility

- Evaluate Technical Accessibility using the supplied normalized Axe evidence.
- Determine the score from the type and severity of violations, affected elements, and relevant passing evidence.
- A low number of violations does not automatically indicate a high score.
- A high number of violations does not automatically determine a low score without considering their severity, scope, and relevance.
- Do not treat incomplete or inapplicable counts as factors that increase or decrease the score.

### Axe Summary Interpretation

The Axe summary contains four counts:

- violations
- passes
- incomplete
- inapplicable

- Use relevant Axe violations and relevant passing checks as supporting evidence when evaluating Technical Accessibility.
- Do not use the number or proportion of passes as a direct scoring mechanism.
- A passing check may support a specific accessibility characteristic, but does not establish that the page is broadly accessible.

Incomplete and inapplicable counts are provided for transparency and reporting context only.

- Incomplete checks indicate that Axe could not conclusively determine the result.
- Inapplicable checks indicate that the corresponding Axe rule did not apply to the evaluated page.
- Do not treat incomplete or inapplicable checks as confirmed accessibility failures or passes.
- Do not use incomplete or inapplicable counts to calculate or influence the Technical Accessibility score.


# 8. Performance Evaluation

- Evaluate Performance using the supplied Lighthouse results for mobile and desktop.
- Consider the Lighthouse Performance Score together with FCP, LCP, Speed Index, TBT, CLS, and relevant performance audit findings.
- Evaluate the overall pattern of the results rather than relying on a single metric.
- Use the mobile and desktop thresholds defined in the UX rubric.
- Do not treat every "Needs Improvement" metric as an issue automatically.
- Consider the magnitude, number, and likely user impact of performance weaknesses.
- Do not interpret Lighthouse results as direct measurements of tablet performance.
- Lighthouse metrics that are better than the "Poor" threshold do not automatically constitute strengths.
Only describe a Lighthouse metric as a strength when it falls within the "Good" threshold defined in the rubric.
- Lighthouse metrics that fall under the 'Poor' threshold is considered an issue. 

# 9. Objective Result Summaries

### Lighthouse Summary

The Performance dimension MUST include a lighthouse_summary containing the supplied Lighthouse metrics for both mobile and desktop.

Copy all Lighthouse metric values exactly as supplied.

Do not estimate, recalculate, round, reinterpret, or modify the values.

The Lighthouse evidence uses these units:

- FCP: seconds
- LCP: seconds
- Speed Index: seconds
- TBT: milliseconds
- CLS: unitless
- Performance score: 0-100

The lighthouse_summary is an objective display of the supplied evidence and must not independently determine or alter the assigned Performance score.

### Axe Summary

The Technical Accessibility component MUST include the supplied Axe summary containing:

- violations_count
- passes_count
- incomplete_count
- inapplicable_count

Copy these values exactly as supplied.

The counts must not be recalculated or used as a simple percentage to determine the Technical Accessibility score.


# 10. Considerations

Considerations are optional pieces of notable, neutral information that are relevant to the UX dimension and useful for the reader.

- A consideration must be directly supported by supplied evidence.
- A consideration must not be presented as a strength or issue.
- Add up to three considerations when necessary, relevant, worthy of noting for each dimension.
- Do not use considerations to introduce weaknesses that should instead be classified as issues.
- Do not use considerations to avoid classifying a clearly supported issue.
- Do not simply copy Luna's observations into the final report.
- Rewrite only observations that are meaningful and relevant to the dimension.
- A dimension may contain no considerations although it is preferred.
- Considerations should provide additional context rather than repeat the summary, strengths, or issues.
- If a supplied observation is relevant but is neither clearly a strength nor issue, consider including it as a consideration.
- Do not classify an observation as a consideration merely because its impact is uncertain. If the rubric establishes that it is a weakness, classify it as an issue.
- Do not manufacture considerations to reach the maximum of three.
- When screenshot integrity issues are reported, acknowledge them in the evaluation only when they materially affect the reliability or interpretation of the visual evidence.
- Do not treat screenshot integrity issues as UX weaknesses or use them to reduce a dimension score.

Example of characteristics worth mentioning as a consideration: 
1. "The hero artwork is visually prominent alongside the primary hero headline."
This may be included as a consideration when the visual prominence is notable but the supplied evidence does not establish that it negatively affects visual hierarchy.
2. "On tablet and mobile layouts, the primary navigation destinations are contained within a hamburger menu rather than displayed directly in the header. This reflects the responsive layout."


### Technical Accessibility Consideration

- The Technical Accessibility component MUST contain exactly one concise consideration.
- It must explain how the Axe results should be interpreted and must mention the violations, passes, incomplete, and inapplicable counts when available.
- It must make clear that incomplete and inapplicable checks were not treated as accessibility failures and do not determine the Technical Accessibility score.
- Do not repeat this Axe explanation in the parent Accessibility consideration.

Example:
"Axe identified [number] passed automated checks, [number] violation types affecting [number] elements, [number] incomplete checks, and [number] inapplicable checks. Incomplete and inapplicable checks were not treated as accessibility failures when determining the Technical Accessibility score."


# 11. Strengths and Issues

- Strengths must be directly supported by evidence and relevant to the assigned score.
- Issues must be directly supported by evidence and relevant to the assigned score.
- Do not manufacture strengths or issues to reach the maximum of two.
- Do not repeat the same strength or issue within a dimension.
- Do not repeat the same detailed Axe finding in both Accessibility and Technical Accessibility unless necessary.
- Do not introduce an issue solely because an automated tool reports a finding; consider its relevance, severity, scope, and impact according to the rubric.

# 12. Recommendations

- Recommendations must directly address issues identified in the evaluation.
- Do not introduce new issues through recommendations.
- Only recommend fixing an issue when the supplied evidence establishes that the issue is present.
- Prioritise recommendations according to likely user impact.
- Each recommendation should address a specific identified issue.
- Do not create separate recommendations for minor weaknesses when a higher-impact issue should take priority.
- Recommendations should be understandable to a non-technical reader.
- When an automated finding is technical, explain the recommended user-facing outcome where possible.


# 13. Writing Style

- Use concise, factual, and objective language.
- Avoid promotional or unnecessarily descriptive language.
- Avoid unsupported subjective opinions.
- Use clear language understandable to a non-technical reader.
- Avoid unnecessary UX, accessibility, or technical terminology.
- When a technical term is necessary, briefly explain it in plain language.
- When reporting technical findings, explain their user impact rather than only repeating the audit rule name.
- Do not expose internal field names, variable names, or implementation terminology in user-facing text.
- Preserve important objective information such as severity, occurrence counts, and audit results when relevant.


# 14. Overall Score

- Do not independently calculate the overall score.
- The application calculates the overall score from the seven dimension scores after the AI evaluation is complete.


# 15. Output Requirements

- Return ONLY a valid JSON object.
- Do not include markdown.
- Do not include code fences.
- Do not include introductory or concluding text.
- Do not omit required fields.
- Do not add additional fields.
- Do not rename fields.
- The JSON must conform exactly to the supplied schema.
- Each dimension may contain up to three considerations, except Technical Accessibility, which must contain exactly one.
- Each dimension may contain up to two strengths and two issues.
- Do not manufacture content to reach these limits.
"""
    evidence = f"""
# Evaluation Evidence

The following evidence was collected from the webpage and validated before evaluation.

{evidence_json}
"""

    prompt = f"""
# Role

{role}

# Task

{task}

# Evaluation Instructions

{instructions}

# Evidence

{evidence}

# UX Rubric

For each UX dimension, prioritize the UX characteristics listed in the
'evidence' list and use only evidence that is relevant to that dimension
when evaluating its score, strengths, and issues. Do not use evidence from
other categories unless it is explicitly relevant to the criteria of that
dimension.

Lighthouse performance findings should primarily be used for the Performance dimension.
They may support another UX dimension only when the finding directly affects a characteristic 
explicitly defined in that dimension and its effect is relevant to the observed interface.

{rubric}

# Expected Output

Return ONLY a valid JSON object.

The JSON MUST conform exactly to the following JSON Schema.

{schema}

Do not omit required fields.
Do not add extra fields.
Do not rename fields.
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

    output_path = Path("runtime/last_response.json")
    output_path.parent.mkdir(exist_ok=True)

    output_path.write_text(
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
    evidence = EvaluationEvidence(
        visual_observations=visual_observations,
        lighthouse=lighthouse_report,
        axe=axe_report,
    )

    rubric = load_rubric()

    prompt = build_prompt(
        rubric,
        evidence,
    )

    response = call_terra(prompt)

    report = validate_response(response)

    return report
