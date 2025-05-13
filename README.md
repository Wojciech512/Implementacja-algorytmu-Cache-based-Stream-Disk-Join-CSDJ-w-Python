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
