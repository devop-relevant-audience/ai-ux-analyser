# AI / UX Analyser Rubric Specification

## Overview

Some UX criteria require user interaction before they can be evaluated. These criteria are intentionally excluded from this project.

For example, error messages and recovery guidance require triggering user interactions and therefore cannot be evaluated reliably.

This web application captures webpage screenshots rather than interacting with the website. Therefore, the AI must evaluate the interface based solely on captured screenshots together with objective automated analysis from Axe and Lighthouse.

The following six dimensions were selected because they can be evaluated consistently using screenshots and objective automated analysis.

---

## Scoring Scale

Each dimension is scored on a **1–5 scale**, where higher scores indicate better adherence to UX principles.

### Score 5

All or nearly all characteristics for this dimension are consistently demonstrated. Any issues are minor and do not meaningfully impact the user experience.

### Score 4

Most characteristics are present and implemented well. Minor usability issues may exist but do not significantly affect the overall experience.

### Score 3

The dimension meets basic usability expectations but contains noticeable weaknesses that reduce the overall quality of the experience.

### Score 2

Several important characteristics are missing or poorly implemented, resulting in a noticeably weaker user experience.

### Score 1

The dimension fails to meet fundamental usability expectations and significantly hinders usability.

---

## Scoring Methodology

Each UX dimension is evaluated independently using the criteria defined in this rubric.

When assigning a score, the evaluator should compare the webpage against the characteristics described for scores **1–5** and assign the **highest score whose criteria are substantially met**.

If a page falls between two score levels, the lower score should be selected unless the higher-level criteria are clearly and consistently satisfied.

Scores should reflect the overall quality of the dimension rather than isolated strengths or weaknesses. A single minor issue should not significantly reduce a score if the rest of the dimension is well executed, while multiple moderate issues may justify a lower score.

The AI should provide a concise summary explaining the score, along with specific strengths and issues observed for each dimension.

---

## Output Requirements

For each UX dimension, the AI must provide:

- One concise summary explaining the overall evaluation and assigned score.
- Do not repeat the strengths and issues verbatim in the summary.
- Two strengths supported by the evaluation evidence.
- Two issues supported by the evaluation evidence.
- One score from 1–5.

Strengths and issues must be directly supported by evidence used during the evaluation.

Issues must not be introduced solely to justify a recommendation.

Recommendations must directly address the identified issues.

---

## Overall Score Calculation

The overall score is not independently evaluated by the AI.

Instead, the application calculates the overall score by computing the arithmetic mean of the six UX dimension scores returned by the AI.

The following six dimensions contribute equally to the overall score:

- Visual Hierarchy
- Navigation
- Aesthetic Design
- Consistency and Standards
- Clarity and Familiarity
- Accessibility

The overall score is calculated using the following equation:

Overall Score = (Visual Hierarchy + Navigation + Aesthetic Design + Consistency and Standards + Clarity and Familiarity + Accessibility) / 6

The overall score may include decimal values (e.g., **4.5**) because it represents the arithmetic mean of the six dimension scores.

---

# Evaluation Dimensions

## 1. Visual Hierarchy

**Definition**

The interface guides users' attention effectively.

### Evidence

Evaluate the following observable characteristics:

- Heading Hierarchy
- Visual emphasis
- Spacing
- Typography
- Visual Contrast
- Primary CTA (Call to Action) Prominence
- Grouping of related content
- Alignment consistency
- Relative size of interface elements
- Placement of important interface elements

### Score Guidance

#### Score 5

- A clear primary focal point is immediately identifiable.
- Headings are visually prominent and establish a clear content hierarchy.
- Typography consistently differentiates headings, subheadings, and body text.
- Spacing consistently separates unrelated content and groups related content.
- Visual contrast appropriately emphasizes important interface elements.
- Primary CTA is immediately distinguishable from secondary actions.
- Related interface elements are consistently grouped together.
- Interface elements are consistently aligned.
- No competing focal points are observable.
- No significant visual hierarchy issues are observable.

