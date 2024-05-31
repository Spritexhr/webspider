import pytesseract
from PIL import Image
import numpy as np
import re
import time
from io import BytesIO
import re
from playwright.sync_api import Playwright, sync_playwright, expect, TimeoutError
import logging

import base64  


logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s : %(message)s")
MAX_RETRY = 3

def preprocess(image_bytes): 
    image = Image.open(image_bytes)
    image = image.convert('L')
    array = np.array(image)
    array = np.where(array < 250, 0, 255)
    image = Image.fromarray(array.astype('uint8'))
    return image

def get_img_information(src):
     # 移除Base64字符串的头部信息，只保留编码部分  
    base64_data = base64.b64decode(src.split(',')[1])  
    
    # 使用io.BytesIO将解码后的数据转换为文件对象  
    image_bytes = BytesIO(base64_data)  
    
    image = preprocess(image_bytes)
    
    string = pytesseract.image_to_string(image)
    captcha = re.sub(r'[^-+*/()0-9]', '', string)
    logging.info('captcha: %s', captcha)
    return captcha
    
def before_captcha(page1):
    page1.wait_for_load_state('load')
    time.sleep(3)
    page1.get_by_placeholder("请输入您的账号").click()
    page1.get_by_placeholder("请输入您的账号").fill("202313141100520")
    #账号
    page1.get_by_placeholder("请输入密码").click()
    page1.get_by_placeholder("请输入密码").fill("12345678a/")
    #密码
    page1.get_by_placeholder("算术答案").click() 

def get_img_src(page1):    
    src = page1.get_by_role("img", name="logo").get_attribute('src')
    logging.info('src: %s', src)  
    return src

def run(playwright: Playwright):
    browser = playwright.firefox.launch(headless=False)
    attempt_2 = 1
    while attempt_2 < MAX_RETRY:
        attempt_1 = 1
        while attempt_1 <= MAX_RETRY:
            try:
                context = browser.new_context()
                page = context.new_page()
                page.goto("https://www.gxmzu.edu.cn/index/VPNycjr.htm")
                with page.expect_popup() as page1_info:
                    page.locator("div").filter(has_text=re.compile(r"^WebVPN$")).click()
                page1 = page1_info.value
                before_captcha(page1)
                captcha = get_img_information(src=get_img_src(page1))
                captcha_result = str(eval(captcha))
                break
            except SyntaxError:
                attempt_1 += 1

        page1.get_by_placeholder("算术答案").fill(captcha_result)  
        logging.info('captcha: %s', captcha) 
        page1.get_by_role("button", name="登 录").click()
        attempt_2 = 1
        try:
            page1.wait_for_selector('body > div:nth-child(7) > div > ul > li:nth-child(1) > a > h4')
            logging.info('status: %s', '登录成功')
            time.sleep(5)
            context.close()
            browser.close()
            break
        except TimeoutError:
            attempt_2 += 1

with sync_playwright() as playwright:
    run(playwright)

