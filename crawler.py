from typing import Set

import aiohttp
from bs4 import BeautifulSoup

from crawler_http import get
from database import DBManager
from printerr import print_err
from scrapping import get_html_text, get_next_urls
from url_tools import is_allowed_by_robots_txt
from web_page import WebPage
from web_page_set import WebPageSet


class Crawler:
    def __init__(self) -> None:
        self.visited_urls: Set[str] = set()
        self.visited_web_pages: WebPageSet = WebPageSet()

    async def __load_urls(self) -> None:
        async with DBManager() as db_manager:
            self.visited_urls = await db_manager.load_all_urls()
            if len(self.visited_urls) != 0:
                print('Previous urls loaded')

    async def url_is_valid(self, session: aiohttp.ClientSession, url: str) -> bool:
        return not await is_allowed_by_robots_txt(session, url) and not await self.url_is_already_saved(url)

    async def explore_url(self, session: aiohttp.ClientSession, url: str) -> Set[str]:
        if await self.url_is_valid(session, url):
            html: str | None = await get(url, session)

            if html is not None:
                soup = BeautifulSoup(html, 'html.parser')
                cleaned_text = await get_html_text(soup)
                if len(cleaned_text) != 0:
                    web_page = WebPage(url=url, content=cleaned_text)
                    print(web_page, len(self.visited_web_pages))
                    self.visited_web_pages.add(web_page)
                    if self.visited_web_pages.size_is_100():
                        await self.save_web_pages()
                self.visited_urls.add(url)
                return await get_next_urls(soup, url)
            else:
                await self.save_blacklisted_page(url, None)
        else:
            await self.save_blacklisted_page(url, None)
        return set()

    async def web_crawler(self, url) -> None:
        async with aiohttp.ClientSession() as session:
            urls: Set[str] = await self.explore_url(session, url)
            while not len(urls) == 0:
                for url in urls:
                    new_urls: Set[str] = await self.explore_url(session, url)
                    urls = urls.union(new_urls)

    async def save_web_pages(self) -> None:
        async with DBManager() as db_manager:
            try:
                await db_manager.insert_web_pages(self.visited_web_pages.to_dict_list())
                self.visited_web_pages.clear()
            except ConnectionError as e:
                print_err(e)

    async def url_is_already_saved(self, url: str) -> bool:
        return url in self.visited_urls

    async def save_blacklisted_page(self, url: str, e: Exception | None) -> None:
        async with DBManager() as db_manager:
            try:
                if e:
                    print_err(e)
                await db_manager.insert_blacklisted_url(url)
            except ConnectionError as ce:
                print_err(ce)
