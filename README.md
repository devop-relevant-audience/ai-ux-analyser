# AI UX Page Analyser

A web-based AI-Powered tool for Webpage UX analysis and evaluation.

## Project Overview

### Background

The AI UX Page Analyser was developed to automate the process of analysing and evaluating a webpage's user experience (UX). The system collects a combination of objective evidence from a webpage and uses AI to analyse various UX aspects based on a defined UX evaluation rubric. 

### Purpose

The purpose of the AI UX Page Analyser is to streamline the process of evaluating the UX of a webpage by using an AI-based automation process and produce a structured UX evaluation report which provides the overall UX evaluation, the webpage's identified strengths, issues, considerations, and provide a list of prioritised recommendations for improvement.

### Scope

The system analyses **individual webpages** provided through the URL submission rather than entire websites.

It evaluates the webpage across seven UX dimensions:

- Visual Hierarchy
- Navigation
- Aesthetic Design
- Consistency and Standards
- Clarity and Familiarity
- Accessibility
- Performance

The analysis combines webpage screenshots across mobile, tablet, and desktop viewports, accessibility audit results from Axe, performance metrics from Lighthouse, and AI-generated evaluation. The results are presented through a web-based dashboard and detailed report, available as PDF for download.

## Features

### Webpage Analysis via URL

Receive up to 5 webpage URL(s) submissions and run batch analyses.

### Analysis progress

Display the progress of an analysis.

### Multi-Viewport Webpage Capture

Capture the webpage across mobile (`375px`)
tablet (`768px`), and desktop, (`1440px`) viewports.

### Accessibility Analysis

Identify and collect accessibility issues and checks in a webpage using Axe.

### Performance Analysis

Identify and collect performance metrics of a webpage using Lighthouse.

### AI-powered Visual Analysis

Generate visual analysis observation report from captured screenshots and provide it as objective evidence for the overall UX evaluation.

### AI-powered Evaluation

Evaluate the webpage against a defined UX rubric using combined objective evidence of visual observation report, Axe results, and Lighthouse metrics.

### Interactive result dashboard

Present evaluation results through an interactive dashboard with options to view the detailed final UX report.

Batch analysis results displays are also supported.

### Final Report

Generate a structured UX report providing:

- an overall UX score
- scores for each UX dimension
- identified strengths and issues
- prioritised recommendations
- visual observations of the webpage across the viewports
- report available for download as PDF

### History viewing and past runs comparison

Store past runs and allow past run comparisons.

## Technology Stack

### Backend

**Python** - Main programming language
**FastAPI** - Backend web framework
**Uvicorn** - ASGI application server
**SQLModel** - Database models and database interaction
**PostgreSQL** - Database
**python-dotenv** - Environment variable management

### Frontend
**HTML/CSS** - User interface presentation
**Jinja2** - Dynamic page rendering
**HTMX** - Interactive page updates and analysis progress

### Analysis & AI
- **Playwright** - Webpage capture
- **Axe** - Automated webpage accessibility testing/analysis
- **Lighthouse CLI** - Automate webpage performance testing/analysis 
- **OpenAI Models** - AI models used for visual analysis and  UX evaluation
- **Pydantic** - Pydantic schema used for structured output and schema validation

### Testing & Development
- **pytest** - Automated testing
- **Git/Github** - Version control and source code management

## Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd AI-Page-UX-Analyser
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv

For Windows PowerShell:
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright

```bash
playwright install
```

### 5. Configure environment variables

Create a `.env` file in the project root and add required API credentials and database configuration

OPENROUTER_API_KEY=your_openrouter_api_key

DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/ai_ux_page_analyser

Do not commit the `.env` file or expose API credentials in the source code.

### 6. Database

The application uses PostgreSQL to store analysis runs and batch information.

Install PostgreSQL and create a local PostgreSQL database.

```bash
createdb -U postgres ai_ux_page_analyser
```

Create a `.env` file in the project root and add credentials following the provided `.env.example` file content.

To access the database:

```bash
psql -U postgres -d ai_ux_page_analyser;
```

### 7. Run the Application

Start the FastAPI development server:

```bash
python -m uvicorn app:app --reload
```



## How to Run The AI UX Page Analyser

1. Open the application in a web browser
2. Enter the URL of the webpage to be analysed
3. Submit up to 5 URLs to start the analysis
4. Wait for analysis process to complete.
5. Review the generated evaluation results through the dashboard.
6. Access the full UX report to view the detailed evaluation report from the dashboard.
7. Download the report as PDF if required.

Optional:
1. Find `How it works` page from the navigation bar to view how webpages are evaluated.
2. Access `History` page to view past analysis runs and compare past runs to view score comparison tables for the same webpage.


