# AI / UX Analyser Rubric Specification

## Rubric Overview

The following 7 dimensions were selected because they can be evaluated consistently using screenshots and objective automated analysis.

## Accessibility, one of the 7 dimensions, contains 2 subcomponents which are Visual Accessibility and Technical Accessibility.

## Page Context

The apparent type and purpose of the webpage may be provided as contextual evidence to support interpretation of the interface.

Different webpage types may have different primary content, user goals, and important actions. The evaluator must not assume that every webpage
has the same type of primary CTA or interaction.

When relevant to a dimension, page context may be used to determine which content or actions would reasonably be expected to receive greater visual
prominence.

Page context must not independently determine a score. Scores must remain based on observable evidence and the dimension-specific scoring criteria.

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

Visual observations must be treated as uncertain when screenshots appear incomplete, incorrectly rendered, or affected by loading/capture artifacts. A suspected capture artifact must not be treated as a confirmed webpage issue or independently lower a score.

Objective results must be used only to confirm issues they actually identify. An objective violation must not be attributed to a specific visual element unless the evidence identifies that element.

---

## Scoring Scale

The Scoring Scale should be treated as guidance as to what a score generally represents. While this should be used as guidance, all scores assigned to each dimension should be evaluated using the dimension-specific scoring.

Each dimension is scored on a **1–5 scale**, where higher scores indicate better adherence to UX principles.

### Score 5

A score of 5 requires positive evidence that the defining characteristics of the dimension are consistently demonstrated.

A score of 5 should not be assigned when a meaningful limitation is identified in any of the defining characteristics of the dimension, even if the remainder of the interface performs strongly.

The absence of significant problems alone is not sufficient for a score of 5.

If the evidence demonstrates a generally good interface but contains noticeable weaknesses or does not consistently satisfy the defining
characteristics of Score 5, the evaluator should consider Score 4 instead.

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

The criteria within each score level are not individual points and must not be counted or averaged. They describe the characteristics that collectively define the score level.

A dimension does not qualify for a higher score simply because most listed characteristics are satisfied. The evaluator must consider whether any meaningful weakness prevents the defining characteristics of that score from being consistently demonstrated.

Technical Accessibility scores must be determined from the normalized Axe evidence rather than from the number of violations alone. The evaluator must consider the type and relevance of each violation, its impact severity, the number of affected elements, and relevant passing checks. Incomplete checks must be considered as limitations of the available evidence rather than automatically treated as accessibility failures.

The presence of a violation does not automatically determine the score. The evaluator must consider the overall accessibility evidence available for the evaluated webpage. Similarly, a low number of violations does not automatically indicate a high score when the identified violations are severe or affect multiple elements.

The AI should provide a concise summary explaining the score, along with specific strengths and issues observed for each dimension.

---

## Positive Evidence Requirement

A high score must be supported by positive evidence that the characteristics associated with that score are demonstrated.

The evaluator must not assign a high score solely because significant problems are absent.

In particular, the absence of identified issues does not by itself justify a score of 5.

---

## Score Justification Requirement

Every assigned score must be supported by evidence that explains why the dimension received that score rather than a higher score.

If a dimension receives a score below 5, the evaluator must identify at least one specific weakness, limitation, or unmet criterion that explains why a score of 5 was not justified.

A score below 5 must not be assigned when both the issue and the supporting evidence are absent.

The evaluator must not lower a score without identifying the evidence or rubric criterion responsible for the deduction.

---

## Issue Impact

Scores must not be determined by simply counting the number of strengths, issues, violations, or observations.

The evaluator should consider:

1. Severity of the issue
2. Scope of the issue
3. Frequency or repetition
4. Importance of the affected interface element
5. Impact on usability
6. Whether the issue is isolated or systemic

A single severe issue may justify a lower score than several minor issues. Conversely, several minor isolated issues should not automatically result
in a low score.

---

## Advertisement

### Possible Advertisement

