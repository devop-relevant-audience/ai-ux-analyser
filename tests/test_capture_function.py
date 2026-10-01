from pathlib import Path

from PIL import Image

from capture import capture_screenshots


def test_capture_screenshots():
    url = "https://example.com"

    screenshots = capture_screenshots(url)

    assert set(screenshots.keys()) == {
        "mobile",
        "tablet",
        "desktop",
    }

    expected_widths = {
        "mobile": 375,
        "tablet": 768,
        "desktop": 1440,
    }

    for viewport, path in screenshots.items():
        screenshot_path = Path(path)

        assert screenshot_path.exists()
        assert screenshot_path.is_file()

        with Image.open(screenshot_path) as image:
            assert image.width == expected_widths[viewport]
            assert image.height > 0