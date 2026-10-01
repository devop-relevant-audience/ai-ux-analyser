import os
import traceback
import base64
from pathlib import Path

from fastapi import BackgroundTasks, FastAPI, Form, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from playwright.sync_api import sync_playwright
from sqlmodel import Session

from axe import run_axe
from capture import capture_screenshots
from database import create_db_and_tables, engine
from evaluation_ai import generate_ux_report
from lighthouse import run_lighthouse
from models import Run
from normalize import build_report
from visual_ai import extract_visual_evidence

app = FastAPI()

create_db_and_tables()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.mount(
    "/runtime",
    StaticFiles(directory="runtime"),
    name="runtime",
)

def build_final_report(
    lighthouse_report,
    axe_report,
    ai_report,
    visual_evidence,
    overall_score,
):
    report = build_report(
        lighthouse_report,
        axe_report,
        ai_report,
    )

    report["visual_evidence"] = visual_evidence
    report["ai"]["overall_score"] = overall_score

    return report

def run_analysis(run_id: int, url: str):
    try:

        with Session(engine) as session:
            run = session.get(Run, run_id)
            run.status = "capturing"
            session.add(run)
            session.commit()

        screenshots = capture_screenshots(url)

        with Session(engine) as session:
            run = session.get(Run, run_id)
            run.screenshots = screenshots
            run.status = "accessibility"
            session.add(run)
            session.commit()

        axe_report = run_axe(url)

        with Session(engine) as session:
            run = session.get(Run, run_id)
            run.status = "performance"
            session.add(run)
            session.commit()

        lighthouse_report = run_lighthouse(url)

        preliminary_report = build_report(
            lighthouse_report,
            axe_report,
            None,
        )

        with Session(engine) as session:
            run = session.get(Run, run_id)
            run.report = preliminary_report
            run.status = "visual"
            session.add(run)
            session.commit()

        visual_evidence = extract_visual_evidence(screenshots)

        with Session(engine) as session:
            run = session.get(Run, run_id)
            run.status = "ai"
            session.add(run)
            session.commit()

        ai_report = generate_ux_report(
            visual_evidence.visual_observations,
            lighthouse_report,
            axe_report,
        )

        priority_order = {
            "High": 0,
            "Medium": 1,
            "Low": 2,
        }

        ai_report.overall.recommendations.sort(
            key=lambda recommendation: priority_order[recommendation.priority]
        )

        UXdimension_scores = [
            ai_report.dimensions.visual_hierarchy.score,
            ai_report.dimensions.navigation.score,
            ai_report.dimensions.aesthetic_design.score,
            ai_report.dimensions.consistency_and_standards.score,
            ai_report.dimensions.clarity_and_familiarity.score,
            ai_report.dimensions.accessibility.score,
            ai_report.dimensions.performance.score,
        ]

        overall_score = sum(UXdimension_scores) / len(UXdimension_scores)

        report = build_final_report(
            lighthouse_report,
            axe_report,
            ai_report.model_dump(),
            visual_evidence.model_dump(),
            overall_score,
        )

        with Session(engine) as session:
            run = session.get(Run, run_id)
            run.status = "report"
            run.report = report
            session.add(run)
            session.commit()

        with Session(engine) as session:
            run = session.get(Run, run_id)
            run.status = "complete"
            session.add(run)
            session.commit()

    except Exception:
        error_text = traceback.format_exc()

        Path("runtime").mkdir(exist_ok=True)

        Path("runtime/analysis_error.txt").write_text(
            error_text,
            encoding="utf-8",
        )

        with Session(engine) as session:
            run = session.get(Run, run_id)
            run.status = "error"
            session.add(run)
            session.commit()

        raise

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"request": request},
    )

@app.get("/how-it-works", response_class=HTMLResponse)
def how_it_works(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="howitworks.html",
        context={"request": request},
    )

@app.get("/analyse", response_class=HTMLResponse)
def analyse_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="analyse.html",
        context={"request": request},
    )


@app.post("/analyse", response_class=HTMLResponse)
def analyse(
    request: Request,
    background_tasks: BackgroundTasks,
    url: str = Form(...),
):
    with Session(engine) as session:
        run = Run(
            url=url,
            status="queued",
        )  
        session.add(run)
        session.commit()
        session.refresh(run)

    background_tasks.add_task(
        run_analysis,
        run.id,
        url,
    )

    return templates.TemplateResponse(
        request=request,
        name="analyse_progress.html",
        context={
            "request": request,
            "run_id": run.id,
            "url": url,
        },
    )

    
@app.get("/analyse/{run_id}/status")
def analysis_status(run_id: int, request: Request):
    with Session(engine) as session:
        run = session.get(Run, run_id)

        if run is None:
            return HTMLResponse("Run not found", status_code=404)

        if run.status == "complete":
            return Response(
                headers={
                    "HX-Redirect": f"/run/{run.id}"
                }
            )

    return templates.TemplateResponse(
        request=request,
        name="analyse_progress.html",
        context={
            "request": request,
            "run_id": run.id,
            "url": run.url,
            "status": run.status,
        },
    )

@app.get("/run/{run_id}", response_class=HTMLResponse)
def get_run(run_id: int, request: Request):
    with Session(engine) as session:
        run = session.get(Run, run_id)

        if run is None:
            return HTMLResponse("Run not found", status_code=404)

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "request": request,
            "url": run.url,
            "screenshots": run.screenshots,
            "report": run.report,
            "run_id": run.id,
        },
    )


