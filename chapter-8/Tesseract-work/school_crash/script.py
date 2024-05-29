import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.gxmzu.edu.cn/index/VPNycjr.htm")
    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="WebVPN", exact=True).click()
    page1 = page1_info.value
    page1.get_by_placeholder("请输入您的账号").click()
    page1.get_by_placeholder("请输入您的账号").fill("202313141100520")
    page1.get_by_role("img", name="logo").click(button="right")
    page1.get_by_role("img", name="logo").click(button="right")
    page1.get_by_role("img", name="logo").click(button="right")
    page1.get_by_role("img", name="logo").dblclick()
    page1.locator(".ant-row > div:nth-child(2) > div").first.click(button="right")
    page1.get_by_role("img", name="logo").click()
    page1.get_by_role("img", name="logo").click(button="right")
    page1.get_by_role("img", name="logo").click(button="right")
    page1.get_by_role("img", name="logo").click()
    page1.get_by_role("img", name="logo").click()
    page1.get_by_role("img", name="logo").click()
    page1.locator("div").filter(has_text=re.compile(r"^123账号登录APP扫码登录请输入密码登 录重 置记住密码常见问题忘记密码验证中，请稍等\.\.\.or短信登录$")).get_by_role("img").first.click()
    page1.get_by_placeholder("请输入密码").click()
    page1.get_by_role("img", name="logo").click()
    page.close()
    page1.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
