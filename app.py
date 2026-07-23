import os
from capture import capture_screenshots
from lighthouse import run_lighthouse
from axe import run_axe
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates



app = FastAPI()

templates = Jinja2Templates(directory="templates")

os.makedirs("screenshots", exist_ok=True)

app.mount("/screenshots", StaticFiles(directory="screenshots"), name="screenshots")


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

    report = {
        "lighthouse": lighthouse_report,
        "axe": axe_report
    }


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