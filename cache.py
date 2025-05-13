from collections import OrderedDict


class LRUCache:
    """Prosta implementacja pamięci podręcznej LRU o ustalonej pojemności."""

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        """
        Pobiera wartość z cache na podstawie klucza.
        Zwraca wartość, jeśli jest w cache (odświeżając położenie jako najnowsze użycie),
        lub None, jeśli klucza brak w pamięci podręcznej.
        """
        if key in self.cache:
            #przeniesienie użytego elementu na koniec (jako najświeższy)
            value = self.cache.pop(key)
            self.cache[key] = value
            return value
        return None

    def put(self, key, value):
        """
        Umieszcza parę (klucz, wartość) w pamięci podręcznej.
        Jeśli klucz już istniał, jego wartość jest aktualizowana i oznaczana jako najświeższa.
        Jeśli cache jest pełny, usuwany jest najdawniej używany element (LRU).
        """
        if key in self.cache:
            #usuń stary wpis (będzie ponownie dodany jako najnowszy poniżej)
            self.cache.pop(key)
        elif len(self.cache) >= self.capacity:
            #usunięcie najrzadziej używanego (pierwszego) elementu
            self.cache.popitem(last=False)
        # dodanie nowego elementu jako najświeższego
        self.cache[key] = value
