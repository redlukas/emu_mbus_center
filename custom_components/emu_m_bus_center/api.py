"""Sample API Client."""
import asyncio
import logging
import socket

import aiohttp
import async_timeout

TIMEOUT = 10


_LOGGER: logging.Logger = logging.getLogger(__package__)

HEADERS = {"Content-type": "application/json; charset=UTF-8"}


class EmuMBusCenterApiClient:
    def __init__(self, ip: str, session: aiohttp.ClientSession) -> None:
        """Sample API Client."""
        self._ip = ip
        self._session = session

    async def async_get_data(self) -> dict:
        """Get data from the API."""
        return await self.api_wrapper("get", self._ip)

    async def async_test_center_ip(self) -> dict:
        """test if there is an M-Bus Center Listening on this IP"""
        return await self.api_wrapper("get", self._ip)

    async def async_get_device_data(self, number: int) -> dict:
        """test if there is an M-Bus Center Listening on this IP"""
        return await self.api_wrapper(
            "get", f"http://${self._ip}/app/api/id/${number}.json"
        )

    async def async_set_title(self, value: str) -> None:
        """Get data from the API."""
        url = "https://jsonplaceholder.typicode.com/posts/1"
        await self.api_wrapper("patch", url, data={"title": value}, headers=HEADERS)

    async def api_wrapper(
        self, method: str, url: str, data: dict = {}, headers: dict = {}
    ) -> dict:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(TIMEOUT, loop=asyncio.get_event_loop()):
                if method == "get":
                    response = await self._session.get(url, headers=headers)
                    return await response.json()

                elif method == "put":
                    await self._session.put(url, headers=headers, json=data)

                elif method == "patch":
                    await self._session.patch(url, headers=headers, json=data)

                elif method == "post":
                    await self._session.post(url, headers=headers, json=data)

        except asyncio.TimeoutError as exception:
            _LOGGER.error(
                "Timeout error fetching information from %s - %s",
                url,
                exception,
            )

        except (KeyError, TypeError) as exception:
            _LOGGER.error(
                "Error parsing information from %s - %s",
                url,
                exception,
            )
        except (aiohttp.ClientError, socket.gaierror) as exception:
            _LOGGER.error(
                "Error fetching information from %s - %s",
                url,
                exception,
            )
        except Exception as exception:  # pylint: disable=broad-except
            _LOGGER.error("Something really wrong happened! - %s", exception)
