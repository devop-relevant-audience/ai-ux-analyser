from playwright.sync_api import sync_playwright
import os


def capture_screenshots(url: str):
    os.makedirs("screenshots", exist_ok=True)

    viewports = {
        "mobile": 375,
        "tablet": 768,
        "desktop": 1440,
    }

    screenshots = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for name, width in viewports.items():
            page = browser.new_page(
                viewport={
                    "width": width,
                    "height": 900, 
                }
            )

            page.goto(url)

            screenshot_path = f"screenshots/{name}.png"

            page.screenshot(
                path=screenshot_path,
                full_page=True
            )

            screenshots[name] = screenshot_path

            page.close()
            
        browser.close()

    return screenshots

