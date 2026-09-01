import base64
import os
import json
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

# UX Rubric

{rubric}

# Instructions

- Examine the mobile, tablet, and desktop screenshots.
- Base every observation only on what is visibly observable.
- Do not infer functionality that cannot be observed.
- Do not assume how an interaction behaves.
- Do not assign scores.
- Do not describe an observation as good, bad, strong, weak, effective, or ineffective.
- Do not make recommendations.
- The presence of an advertisement does not automatically constitute visual clutter or an aesthetic issue. Only report the observable characteristics of its size, repetition, placement, visual prominence, and visible relationship to the primary content flow. The Evaluation AI determines whether those characteristics have a negative impact on any applicable UX dimension.
- Distinguish observations between viewport sizes when the visual presentation differs.
- Do not invent information that is not visible in the screenshots.
- Do not repeat the same observation across multiple dimensions unless the observation is directly relevant to each dimension.
- Use clear, factual, user-readable language.
- If a characteristic is not visible or cannot be reliably determined from the screenshots, do not report it.
- Check each screenshot for signs of incomplete loading, corrupted rendering, missing images, missing styles, broken layout, or other possible capture artifacts.
- If a screenshot appears to contain a rendering or capture artifact, explicitly report it as an observation and identify the affected viewport.
- If a screenshot is partially affected but still contains reliable visual evidence, use the reliable portions of the screenshot while clearly noting that the screenshot contains a possible capture artifact.
- When the cause of a visual anomaly cannot be determined from the screenshot alone, describe the anomaly without claiming that it is caused by the webpage.
- Do not use a suspected capture artifact as evidence for a negative UX evaluation unless the underlying webpage issue is independently supported by reliable evidence.
- Do not assume that a visual anomaly caused by a possible capture artifact is a problem with the actual webpage.

## Visual observations

# Page Context

Identify the apparent type and purpose of the webpage based only on
observable visual evidence.

Report:

- The apparent webpage type.
- The apparent primary purpose of the webpage.
- The primary content or user goal that appears to be emphasized.
- Prominent user actions or calls-to-action that are visually observable.

Describe the page context objectively.

The webpage type may include categories such as:

- News or media
- E-commerce or retail
- Corporate or business
- Service or agency
- Blog or editorial
- Documentation or knowledge base
- Portfolio
- Social or community
- Informational or institutional
- Search or discovery
- Other, when appropriate

Do not assume a webpage type solely from its visual appearance when the
evidence is insufficient.

Do not infer functionality that cannot be observed.

Do not determine which action is objectively the "correct" primary CTA.
Instead, report the actions and primary content that appear visually
prominent and describe their visible relationship to the page content.

Do not evaluate the quality or usability of the webpage when identifying its type.

When the page purpose or type cannot be reliably determined, use a
conservative description based on observable content rather than
inventing a classification.

Return the identified context using the 'page_context' object with all required fields:

- `page_type`
- `primary_purpose`
- `primary_content`
- `prominent_actions`

If no prominent user action can be reliably identified,
`prominent_actions` may be an empty list.

For example:

{{
  "page_context": {{
    "page_type": "News and editorial webpage",
    "primary_purpose": "Present current news and information to users",
    "primary_content": "News headlines, featured stories, and article previews",
    "prominent_actions": [
      "Open news articles",
      "Navigate between news categories"
    ]
  }},
  "visual_observations": {{
    "...": "..."
  }},
  "screenshot_integrity": {{
    "...": "..."
  }}
}}

Page context is provided to the Evaluation AI as contextual evidence.
It must not contain UX scores, judgments, recommendations, or conclusions.

# Possible Advertisements

- Identify visually prominent elements that interrupt or compete with the primary content flow, including advertisements, promotional blocks, banners, overlays, repeated calls to action, or other secondary content.
- When large or repeated visually distinct blocks appear to be advertisements or promotional content, report their presence and placement as observable visual evidence.
- Do not assume that a visually distinct block is an advertisement solely from its appearance. If its purpose cannot be reliably determined, describe the block factually without identifying it as an advertisement.
- Pay particular attention to large, repeated, or visually prominent advertisement blocks, including advertisements that appear as grey or otherwise minimally styled rectangular areas.
- Report advertisements or other secondary content when their placement, size, repetition, or visual prominence is clearly observable.
- Do not determine whether the presence of an advertisement or secondary
content warrants a score deduction. Only report the observable evidence.
The Evaluation AI determines its relevance and impact on any UX dimension
for which the evidence is applicable.

# Do not identify an element as an advertisement solely because it is:

grey or blank
rectangular
visually separated from other content
an image placeholder
a loading skeleton
a decorative block
a generic content card

# If an element appears visually similar to an advertisement but its purpose cannot be reliably determined, describe what is observable without calling it an advertisement.

For example:

"A large grey rectangular block appears between content sections."

rather than:

"A large advertisement appears between content sections."

If the element can reasonably be identified as an advertisement, report both:
its presence and placement.

