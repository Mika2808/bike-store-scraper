from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json

def load_gravels_from_page(i):
    # stworzenie odpowiedniego url
    url = f"https://www.centrumrowerowe.pl/rowery/gravel/?page={i}"

    # odpalenie drivera
    driver = webdriver.Chrome()
    driver.get(url)

    # czekamy aż produkty się pojawią
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "item.product"))
    )

    html_content = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html_content, "html.parser")

    # pobranie rowerów i danych o nich
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

    # info
    print(f"Pobrano {len(products)} produktów")

# Centrum Rowerowe 
def centrum_rowerowe():

    # pobranie html z kategorii gravele
    url = f"https://www.centrumrowerowe.pl/rowery/gravel/"

    # uruchomienie drivera (stronka z ajaxem)
    driver = webdriver.Chrome()
    driver.get(url)

    # czekamy aż produkty się pojawią
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "item.product"))
    )

    # pobranie contentu po załdowaniu się strony
    html_content = driver.page_source

    # wyłączenie drivera
    driver.quit()

    soup = BeautifulSoup(html_content, "html.parser")
    
    # pobranie stron z pagination
    pages = []

    for el in soup.select(".pagination li"):
        text = el.get_text(strip=True)
        if text.isdigit():
            pages.append(int(text))

    # pobranie ilości stron
    last_page = max(pages) if pages else 1
    
    # # robocze
    # print(last_page)

    # pobranie rowerów z każdej strony
    for i in range(last_page):
        load_gravels_from_page(i+1)

centrum_rowerowe()