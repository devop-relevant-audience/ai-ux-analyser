# AI / UX Analyser Rubric Specification

## Rubric Overview

The following 7 dimensions were selected because they can be evaluated consistently using screenshots and objective automated analysis.

---

## Evidence

Some UX criteria require user interaction before they can be evaluated. These criteria are intentionally excluded from this project.

For example, error messages and recovery guidance require triggering user interactions and therefore cannot be evaluated reliably.

This web application captures webpage screenshots rather than interacting with the website. Therefore, the AI must evaluate the interface based solely on captured screenshots together with objective automated analysis from Axe and Lighthouse.

Each evidence source serves a different purpose during the evaluation:

1. Screenshots (mobile, tablet, and desktop) are used to evaluate observable visual characteristics of the user interface.
2. Lighthouse provides objective performance metrics that primarily support the Performance dimension. It may also support another UX dimension when a finding is directly relevant to a characteristic defined for that dimension.
3. Axe provides objective accessibility findings that support the Accessibility dimension.

The evidence listed for each UX dimension defines the observable UX characteristics that should be considered when evaluating that dimension. These characteristics guide the analysis towards evidence relevant to the specific UX dimension.

Objective findings from Lighthouse and Axe must always be treated as factual and must not be contradicted by observations derived from the screenshots.

Only characteristics that can be reliably determined from the supplied evidence should be considered. Characteristics that cannot be observed or reliably determined should not be treated as issues.

Absence of evidence is not evidence of an issue. If a characteristic cannot be evaluated from the supplied evidence, it should not be listed as a strength or issue.

---

## Scoring Scale

The Scoring Scale should be treated as guidance as to what a score generally represents. While this should be used as guidance, all scores assigned to each dimension should be evaluated using the dimension-specific scoring.

Each dimension is scored on a **1–5 scale**, where higher scores indicate better adherence to UX principles.

### Score 5

All or nearly all relevant characteristics are consistently demonstrated and implemented to a high standard. Any remaining issues are minor and do not meaningfully impact the overall user experience.

### Score 4

Most relevant characteristics are consistently demonstrated and implemented well. Minor issues or inconsistencies may be present, but they do not significantly affect the overall experience.

### Score 3

The dimension meets basic usability expectations, but noticeable weaknesses or inconsistencies reduce the overall quality of the experience.

### Score 2

Several important characteristics are missing or poorly implemented, resulting in a noticeably weaker user experience.

### Score 1

The dimension fails to meet fundamental usability expectations, with significant issues that substantially hinder usability.

---

## Scoring Methodology

Each UX dimension is evaluated independently using the criteria defined in this rubric.

The general scoring scale provides an overall interpretation of each score level. Each UX dimension contains dimension-specific score guidance that defines how these score levels apply to that particular dimension. When assigning a score, the evaluator must use the dimension-specific score guidance as the primary criteria and consider the general scoring scale as supporting guidance.

If a page falls between two score levels, the lower score should be selected unless the higher-level criteria are clearly and consistently satisfied.

Scores should reflect the overall quality of the dimension rather than isolated strengths or weaknesses.

Technical Accessibility scores must be determined from the normalized Axe evidence rather than from the number of violations alone. The evaluator must consider the type and relevance of each violation, its impact severity, the number of affected elements, and relevant passing checks. Incomplete checks must be considered as limitations of the available evidence rather than automatically treated as accessibility failures.

The presence of a violation does not automatically determine the score. The evaluator must consider the overall accessibility evidence available for the evaluated webpage. Similarly, a low number of violations does not automatically indicate a high score when the identified violations are severe or affect multiple elements.

The AI should provide a concise summary explaining the score, along with specific strengths and issues observed for each dimension.

---

# Evaluation Dimensions

## 1. Visual Hierarchy

**Definition**

The interface guides users' attention effectively.

### Evidence

Evaluate the following observable characteristics for this dimension:

- Heading hierarchy
- Visual emphasis
- Spacing
- Typography
- Visual contrast for emphasis
- Primary CTA (Call to Action) prominence
- Grouping of related content
- Alignment
- Relative size of interface elements
- Placement of important interface elements
- Visual density
- Visual hierarchy across viewport sizes

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

#### Score 4

- A primary focal point is identifiable.
- Headings establish a clear content hierarchy.
- Typography differentiates headings and body text with minor inconsistencies.
- Spacing generally groups related content together appropriately.
- Visual contrast emphasizes important interface elements.
- Primary CTA is easily identifiable.
- Related interface elements are grouped appropriately.
- Minor inconsistencies in alignment or emphasis are observable.
- Minor visual hierarchy issues are observable but do not significantly affect usability.

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

#### Score 2

