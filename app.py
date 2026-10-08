import base64
import traceback
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse

from fastapi import BackgroundTasks, FastAPI, Form, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from playwright.sync_api import sync_playwright
from sqlmodel import Session, select

from axe import run_axe
from capture import capture_screenshots
from database import create_db_and_tables, engine
from evaluation_ai import generate_ux_report
from lighthouse import run_lighthouse
from models import Batch, Run
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


def cleanup_old_screenshots():
    screenshots_dir = Path("runtime/screenshots")

    if not screenshots_dir.exists():
        return

    cutoff_time = datetime.now() - timedelta(days=7)

    for screenshot in screenshots_dir.iterdir():
        if screenshot.is_file():
            modified_time = datetime.fromtimestamp(screenshot.stat().st_mtime)

            if modified_time < cutoff_time:
                screenshot.unlink()


cleanup_old_screenshots()


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

        screenshots, page_title, page_name = capture_screenshots(url, run_id)

        with Session(engine) as session:
            run = session.get(Run, run_id)
            run.screenshots = screenshots
            run.page_title = page_title
            run.page_name = page_name
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


def run_batch_analysis(batch_id: int):
    with Session(engine) as session:
        batch = session.get(Batch, batch_id)

        if batch:
            batch.status = "running"
            session.add(batch)
            session.commit()

        runs = session.exec(select(Run).where(Run.batch_id == batch_id)).all()

        run_data = [(run.id, run.url) for run in runs]

    for run_id, url in run_data:
        try:
            run_analysis(run_id, url)
        except Exception:
            pass

    with Session(engine) as session:
        batch = session.get(Batch, batch_id)

        if batch:
            runs = session.exec(select(Run).where(Run.batch_id == batch_id)).all()

            if all(run.status == "complete" for run in runs):
                batch.status = "complete"
            else:
                batch.status = "error"

            session.add(batch)
            session.commit()


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
    urls = [line.strip() for line in url.splitlines() if line.strip()]

    if len(urls) > 5:
        return templates.TemplateResponse(
            request=request,
            name="analyse.html",
            context={
                "request": request,
                "error": "Please enter a maximum of 5 URLs.",
            },
        )

    if len(urls) == 1:
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
            urls[0],
        )

        return templates.TemplateResponse(
            request=request,
            name="analyse_progress.html",
            context={
                "request": request,
                "run_id": run.id,
                "url": urls[0],
            },
        )

    with Session(engine) as session:
        batch = Batch(
            status="queued",
        )

        session.add(batch)
        session.commit()
        session.refresh(batch)

        runs = []

        for webpage_url in urls:
            run = Run(
                url=webpage_url,
                status="queued",
                batch_id=batch.id,
            )

            session.add(run)
            runs.append(run)

        session.commit()

        for run in runs:
            session.refresh(run)

        background_tasks.add_task(
            run_batch_analysis,
            batch.id,
        )

    return templates.TemplateResponse(
        request=request,
        name="batch_progress.html",
        context={
            "request": request,
            "batch_id": batch.id,
            "runs": runs,
        },
    )


def get_history_page_name(run):
    if run.page_name:
        return run.page_name

    if run.page_title:
        return run.page_title

    hostname = urlparse(run.url).netloc
    return hostname.removeprefix("www.").split(".")[0].title()


def get_history_overall_score(run):
    stored_score = run.report.get("ai", {}).get("overall_score")

    if stored_score is not None:
        return stored_score

    dimensions = run.report["ai"]["dimensions"]

    scores = [
        dimensions["visual_hierarchy"]["score"],
        dimensions["navigation"]["score"],
        dimensions["aesthetic_design"]["score"],
        dimensions["consistency_and_standards"]["score"],
        dimensions["clarity_and_familiarity"]["score"],
        dimensions["accessibility"]["score"],
        dimensions["performance"]["score"],
    ]

    return sum(scores) / len(scores)


@app.get("/history", response_class=HTMLResponse)
def history(request: Request):
    with Session(engine) as session:
        runs = session.exec(
            select(Run).where(Run.status == "complete").order_by(Run.timestamp.desc())
        ).all()

    history_groups = {}

    for run in runs:
        history_groups.setdefault(run.url, []).append(run)

    history_groups = dict(
        sorted(
            history_groups.items(),
            key=lambda item: item[1][0].timestamp,
            reverse=True,
        )
    )

    history_page_names = {
        url: get_history_page_name(runs[0]) for url, runs in history_groups.items()
    }

    return templates.TemplateResponse(
        request=request,
        name="history_view.html",
        context={
            "request": request,
            "history_groups": history_groups,
            "history_page_names": history_page_names,
        },
    )


@app.get("/history/run/{run_id}", response_class=HTMLResponse)
def history_run(run_id: int, request: Request):
    with Session(engine) as session:
        run = session.get(Run, run_id)

        if run is None:
            return HTMLResponse("Run not found", status_code=404)

    page_name = get_history_page_name(run)

    return templates.TemplateResponse(
        request=request,
        name="history_run.html",
        context={
            "request": request,
            "run": run,
            "page_name": page_name,
            "from_history": True,
        },
    )


