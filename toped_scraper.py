"""Digunakan sebagai scraper tokopedia"""

import urllib.parse
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--headless")
options.add_argument(
    "--disable-gpu"
)  # tanpa ini sudah bisa jalan, tapi katanya ini bikin lebih cepat
options.add_argument(
    "--disable-dev-shm-usage"
)  # tanpa ini sudah bisa jalan, tapi katanya ini bikin lebih cepat
options.add_argument(
    "--disable-blink-features=AutomationControlled"
)  # ini supaya tidak terdeteksi bot?


BASE_URL = "https://www.tokopedia.com/search?ob=5&page="
query = input("Kata Kunci: ")
encoded_term = urllib.parse.quote(query)

driver = webdriver.Chrome(options=options)

JS_CODE = "window.scrollBy(0,320)"

links = []

page = 1
for i in range(1, 3):
    page = i
    this_page = str(page) + "&q="
    url = BASE_URL + this_page + encoded_term
    print(url)
    driver.get(url)

    scroll = 0
    while scroll < 14:
        driver.execute_script(JS_CODE)
        time.sleep(0.9)
        scroll += 1

    XPATH = '//div[@class="css-19oqosi"]/a'
    elements = driver.find_elements(By.XPATH, XPATH)

    for element in elements:
        link = element.get_attribute("href")
        links.append(link)

df = pd.DataFrame(data=links, columns=["link"])

driver.close()

cwd = os.path.dirname(__file__)
file_path = os.path.join(cwd, "hasil_scrape.csv")
df.to_csv(file_path, index=False)