- Do not assume that every evaluated webpage contains advertisements.
- Only report advertisements when there is sufficient visual evidence to reasonably support that interpretation.
- If no advertisement or promotional content can be reliably identified, do not invent or infer one.

Look for visually prominent secondary content that may represent advertisements or promotional content:

- grey boxes
- advertisement placements
- promotional banners
- repeated promotional cards
- subscription or campaign banners unrelated to the website
- overlays or other promotional elements

Only identify an element as an advertisement when there is sufficient visual evidence to reasonably support that interpretation.

Visual indicators that may support an advertisement interpretation include:

- explicit advertising or sponsored labels
- recognizable advertisement formatting
- promotional messaging for an external product, service, or organization
- repeated rectangular advertising placements that are visually separated from the site's primary content
- content that is clearly distinct from the surrounding editorial or primary page content

Do not identify an element as an advertisement solely because it is:

- grey or blank
- rectangular
- visually separated from other content
- an image placeholder
- a loading skeleton
- a decorative block
- a generic content card

Advertisements, promotional content, and other secondary visual elements must be considered independently for each UX dimension where their
observable effects are relevant.

The same element may legitimately contribute to multiple dimension scores when it creates different UX problems in each dimension.

For example:

- Under Visual Hierarchy, a large advertisement may reduce the prominence of a primary heading, CTA, or other important interface element.
- Under Aesthetic Design, the same advertisement may increase visual clutter, visual density, or interrupt the primary content flow.

The evaluator must not automatically apply the same deduction to every dimension in which the element appears. A deduction must be supported by
an observable impact that is specifically relevant to that dimension.

An issue identified in one dimension may therefore also be considered in another dimension when the evidence demonstrates a distinct and relevant UX impact.

### Relevant Dimensions

Advertisements and secondary content may be relevant to any UX dimension where their observable impact directly matches that dimension's criteria.

The evaluator must determine relevance independently for each dimension rather than assuming that an advertisement requires deductions in specific
dimensions.

---

### Score Boundary Rule

When deciding between two adjacent scores, the evaluator must identify the specific characteristic that distinguishes the two score levels.

For example, when deciding between 4 and 5:

- If the defining characteristics of 5 are consistently demonstrated,
  assign 5.
- If the interface is generally strong but contains noticeable
  inconsistencies or lacks evidence for one or more defining
  characteristics of 5, assign 4.

When deciding between 3 and 4:

- Assign 4 only when the dimension remains generally strong despite
  minor limitations.
- Assign 3 when weaknesses are noticeable enough to reduce the overall
  quality of the dimension.

---

# Evaluation Dimensions

## 1. Visual Hierarchy

**Definition**

The interface guides users' attention effectively using clear hierarchy of contents.

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
- Competing visual elements that may draw attention away from more important content or actions

### Priority Elements

- Primary CTA
- Primary heading/hero message
- Primary navigation
- Important forms or conversion actions
- Primary content immediately relevant to the page purpose.

#### CTA Evaluation

When a primary CTA is present, evaluate its visual prominence separately from the prominence of secondary actions.

Consider:

- Whether the CTA can be identified without searching.
- Whether its visual treatment distinguishes it from surrounding content.
- Whether it is visually more prominent than secondary actions when it represents the primary action.
- Whether competing actions have similar or greater visual emphasis.
- Whether the CTA remains appropriately prominent across mobile, tablet, and desktop.

A CTA should be evaluated separately at each viewport. A CTA that is clear on one viewport does not establish that the CTA is clear on the other viewports.

If the primary CTA is difficult to identify or is substantially less prominent than surrounding secondary content on a tested viewport, this is a meaningful Visual Hierarchy weakness even when other hierarchy characteristics are strong.

### Cross-Viewport Hierarchy

The evaluator must compare the visual hierarchy of the mobile, tablet, and desktop screenshots.

Responsive rearrangement alone is not a hierarchy problem.

