# AI / UX Analyser Rubric Specification

## Overview

Some UX criteria require user interaction before they can be evaluated. These criteria are intentionally excluded from this project.

For example, error messages and recovery guidance require triggering user interactions and therefore cannot be evaluated reliably.

This web application captures webpage screenshots rather than interacting with the website. Therefore, the AI must evaluate the interface based solely on captured screenshots together with objective automated analysis from Axe and Lighthouse.

The following six dimensions were selected because they can be evaluated consistently using screenshots and objective automated analysis.

---

## Scoring Scale

Each dimension is scored on a **1–5 scale**, where higher scores indicate better adherence to UX principles.

### Score 5 – Excellent

All or nearly all characteristics for this dimension are consistently demonstrated. Any issues are minor and do not meaningfully impact the user experience.

### Score 4 – Good

Most characteristics are present and implemented well. Minor usability issues may exist but do not significantly affect the overall experience.

### Score 3 – Acceptable

The dimension meets basic usability expectations but contains noticeable weaknesses that reduce the overall quality of the experience.

### Score 2 – Poor

Several important characteristics are missing or poorly implemented, resulting in a noticeably weaker user experience.

### Score 1 – Very Poor

The dimension fails to meet fundamental usability expectations and significantly hinders usability.

---

## Scoring Methodology

Each UX dimension is evaluated independently using the criteria defined in this rubric.

When assigning a score, the evaluator should compare the webpage against the characteristics described for scores **1–5** and assign the **highest score whose criteria are substantially met**.

If a page falls between two score levels, the lower score should be selected unless the higher-level criteria are clearly and consistently satisfied.

Scores should reflect the overall quality of the dimension rather than isolated strengths or weaknesses. A single minor issue should not significantly reduce a score if the rest of the dimension is well executed, while multiple moderate issues may justify a lower score.

The AI should provide a concise summary explaining the score, along with specific strengths and issues observed for each dimension.

---

## Overall Score Calculation

The overall score is not independently evaluated by the AI. Instead, it is derived solely from the arithmetic mean of the six dimension scores.

Each dimension score is determined using the evidence defined in this specification. Depending on the dimension, this evidence may include:

- Visual observations from the captured mobile, tablet, and desktop screenshots.
- Objective measurements from Lighthouse.
- Objective accessibility findings from Axe.

Where objective measurements are available, they should be incorporated into the evaluation where relevant.

Axe findings should be used as the primary source of technical accessibility evidence.

Lighthouse metrics should be used to support evaluations involving performance and overall page quality but should not contradict objective findings.

The following six dimensions contribute equally to the overall score:

- Visual Hierarchy
- Navigation
- Aesthetic Design
- Consistency and Standards
- Clarity and Familiarity
- Accessibility

The overall score is calculated as the arithmetic mean of the six individual dimension scores.

Overall Score = (Visual Hierarchy + Navigation + Aesthetic Design + Consistency and Standards + Clarity and Familiarity + Accessibility) / 6

The overall score may include decimal values (e.g., **4.5**) because it is an average rather than an integer rating.

---

# Evaluation Dimensions

## 1. Visual Hierarchy

**Definition**

The interface guides users' attention effectively.

### Evidence

- Heading prominence
- Spacing
- Typography
- Emphasis
- Contrast
- Primary CTA (Call to Action)
- Grouping and alignment

---

## 2. Navigation

**Definition**

The interface provides clear and intuitive navigation.

### Evidence

- Obvious navigation
- Obvious buttons
- Visible menu
- Logical page structure

---

## 3. Aesthetic Design

**Definition**

The interface has visual cleanliness and contains no unnecessary elements that distract users.

### Evidence

- No unnecessary clutter
- Effective use of whitespace
- No excessive use of unnecessary decorations
- Visual balance
- Appropriate spacing

---

## 4. Consistency and Standards

**Definition**

The interface is visually consistent and follows established design standards.

### Evidence

- Button styles
- Icon styles
- Colors
- Typography
- Spacing
- Repeated styles
- Layout consistency

---

## 5. Clarity and Familiarity

**Definition**

The interface communicates information using clear, familiar, and easily understandable language and visual elements.

### Evidence

- Understandable language
- Recognizable and clear icons
- Familiar terminology
- Clearly labeled buttons
- Clear content organization
- No unnecessary jargon

---

## 6. Accessibility

**Definition**

The interface follows accessibility best practices for users with diverse abilities.

### Visual Accessibility Evidence

- Readable font size
- Adequate visual contrast
- Clearly identifiable interactive elements

### Technical Accessibility (Axe) Evidence

- Color contrast
- Alternative text (Alt text)
- Semantic structure
- ARIA (Accessible Rich Internet Applications)
- Heading structure and hierarchy

## Evaluation Process

The AI evaluates the webpage using:

1. Captured screenshots (mobile, tablet, and desktop)
2. Lighthouse metrics
3. Axe accessibility results

Screenshots are used to evaluate the visual characteristics of the interface.

Axe provides objective accessibility findings that support the Accessibility dimension.

Lighthouse provides objective quality metrics that may support the AI's evaluation where relevant but should not contradict objective findings.

Each of the six dimensions is assigned a score from 1–5 based on the evidence listed in this specification.

The AI then provides:

- An overall score
- An overall summary of the interface
- Overall strengths
- Overall issues
- Strengths and issues for each dimension
- Actionable recommendations for improvement