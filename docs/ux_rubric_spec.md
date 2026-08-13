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

The normalized Axe accessibility results should be used as the primary source of technical accessibility evidence.

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

### Score Guidance

**Score 5**
The interface consistently guides user attention through effective use of headings, spacing, typography, contrast, grouping, and emphasis. Primary actions are immediately identifiable.

**Score 4**
The interface demonstrates a strong visual hierarchy with only minor weaknesses that do not significantly affect usability.

**Score 3**
The interface demonstrates a basic visual hierarchy, but some important elements compete for attention or lack sufficient visual emphasis.

**Score 2**
The interface contains several weaknesses in visual hierarchy, making important content or actions more difficult to identify.

**Score 1**
The interface lacks a clear visual hierarchy, making it difficult for users to identify important content or primary actions.

---

## 2. Navigation

**Definition**

The interface provides clear and intuitive navigation.

### Evidence

- Obvious navigation
- Obvious buttons
- Visible menu
- Logical page structure

### Score Guidance

**Score 5**

Navigation is immediately visible, intuitive, and logically organized. Menus, buttons, and page structure are consistently easy to understand and use.

**Score 4**

Navigation is generally clear and easy to use. Minor improvements could be made to labels or organization, but navigation remains intuitive.

**Score 3**

Navigation is generally usable but may require additional effort to locate or understand. Some navigation elements or page organization are unclear.

**Score 2**

Navigation contains several confusing or poorly organized elements that reduce usability and make important actions harder to locate.

**Score 1**

Navigation is confusing, inconsistent, or difficult to locate, making it challenging for users to move through the interface.

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

### Score Guidance

**Score 5**

The interface is visually clean, balanced, and free from unnecessary clutter. Whitespace, spacing, and visual elements effectively support usability.

**Score 4**

The interface is visually appealing and generally well balanced. Minor clutter or spacing issues exist but do not significantly affect the overall design.

**Score 3**

The interface maintains an acceptable appearance but contains noticeable clutter, inconsistent spacing, or unnecessary visual elements.

**Score 2**

The interface contains excessive clutter, poor visual balance, or inconsistent spacing that noticeably distracts users.

**Score 1**

The interface is visually cluttered, unbalanced, or overloaded with unnecessary decorative elements that significantly hinder usability.

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

### Score Guidance

**Score 5**

Buttons, typography, colors, spacing, icons, and layouts are applied consistently throughout the interface and follow established design standards.

**Score 4**

Most interface elements are visually consistent. Minor inconsistencies exist but do not significantly affect usability.

**Score 3**

The interface is generally consistent, although several noticeable inconsistencies reduce the overall cohesiveness of the design.

**Score 2**

The interface contains frequent inconsistencies in styling, spacing, layouts, or interaction patterns that reduce usability.

**Score 1**

The interface lacks consistency across visual elements and interaction patterns, creating confusion and reducing usability.

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

### Score Guidance

**Score 5**

Content is communicated using clear, familiar, and understandable language. Labels, icons, terminology, and content organization are intuitive and require minimal interpretation.

**Score 4**

Information is generally clear and easy to understand. Minor wording or organizational improvements could improve overall clarity.

**Score 3**

Most content is understandable, although some terminology, labels, or organization may reduce clarity for certain users.

**Score 2**

Several labels, icons, or terminology are unclear or unfamiliar, making information more difficult to understand.

**Score 1**

Language, labels, icons, or content organization are confusing or unfamiliar, significantly reducing comprehension.

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

The Accessibility score should reflect both the visual accessibility observations from the screenshots and the technical accessibility findings reported by Axe. Neither source should be considered in isolation.

### Score Guidance

**Score 5 – Excellent**

The interface demonstrates strong visual accessibility and follows accessibility best practices. Visual accessibility issues are minimal, and Axe identifies few or no significant accessibility violations.

**Score 4 – Good**

The interface is generally accessible with only minor visual accessibility issues. Axe identifies a small number of technical accessibility violations that have limited impact on usability.

**Score 3 – Acceptable**

The interface meets basic accessibility expectations but contains noticeable visual accessibility issues and several technical accessibility violations identified by Axe.

**Score 2 – Poor**

The interface contains multiple visual accessibility issues that reduce usability. Axe identifies numerous technical accessibility violations that significantly affect accessibility.

**Score 1 – Very Poor**

The interface demonstrates substantial visual accessibility problems and fails to meet fundamental accessibility best practices. Axe identifies widespread or severe technical accessibility violations that significantly hinder accessibility.

---

## Evaluation Process

The AI evaluates the webpage using:

1. Captured screenshots (mobile, tablet, and desktop)
2. Lighthouse metrics
3. Axe accessibility results

Screenshots are used to evaluate the visual characteristics of the interface.

Axe provides objective accessibility findings that support the Accessibility dimension.

Lighthouse provides objective quality metrics that may support the AI's evaluation where relevant but should not contradict objective findings.

Each of the six dimensions is assigned a score from 1–5 using the evidence and score guidance defined in this specification.

The AI then provides:

- An overall summary of the interface
- Overall strengths
- Overall issues
- A score, summary, strengths, and issues for each evaluation dimension
- Actionable recommendations for improvement

The application calculates the overall score by computing the arithmetic mean of the six dimension scores returned by the AI.