---

#### Score 4

- A primary focal point is identifiable.
- Headings establish a clear content hierarchy.
- Typography differentiates headings and body text with minor inconsistencies.
- Spacing generally groups related content appropriately.
- Visual contrast emphasizes important interface elements.
- Primary CTA is easily identifiable.
- Related interface elements are grouped appropriately.
- Minor inconsistencies in alignment or emphasis are observable.
- Minor visual hierarchy issues are observable but do not significantly affect usability.

---

#### Score 3

- A primary focal point is present but competes with other interface elements.
- Heading hierarchy contains noticeable inconsistencies.
- Typography inconsistently differentiates content hierarchy.
- Spacing inconsistently groups related content.
- Visual contrast does not consistently emphasize important interface elements.
- Primary CTA requires additional visual searching.
- Some unrelated content appears visually grouped.
- Alignment inconsistencies are observable.
- Multiple visual hierarchy issues reduce the clarity of the interface.

---

#### Score 2

- No obvious primary focal point is identifiable.
- Headings provide limited visual distinction between content levels.
- Typography provides limited differentiation between interface elements.
- Spacing frequently reduces the visual organization of content.
- Visual contrast does not consistently emphasize important interface elements.
- Primary CTA is difficult to distinguish from surrounding content.
- Related interface elements are inconsistently grouped.
- Alignment inconsistencies frequently reduce visual organisation.
- Significant visual hierarchy issues substantially reduce usability.

---

#### Score 1

- No clear visual hierarchy is observable.
- Headings do not establish a recognizable content hierarchy.
- Typography does not differentiate interface elements.
- Spacing does not visually organize content.
- Important interface elements receive little or no visual emphasis.
- Primary CTA is difficult or impossible to identify.
- Related interface elements appear visually disconnected.
- Alignment inconsistencies are widespread.
- Widespread visual hierarchy issues significantly hinder usability.
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

Accessibility evaluates how effectively the interface can be perceived and understood by users with diverse abilities.

The evaluation consists of two independent components:

- Visual Accessibility, evaluated from the supplied screenshots.
- Technical Accessibility, evaluated using the normalized Axe accessibility report.

Both components must be considered together when determining the final Accessibility score. Neither component should be evaluated in isolation. Objective Axe findings must not be contradicted by visual observations.

### Visual Accessibility Evidence

Identify whether the following characteristics are present:

• Text is visually legible against its background.
• Font sizes are sufficiently readable throughout the interface.
• Colour contrast appears adequate between foreground and background elements.
• Interactive elements are visually distinguishable.
• Icons are visually recognizable.
• Text displayed over images remains visually readable.

### Technical Accessibility (Axe) Evidence

- Color contrast
- Alternative text (Alt text)
- Semantic structure
- ARIA (Accessible Rich Internet Applications)
- Heading structure and hierarchy

The Accessibility score should reflect both the visual accessibility observations from the screenshots and the technical accessibility findings reported by Axe. Neither source should be considered in isolation.

### Score Guidance

### Score 5

### Visual Accessibility

- Text is visually legible against its background throughout the interface.
- Font sizes are visually readable throughout the interface.
- Foreground and background colours provide sufficient contrast throughout the interface.
- Interactive elements are visually distinguishable throughout the interface.
- Icons are visually recognizable throughout the interface.
- Text displayed over images remains visually readable.
- No significant visual accessibility issues are observable.

### Technical Accessibility (Axe)

- Axe violations_count = 0
- No serious or critical accessibility violations are reported.
- No widespread moderate violations are reported.
- Semantic HTML and accessibility practices are correctly implemented where evaluated by Axe.

### Score 4

#### Visual Accessibility

- Text is visually legible against its background throughout most of the interface.
- Most font sizes are visually readable.
- Foreground and background colours provide sufficient contrast for most interface elements.
- Interactive elements are visually distinguishable.
- Icons are visually recognizable.
- Text displayed over images remains visually readable.
- Minor visual accessibility issues are observable but do not reduce usability.

