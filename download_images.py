import argparse
import time
import requests
import io
import logging

from PIL import Image

from hashlib import sha256
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from pathlib import Path


def download_image(download_dir: Path, url: str, file_name: str):
       
    try:
        image_content = requests.get(url, timeout=30).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_dir / file_name

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")

        # print(f'Success: {file_path}\r', end='')
    except Exception as e:
        print(f'FAILED:\n{url}\n{e}')

def download_url(args):
    global counter
    t0 = time.time()
    url, dd, fn = args[0], args[1], args[2]
               
    try:
        subdir = Path(PATH) / dd
        subdir.mkdir(exist_ok=True, parents=True)
        full_path = subdir / fn
        r = requests.get(url, timeout=30)
        with open(full_path, 'wb') as f:
            f.write(r.content)
        counter += 1
        
        return(url, fn, time.time() - t0)
    except Exception as e:
        print('Exception in download_url():', e)
        counter += 1
        return('Bad URL', fn, time.time() - t0)
        
def download_parallel(args, url_length):
    cpus = cpu_count()
    # results = ThreadPool(cpus - 1).imap_unordered(download_url, args)
    # results = ThreadPool(THREADS).imap_unordered(download_url, args)

    with ThreadPool(THREADS) as pool:
        for result in pool.imap_unordered(download_url, args):
            print(f'{counter} / {url_length}')
            print(f'url: {result[0]} name: {result[1]} time (s): {result[2]:.2f}')
    #for result in results:
     #   print(f'{counter} / {url_length}')
      #  print(f'url: {result[0]} name: {result[1]} time (s): {result[2]:.2f}')

def main() -> None:
  
    urls = []
    download_dirs = []
    image_names = []

    with open(PATH_TO_URL_FILE, 'r') as file:
        for line in file:
            try:
                url, manufacturer, model, year, image_name = line.rstrip().split(',')
            except Exception as e:
                logger.error(f'Exception in url file line "{line}":', e)
                print(e)
                print(line)
                continue
                
            if url.endswith('.svg'):
                continue
            
            urls.append(url)       
            download_dir = '/'.join([manufacturer, model, year])
                        
            download_dirs.append(download_dir)
            
            # Encode image names using hash
            # image_name = sha256(image_name.split(".")[0].encode("utf-8")).hexdigest() + ".jpg"
            
            image_names.append(image_name)

    global counter
    counter = 0
    
    inputs = zip(urls, download_dirs, image_names)
    download_parallel(inputs, len(urls))
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parameters')
    parser.add_argument('--image_folder', required=True, help='Path to saved images folder')
    parser.add_argument('--url_file', required=True, help='Path to txt file with image urls')
    parser.add_argument('--threads', required=True, help='Number of threads for multiprocessing')
    args = parser.parse_args()
    
    # path to saved images
    PATH = args.image_folder

    # path to txt file with urls
    PATH_TO_URL_FILE = args.url_file
    
    THREADS = int(args.threads)
    
    main()