@app.post("/history/compare", response_class=HTMLResponse)
def history_compare(
    request: Request,
    run_ids: list[int] = Form(...),
):
    with Session(engine) as session:
        if len(run_ids) != 2:
            return templates.TemplateResponse(
                request=request,
                name="history_compare.html",
                context={
                    "request": request,
                    "error": "Please select exactly two runs to compare.",
                },
            )

        runs = [session.get(Run, run_id) for run_id in run_ids]

        if any(run is None for run in runs):
            return templates.TemplateResponse(
                request=request,
                name="history_compare.html",
                context={
                    "request": request,
                    "error": "One or more selected runs could not be found.",
                },
            )

        if runs[0].url != runs[1].url:
            return templates.TemplateResponse(
                request=request,
                name="history_compare.html",
                context={
                    "request": request,
                    "error": "Runs must belong to the same webpage.",
                },
            )

        earlier_run, later_run = sorted(
            runs,
            key=lambda run: (run.timestamp, run.id),
        )

        earlier_scores = earlier_run.report["ai"]["dimensions"]
        later_scores = later_run.report["ai"]["dimensions"]

        score_comparison = [
            {
                "name": "Visual Hierarchy",
                "earlier": earlier_scores["visual_hierarchy"]["score"],
                "later": later_scores["visual_hierarchy"]["score"],
            },
            {
                "name": "Navigation",
                "earlier": earlier_scores["navigation"]["score"],
                "later": later_scores["navigation"]["score"],
            },
            {
                "name": "Aesthetic Design",
                "earlier": earlier_scores["aesthetic_design"]["score"],
                "later": later_scores["aesthetic_design"]["score"],
            },
            {
                "name": "Consistency & Standards",
                "earlier": earlier_scores["consistency_and_standards"]["score"],
                "later": later_scores["consistency_and_standards"]["score"],
            },
            {
                "name": "Clarity & Familiarity",
                "earlier": earlier_scores["clarity_and_familiarity"]["score"],
                "later": later_scores["clarity_and_familiarity"]["score"],
            },
            {
                "name": "Accessibility",
                "earlier": earlier_scores["accessibility"]["score"],
                "later": later_scores["accessibility"]["score"],
            },
            {
                "name": "Performance",
                "earlier": earlier_scores["performance"]["score"],
                "later": later_scores["performance"]["score"],
            },
        ]

        return templates.TemplateResponse(
            request=request,
            name="history_compare.html",
            context={
                "request": request,
                "earlier_run": earlier_run,
                "later_run": later_run,
                "page_name": get_history_page_name(later_run),
                "earlier_overall": get_history_overall_score(earlier_run),
                "later_overall": get_history_overall_score(later_run),
                "score_comparison": score_comparison,
            },
        )


@app.get("/analyse/{run_id}/status")
def analysis_status(run_id: int, request: Request):
    with Session(engine) as session:
        run = session.get(Run, run_id)

        if run is None:
            return HTMLResponse("Run not found", status_code=404)

        if run.status == "complete":
            return Response(headers={"HX-Redirect": f"/run/{run.id}"})

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


@app.get("/analyse/batch/{batch_id}/status", response_class=HTMLResponse)
def batch_analysis_status(
    request: Request,
    batch_id: int,
):
    with Session(engine) as session:
        batch = session.get(Batch, batch_id)

        if not batch:
            return HTMLResponse(
                "Batch not found.",
                status_code=404,
            )

        runs = session.exec(
            select(Run).where(Run.batch_id == batch_id).order_by(Run.id)
        ).all()

    completed = sum(1 for run in runs if run.status == "complete")

    total = len(runs)

    progress = int((completed / total) * 100) if total else 0

    all_finished = all(run.status in {"complete", "error"} for run in runs)

    if all_finished:
        return Response(headers={"HX-Redirect": f"/batch/{batch_id}"})

    return templates.TemplateResponse(
        request=request,
        name="batch_progress_status.html",
        context={
            "request": request,
            "batch_id": batch_id,
            "runs": runs,
            "completed": completed,
            "total": total,
            "progress": progress,
            "all_finished": all_finished,
        },
    )


@app.get("/batch/{batch_id}", response_class=HTMLResponse)
def get_batch_dashboard(batch_id: int, request: Request):
    with Session(engine) as session:
        batch = session.get(Batch, batch_id)

        if batch is None:
            return HTMLResponse("Batch not found", status_code=404)

        runs = session.exec(
            select(Run).where(Run.batch_id == batch_id).order_by(Run.id)
        ).all()

        if not runs:
            return HTMLResponse("No runs found for this batch", status_code=404)

    current_index = 0

    previous_run = None
    next_run = runs[1] if len(runs) > 1 else None

    return templates.TemplateResponse(
        request=request,
        name="batch_dashboard.html",
        context={
            "request": request,
            "batch_id": batch_id,
            "run": runs[current_index],
            "url": runs[current_index].url,
            "screenshots": runs[current_index].screenshots,
            "report": runs[current_index].report,
            "run_id": runs[current_index].id,
            "current_index": current_index,
            "total_runs": len(runs),
            "previous_run": previous_run,
            "next_run": next_run,
        },
    )


