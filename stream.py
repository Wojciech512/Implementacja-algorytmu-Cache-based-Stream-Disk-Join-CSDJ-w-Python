import threading, time, random
from queue import Queue


class StreamGenerator(threading.Thread):
    """Wątek generujący dane strumieniowe i umieszczający je w kolejce."""

    def __init__(
        self,
        output_queue: Queue,
        event_count: int = 100,
        interval: float = 0.1,
        skew_prob: float = 0.5,
        name: str = "StreamGenerator",
    ):
        """
        output_queue: kolejka, do której będą wrzucane wygenerowane elementy strumienia.
        event_count: opcjonalnie, liczba zdarzeń do wygenerowania (None oznacza strumień nieskończony).
        interval: odstęp czasu (sekundy) między kolejnymi wygenerowanymi zdarzeniami.
        """
        super().__init__(name=name, daemon=True)
        self.output_queue = output_queue
        self.event_count = event_count
        self.interval = interval
        self.skew = skew_prob
        self.generated = 0  # licznik wygenerowanych zdarzeń

    def run(self):
        """Uruchamia generowanie strumienia w osobnym wątku."""
        # Przykładowo generujemy zdarzenia z losowym kluczem i wartością
        # Zakładamy, że klucze referencyjne to liczby całkowite np. 1-100
        # aby zasymulować częste powtórzenia, generujemy więcej zdarzeń dla mniejszych kluczy (skewed distribution)
        while self.event_count is None or self.generated < self.event_count:
            # losowy klucz (np. 80% szans na zakres 1-10, 20% na zakres 11-20)
            if random.random() < self.skew:
                key = random.randint(1, 10)
            else:
                key = random.randint(11, 20)
            value = random.random()  # jakaś przykładowa wartość (np. pomiar, cena itp.)
            event = {"id": key, "value": value}
            # wstawienie do kolejki
            self.output_queue.put(event)
            self.generated += 1
            # opcjonalne opóźnienie symulujące czas między przybyciem zdarzeń
            time.sleep(self.interval)
        # po wygenerowaniu określonej liczby zdarzeń, wysyłamy sygnał 'None' oznaczający koniec strumienia
        self.output_queue.put(None)
