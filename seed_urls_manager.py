import csv
from typing import Set


class SeedUrlsManager:
    def __init__(self) -> None:
        self.__seed_urls: Set[str] = set()

    def load(self) -> Set[str]:
        self.__load_from_csv()
        return self.__seed_urls

    def __load_from_csv(self) -> None:
        with open('seed_urls.csv', 'r') as f:
            reader = csv.reader(f)
            for line in reader:
                url = line[0]
                self.__seed_urls.add(url)
