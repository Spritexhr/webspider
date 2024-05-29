import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.gxmzu.edu.cn/index/VPNycjr.htm")
    with page.expect_popup() as page1_info:
        page.locator("div").filter(has_text=re.compile(r"^WebVPN$")).click()
    page1 = page1_info.value
    page1.get_by_placeholder("请输入您的账号").click()
    page1.get_by_placeholder("请输入您的账号").fill("202313141100520")
    page1.get_by_placeholder("请输入密码").click()
    page1.get_by_placeholder("请输入密码").fill("12345678a/")
    page1.get_by_placeholder("算术答案").click()
    page1.get_by_placeholder("算术答案").fill("9")
    page1.get_by_role("button", name="登 录").click()
    page1.get_by_role("button", name="关闭").click()
    with page1.expect_popup() as page2_info:
        page1.get_by_role("link", name="教务系统").click()
    page2 = page2_info.value
    page2.get_by_role("link", name="选课中心").click()
    page2.get_by_role("link", name="学生选课中心").click()
    page2.get_by_role("link", name="学生预选管理").click()
    page2.get_by_role("link", name="学生选课结果查询").click()
    page2.get_by_role("link", name="辅修报名").click()
    page2.get_by_role("link", name="学生选课结果查询").click()
    page2.get_by_role("link", name="学生选课中心").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