- No obvious primary focal point is identifiable.
- Headings provide limited visual distinction between content levels.
- Typography provides limited differentiation between interface elements.
- Spacing frequently reduces the visual organization of content.
- Visual contrast does not consistently emphasize important interface elements.
- Primary CTA is difficult to distinguish from surrounding content.
- Related interface elements are inconsistently grouped.
- Alignment inconsistencies frequently reduce visual organization.
- Significant visual hierarchy issues substantially reduce usability.

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

The interface presents navigation controls and destinations in a clear, identifiable, and logically organized manner.

### Evidence

Evaluate the following observable characteristics for this dimension:

- Navigation controls are identifiable
- Navigation destinations are clearly labelled
- Navigation controls are visually distinguishable
- Menus are visually identifiable
- Navigation hierarchy
- Navigation structure is logically organized
- Hidden menu controls are visually identifiable as menus without requiring interaction
- Visible active/current navigation states are identifiable when present
- Navigation adapts appropriately across viewport sizes

### Score Guidance

#### Score 5

Navigation is immediately visible, identifiable, and clearly organized. Menus, buttons, and page structure are consistently easy to understand and use based on their observable presentation.

#### Score 4

Navigation is generally clear and easy to use. Minor improvements could be made to labels or organization, but navigation remains mostly visually understandable.

#### Score 3

Navigation is generally usable but may require additional effort to locate or understand. Some navigation elements or page organization are unclear.

#### Score 2

Navigation contains several confusing or poorly organized elements that reduce usability and make important actions harder to locate.

#### Score 1

Navigation is confusing, inconsistent, or difficult to locate, making it challenging for users to move through the interface.

---

## 3. Aesthetic Design

**Definition**

The interface presents a visually coherent and balanced design without visual elements that unnecessarily interfere with the clarity of primary content.

### Evidence

Evaluate the following observable characteristics for this dimension:

- Visual cleanliness
- Visual density
- Visual balance
- Visual coherence
- Appropriate spacing
- Effective use of whitespace
- Placement of decorative elements
- Placement and presentation of imagery

### Score Guidance

#### Score 5

The interface is visually clean and balanced. Decorative elements are visually integrated without obscuring or competing excessively with primary content. Whitespace, spacing, and visual elements effectively support usability.

#### Score 4

The interface is visually appealing and generally well balanced. Minor visual clutter may be present but does not interfere with primary content. Minor spacing issues may exist but do not significantly affect the overall design.

#### Score 3

The interface maintains an acceptable appearance but contains noticeable visual density, inconsistent spacing, or decorative elements that occasionally compete with primary content.

#### Score 2

The interface contains excessive visual density, poor visual balance, or decorative elements that noticeably distract from or compete with primary content.

#### Score 1

The interface is visually cluttered or unbalanced, overloaded with decorative or other visual elements that significantly interfere with the clarity of primary content and hinder usability.

---

## 4. Consistency and Standards

**Definition**

The interface is visually consistent and follows established design standards.

### Evidence

Evaluate the following observable characteristics for this dimension:

- Button styles
- Icon styles
- Colours
- Typography
- Spacing
- Repeated component styles
- Layout consistency
- Consistency across viewport sizes

### Score Guidance

#### Score 5

Buttons, typography, colours, spacing, icons, and layouts are applied consistently throughout the interface and follow established design standards.

#### Score 4

Most interface elements are visually consistent. Minor inconsistencies exist but do not significantly affect usability.

#### Score 3

The interface is generally consistent, although several noticeable inconsistencies reduce the overall cohesiveness of the design.

#### Score 2

The interface contains frequent inconsistencies in styling, spacing, layouts, or observable interface patterns that reduce usability.

#### Score 1

The interface lacks consistency across visual elements and observable interface patterns, creating confusion and reducing usability.

---

## 5. Clarity and Familiarity

**Definition**

The interface communicates information using clear, familiar, and easily understandable language and visual elements.

### Evidence

Evaluate the following observable characteristics for this dimension:

- Understandable language
- Recognisable and clear icons
- Terminology that is understandable in context
- Clearly labelled controls
- Clear content organization
- Clear and concise labels
- No unnecessary jargon

### Score Guidance

#### Score 5

Content is communicated using clear, familiar, and understandable language. Labels, icons, terminology, and content organization are intuitive and require minimal interpretation.

#### Score 4

Information is generally clear and easy to understand. Minor wording or organizational improvements could improve overall clarity.

#### Score 3

Most content is understandable, although some terminology, labels, or organization may reduce clarity for certain users.

#### Score 2

Several labels, icons, or terminology are unclear or unfamiliar, making information more difficult to understand.

#### Score 1

Language, labels, icons, or content organization are confusing or unfamiliar, significantly reducing comprehension.

---

## 6. Accessibility

**Definition**

Accessibility evaluates how effectively the interface can be perceived and understood by users with diverse abilities.

The evaluation consists of two independent components:

