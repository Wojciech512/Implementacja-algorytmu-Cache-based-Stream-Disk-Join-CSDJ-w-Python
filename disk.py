# disk.py
import csv
import time


class DiskData:
    def __init__(self, csv_file_path, delay: float = 0.01):
        self.csv_file_path = csv_file_path
        self.delay = delay
        with open(csv_file_path, mode="r", newline="") as f:
            reader = csv.reader(f)
            self.header = next(reader, None)

    def lookup(self, key):
        #użyj opóźnienia ustawionego przy tworzeniu obiektu
        time.sleep(self.delay)

        with open(self.csv_file_path, mode="r", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) > 0 and str(row[0]) == str(key):
                    if self.header:
                        return {self.header[i]: row[i] for i in range(len(row))}
                    return row
        return None
