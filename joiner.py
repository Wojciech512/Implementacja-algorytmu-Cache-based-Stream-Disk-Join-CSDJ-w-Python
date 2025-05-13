import threading, logging
from queue import Queue
from cache import LRUCache
from disk import DiskData


class StreamDiskJoiner(threading.Thread):
    """
    Wątek łączący dane strumieniowe z danymi dyskowymi przy użyciu pamięci podręcznej.
    Pobiera elementy strumienia z kolejki, dla każdego wykonuje operację join i zapisuje wynik.
    """

    def __init__(
        self,
        input_queue: Queue,
        cache: LRUCache,
        disk: DiskData,
        join_condition: str = "==",
        output_queue: Queue = None,
        name: str = "Joiner",
    ):
        """
        input_queue: kolejka wejściowa (z elementami strumienia do przetworzenia).
        cache: obiekt LRUCache do przechowywania ostatnio użytych rekordów dyskowych.
        disk: obiekt DiskData do odczytu danych z pliku CSV.
        join_condition: warunek łączenia ('==' domyślnie). Inne wartości mogą być '!=', '>=', itp. (rozszerzenie funkcjonalności).
        output_queue: opcjonalna kolejka wyjściowa na wyniki join (jeśli chcemy dalej je przetwarzać w innym wątku).
        """
        super().__init__(name=name, daemon=True)
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.cache = cache
        self.disk = disk
        self.join_condition = join_condition

    def run(self):
        """Uruchamia pętlę do przetwarzania elementów strumienia z kolejki."""
        while True:
            item = self.input_queue.get()
            if item is None:
                # None jako sygnał zakończenia
                logging.info("Joiner: otrzymano sygnał zakończenia. Kończę działanie.")
                if self.output_queue:
                    self.output_queue.put(None)
                break
            # Zakładamy, że item jest słownikiem zawierającym klucz 'id'
            key = item.get("id")
            if key is None:
                # jeśli z jakiegoś powodu brak klucza, pomijamy
                logging.warning("Joiner: element strumienia bez klucza 'id': %s", item)
                continue
            # sprawdzenie w cache
            result_record = self.cache.get(key)
            if result_record:
                source = "cache"
            else:
                # odczyt z 'dysku'
                result_record = self.disk.lookup(key)
                source = "disk"
                # wstaw do cache (nawet jeśli result_record jest None, zapisujemy None by nie ponawiać odczytu w krótkim czasie)
                self.cache.put(key, result_record)
            # złączenie danych jeśli znaleziono
            if result_record:
                # scal dwa słowniki: dane strumienia + dane referencyjne
                joined = {**item, **result_record}
                logging.info(f"Join hit ({source}): %s -> %s", item, joined)
                if self.output_queue:
                    self.output_queue.put(joined)
            else:
                # brak dopasowania w danych dyskowych
                logging.info(f"Join miss ({source}): %s -> BRAK DOPASOWANIA", item)
                if self.output_queue:
                    self.output_queue.put(item)