However, if an important element such as the primary CTA, primary heading, or primary content:

becomes substantially less prominent,
becomes difficult to identify,
disappears without an observable alternative,
or becomes visually subordinate to less important elements

### Score Guidance

#### Score 5

- A clear primary focal point is immediately identifiable.
- Headings are visually prominent and establish a clear content hierarchy.
- Important content and actions have clearly differentiated visual priority, with no meaningful competition between elements that should have different levels of importance.
- Typography consistently differentiates headings, subheadings, and body text.
- Spacing consistently separates unrelated content and groups related content.
- Visual contrast appropriately emphasizes important interface elements.
- Primary CTA is immediately distinguishable from secondary actions.
- Related interface elements are consistently grouped together.
- Interface elements are consistently aligned.
- No competing focal points are observable.
- No significant visual hierarchy issues are observable.
- Where cross-viewport hierarchy is relevant, important elements maintain
  appropriate visual priority across the tested viewports.

#### Score 4

- A primary focal point is identifiable.
- Headings establish a clear content hierarchy.
- Typography differentiates headings and body text with inconsistencies which are hard to notice and does not affect user experience.
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

- Navigation controls are identifiable across all viewport
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

Ease of identifying navigation should exist for all viewports.

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
- Content can be visually scanned and understood without unnecessary
  visual searching caused by poor organization or excessive visual density.
- Secondary content that may contribute to visual clutter

### Visual Clutter

For this dimension, visual clutter refers to a concentration or repetition of visual elements that competes for attention, interrupts the visual flow, or makes primary content harder to identify or scan.

The evaluator should consider whether the visual organization allows important content and key points to be identified and scanned without unnecessary visual searching.

The evaluated webpage should not contain texts which overpowers whitespaces.

The evaluated webpage should be convenient and does not force high cognitive load or mental effort to read.

Visual clutter may result from:

- advertisements
- promotional blocks
- banners
- repeated calls to action
- decorative elements
- excessive imagery
- dense groups of content
- repeated secondary components
- insufficient spacing between competing elements
- text density, poor formatting, and layout

The presence of multiple visual elements alone does not constitute clutter. The evaluator must determine whether those elements compete for attention or reduce the clarity of primary content.

### Score Guidance

#### Score 5

The interface is visually clean, balanced, and cohesive, with visual elements supporting the clarity of primary content.

- Visual density is well controlled throughout the interface.
- Spacing and whitespace effectively separate primary and secondary content.
- Decorative elements and imagery are visually integrated without competing with primary content.
- Secondary content such as advertisements, promotional blocks, banners, or other repeated elements does not create noticeable visual clutter.
- Primary content remains visually dominant throughout the interface.
- Visual balance and organization are maintained across the observed viewport sizes.
- No significant aesthetic design issues are observable.

#### Score 4

The interface is visually appealing and generally well balanced, with only minor visual clutter or inconsistencies that do not significantly interfere with primary content.

- Visual density is generally well controlled.
- Spacing and whitespace generally provide sufficient separation between content.
- Decorative elements and imagery generally support rather than compete with primary content.
- Minor visual clutter may be present, including limited advertisements, promotional blocks, banners, or other secondary content, but primary content remains visually dominant.
- Secondary content may occasionally interrupt the visual flow but does not substantially reduce clarity.
- Minor spacing, balance, or visual organization issues may be observable.
- The overall visual presentation remains clear and usable across the observed viewport sizes.

#### Score 3

The interface maintains an acceptable appearance but contains noticeable visual density, spacing, balance, or visual clutter issues that occasionally reduce the clarity of primary content.

- Visual density is noticeable in some areas of the interface.
- Spacing or whitespace is inconsistent and may not always separate related and unrelated content effectively.
- Decorative elements or imagery occasionally compete with primary content.
- Noticeable visual clutter may be present, such as repeated advertisements, promotional blocks, banners, or other secondary content that interrupt the primary content flow.
- Secondary content may compete with important content for visual attention in some areas.
- Visual balance or organization is reduced in some sections or viewport sizes.
- The issues reduce the overall visual quality but do not substantially hinder usability.

