from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from capture import capture_screenshot

app = FastAPI()

templates = Jinja2Templates(directory="templates")

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
    screenshot = capture_screenshot(url)

    report = {
        "overall": 100,
        "performance": 95,
        "accessibility": 90,
        "comment": "This is a fake report for M0."
    }

    return templates.TemplateResponse(
        request=request,
        name="report.html",
        context={
            "request": request,
            "url": url,
            "screenshot": screenshot,
            "report": report,
        },
    )