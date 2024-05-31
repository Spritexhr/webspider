#实战
import time
import re
import pytesseract
from PIL import Image
import numpy as np
from retrying import retry
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def preprocess(image): 
    image = image.convert('L')
    array = np.array(image)
    array = np.where(array < 250, 0, 255)
    image = Image.fromarray(array.astype('uint8'))
    return image

# @retry(stop_max_attempt_number=3, retry_on_result=lambda x: x is False)
def login():
    browser.get('https://www.gxmzu.edu.cn/index/VPNycjr.htm')
    browser.find_element(By.XPATH, '//*[@id="vsb_content"]/div/div[1]/div[1]/a').click()
    time.sleep(3)
    browser.find_element(By.CSS_SELECTOR, "input[id='userName']").send_keys('202313141100520')
    
    browser.find_element(By.CSS_SELECTOR, "input[id='password']").send_keys('12345678a/')
    captcha = browser.find_element(By.XPATH, '//*[@id="root"]/span/div[4]/div/div/div[1]/div/div/form/div[4]/div/div/span/div/div[2]/div/img')
    image = Image.open(BytesIO(captcha.screenshot_as_png))
    image = preprocess(image)
    string = pytesseract.image_to_string(image)
    captcha = re.sub(r'[^-+*/()0-9]', '', string)
    browser.find_element(By.XPATH, '//*[@id="captcha"]').send_keys(captcha)   
    print([captcha])
    browser.find_element(By.XPATH, '//*[@id="root"]/span/div[4]/div/div/div[1]/div/div/form/div[5]/button[1]').click()
    
    try:
        WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[6]/div/ul/li[1]/a')))       
        time.sleep(10)
        browser.close()
        return True
    except TimeoutError:
        return False


if __name__ == '__main__':
    browser = webdriver.Edge()
    login()
