from typing import List, Set

from web_page import WebPage


class WebPageSet:
    def __init__(self) -> None:
        self.web_pages: Set[WebPage] = set()

    def add(self, web_page: WebPage) -> None:
        if web_page not in self.web_pages:
            self.web_pages.add(web_page)

    def clear(self) -> None:
        self.web_pages = set()

    def union(self, other: Set[WebPage]) -> None:
        self.web_pages = self.web_pages.union(other)

    def size_is_100(self) -> bool:
        return len(self.web_pages) == 100

    def to_dict_list(self) -> List[dict]:
        web_pages_dict_list: List[dict] = []
        for web_page in self.web_pages:
            web_pages_dict_list.append(web_page.to_dict())
        return web_pages_dict_list

    def __len__(self) -> int:
        return len(self.web_pages)
