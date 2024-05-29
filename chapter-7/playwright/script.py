import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page1 = context.new_page()
    page1.goto("https://www.bilibili.com/")
    with page1.expect_popup() as page2_info:
        page1.get_by_role("link", name="热门", exact=True).click()
    page2 = page2_info.value 
    page2.get_by_text("排行榜").click()
    with page2.expect_popup() as page3_info:
        page2.get_by_role("link", name="他是保安界的天花板，离任时，全小区业主都哭着挽留。").click()
    page3 = page3_info.value
    page3.close()
    with page2.expect_popup() as page4_info:
        page2.get_by_role("link", name="原来，不是一份饭3块钱…8").click()
    page4 = page4_info.value
    page4.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
