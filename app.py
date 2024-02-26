import asyncio

from crawler import Crawler
from seed_urls_manager import SeedUrlsManager


async def main(crawler: Crawler):
    try:
        seed_urls_manager = SeedUrlsManager()
        seed_urls = seed_urls_manager.load()
        tasks = [crawler.web_crawler(url) for url in seed_urls]
        await asyncio.gather(*tasks)
    except asyncio.TimeoutError as e:
        await crawler.save_web_pages()
        print(e)


if __name__ == '__main__':
    crawler = Crawler()
    asyncio.run(main(crawler))
