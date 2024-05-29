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
    image.save('gray_image_1.jpg')
    array = np.array(image)
    array = np.where(array > 150, 255, 0)
    image = Image.fromarray(array.astype('uint8'))
    image.save('gray_image_2.jpg')
    return image

@retry(stop_max_attempt_number=10, retry_on_result=lambda x: x is False)
def login():
    browser.get('http://captcha7.scrape.center/')
    browser.find_element(By.CSS_SELECTOR, '.username input[type="text"]').send_keys('admin')
    browser.find_element(By.CSS_SELECTOR, '.password input[type="password"]').send_keys('admin')
    captcha = browser.find_element(By.CSS_SELECTOR, '#captcha')
    image = Image.open(BytesIO(captcha.screenshot_as_png))
    image = preprocess(image)
    captcha = pytesseract.image_to_string(image)
    print([captcha])
    captcha = re.sub('[^A-Za-z0-9]', '', captcha)
    browser.find_element(By.CSS_SELECTOR, '.captcha input[type="text"]').send_keys(captcha)   
    print([captcha])
    browser.find_element(By.CSS_SELECTOR, '.login').click()
    
    try:
        WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//h2[contains(.,"登录成功")]')))       
        time.sleep(10)
        browser.close()
        return True
    except TimeoutError:
        return False


if __name__ == '__main__':
    browser = webdriver.Edge()
    login()
