import os

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
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

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"request": request},
    )


@app.post("/analyze", response_class=HTMLResponse)
def analyze(request: Request, url: str = Form(...)):
    screenshots = capture_screenshots(url)

    visual_evidence = extract_visual_evidence(screenshots)

    lighthouse_report = run_lighthouse(url)
    axe_report = run_axe(url)

    ai_report = generate_ux_report(
        visual_evidence.visual_observations,
        lighthouse_report,
        axe_report,
    )

    report = build_report(
        lighthouse_report,
        axe_report,
        ai_report.model_dump(),
    )
    

    with Session(engine) as session:
        run = Run(
            url=url,
            screenshots=screenshots,
            report=report,
        )

        session.add(run)
        session.commit()

    return templates.TemplateResponse(
        request=request,
        name="report.html",
        context={
            "request": request,
            "url": url,
            "screenshots": screenshots,
            "report": report,
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
        name="report.html",
        context={
            "request": request,
            "url": run.url,
            "screenshots": run.screenshots,
            "report": run.report,
        },
    )
