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
    array = np.where(array > 50, 255, 0)
    image = Image.fromarray(array.astype('uint8'))
    return image

@retry(stop_max_attempt_number=10, retry_on_result=lambda x: x is False)
def login():
    browser.get('http://captcha7.scrape.center/')
    browser.find_element(By.CSS_SELECTOR, '.username input[type="text"]').send_keys('admin')
    browser.find_element(By.CSS_SELECTOR, '.password input[type="password"]').send_keys('admin')
    captcha = browser.find_element(By.CSS_SELECTOR, '#captcha')
    image = Image.open(BytesIO(captcha.screenshot))
    







if __name__ == 'main':
    browser = webdriver.Chrome()
    login()