- **Visual Accessibility**, evaluated from the supplied screenshots.
- **Technical Accessibility**, evaluated using the normalized Axe accessibility report.

The overall Accessibility score should reflect both components. The Visual Accessibility and Technical Accessibility scores should be considered together with equal importance. The final Accessibility score must be a whole number from 1–5. Neither source should be considered in isolation. Objective Axe findings must not be contradicted by visual observations.

### Visual Accessibility Evidence

Evaluate the following observable characteristics for this component:

- Text is visually legible against its background.
- Font sizes and styles are sufficiently readable throughout the interface.
- Colour contrast appears adequate and is visually distinguishable between foreground and background elements.
- Interactive elements are visually distinguishable.
- Icons are visually recognizable.
- Text displayed over images remains readable.

### Technical Accessibility (Axe) Evidence

When evaluating Technical Accessibility, consider relevant Axe violations, passes, and incomplete results. For violations, consider the violation type, impact severity, and number of affected elements. Passing results may provide evidence that an automated accessibility check was successfully satisfied. Incomplete results indicate that Axe could not make a definitive determination and must not be treated as confirmed violations or passes.

Two minor violations affecting one element each should not be treated as equivalent to two serious violations affecting multiple elements. The latter represents a greater accessibility concern even though both cases contain the same number of violation types.

A passing Axe check should only be considered evidence for the specific accessibility characteristic and rule that it evaluates. The absence of a violation should not be interpreted as proof that all aspects of those characteristics are accessible.

Evaluate the following observable characteristics for this component:

- Colour contrast
- Alternative text
- Link names
- Buttons/accessibility names
- Form labels
- Semantic structure
- ARIA
- Heading structure and hierarchy
- Landmark structure
- Interactive control structure

### Score Guidance

#### Score 5

##### Visual Accessibility

- Text is visually legible against its background throughout the interface.
- Font sizes and styles are visually readable throughout the interface.
- Foreground and background colours provide sufficient contrast throughout the interface.
- Interactive elements are visually distinguishable throughout the interface.
- Icons are visually recognizable throughout the interface.
- Text displayed over images remains visually readable.
- No significant visual accessibility issues are observable.

##### Technical Accessibility (Axe)

Technical accessibility is consistently implemented across the evaluated checks. No serious or critical Axe violations are present, and * relevant accessibility checks are passed.

#### Score 4

##### Visual Accessibility

- Text is visually legible against its background throughout most of the interface.
- Most font sizes are visually readable.
- Foreground and background colours provide sufficient contrast for most interface elements.
- Interactive elements are visually distinguishable.
- Icons are visually recognizable.
- Text displayed over images remains visually readable.
- Minor visual accessibility issues are observable but do not reduce usability.

##### Technical Accessibility (Axe)

Technical accessibility is generally well implemented. Minor or limited accessibility issues may be present, but no serious or critical violations are present. Relevant Axe checks are predominantly passed.

#### Score 3

##### Visual Accessibility

- Most text is visually legible against its background.
- Some font sizes reduce readability.
- Some foreground and background colours provide insufficient contrast.
- Some interactive elements are not immediately visually distinguishable.
- Some icons require additional interpretation.
- Some text displayed over images reduces readability.
- Multiple visual accessibility issues are observable and reduce overall usability.

##### Technical Accessibility (Axe)

Basic technical accessibility expectations are met, but noticeable accessibility weaknesses are present. One or more meaningful violations may affect the evaluated interface, including serious violations with limited scope or impact.

#### Score 2

##### Visual Accessibility

- Multiple areas contain text that is difficult to read against its background.
- Font sizes frequently reduce readability.
- Multiple foreground and background colour combinations provide insufficient contrast.
- Interactive elements are not consistently visually distinguishable.
- Icons are frequently unclear or difficult to recognize.
- Text displayed over images frequently reduces readability.
- Significant visual accessibility issues substantially reduce usability.

##### Technical Accessibility (Axe)

Several important technical accessibility problems are present. Serious or critical violations, repeated failures, or violations affecting multiple elements significantly reduce accessibility.

#### Score 1

##### Visual Accessibility

- Text is often visually illegible against its background.
- Font sizes consistently reduce readability.
- Foreground and background colour combinations frequently provide insufficient contrast.
- Interactive elements are difficult to visually identify.
- Icons are frequently unclear or difficult to recognize.
- Text displayed over images is frequently difficult to read.
- Widespread visual accessibility issues significantly hinder usability.

##### Technical Accessibility (Axe)

Technical accessibility is substantially inadequate. Multiple severe or widespread accessibility violations affect fundamental aspects of the interface, with significant barriers for users of assistive technologies.

---

## 7. Performance

### Definition

The Performance dimension evaluates objective page performance measurements reported by Lighthouse, including content rendering, loading progression, main-thread blocking, and layout stability.

### Evidence

