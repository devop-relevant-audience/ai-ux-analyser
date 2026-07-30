import os
from capture import capture_screenshots
from lighthouse import run_lighthouse
from axe import run_axe
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from normalize import build_report
from sqlmodel import Session
from database import create_db_and_tables, engine
from models import Run

app = FastAPI()

create_db_and_tables()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


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

    lighthouse_report = run_lighthouse(url)
    axe_report = run_axe(url)

    report = build_report(lighthouse_report, axe_report)

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