import json
import time
import re

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import Select


def main() -> None:
    options = Options()
    options.add_argument("--start-maximized")
    # options.page_load_strategy = 'eager'
    driver = webdriver.Chrome(options=options)
    
    driver.get('https://www.autoscout24.com/?genlnk=navi&genlnkorigin=com-all-all-home')
    select_make = driver.find_element(By.CSS_SELECTOR, 'select[id="make"]')
    top_makes = select_make.find_element(By.CSS_SELECTOR, 'optgroup[label="Top makes"]')
    other_makes = select_make.find_element(By.CSS_SELECTOR, 'optgroup[label="Other makes"]')
    
    manufacturers = {}
    makes = top_makes.text.split('\n') + other_makes.text.split('\n')
    
    select = Select(driver.find_element(By.CSS_SELECTOR, 'select[id="make"]'))
    for make in makes:
        select.select_by_visible_text(make)
        time.sleep(0.25)
        select_model = driver.find_element(By.CSS_SELECTOR, 'select[id="model"]')
        models = select_model.text.lower().split('\n')
        models_stripped = []
        for model in models:
            if 'model' in model or 'all' in model:
                continue
            model_text = '-'.join(model.split())
            model_text = re.sub(' +', '', model_text)
            models_stripped.append(model_text)
        manufacturers[make] = models_stripped
    
    with open('data/manufacturers.json', 'w', encoding='utf8') as f:
        json.dump(manufacturers, f, indent=4, ensure_ascii=False)
        

if __name__ == '__main__':
    main()