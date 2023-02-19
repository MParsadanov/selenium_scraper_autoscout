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
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from pathlib import Path
from tqdm import tqdm

def load_json(load_path):
    with open(load_path, 'r') as f:
        data = json.load(f)
    return data

def main() -> None:
    options = Options()
    options.add_argument("--start-maximized")
    options.page_load_strategy = 'eager'
    driver = webdriver.Chrome(options=options)
    
    ad_urls_dir = Path('ad_urls')
    ad_urls_dir.mkdir(exist_ok=True)
    
    manufacturer_names = load_json('data/manufacturers.json')
    countries = load_json('data/countries.json')

    #######################
    manufacturer_start = 0
    #######################
           
    for i, manufacturer in enumerate(manufacturer_names):
        if i + 1 <= manufacturer_start:
            continue
        
        models = manufacturer_names[manufacturer]
        
        ###########################################
        if manufacturer == 'Lynk & Co':
            manufacturer = 'lynk-%26-co'
        
        if ' ' not in manufacturer:
            continue
        else:
            manufacturer = '-'.join(manufacturer.split(' '))
        ###########################################
                
        manufacturer = manufacturer.lower()
        
        # if manufacturer != sys.argv[1]:
        #     continue
        
        for model in models:
            print(f'{i+1}/{len(manufacturer_names)}. Manufacturer {manufacturer}, model {model}')
            
        
            for country_name in countries:
                country_code = countries[country_name]
                
                print(f'Country: {country_name}')
                                    
                page_not_found_counter = 0
                for page_number in tqdm(range(1, 21)):        
                    ad_urls = []
                    driver.get(f'https://www.autoscout24.com/lst/{manufacturer}/{model}?sort=standard&desc=0&ustate=N%2CU&atype=C&cy={country_code}&page={page_number}')   
                    
                    no_results = driver.find_elements(By.CSS_SELECTOR, 'div[class="NoResults_text__W6tkE"]')
                    if no_results:
                        # print('No results')
                        break
                    
                    try:
                        ads = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[class="ListItem_title__znV2I Link_link__pjU1l"]')))
                    except (TimeoutException, NoSuchElementException):
                        continue
                    
                    for ad in ads:
                        try:
                            ad_href = ad.get_attribute('href')
                        except:
                            continue
                        
                        ad_url = ','.join([ad_href, manufacturer, model])
                        ad_urls.append(ad_url)
                        
                    if ad_urls:
                        with open(ad_urls_dir / f'{manufacturer}_ads_urls.txt', 'a') as f:
                            for ad_url in ad_urls:
                                f.write(ad_url + '\n')

if __name__ == '__main__':
    main() 
    