The presence of an advertisement does not automatically constitute visual clutter or an aesthetic issue. Evaluate whether its size, repetition, placement, or visual prominence 
actually affects the clarity or flow of the primary content.


# CTA

- Identify prominent calls-to-action (CTAs) when they are visually observable.
- Describe the CTA's visible label, placement, prominence, and relationship to the content it is associated with.
- Distinguish primary CTAs from secondary actions when their visual hierarchy makes this distinction observable.
- If the intended primary action is not visually clear from the screenshot, explicitly describe the competing or ambiguous actions that make the hierarchy unclear.
- Do not assume that a button is a primary CTA solely because it is styled as a button.
- Do not determine whether a CTA is effective; only describe the visual evidence that affects its clarity and prominence.

Observable CTA characteristics may include:
- clear or ambiguous button labels
- number of competing prominent actions
- visual prominence relative to surrounding content
- placement within the relevant content section
- whether the primary action is visually distinguishable from secondary actions
- whether the action is visually associated with the content it controls or follows

# Visual clutter

# Visual clutter

- Identify visually observable characteristics that may indicate visual clutter.
- Visual clutter may include excessive competing visual elements, dense grouping of unrelated content, excessive text density, insufficient spacing between distinct elements, repeated competing calls-to-action, overlapping visual emphasis, or crowded layouts that make the visual hierarchy difficult to distinguish.
- Consider whether a large amount of text, multiple text-heavy content blocks, or densely grouped headlines and descriptions make the page difficult to visually scan or process at once.
- Do not classify a page as visually cluttered solely because it contains a large amount of text, many elements, or multiple content items.
- Consider the apparent type and purpose of the webpage when describing text density and content volume. Content-heavy pages, such as news, editorial, documentation, or information-focused webpages, may intentionally present multiple text items or dense information.
- Even when dense information is appropriate for the apparent page type, report observable evidence when the visual arrangement creates competing emphasis, makes content difficult to distinguish, reduces scanability, or makes the amount of information presented at once appear difficult to process.
- Do not classify intentional dense layouts, grids, or repeated content as clutter unless the visual arrangement creates competing or unclear visual hierarchy.
- Describe the specific observable characteristics that contribute to the apparent clutter or density rather than simply labeling the page "cluttered" or "overwhelming."
# Consistency across viewport sizes

- For Consistency and Standards, explicitly compare the mobile, tablet, and desktop screenshots.
- Identify whether recurring interface elements maintain consistent visual treatment across viewport sizes.
- Compare recurring typography, buttons, CTAs, navigation elements, cards, spacing patterns, icon treatment, colors, and component styling across viewports.
- Identify meaningful inconsistencies in the visual treatment of the same or equivalent interface elements between viewport sizes.
- Do not treat responsive layout changes as inconsistencies when the same design system or visual treatment is preserved.
- Distinguish intentional responsive changes from inconsistent styling.

For screenshot integrity:

- Provide up to 2 observation for mobile.
- Provide up to 2 observation for tablet.
- Provide up to 2 observation for desktop.
- Provide up to 2 cross-viewport observations in summary.
- Only report a screenshot integrity issue when there is visible evidence of incomplete loading, corrupted rendering, missing assets, broken layout, or another possible capture artifact.
- Do not report an issue simply because the design differs between viewport sizes.
- Do not assume that a screenshot artifact is caused by the webpage.
- Describe the observable artifact factually and identify the affected viewport.
- If no screenshot integrity issue is observable, return an empty list.
- Screenshot integrity observations must only describe the reliability of the screenshot itself and must not be treated as UX problems.
- A screenshot integrity observation must not be placed under any UX dimension such as Visual Hierarchy, Aesthetic Design, or Accessibility.
- If no screenshot integrity issue is observable, return an empty list.
- Do not repeat the same screenshot integrity observation across multiple viewports unless the artifact is independently visible in each viewport.

The "screenshot_integrity" field is mandatory and must always be included.

If no screenshot integrity issues are observed, return empty arrays for
mobile, tablet, desktop, and summary.

Never omit the screenshot_integrity field.


# Expected Output

The response MUST use exactly the following JSON structure:

{{
  "page_context": {{
    "page_type": "",
    "primary_purpose": "",
    "primary_content": "",
    "prominent_actions": []
  }},

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
    }},

    "screenshot_integrity": {{
    "mobile": [],
    "tablet": [],
    "desktop": [],
    "summary": []
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
  }},

     "screenshot_integrity": {{
    "mobile": [],
    "tablet": [],
    "desktop": [],
    "summary": []
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

The page_context field is mandatory and must always be included in the response.

If the webpage type, purpose, primary content, or prominent actions cannot be
reliably determined, provide a conservative description based only on the
visible evidence rather than omitting the page_context object.

Do not omit required fields within page_context. When a specific value cannot
be reliably determined, use a conservative observable description. If no
prominent user actions can be identified, return an empty list for
prominent_actions.

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

    output_path = Path("runtime/luna_observations.json")
    output_path.parent.mkdir(exist_ok=True)

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
