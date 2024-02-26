from urllib.parse import urlparse, urljoin

import aiohttp

from crawler_http import get
from database import DBManager
from printerr import print_err
from robot_txt import RobotTxt


def get_robot_txt_url(url: str) -> str:
    parsed_url = urlparse(url)
    domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return urljoin(domain, "/robots.txt")


async def is_allowed_by_robots_txt(session: aiohttp.ClientSession, url: str) -> bool:
    async with DBManager() as db_manager:
        try:
            parsed_url = urlparse(url)
            domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
            saved_robots_txt = await db_manager.get_robots_txt(domain)
            if saved_robots_txt is not None:
                robots_txt = saved_robots_txt
            else:
                robots_url = get_robot_txt_url(url)
                robots_txt: str | None = await get(robots_url, session)
                if robots_txt:
                    print(f"Saved robot.txt from url: {robots_url}")
                    await db_manager.insert_robots_txt(RobotTxt(domain=domain, robots_txt=robots_txt))
                else:
                    return False

            for line in robots_txt.split('\n'):
                if line.startswith('Disallow:') and len(line.split(': ')) >= 2:
                    disallowed_path = line.split(': ')[1]
                    if disallowed_path == '/' or url.startswith(disallowed_path):
                        return False
            return True
        except ConnectionError as e:
            print_err(e)
            return False
