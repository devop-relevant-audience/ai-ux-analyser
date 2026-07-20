from playwright.sync_api import sync_playwright
import os


def capture_screenshot(url: str):
    os.makedirs("screenshots", exist_ok=True)

    screenshot_path = "screenshots/page.png"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page(
            viewport={
                "width": 1440,
                "height": 900
            }
        )

        page.goto(url)

        page.screenshot(
            path=screenshot_path,
            full_page=True
        )

        browser.close()

    return screenshot_path

