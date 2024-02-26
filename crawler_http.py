from asyncio import TimeoutError
from aiohttp import ClientSession, ClientError, ClientConnectionError, ServerDisconnectedError
from aiohttp.client_exceptions import ClientConnectorCertificateError


def is_https(url: str) -> bool:
    return url.startswith('https://')


async def get(url: str, session: ClientSession) -> str | None:
    if is_https(url):
        headers = {'User-Agent': 'Custom Web Crawler/v0.0.1-indev'}
        async with session.get(url, timeout=30, headers=headers) as response:
            try:
                response.raise_for_status()
                text: str = await response.text()
                return text
            except UnicodeDecodeError as e:
                print(e)
                return None
            except ClientConnectionError as e:
                print(e)
                return None
            except ClientError as e:
                print(e)
                return None
            except TimeoutError as e:
                print(e)
                return None
            except ClientConnectorCertificateError as e:
                print(e)
                return None
            except ServerDisconnectedError as e:
                print(e)
                return None
    else:
        return None
