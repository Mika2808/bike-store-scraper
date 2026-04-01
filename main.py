from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import re
import pandas as pd
from datetime import datetime

def load_gravels_from_page_centrum_rowerowe(i, driver):
    # stworzenie odpowiedniego url
    url = f"https://www.centrumrowerowe.pl/rowery/gravel/?page={i}"

    # odpalenie drivera
    driver.get(url)

    # czekamy aż produkty się pojawią
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "item.product"))
    )

    html_content = driver.page_source

    soup = BeautifulSoup(html_content, "html.parser")

    # pobranie rowerów i danych o nich
    products = []

    # dla każdego roweru
    for item_div in soup.select("div.item.product"):
        input_tag = item_div.find("input", {"name": "dataLayerItem"})
        if input_tag:
            json_str = input_tag["value"].replace("&quot;", '"')
            try:
                product_data = json.loads(json_str)

                # --- ujednolicenie do wspólnego formatu ---
                unified_product = {
                    "id": str(product_data.get("item_id") or ""),
                    "brand": product_data.get("item_brand") or "",
                    "name": product_data.get("item_name") or "",
                    "url": product_data.get("url") or url,
                    "price": float(str(product_data.get("price") or 0).replace(",", "").replace("\xa0", "")),
                    "rating": str(product_data.get("rating") or ""),
                    "shop": product_data.get("shop") or "centrumrowerowe",
                    "date": datetime.now().strftime("%d.%m.%y")
                }

                # załadowanie nowego produktu
                products.append(unified_product)
            except json.JSONDecodeError:
                print("Błąd dekodowania JSON:", json_str[:100])

    # info
    print(f"Pobrano {len(products)} produktów")
    
    return products

# Centrum Rowerowe 
def centrum_rowerowe(driver):

    # pobranie html z kategorii gravele
    url = f"https://www.centrumrowerowe.pl/rowery/gravel/"

    # uruchomienie drivera (stronka z ajaxem)
    driver.get(url)

    # czekamy aż produkty się pojawią
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "item.product"))
    )

    # pobranie contentu po załdowaniu się strony
    html_content = driver.page_source

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
    products = []

    # pobranie rowerów z każdej strony
    for i in range(last_page):
        products.extend(load_gravels_from_page_centrum_rowerowe(i+1, driver))
    
    # zrócenie wszystich rowerów z danego sklepu
    return products

def decathlon(driver):
    url="https://www.decathlon.pl/sporty/rowery/rowery-gravel"

     # uruchomienie drivera (stronka z ajaxem)
    driver.get(url)

    # pobranie contentu po załdowaniu się strony
    html_content = driver.page_source

    soup = BeautifulSoup(html_content, "html.parser")

    pagination_nav = soup.find("nav", {"aria-label": "Pagination product list page"})
    pages = []

    if pagination_nav:
        for btn in pagination_nav.find_all("button"):
            text = btn.get_text(strip=True)
            if text.isdigit():  # tylko numery stron
                pages.append(int(text))

    last_page = max(pages) if pages else 1
    print("Ostatnia strona:", last_page)
    
    products = []
    # pobranie rowerów z każdej strony

    for i in range(last_page):
        products.extend(load_gravels_from_page_decathlon(i, driver))

    return products

def load_gravels_from_page_decathlon(page, driver):
    # stworzenie odpowiedniego url
    url = f"https://www.decathlon.pl/sporty/rowery/rowery-gravel?from={page*40}&size=40"

    # odpalenie drivera
    driver.get(url)

    html_content = driver.page_source

    soup = BeautifulSoup(html_content, "html.parser")

    # pobranie rowerów i danych o nich
    products = []

    # dla każdego roweru
    for item in soup.select("[data-supermodelid]"):
        supermodelid = item['data-supermodelid']
        link_tag = item.select_one(".dpb-product-link")
        brand = link_tag.select_one("strong").get_text(strip=True) if link_tag else None
        name = link_tag.select_one("span").get_text(strip=True) if link_tag else None
        price_tag = item.select_one(".price-wrapper .vtmn-font-bold")
        price = 0
        if price_tag:
            text = price_tag.get_text()
            # dopasowanie cyfr i przecinka/kropki
            match = re.search(r"[\d\s\xa0]+[,\.]\d+", text)
            if match:
                number_str = match.group(0)
                # usuń WSZYSTKIE spacje, w tym niełamliwe \xa0
                number_str = number_str.replace("\xa0","").replace(" ","").replace(",",".")
                price = float(number_str)
            else:
                price = None
        else:
            price = None
        rating_tag = item.select_one(".stars")
        rating = rating_tag["data-note"] if rating_tag and rating_tag.has_attr("data-note") else None
        
        product = {
            "id": supermodelid,
            "brand": brand,
            "name": name,
            "url": url,
            "price": price,
            "rating": rating,
            "shop": "Decathlon",
            "date": datetime.now().strftime("%d.%m.%y")
        }
        products.append(product)

    # info
    print(f"Pobrano {len(products)} produktów")
    
    return products

def loading_gravels():
    # odpalenie drivera
    driver = webdriver.Chrome()

    # zmienna na rowery
    all_products = []

    # Przeszukanie Centrum Rowerowe/ Decathlon
    all_products.extend(centrum_rowerowe(driver))
    all_products.extend(decathlon(driver))

    # zapis do pliku
    filename = f"rowery_{datetime.now().strftime('%d.%m.%y')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_products, f, ensure_ascii=False, indent=2)

    # wyłączenie silnika Chrome
    driver.quit()

loading_gravels()

# Wczytanie pliku JSON do Pythona
filename = f"rowery_{datetime.now().strftime('%d.%m.%y')}.json"
with open(filename, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Zamiana na DataFrame
df = pd.DataFrame(data)

# Podgląd
print(df.head())
print (df.shape)
df.info()
