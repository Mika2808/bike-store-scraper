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

    # dla każdego roweru
    for item_div in soup.select("div.item.product"):
        input_tag = item_div.find("input", {"name": "dataLayerItem"})
        if input_tag:
            # pobranie roweru
            json_str = input_tag["value"].replace("&quot;", '"')
            try:
                # onwersja do jsona
                product_data = json.loads(json_str)

                # dodanie sklepu oraz url
                product_data["shop"] = "centrumrowerowe"
                product_data["url"] = url
                
                # załadowanie nowego produktu
                products.append(product_data)
            except json.JSONDecodeError:
                print("Błąd dekodowania JSON:", json_str[:100])

    # info
    print(f"Pobrano {len(products)} produktów")
    
    return products

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
    
    # info
    print(f"Jest {last_page} stron z gravelami")
    
    # zmienne
    all_products = []

    # pobranie rowerów z każdej strony
    for i in range(last_page):
        all_products.append(load_gravels_from_page(i+1))
    
    with open("rowery.json", "w", encoding="utf-8") as f:
        json.dump(all_products, f, ensure_ascii=False, indent=2)

centrum_rowerowe()