#### Score 2

The interface contains significant visual density, poor visual balance, or repeated secondary content that noticeably interferes with the clarity and organization of primary content.

- Visual density is excessive across multiple areas of the interface.
- Spacing and whitespace frequently provide insufficient separation between competing content.
- Decorative elements, imagery, advertisements, promotional blocks, banners, or other secondary content frequently compete with primary content.
- Repeated or visually prominent secondary elements noticeably interrupt the primary content flow.
- Important content may be harder to identify or scan because of competing visual elements.
- Visual clutter is observable across multiple sections or viewport sizes.
- Visual balance and organization are substantially reduced.
- The issues substantially reduce the overall quality of the visual experience.

#### Score 1

The interface is heavily cluttered or visually unbalanced, with widespread visual elements substantially interfering with the clarity and organization of primary content.

- Visual density is excessive throughout major areas of the interface.
- Spacing and whitespace provide little separation between competing visual elements.
- Advertisements, promotional blocks, banners, decorative elements, imagery, or other secondary content are widespread and substantially interrupt the primary content flow.
- Large or repeated secondary elements dominate or compete heavily with primary content.
- Primary content is difficult to identify, follow, or scan because of competing visual elements.
- Visual clutter is widespread across major sections or multiple viewport sizes.
- Visual balance and organization are severely disrupted.
- The overall visual presentation significantly hinders usability.

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

The overall Accessibility score is calculated from the Visual Accessibility and Technical Accessibility components with equal weighting.

The application calculates:

Overall Accessibility =
(Visual Accessibility Score + Technical Accessibility Score) / 2

The result is rounded to the nearest whole number using standard rounding, with .5 rounded upward.

Neither component should automatically determine the overall score by itself. A low score in one component should influence, but not completely replace, the contribution of the other component.

Examples:

Visual 5 + Technical 5 → Accessibility 5
Visual 5 + Technical 4 → Accessibility 5
Visual 5 + Technical 3 → Accessibility 4
Visual 4 + Technical 3 → Accessibility 4
Visual 3 + Technical 2 → Accessibility 3
Visual 2 + Technical 1 → Accessibility 2

### Visual Accessibility Evidence

Evaluate the following observable characteristics for this component:

- Text is visually legible against its background.
- Font sizes and styles are sufficiently readable throughout the interface.
- Colour contrast appears adequate and is visually distinguishable between foreground and background elements.
- Interactive elements are visually distinguishable.
- Icons are visually recognizable.
- Text displayed over images remains readable.

### Accessibility Scoring Boundary

Visual Accessibility and Technical Accessibility must be evaluated independently.

A weakness in one component must not automatically be treated as a weakness in the other component.

For Visual Accessibility, use only observable evidence from the supplied screenshots.

For Technical Accessibility, use only the supplied Axe evidence.

Do not infer technical accessibility from screenshots, and do not infer visual accessibility from Axe results.

When choosing between two adjacent scores, use the scope and severity of the demonstrated weakness to determine the appropriate boundary.

A localized issue should not automatically produce a score of 3 or below.

Conversely, a meaningful or repeated issue should prevent a score of 5 even when the remainder of the interface performs well.

If the evidence does not support a particular accessibility characteristic, do not invent a weakness or a strength for that characteristic.

### Technical Accessibility (Axe) Evidence

When evaluating Technical Accessibility, use Axe violations as the primary evidence for identifying accessibility problems. Consider the violation type, impact severity, affected elements, and scope.

Relevant passing checks may be used only as supporting evidence for the specific accessibility characteristic they test. They must not increase
the score simply because more checks passed.

Incomplete results indicate that Axe could not make a definitive determination. They must not be treated as confirmed violations or
passes and must not directly increase or decrease the score.

