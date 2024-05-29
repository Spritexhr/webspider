import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.locator("html").click()
    expect(page.get_by_role("link", name="WebVPN", exact=True)).to_be_visible()
    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="WebVPN", exact=True).click()
    page1 = page1_info.value

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
