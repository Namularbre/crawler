from typing import Set
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import re


async def get_next_urls(soup: BeautifulSoup, url: str) -> Set[str]:
    anchor_tags = soup.find_all('a', href=True)
    next_urls: Set[str] = set()
    for anchor in anchor_tags:
        next_url: str = urljoin(url, anchor['href'])
        if next_url.endswith('/'):
            next_url = next_url[:-1]
        next_urls.add(next_url.lower())
    return next_urls


async def get_html_text(soup: BeautifulSoup) -> str:
    text_content = '\n'.join([p.get_text() for p in
                              soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'div'],
                                            text=True)])
    return (re.sub('\s+', ' ', text_content)
            .strip()
            .lower())