@app.get("/batch/{batch_id}/run/{run_id}", response_class=HTMLResponse)
def get_batch_run(batch_id: int, run_id: int, request: Request):
    with Session(engine) as session:
        runs = session.exec(
            select(Run).where(Run.batch_id == batch_id).order_by(Run.id)
        ).all()

        if not runs:
            return HTMLResponse("No runs found for this batch", status_code=404)

        current_index = next(
            (index for index, run in enumerate(runs) if run.id == run_id),
            None,
        )

        if current_index is None:
            return HTMLResponse("Run not found in this batch", status_code=404)

        current_run = runs[current_index]

    previous_run = runs[current_index - 1] if current_index > 0 else None

    next_run = runs[current_index + 1] if current_index < len(runs) - 1 else None

    return templates.TemplateResponse(
        request=request,
        name="batch_dashboard.html",
        context={
            "request": request,
            "batch_id": batch_id,
            "run": current_run,
            "url": current_run.url,
            "screenshots": current_run.screenshots,
            "report": current_run.report,
            "run_id": current_run.id,
            "current_index": current_index,
            "total_runs": len(runs),
            "previous_run": previous_run,
            "next_run": next_run,
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
            "run": run,
            "url": run.url,
            "screenshots": run.screenshots,
            "report": run.report,
            "run_id": run.id,
        },
    )


@app.get("/report/{run_id}", response_class=HTMLResponse)
def get_report(
    run_id: int,
    request: Request,
    from_history: bool = False,
):
    with Session(engine) as session:
        run = session.get(Run, run_id)

        if run is None:
            return HTMLResponse("Run not found", status_code=404)

    return templates.TemplateResponse(
        request=request,
        name="report.html",
        context={
            "request": request,
            "run": run,
            "url": run.url,
            "screenshots": run.screenshots,
            "report": run.report,
            "run_id": run.id,
            "from_history": from_history,
        },
    )


@app.get("/report/{run_id}/pdf")
def get_report_pdf(run_id: int):
    with Session(engine) as session:
        run = session.get(Run, run_id)

        if run is None:
            return HTMLResponse("Run not found", status_code=404)

        screenshots = run.screenshots

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(f"http://127.0.0.1:8000/report/{run_id}")

        page.wait_for_load_state("networkidle")

        screenshot_urls = {}

        for viewport, path in screenshots.items():
            image_data = Path(path).read_bytes()
            encoded_image = base64.b64encode(image_data).decode("utf-8")
            screenshot_urls[viewport] = f"data:image/png;base64,{encoded_image}"

        page.evaluate(
            """
        (screenshots) => {
            const appendix = document.createElement("section");

            appendix.className = "pdf-screenshot-appendix";

                    appendix.innerHTML = `
            <div class="pdf-appendix-header">
                <p>APPENDIX</p>
                <h2>Webpage Preview</h2>
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

        .navbar,
        .report-actions,
        .report-back-button {
            display: none !important;
        }
        
        .axe-details-box {
            break-before: page;
            page-break-before: always;
        }

        .report-recommendations {
            margin-top: 30px;
            break-before: page;
            page-break-before: always;
        }

        .report-page {
            max-width: none;
            padding: 0;
        }

        .report-hero-section {
            margin-bottom: 25px;
        }

        .report-intro-section {
            margin-bottom: 30px;
        }

        .report-overall-grid {
            grid-template-columns: 1fr;
            gap: 25px;
        }

        .report-overall-card,
        .report-recommendations {
            padding: 24px;
        }

        .report-highlights {
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        .report-preview {
            break-before: page;
            page-break-before: always;
            break-inside: avoid;
            page-break-inside: avoid;
        }

        .report-preview-grid {
            grid-template-columns: 1fr;
            gap: 20px;
        }

        .report-preview-card {
            padding: 18px 24px;
        }

        .report-dimension-grid {
            grid-template-columns: 1fr;
            gap: 16px;
        }

        .accessibility-components {
            grid-template-columns: 1fr;
            gap: 16px;
        }

        .performance-overview {
            grid-template-columns: 1fr;
            gap: 16px;
        }

        .report-lighthouse-section {
            grid-template-columns: 1fr;
            gap: 16px;
        }

            .report-recommendation,
            .report-dimension-card,
            .report-dimension-box,
            .report-preview-card,
            .axe-summary-box,
            .axe-violation,
            .axe-node,
            .report-lighthouse-box {
                break-inside: avoid;
                page-break-inside: avoid;
            }

            .report-dimension-title,
            .report-dimension-score,
            .report-preview h2,
            .report-recommendations h2,
            .report-overall-title,
            .axe-details-box h3,
            .report-lighthouse-box h3 {
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
                "top": "10mm",
                "right": "10mm",
                "bottom": "10mm",
                "left": "10mm",
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
def get_screenshot(run_id: int, viewport: str, request: Request):
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
