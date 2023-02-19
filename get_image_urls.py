import json
import shutil
import time
import re
import sys

import multiprocessing as mp

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, InvalidSessionIdException

from pathlib import Path
from tqdm import tqdm

from main import load_json

def get_image_urls(driver, ad_url: str) -> list:    
    try: 
        driver.get(ad_url)
        
        year = None
        year_elements = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[class="VehicleOverview_itemText__V1yKT"]')))
        for year_element in year_elements:
            year_text = re.match('([0-9]{2}\/[1-2][0-9]{3})', year_element.text)
            if year_text:    
                year = year_element.text.split('/')[-1]
                
        if not year:
            return
            
        image_container = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="image-gallery-thumbnails-container"]')))
        
        images = image_container.find_elements(By.CSS_SELECTOR, 'img[class="image-gallery-thumbnail-image"]')

        image_urls = []

        for image in images:
            src = image.get_attribute('src')
            image_url = src.replace('/120x90.jpg', '')
            image_urls.append(image_url)
                            
        return [image_urls, year]
    
    # except InvalidSessionIdException as e:
    #     print(e)
    #     exit()
    except Exception as e:
        print(f'{e} - {ad_url}')
        return
    
def main() -> None:   
    image_urls_dir = Path('image_urls')
    image_urls_dir.mkdir(exist_ok=True)
    
    manufacturer_names = load_json('data/manufacturers.json')
    countries = load_json('data/countries.json')
           
    for idx, manufacturer in enumerate(manufacturer_names):
        manufacturer = manufacturer.lower()
                
        # if manufacturer != sys.argv[1]:
        #     continue
               
        ####################################################
        # if idx + 1 < 219:
        #     continue
        ####################################################
               
        ad_urls_file = f'ad_urls/{manufacturer}_ads_urls.txt'
        image_urls_file = image_urls_dir / f'{manufacturer}_image_urls.txt'
            
        try:
            with open(ad_urls_file, 'r') as f:
                ad_url_lines = f.read().splitlines()
            print(f'{idx+1}/{len(manufacturer_names)}. Reading ad urls for manufacturer {manufacturer}, {len(ad_url_lines)} lines')
        except FileNotFoundError:
            continue
        
        options = Options()
        options.add_argument("--start-maximized")
        options.page_load_strategy = 'eager'
        driver = webdriver.Chrome(options=options) 
        
        image_urls_counter = 0
        
        # start_ad = int(sys.argv[2])
        # ad_url_lines = ad_url_lines[start_ad:]
        
        # ad_url_lines = ad_url_lines[start_ad:10000]
        
        for ad_url in tqdm(ad_url_lines):
            
            ad_href, manufacturer, model = ad_url.split(',')
            
            result = get_image_urls(driver, ad_href)
            if result is None:
                continue
            
            image_urls, year = result
                                    
            with open(image_urls_file, 'a') as f:
                for image_url in image_urls:
                    image_name = image_url.split("/")[-1]
                    f.write(f'{image_url},{manufacturer},{model},{year},{image_name}\n')

            image_urls_counter += len(image_urls)
                    
        print(f'{image_urls_counter} image urls saved to file "{image_urls_file}"')
                    
           
if __name__ == '__main__':
    main()