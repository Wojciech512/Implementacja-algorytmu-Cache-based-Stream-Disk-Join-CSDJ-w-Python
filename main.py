import os, logging, csv
from pathlib import Path
from cache import LRUCache
from disk import DiskData
from stream import StreamGenerator
from joiner import StreamDiskJoiner


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    data_path = Path("data") / "reference.csv"
    #Jeśli plik nie istnieje, utwórz przykładowy dataset
    if not data_path.exists():
        with open(data_path, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "name", "age"])
            sample_data = [
                (1, "Alice", 30),
                (2, "Bob", 25),
                (3, "Charlie", 40),
                (4, "Diana", 35),
                (5, "Eve", 28),
                (6, "Frank", 50),
                (7, "Grace", 22),
                (8, "Heidi", 31),
                (9, "Ivan", 29),
                (10, "Judy", 45),
            ]
            for row in sample_data:
                writer.writerow(row)

    #Konfiguracja logowania do pliku
    logging.basicConfig(
        filename="logs/join_process.log",
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filemode="w",
    )
    logging.info("Uruchomienie algorytmu CSDJ z pamięcią LRU")

    #Inicjalizacja obiektów
    disk = DiskData(str(data_path), delay=0.05)  # 50 ms opóźnienia dysku
    cache = LRUCache(capacity=2)  # pojemność cache np. 5 rekordów

    #Utworzenie kolejki i wątków
    stream_queue = __import__("queue").Queue()
    generator = StreamGenerator(
        output_queue=stream_queue, event_count=500, interval=0.05
    )
    joiner = StreamDiskJoiner(input_queue=stream_queue, cache=cache, disk=disk)

    #Start wątków
    generator.start()
    joiner.start()

    #Oczekiwanie na zakończenie wątków
    generator.join()
    joiner.join()
    logging.info("Zakończono działanie.")
