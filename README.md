# Gravel Scraper – porównywarka rowerów gravel

## Opis projektu

Chciałem kupić rower gravel i szybko porównać dostępne modele z różnych sklepów. Zamiast ręcznie przeglądać setki ofert, stworzyłem narzędzie do automatycznego zbierania danych. Aplikacja pobiera informacje o rowerach gravel z dwóch popularnych sklepów internetowych:
- Centrum Rowerowe  
- Decathlon  

Następnie ujednolica dane i zapisuje je w jednym pliku JSON, co umożliwia łatwą analizę i porównanie ofert.


## Jak to działa?

Projekt wykorzystuje:
- **Selenium** – do obsługi stron dynamicznych (JavaScript / AJAX)
- **BeautifulSoup** – do parsowania HTML
- **Pandas** – do analizy danych
- **JSON** – do przechowywania wyników

### Proces działania:

1. Uruchamiany jest webdriver (Chrome)
2. Skrypt odwiedza strony z rowerami gravel
3. Automatycznie wykrywa liczbę stron
4. Iteruje przez wszystkie strony
5. Dla każdej strony zanjduje produkty
6. Dla każdego produktu pobiera:
   - ID
   - markę
   - nazwę
   - cenę
   - ocenę
   - link
   - sklep
7. Dane są ujednolicane do wspólnego formatu
8. Wszystkie wyniki zapisywane są do pliku `rowery.json`


## Struktura danych

Każdy rower zapisany jest w formacie:

```json
{
  "id": "12345",
  "brand": "Triban",
  "name": "Gravel 120",
  "url": "https://...",
  "price": 3499.99,
  "rating": "4.5",
  "shop": "Decathlon"
}
```
<<<<<<< HEAD
Dzięki temu dane możemy szybko wczytać za pomocą biblioteki pandas i wyszukiwać nasze zachcianki
=======
Dzięki temu dane możemy szybko wczytać za pomocą biblioteki pandas i wyszukiwać nasze zachcianki
>>>>>>> 3ee3c5d2e5873bc28077c524684c2b8c1dfa5aab