#### Technical Accessibility (Axe)

- Axe violations_count = 1–2
- No serious or critical accessibility violations are reported.
- Reported violations are minor or moderate.
- Minor or moderate violations are isolated to a small number of affected elements.
- Semantic HTML and accessibility practices are correctly implemented for most evaluated elements.

---

### Score 3

#### Visual Accessibility

- Most text is visually legible against its background.
- Some font sizes reduce readability.
- Some foreground and background colours provide insufficient contrast.
- Some interactive elements are not immediately visually distinguishable.
- Some icons require additional interpretation.
- Some text displayed over images reduces readability.
- Multiple visual accessibility issues are observable and reduce overall usability.

#### Technical Accessibility (Axe)

- Axe violations_count = 3–4
- No critical accessibility violations are reported.
- 1-2 serious accessibility violations may be present but are not widespread across the interface.
- Semantic HTML and accessibility practices are only partially implemented where evaluated by Axe.

---

### Score 2

#### Visual Accessibility

- Multiple areas contain text that is difficult to read against its background.
- Font sizes frequently reduce readability.
- Multiple foreground and background colour combinations provide insufficient contrast.
- Interactive elements are not consistently visually distinguishable.
- Icons are frequently unclear or difficult to recognize.
- Text displayed over images frequently reduces readability.
- Significant visual accessibility issues substantially reduce usability.

#### Technical Accessibility (Axe)

- Axe violations_count = 5-6
- 3-4 serious accessibility violations are present and affect many elements.
- Accessibility violations affect a significant proportion of evaluated elements.
- Semantic HTML and accessibility practices are inconsistently implemented where evaluated by Axe.

---

### Score 1

#### Visual Accessibility

- Text is often visually illegible against its background.
- Font sizes consistently reduce readability.
- Foreground and background colour combinations frequently provide insufficient contrast.
- Interactive elements are difficult to visually identify.
- Icons are frequently unclear or difficult to recognize.
- Text displayed over images is frequently difficult to read.
- Widespread visual accessibility issues significantly hinder usability.

#### Technical Accessibility (Axe)

- Axe violations_count >6, OR critical accessibility violations are reported, OR serious accessibility violations are widespread across the interface.
- Multiple levels of accessibility violations significantly affect the interface.
- Semantic HTML and accessibility best practices are largely absent or incorrectly implemented where evaluated by Axe.

---

## Evaluation Process

The AI evaluates the webpage using the following evidence sources:

1. Captured webpage screenshots (mobile, tablet, and desktop)
2. Lighthouse metrics
3. Axe accessibility results

Each evidence source serves a different purpose during the evaluation.

- **Screenshots** are used to evaluate observable visual characteristics of the user interface.
- **Lighthouse** provides objective website quality metrics that support relevant UX dimensions.
- **Axe** provides objective accessibility findings that support the Accessibility dimension.

Objective findings from Lighthouse and Axe must always be treated as factual and must not be contradicted by observations derived from the screenshots.

The AI evaluates each UX dimension independently using the following process:

1. Review the evaluation criteria and score guidance for the current UX dimension.
2. Identify all relevant evidence from the supplied screenshots, Lighthouse metrics, and Axe accessibility results.
3. Compare the identified evidence against each score level defined in this specification.
4. Assign the highest score whose criteria are substantially satisfied by the available evidence.
5. If the available evidence falls between two score levels, assign the lower score unless the higher score is clearly justified by the evidence.
6. Generate the dimension summary, strengths, and issues using only the evidence that supports the assigned score.

This process is repeated independently for all six UX dimensions.

After all dimensions have been evaluated, the AI generates:

- An overall summary of the interface.
- Overall strengths.
- Overall issues.
- A score, summary, strengths, and issues for each UX dimension.
- Actionable recommendations that directly address the identified issues.

The application calculates the overall UX score by computing the arithmetic mean of the six dimension scores returned by the AI.