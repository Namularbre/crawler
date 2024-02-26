from datetime import date
from typing import Set

from motor.motor_asyncio import AsyncIOMotorClient

from robot_txt import RobotTxt
from web_page import WebPage


class DBManager:
    __DB_NAME = "crawler"
    __DB_WEB_PAGES_COLLECTION = "web_site"
    __DB_ROBOT_TXT_COLLECTION = "robot_txt"
    __CONN_STR = 'mongodb://crawler:1234@localhost:27017'

    async def __aenter__(self):
        self.mongo_client = AsyncIOMotorClient(self.__CONN_STR)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.mongo_client.close()

    async def create_indexes(self):
        await self.mongo_client[self.__DB_NAME][self.__DB_WEB_PAGES_COLLECTION].create_index([('text', 'text')])
        await self.mongo_client[self.__DB_NAME][self.__DB_WEB_PAGES_COLLECTION].create_index([('url', 1)], unique=True)

    async def insert_web_pages(self, web_pages: Set[dict]) -> None:
        await self.mongo_client[self.__DB_NAME][self.__DB_WEB_PAGES_COLLECTION].insert_many(web_pages)

    async def load_all_urls(self) -> Set[str]:
        urls = await self.mongo_client[self.__DB_NAME][self.__DB_WEB_PAGES_COLLECTION].distinct('url')
        urls_set: Set[str] = set()
        for url in urls:
            urls_set.add(url)
        return urls_set

    async def page_exists_and_is_not_outdated(self, url: str) -> bool:
        today = date.today()
        data = await self.mongo_client[self.__DB_NAME][self.__DB_WEB_PAGES_COLLECTION].find_one(
            {'$and': [
                {'url': url},
                {'createdAt': {'$ne': today}}
            ]})
        return data != {}

    async def insert_blacklisted_url(self, url: str) -> None:
        if not await self.page_exists_and_is_not_outdated(url):
            web_page = WebPage(url, blacklisted=True)
            await self.mongo_client[self.__DB_NAME][self.__DB_WEB_PAGES_COLLECTION].insert_one(web_page.to_dict())

    async def insert_robots_txt(self, robots_txt: RobotTxt) -> None:
        await self.mongo_client[self.__DB_NAME][self.__DB_ROBOT_TXT_COLLECTION].replace_one(
            {"domain": robots_txt.domain},
            robots_txt.to_dict(),
            upsert=True
        )

    async def get_robots_txt(self, domain: str) -> str:
        result = await self.mongo_client[self.__DB_NAME][self.__DB_ROBOT_TXT_COLLECTION].find_one({"domain": domain})
        return result["robots_txt"] if result else None
