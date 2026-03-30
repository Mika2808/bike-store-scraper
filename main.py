from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json

def load_gravels_from_page(i):
    url = f"https://www.centrumrowerowe.pl/rowery/gravel/?page={i}"

    driver = webdriver.Chrome()
    driver.get(url)

    # czekamy aż produkty się pojawią
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "item.product"))
    )

    html_content = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html_content, "html.parser")

    products = []

    for item_div in soup.select("div.item.product"):
        input_tag = item_div.find("input", {"name": "dataLayerItem"})
        if input_tag:
            json_str = input_tag["value"].replace("&quot;", '"')
            try:
                product_data = json.loads(json_str)
                products.append(product_data)
            except json.JSONDecodeError:
                print("Błąd dekodowania JSON:", json_str[:100])

    # zapis do pliku
    with open("rowery.json", "a", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=4)

    print(f"Pobrano {len(products)} produktów")

# Centrum Rowerowe 
def centrum_rowerowe():

    url = f"https://www.centrumrowerowe.pl/rowery/gravel/"

    driver = webdriver.Chrome()
    driver.get(url)

    # czekamy aż produkty się pojawią
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "item.product"))
    )

    html_content = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html_content, "html.parser")
    pages = []

    for el in soup.select(".pagination li"):
        text = el.get_text(strip=True)
        if text.isdigit():
            pages.append(int(text))

    last_page = max(pages) if pages else 1
    
    print(last_page)

    for i in range(last_page):
        load_gravels_from_page(i+1)

centrum_rowerowe()