Performance scoring should consider the Lighthouse Performance score and the reported metric classifications for FCP, LCP, Speed Index, TBT, and CLS. The evaluator should consider the overall pattern of these results rather than relying on a single metric.

Evaluate the supplied Lighthouse performance evidence separately for the tested mobile and desktop configurations. Performance findings should not be interpreted as direct measurements of tablet performance.

Evaluate the following characteristics using the supplied Lighthouse performance evidence:

- **Lighthouse Performance score**
  - Good: 90–100
  - Needs Improvement: 50–89
  - Poor: 0–49

- **First Contentful Paint (FCP)**
  - Mobile: Good <1.8s; Needs Improvement 1.8–3s; Poor >3s
  - Desktop: Good 0–0.9s; Needs Improvement 0.9–1.6s; Poor >1.6s

- **Largest Contentful Paint (LCP)**
  - Mobile: Good <2.5s; Needs Improvement 2.5–4s; Poor >4s
  - Desktop: Good 0–1.2s; Needs Improvement 1.2–2.4s; Poor >2.4s

- **Speed Index**
  - Mobile: Good 0–3.4s; Needs Improvement 3.4–5.8s; Poor >5.8s
  - Desktop: Good 0–1.3s; Needs Improvement 1.3–2.3s; Poor >2.3s

- **Total Blocking Time (TBT)**
  - Mobile: Good <200ms; Needs Improvement 200–600ms; Poor >600ms
  - Desktop: Good <150ms; Needs Improvement 150–350ms; Poor >350ms

- **Cumulative Layout Shift (CLS)**
  - Good: ≤0.1
  - Values above 0.1 indicate increasing layout instability.
  - Higher values represent greater concern.

### Score Guidance

#### Score 5

Lighthouse reports strong performance across the evaluated metrics, with no significant performance issues identified by the supplied Lighthouse evidence.

#### Score 4

Lighthouse reports generally good performance, with minor weaknesses in one or more evaluated metrics that are unlikely to substantially affect the user experience.

#### Score 3

Lighthouse reports noticeable performance weaknesses in one or more evaluated metrics that may affect the user experience.

#### Score 2

Lighthouse reports significant performance weaknesses across one or more evaluated metrics that are likely to negatively affect the user experience.

#### Score 1

Lighthouse reports severe performance weaknesses that substantially affect loading, responsiveness, or visual stability according to the evaluated metrics.

---

## Evaluation Process

The AI evaluates each UX dimension independently using the following process:

1. Review the evaluation criteria and score guidance for the current UX dimension.

2. Identify only the supplied evidence that is relevant to the current UX dimension and its defined evidence characteristics.

3. Compare the identified evidence against each score level defined in this specification.

4. Assign the highest score whose criteria are substantially satisfied by the available evidence.

5. If the available evidence falls between two score levels, assign the lower score unless the higher-level criteria are clearly justified by the evidence.

6. Generate the dimension summary, strengths, and issues using only the evidence that supports the assigned score.

This process is repeated independently for all 7 UX dimensions.

After all dimensions have been evaluated, the AI generates:

- An overall summary of the interface.
- Overall strengths.
- Overall issues.
- A score, summary, strengths, and issues for each UX dimension.
- Actionable recommendations that directly address the identified issues.

The application calculates the overall UX score by computing the arithmetic mean of the 7 dimension scores returned by the AI.

---

## Output Requirements

For each UX dimension, the AI must provide:

- One concise summary explaining the overall evaluation and assigned score.
- Do not repeat the strengths and issues verbatim in the summary.
- Up to two strengths supported by the evaluation evidence.
- Up to two issues supported by the evaluation evidence.
- One score from 1–5.
- Do not invent, repeat, or manufacture strengths or issues to reach the maximum.

Strengths and issues must be directly supported by evidence used during the evaluation.

Issues must not be introduced solely to justify a recommendation.

Recommendations must directly address the identified issues.

The AI must not invent, repeat, or manufacture strengths or issues to reach the maximum number. If fewer than two relevant strengths or issues are supported by the available evidence, provide only those that are supported.

---

## Overall Score Calculation

The overall score is not independently evaluated by the AI. **Do not calculate the overall score.**

Instead, the application calculates the overall score by computing the arithmetic mean of the 7 UX dimension scores returned by the AI.

The following 7 dimensions contribute equally to the overall score:

- Visual Hierarchy
- Navigation
- Aesthetic Design
- Consistency and Standards
- Clarity and Familiarity
- Accessibility
- Performance

The overall score is calculated using the following equation:

**Overall Score = (Visual Hierarchy Score + Navigation Score + Aesthetic Design Score + Consistency and Standards Score + Clarity and Familiarity Score + Accessibility Score + Performance Score) / 7**

The overall score may include decimal values (e.g., **4.5**) because it represents the arithmetic mean of the 7 dimension scores.