## How the AI UX Page Analyser Works

The AI UX Page Analyser follows an automated analysis pipeline which includes combining webpage capture, automated Lighthouse and Axe audits, AI-based visual analysis, UX evaluation, and UX evaluation report generation.

### 1. URL Submission

The user pastes the URL of a webpage or in a batch up to 5 URLs, through the application interface. The submitted URL is passed to the backend to initiate the analysis process.

### 2. Webpage capture

Playwright automates a browser session and captures screenshots of the submitted webpage at three viewport sizes:

- Mobile — `375px`
- Tablet — `768px`
- Desktop — `1440px`

The capture process is optimised and includes additional handling such as page loading, scrolling, and cookie-banner handling to improve consistency of the captured screenshots and prevent obstructed screenshots.

Webpage screenshots are subsequently analysed and used as one of the objective evidence sources, used during the UX evaluation.

### 3. Automated webpage analysis

Lighthouse and Axe automatically run against the submitted webpage.

Lighthouse and Axe act as the objective evidence layer within the analysis pipeline to lower subjectivity in the evaluation. Their results are collected and provided to the AI during the UX evaluation process.

Lighthouse provides performance metrics and audit results, while Axe provides findings related to accessibility. 

### 4. AI Visual Analysis

The captured screenshots are supplied to an AI model for visual analysis. The AI then generates a visual observation report describing relevant characteristics of the webpage across the different viewport sizes.

Webpage contexts and elements related to UX evaluation are also collected and included in the visual observation report.

Subsequently, the visual observation report is provided to the AI Model responsible for the UX evaluation.

### 5. AI UX Evaluation

The collected Lighthouse and Axe audit results are combined with the visual observation report. The combined evidence is evaluated against the defined UX rubric.

The evaluation produces scores, strengths, issues, considerations, and prioritised recommendations.

### 6. Data Storage and Preliminary Saving

The application uses PostgreSQL to store analysis data throughout the evaluation process. After the initial webpage analysis involving the Lighthouse and Axe audits are completed, the collected results are saved before the AI evaluation stage begins. The preliminary save ensures that the collected data during the initial analysis is retained even if an error occurs during subsequent stages involving AI. 

### 7.Validation

AI-generated outputs are validated against the Pydantic schemas to ensure that the returned outputs follow the required structure and fields before being used to produce the final UX report.

### 8. Result and Report

The final UX report is generated and presented to users through the interactive dashboard. Users can view the overall UX score, individual dimension scores, findings, prioritised recommendations, and webpage preview section where the screenshots are available for viewing.

The full detailed UX report is also available through the Dashboard for users to view and download as PDF for offline use.

## Recognised Constraints

The current implementation has several recognised constraints that define the scope of the AI UX Page Analyser.

### Individual Webpage Analysis

The system evaluates individual webpages rather than complete websites and the system does not currently perform a complete site-wide UX evaluation across multiple pages.

### Non-interactive UX Evaluation

The system mainly focuses on observable characteristics of the webpage, particularly ones that can be identified from the captured screenshots. As a result, interaction-based UX characteristics which require direct user interaction may not be fully evaluated.

For example, a collapsed navigation menu that expands only when clicked, may not be fully assessed through static webpage screenshots alone.

### AI Output Variability

AI-generated evaluations may contain some variation between runs. Various components are implemented to improve consistency such as the defined UX rubric, consistent evaluation prompts, and schema enforcement for output validation. However, AI-generated results should still be considered an automated evaluation rather than an absolute assessment of UX quality.

### Webpage Accessibility and Capture Limitations

The accuracy of the overall evaluation and the visual observation report generation partly depends on the quality and completeness of the captured webpage screenshots. Dynamic webpage behaviour, content requiring direct interaction, animations, or externally controlled content may affect what can be captured and subsequently evaluated.

The application is designed to analyse webpages provided through a URL; however, not all webpages can be successfully captured. Some websites may restrict automated browser access or return access errors when Playwright attempts to load the webpage. For example, certain websites may return a 403 Forbidden response during the capture process. As a result, the application may not be able to analyse every webpage, and successful analysis depends on the webpage being accessible to the automated capture process.

### External Dependencies

The application depends on external technologies and services, including the AI API, Lighthouse, Axe, Playwright, and the PostgreSQL database. Changes, availability issues, or limitations within these external components may affect the analysis process.

### Security Considerations

The application accepts user-submitted URLs and automatically accesses them during the webpage analysis process. A production deployment would therefore require additional security measures, including stronger URL validation and protection against potentially unsafe or restricted destinations.

Sensitive credentials, including API and database credentials, should be stored through environment variables and should not be included directly in the source code or committed to version control.