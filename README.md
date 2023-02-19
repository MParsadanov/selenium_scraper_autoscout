# Selenium image scraper for autoscout24.com

Scape car images from autoscout24.com into the following folder structure (manufacturer - model - year):

```
autoscout24.com 
│
├───Audi
│   ├───A4
│   │   ├───2019
│   │   ├───2021
│   │   └───2022
│   ├───A6
│   │   ├───2015
│   │   ├───2016
│   │   └───2022
│   ├───Q5
│   │   ├───2014
│   │   ├───2017
│   │   └───2022
│   └───...
│       ├───...
│       ├───...
│       └───...
├───BMW
│   ├───1-series
│   │   ├───2019
│   │   ├───2021
│   │   └───2022
│   ├───3-series
│   │   ├───2015
│   │   ├───2016
│   │   └───2022
│   ├───X5
│   │   ├───2014
│   │   ├───2017
│   │   └───2022
│   └───...
│       ├───...
│       ├───...
│       └───...
├───...  
```

## How to use

1. Run `get_manufacturers.py` to update the list of manufacturers
2. Run `get_ads_urls.py` to get the list of ads URLs
3. Run `get_image_urls.py` to get the list of image URLS, including manufacturer name, model name, production year
4. Run `download_images.py` to download images to corresponding folders