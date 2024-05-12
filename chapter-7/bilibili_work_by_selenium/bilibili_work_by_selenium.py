from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s : %(message)s")

INDEX_URL = 'https://www.bilibili.com/v/popular/rank/all'
TIMEOUT = 10
TOTAL_PAGE = 20

browser = webdriver.Edge()
wait = WebDriverWait(browser, TIMEOUT)

def scrape_page(url, condition, locator):
    logging.info('scraping %s', url)
    try:
        browser.get(url)
        wait.until(condition(locator))
    except TimeoutException:
        logging.error('error occurred while scraping %s', url, exc_info=True)

def scrape_index():
    url = INDEX_URL
    scrape_page(url, condition=EC.visibility_of_all_elements_located,
                locator=(By.XPATH, '//div/ul/li'))

def parse_index(which_one):
    items = []
    title = browser.find_element(By.XPATH,
                                    f"//div/ul/li[@data-rank = '{which_one+1}']/div/div[@class = 'info']/a").text
    href = browser.find_element(By.XPATH,
                                    f"//div/ul/li[@data-rank = '{which_one+1}']/div/div[@class = 'info']/a").get_attribute('href')

    author = browser.find_element(By.XPATH,
                                  f"//div/ul/li[@data-rank = '{which_one+1}']/div/div[@class = 'info']/div[@class = 'detail']/a/span").text
    icon_play = browser.find_element(By.XPATH,
                                     f"//div/ul/li[@data-rank = '{which_one+1}']/div/div[@class = 'info']/div[@class = 'detail']/div/span[1]").text
    return {
        "title": title,
        "href": href,
        "author": author,
        "icon_play": icon_play
    }


def scrape_detail(href):
    scrape_page(href, condition=EC.visibility_of_element_located,
                locator=(By.XPATH, '//*[@id="viewbox_report"]'))
    
def parse_detail():
    
    try:
        # url = browser.current_url
        introduction = browser.find_element(By.XPATH, 
                                    "//div[@class = 'left-container-under-player']/div/div[@class = 'basic-desc-info']/span").text

        likes = browser.find_element(By.XPATH,
                                    '//*[@id="arc_toolbar_report"]/div[1]/div[1]/div[1]/div/span').text
        coins = browser.find_element(By.XPATH,
                                    '//*[@id="arc_toolbar_report"]/div[1]/div[1]/div[2]/div/span').text
        collection = browser.find_element(By.XPATH,
                                    '//*[@id="arc_toolbar_report"]/div[1]/div[1]/div[2]/div/span').text
        
        return {
            'introduction': introduction,
            'likes': likes,
            'coins': coins,
            'collection': collection
        }
    except:
        print('抓取细节时有错误产生')
    

options = webdriver.EdgeOptions()
options.add_argument('--headless')
browser = webdriver.Edge(options=options)

def main():
    items = []
    try:
        scrape_index()
        for num in range(TOTAL_PAGE):
            index_data = parse_index(num)
            logging.info('get detail url %s', index_data)
            items.append(index_data)
            
        for index,item in enumerate(items):
            
            scrape_detail(item['href'])
            detail_data = parse_detail()
            logging.info('detail data %s',detail_data)   
            try:
                merge_data =  {**items[index], **detail_data}
                save_data(data=merge_data)
                logging.info('merge_data: %s', merge_data)
            except:
                print('存入时有错误产生')

    finally:
        browser.close()

from os import makedirs
from os.path import exists
import json

RESULTS_DIR = 'results'

exists(RESULTS_DIR) or makedirs(RESULTS_DIR)

def save_data(data):
    name = data.get('title')
    data_path = f'{RESULTS_DIR}/{name}.json'
    json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()