Two minor violations affecting one element each should not be treated as equivalent to two serious violations affecting multiple elements. The latter represents a greater accessibility concern even though both cases contain the same number of violation types.

A passing Axe check should only be considered evidence for the specific accessibility characteristic and rule that it evaluates. The absence of a violation should not be interpreted as proof that all aspects of those characteristics are accessible.

### Technical Accessibility Severity and Scope

Technical accessibility is evaluated independently from Visual
Accessibility using only the supplied normalized Axe evidence.

When evaluating Axe violations, prioritize evidence in the following order:

1. Violation severity
2. Functional or accessibility importance of the affected element
3. Number and proportion of affected elements
4. Whether the violation is isolated or repeated
5. The impact of the violation on users

Severity should carry greater weight than raw violation count.

Affected-element count should be used to determine the scope of a violation,
not as a simple numerical multiplier.

A minor violation affecting many low-impact elements should not automatically
outweigh a serious violation affecting a critical interaction.

Individual passing checks may only be referenced as supporting evidence
for the specific accessibility characteristic that the check evaluates.

The number of Axe checks performed, passes, incomplete checks, or
inapplicable checks must not influence the Technical Accessibility score
simply because of their quantity.

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

### Technical Accessibility Score Boundary

When choosing between two adjacent Technical Accessibility scores, the evaluator must identify the characteristic that distinguishes the two scores.

A higher score must not be assigned solely because the number of violations is low.

A lower score must not be assigned solely because a violation exists.

The evaluator must consider the severity, type, scope, and impact of the violation when determining the appropriate score.

If the assigned score is below 5, the evaluation must identify the specific accessibility weakness that prevents a score of 5.

### Score Guidance

##### Visual Accessibility

Visual accessibility is evaluated independently from Technical Accessibility using only the supplied visual observations provided.

#### Score 5

Visual accessibility is consistently strong across the observed viewports.

- Text remains visually legible against its background throughout the interface.
- Font sizes and typography remain visually readable throughout the interface.
- Foreground and background colours provide sufficient visible distinction for important content and controls.
- Interactive elements are visually distinguishable from surrounding content.
- Icons and visual symbols are sufficiently recognizable in context.
- Text displayed over images remains readable.
- No meaningful visual accessibility weakness is observable across the tested viewports.

A score of 5 must not be assigned solely because no obvious accessibility problem was noticed. The available screenshots must provide positive evidence that the defining visual accessibility characteristics are consistently demonstrated.

A meaningful visual accessibility weakness affecting an important control, important content, or a visually prominent area prevents a Score 5, even when the remainder of the interface is visually accessible.

#### Score 4

Visual accessibility is generally strong, but one or more limited and localized weaknesses are observable.

- Most text remains visually legible and readable.
- Most foreground and background combinations provide sufficient visible distinction.
- Interactive elements are generally visually distinguishable.
- Icons and symbols are generally recognizable.
- Text displayed over images remains readable in most cases.
- One or more localized visual accessibility weaknesses may be present
- The weaknessed are confied to a small number of elements or localized areas and do not substantially interfere with, or reduce the readability or identification of important content or controls.

A score of 4 should be assigned when the interface is generally strong and accessible visually but does not consistently demonstrate all of the interface-wide requirements of Score 5.

#### Score 3

Visual accessibility meets basic expectations but contains noticeable weaknesses that reduce readability or the identification of important interface elements.

- Most text remains readable, but some text has reduced legibility.
- One or more foreground/background combinations provide noticeably weaker visual contrast.
- Some interactive elements are not immediately distinguishable.
- Some icons or visual symbols require additional interpretation.
- Text displayed over images may have reduced readability in some areas.
- Multiple localized visual accessibility weaknesses may be present, or one noticeable weakness may affect an important interface element.
- The weakness is sufficiently noticeable that the interface does not consistently provide clear visual accessibility.

A score of 3 should be preferred over 4 when the weakness affects an important control, important content, or a visually prominent area.

