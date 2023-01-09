from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

t0 = time.time()

service = Service(ChromeDriverManager().install())
options = Options()
options.add_argument("--start-maximized")
options.headless = True

driver = webdriver.Chrome(service=service, options=options)

url = 'https://www.youtube.com/@miguel11mom/videos'

driver.get(url)
form = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.TAG_NAME, "form"))
    )

button = form.find_element(By.TAG_NAME, "button")
button.click()

videos = WebDriverWait(driver, 100).until(
        EC.visibility_of_element_located((By.TAG_NAME, "ytd-rich-grid-row"))
    )

counter = 0
find_videos = lambda driver: BeautifulSoup(driver.page_source, 'html.parser').find_all("ytd-rich-grid-row")
videos = find_videos(driver)

more_videos = True
while more_videos:    
    driver.execute_script(f"scrollTo(0, window.innerHeight*{counter}*2);")
    time.sleep(0.1)
    counter += 1
    if counter % 20 == 0:
        updated_videos = find_videos(driver)
        if len(videos) == len(updated_videos):
            more_videos = False
            
        videos = updated_videos

parent_url = urlparse(driver.current_url)
parent_url = f'{parent_url.scheme}://{parent_url.netloc}'
print(parent_url)

driver.quit()

video_urls = []
for row in videos:
    urls = [x.attrs["href"] for x in row.find_all("a") if "href" in x.attrs]
    video_urls += [urljoin(parent_url, url) for url in urls]

print(video_urls)


t1 = time.time()

print(t1 - t0)

# print(videos[-1].text, len(videos))
    
