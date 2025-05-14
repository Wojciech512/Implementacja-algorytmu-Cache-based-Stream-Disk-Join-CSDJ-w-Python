# Implementacja algorytmu Cache-based Stream-Disk Join (CSDJ) w Python

## Wprowadzenie

Algorytm Cache-based Stream-Disk Join (CSDJ) służy do wydajnego łączenia ciągłego strumienia danych z dużym statycznym zbiorem danych (tzw. danymi "dyskowymi", np. tabelą główną) w warunkach ograniczonej pamięci operacyjnej. Kluczową ideą jest wykorzystanie pamięci podręcznej (cache) do przechowywania najczęściej używanych fragmentów danych dyskowych w pamięci, co pozwala ograniczyć liczbę kosztownych odczytów z dysku. Innymi słowy, jeśli pewne klucze z danych referencyjnych są często poszukiwane przez nadchodzące tuple strumienia, to ich odpowiedniki z dysku zostają zachowane w pamięci podręcznej, przyspieszając kolejne operacje łączenia. CSDJ zakłada zazwyczaj łączenie po kluczu (tzw. equi-join na kluczu, np. klucz główny w danych dyskowych i klucz obcy w danych strumieniowych). W niniejszym projekcie skupimy się na takim przypadku, implementując pamięć podręczną LRU (Least Recently Used) do przechowywania ostatnio użytych rekordów. Polityka LRU usuwa z cache najdawniej nieużywany element, gdy brakuje miejsca na nowy element, co w praktyce często pokrywa się z usuwaniem rzadko używanych elementów. Dodatkowo, rozwiązanie zostanie zaprojektowane w sposób modularny z wykorzystaniem wątków, tak aby strumień danych był przetwarzany równolegle (np. jeden wątek generuje dane strumieniowe, drugi dokonuje łączenia). Struktura projektu jest podzielona na odrębne moduły (pliki Python) zgodnie z wymaganiami, a kod zawiera komentarze i pseudokod ułatwiające zrozumienie działania algorytmu.
Struktura projektu

### Projekt składa się z następujących plików i katalogów:

- cache.py – implementacja pamięci podręcznej LRU (klasa LRUCache).
- stream.py – moduł obsługi danych strumieniowych; generuje dynamicznie dane wejściowe (klucz i ewentualnie dodatkowe atrybuty).
- disk.py – moduł symulujący „dysk”; odczytuje dane wzorcowe (referencyjne) z pliku CSV tylko w razie potrzeby (brak w cache).
- joiner.py – moduł łączenia strumienia z danymi dyskowymi; zawiera logikę algorytmu CSDJ korzystającego z cache oraz obsługę warunków łączenia.
- main.py – główny plik uruchamiający, który tworzy obiekty powyższych klas, uruchamia wątki i koordynuje cały proces.
- data/ – katalog z danymi; np. plik reference.csv zawierający dane referencyjne (dyskowe).
- logs/ – katalog na logi działania programu (np. plik log zawierający informacje o przetwarzaniu i cache).

## Uruchomienie

Aby uruchomić projekt, wystarczy wywołać plik main.py. Program automatycznie utworzy potrzebne katalogi (data/, logs/) oraz plik reference.csv z danymi referencyjnymi, jeśli ten nie istnieje. Wyniki działania zostaną zapisane w pliku logów w katalogu logs/. Program można uruchomić bezpośrednio w środowisku PyCharm (konfiguracja: Pure Python, interpreter: venv) lub z terminala:

```
python main.py
```

## Parametry konfiguracyjne

Wyniki działania algorytmu można modyfikować poprzez zmianę poniższych parametrów w pliku main.py (w funkcji **main**):

- event_count (w StreamGenerator) – liczba wygenerowanych zdarzeń (np. 100, 500, 1000). Wpływa na długość strumienia i czas działania testu.

- interval – odstęp czasu (w sekundach) między kolejnymi zdarzeniami (np. 0.1, 0.05, 0.01). Pozwala symulować różne natężenie strumienia.

- skew_prob – prawdopodobieństwo wystąpienia klucza z zakresu „gorącego” (częstego), np. 0.8. Wyższe wartości oznaczają bardziej skupiony rozkład.

- capacity (w LRUCache) – maksymalna liczba rekordów przetrzymywanych w cache. Im większa, tym mniejsze ryzyko usunięcia często używanych rekordów.

- Rozmiar pliku reference.csv (w data/) – można ręcznie rozszerzyć lub ograniczyć liczbę rekordów referencyjnych (np. 10, 50, 100). Wpływa to na to, czy wszystkie klucze strumienia mają swoje odpowiedniki na „dysku”.

Zmieniając te parametry, możliwe jest przeprowadzenie testów w różnych warunkach (mała lub duża pamięć, szybki lub wolny strumień, skośny lub równomierny rozkład), co umożliwia analizę wpływu konfiguracji na skuteczność pamięci podręcznej i liczbę operacji dyskowych.