#### Score 2

Visual accessibility has significant problems that affect multiple areas of the interface.

- Multiple areas contain text with reduced or poor legibility.
- Multiple foreground/background combinations provide insufficient visual distinction.
- Interactive elements are frequently difficult to distinguish from surrounding content.
- Icons or visual symbols are frequently unclear or difficult to recognize.
- Text displayed over images is frequently difficult to read.
- Visual accessibility weaknesses occur repeatedly across sections or viewport sizes.
- The problems substantially reduce the ability to perceive or understand important interface content or controls.

#### Score 1

Visual accessibility has severe or widespread problems that substantially hinder the perception or understanding of the interface.

- Text is frequently difficult or impossible to read.
- Poor foreground/background distinction is widespread.
- Interactive elements are frequently difficult or impossible to identify.
- Icons or visual symbols are frequently unclear or indistinguishable.
- Text displayed over images is frequently difficult or impossible to read.
- Severe visual accessibility problems affect major portions of the
  interface or multiple important interface elements.
- The available visual evidence indicates a widespread visual accessibility failure.

---

##### Technical Accessibility (Axe)

Technical accessibility is evaluated independently from Visual Accessibility using only the supplied normalized Axe evidence.

##### Score 5

Technical accessibility is consistently well implemented.

- No moderate, critical, or serious Axe violations are present.
- Any minor violations are isolated and have negligible accessibility impact.
- Minor findings affect only a very limited number of non-critical elements.
- No evidence indicates a repeated, broader, or systematic accessibility problem.

A score of 5 must not be assigned solely because the number of violations is low. The evaluator must consider the severity, type, affected elements, scope, and accessibility importance of the findings.

A score of 5 should represent an exceptionally strong technical accessibility implementation rather than merely a low number of violations.

Boundary rule:
A confirmed moderate, serious, or critcal violation prevents a score of 5.

#### Score 4

Technical accessibility is generally strong with limited technical accessibility weaknesses.

- No critical, serious or moderate Axe violations are present.
- One or more minor violations may be present.
- Minor violations have limited overall impact and remains isolated or localized.
- The findings do not indicate a broader technical accessibility problem.
- Important accessibility structures and functionality do not show meaningful weaknesses.

A score of 4 should be assigned when the overall implementation remains strongly accessible and existing minor impact remains limited.

Boundary rule:
A confirmed moderate, serious, or critcal violation prevents a score of 4.

A score of 4 should be assigned when confirmed minor accessibility issues exists, but the overall implementation remains strongly accessible.

#### Score 3

Technical accessibility has noticeable but moderate accessibility weaknesses.

- No critical violations are present.
- An isolated serious violation may be present when its scope and impact remains limited.
- One or more moderate violations may be present and may affect multiple elements, but their impact is limited or localised.
- Multiple minor violations may indicate a repeated implementation weakness when they affect related or important interface elements.
- The findings represent meaningful accessibility weaknesses but do not demonstrate severe, widespread, or systemic accessibility failure.
- Important interface elements or multiple areas may be affected, but the problems remain limited enough that fundamental accessibility remains generally available.

A score of 3 should be assigned when the available Axe evidence demonstrates meaningful accessibility weaknesses, including one or more moderate violations, but the problems remain limited in scope and do not indicate severe, widespread, or systemic accessibility failure.

Boundary rule:
A confirmed moderate violation that creates a meaningful accessibility weakness should generally prevent a score above 3.

#### Score 2

Technical accessibility has significant accessibility problems that substantially affect accessibility.

- Serious violations have repeated, broad, or significant impact, or
- A Critical violation is present with meaningful but limited scope, or
- Multiple moderate violations affect multiple important elements, components, or areas, or
- Multiple violations indicate a repeated or broader implementation problem.
- Important interface elements or multiple areas of the interface are affected.
- The findings indicate substantial accessibility weaknesses that extend beyond isolated or localized issues.
- The problems significantly reduce the accessibility of the evaluated interface but do not necessarily demonstrate the widespread or severe failure required for Score 1.