@app.get("/report/{run_id}", response_class=HTMLResponse)
def get_report(run_id: int, request: Request):
    with Session(engine) as session:
        run = session.get(Run, run_id)

        if run is None:
            return HTMLResponse("Run not found", status_code=404)

    return templates.TemplateResponse(
        request=request,
        name="report.html",
        context={
            "request": request,
            "url": run.url,
            "screenshots": run.screenshots,
            "report": run.report,
            "run_id": run.id,
        },
    )

@app.get("/report/{run_id}/pdf")
def get_report_pdf(run_id: int, request: Request):
    with Session(engine) as session:
        run = session.get(Run, run_id)

        if run is None:
            return HTMLResponse("Run not found", status_code=404)

        screenshots = run.screenshots

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(
            f"http://127.0.0.1:8000/report/{run_id}"
        )

        page.wait_for_load_state("networkidle")

        screenshot_urls = {}

        for viewport, path in screenshots.items():
            image_data = Path(path).read_bytes()
            encoded_image = base64.b64encode(image_data).decode("utf-8")
            screenshot_urls[viewport] = (
                f"data:image/png;base64,{encoded_image}"
            )

        page.evaluate(
        """
        (screenshots) => {
            const appendix = document.createElement("section");

            appendix.className = "pdf-screenshot-appendix";

                    appendix.innerHTML = `
            <div class="pdf-appendix-header">
                <p>APPENDIX</p>
                <h2>Screenshots</h2>
            </div>

            <div class="pdf-screenshot-grid">

                <div class="pdf-screenshot-item">
                    <h3>A. Mobile</h3>
                    <div class="pdf-screenshot-image">
                        <img src="${screenshots.mobile}" alt="Mobile screenshot">
                    </div>
                </div>

                <div class="pdf-screenshot-item">
                    <h3>B. Tablet</h3>
                    <div class="pdf-screenshot-image">
                        <img src="${screenshots.tablet}" alt="Tablet screenshot">
                    </div>
                </div>

            </div>

            <div class="pdf-screenshot-item pdf-desktop-page">
                <h3>C. Desktop</h3>
                <div class="pdf-screenshot-image">
                    <img src="${screenshots.desktop}" alt="Desktop screenshot">
                </div>
            </div>
        `;

        const style = document.createElement("style");

        style.textContent = `

            .report-recommendation,
            .report-dimension-card,
            .report-dimension-box,
            .preview-card,
            .axe-summary-box,
            .axe-violation,
            .axe-node,
            .lighthouse-box {
                break-inside: avoid;
                page-break-inside: avoid;
            }

            /* Keep headings with the content that follows them */
            .report-dimension-title,
            .report-dimension-score,
            .report-preview h2,
            .report-recommendations h2,
            .report-overall h2,
            .axe-details-box h3,
            .lighthouse-box h3 {
                break-after: avoid;
                page-break-after: avoid;
            }

                hr {
                    break-after: avoid;
                    page-break-after: avoid;
                }

            .pdf-screenshot-appendix {
                break-before: page;
                page-break-before: always;
            }

            .pdf-appendix-header {
                margin-bottom: 10mm;
            }

            .pdf-appendix-header p {
                margin: 0 0 5px;
                color: #66735f;
                font-size: 10px;
                font-weight: 600;
                letter-spacing: 0.12em;
                text-transform: uppercase;
            }

            .pdf-appendix-header h2 {
                margin: 0;
                font-family: Georgia, "Times New Roman", serif;
                font-size: 26px;
                font-weight: 400;
                color: #252522;
            }

            .pdf-screenshot-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10mm;
                align-items: start;
                break-inside: avoid;
                page-break-inside: avoid;
            }

            .pdf-screenshot-item {
                min-width: 0;
            }

            .pdf-screenshot-item h3 {
                margin: 0 0 6mm;
                color: #66735f;
                font-size: 10px;
                font-weight: 600;
                letter-spacing: 0.12em;
                text-transform: uppercase;
            }

            .pdf-screenshot-image {
                display: flex;
                justify-content: center;
                align-items: flex-start;
                background: #f5f2eb;
                border: 1px solid #d5d0c6;
            }

            .pdf-screenshot-image img {
                display: block;
                width: auto;
                max-width: 100%;
                max-height: 220mm;
                height: auto;
                object-fit: contain;
            }

            .pdf-desktop-page {
                break-before: page;
                page-break-before: always;
                margin-top: 10mm;
            }

            .pdf-desktop-page .pdf-screenshot-image {
                width: 100%;
            }

            .pdf-desktop-page .pdf-screenshot-image img {
                max-width: 100%;
                max-height: 235mm;
            }
        `;

            document.head.appendChild(style);
            document.body.appendChild(appendix);
        }
        """,
        screenshot_urls,
    )

        pdf = page.pdf(
            format="A4",
            print_background=True,
            margin={
                "top": "20mm",
                "right": "15mm",
                "bottom": "20mm",
                "left": "15mm",
            },
        )

        browser.close()

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="ux-report-{run_id}.pdf"'
        },
    )

@app.get("/screenshots/{run_id}/{viewport}", response_class=HTMLResponse)
def get_screenshot(
    run_id: int, 
    viewport: str, 
    request: Request
):
    with Session(engine) as session:
        run = session.get(Run, run_id)

        if run is None:
            return HTMLResponse("Run not found", status_code=404)

    if viewport not in ["mobile", "tablet", "desktop"]:
        return HTMLResponse("Invalid viewport", status_code=400)

    screenshot = run.screenshots[viewport]

    return templates.TemplateResponse(
        request=request,
        name="screenshot_viewer.html",
        context={
            "request": request,
            "run_id": run.id,
            "url": run.url,
            "viewport": viewport,
            "screenshot": screenshot,
        },
    )