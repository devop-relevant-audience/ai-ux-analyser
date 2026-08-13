from playwright.sync_api import sync_playwright, TimeoutError
from datetime import datetime
import os

def dismiss_cookie_banner(page):
    buttons = [
        "Accept",
        "Accept All",
        "Accept all",
        "I Agree",
        "Allow all",
        "Agree",
        "ยอมรับคุกกี้ทั้งหมด",
        "OK",
        "Ok",
        "Okay",
    ]

    for text in buttons:
        try:
            page.get_by_role(
                "button",
                name=text,
                exact=True
            ).first.click(timeout=1000)

            print(f"Clicked cookie button: {text}")
            return
        except TimeoutError:
            pass


def scroll_page(page):
    last_scroll = -1

    while True:
        page.mouse.wheel(0, 1000)
        page.wait_for_timeout(500)

        current_scroll = page.evaluate("window.scrollY")

        if current_scroll == last_scroll:
            break

        last_scroll = current_scroll

    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(500)


def capture_screenshots(url: str):
    os.makedirs("screenshots", exist_ok=True)

    viewports = {
        "mobile": 375,
        "tablet": 768,
        "desktop": 1440,
    }

    screenshots = {}

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for name, width in viewports.items():
            page = browser.new_page(
                viewport={
                    "width": width,
                    "height": 900,
                }
            )

            page.goto(url, wait_until="domcontentloaded")

            try:
                page.wait_for_load_state(
                    "networkidle",
                    timeout=2000
                )
            except TimeoutError:
                print("Network never became idle. Continuing...")

            dismiss_cookie_banner(page)

            page.wait_for_timeout(1000)

            scroll_page(page)

            screenshot_path = f"screenshots/{timestamp}_{name}.png"

            page.screenshot(
                path=screenshot_path,
                full_page=True
            )

            screenshots[name] = screenshot_path

            page.close()

        browser.close()

    return screenshots