A score of 2 should be assigned when the available Axe evidence demonstrates significant accessibility problems affecting important or multiple areas of the interface, but the problems do not yet indicate severe or widespread technical accessibility failure.

Boundary rule:
When accessibility problems are repeated, broad, or significantly affect important elements or multiple areas, but the evidence does not demonstrate severe or systemic failure, assign a score of 2.

#### Score 1

Technical accessibility has severe or widespread accessibility failures that substantially hinder access to the interface.

- Multiple critical and/or serious violations have substantial or widespread impact, or
- Critical or serious violations affect important functionality across a substantial portion of the interface, or
- Severe accessibility problems are repeated across multiple important elements, components, or areas.
- The findings indicate widespread or systemic technical accessibility failure.
- Accessibility problems substantially affect the ability of users to access, understand, or interact with important functionality.

Boundary rule:
A score of 1 applies when the available evidence demonstrates severe, widespread, or systemic technical accessibility failure that substantially hinders access to important functionality.

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

---

### Performance Score Determination

The Performance score must be determined from the overall distribution of Lighthouse results across mobile and desktop.

The evaluator must consider:

1. Lighthouse Performance Score
2. Number of Poor metrics
3. Number of Needs Improvement metrics
4. Severity of Poor metrics
5. Whether weaknesses occur on mobile, desktop, or both
6. The overall consistency of results across viewports

The evaluator must not determine the score from the number of Poor metrics alone.

The Lighthouse Performance Score should be treated as an important overall indicator, while the individual metrics provide supporting evidence explaining the result.

Poor metrics should have greater influence than Needs Improvement metrics, but a single Poor metric should not automatically result in a low Performance score.

A single Needs Improvement metric must not automatically reduce the score to 3 or below.

---

### Viewport Weighting

Mobile and desktop results must both be considered.

A poor mobile result must not automatically determine the entire Performance score when desktop performance is strong.

Similarly, a strong desktop result must not compensate completely for severe mobile performance problems.

The evaluator must consider the severity and consistency of the problem across the tested configurations.

---

### Score Guidance

#### Score 5

Performance is consistently strong across mobile and desktop configurations.

- No Poor metrics are present across mobile and desktop results.
- Most individual metrics are within Good thresholds.
- Performance Scores are predominantly Good.
- Any Needs Improvement result is isolated and has limited impact.
- Performance does not show a meaningful loading, responsiveness, or layout-stability problem.

#### Score 4

Performance is generally strong with minor or limited weaknesses.

- No severe or widespread Poor performance.
- Performance is generally Good.
- One or several Needs Improvement metrics may be present.
- Any Poor result must be isolated and must not represent a major loading or responsiveness problem.

#### Score 3

Performance is acceptable but has noticeable weaknesses that reduce the quality of the experience.

- Lighthouse Performance Scores may range from Good to Poor.
- Multiple Needs Improvement metrics may be present.
- One or more meaningful Poor metric may be present.
- Weaknesses are noticeable but do not indicate severe or widespread performance failure.
- Performance problems may be concentrated on one viewport.

#### Score 2

Performance has significant weaknesses that substantially affect the evaluated experience.

- A substantially poor Performance Score may be accompanied by several Poor individual metrics.
- Significant problems may affect one viewport heavily or both viewports.
- Multiple Poor metrics are present, particularly across important loading or responsiveness metrics.
- Evidence indicates substantial loading, rendering, responsiveness, or stability problems.

#### Score 1

Performance has severe and widespread problems that substantially hinder the evaluated experience.

- Multiple important metrics are Poor across the evaluated viewports.
- Lighthouse Performance Scores indicate consistently poor performance.
- Severe problems affect loading, rendering, responsiveness, or layout stability.
- The evidence indicates a substantial performance failure rather than an isolated weakness.

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
