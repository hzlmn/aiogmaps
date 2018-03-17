import asyncio

import aiohttp
import async_timeout
from yarl import URL

from .places import (place, places_autocomplete, places_nearby, places_photo,
                     places_radar)


class Client:
    def __init__(self, key, loop=None, session=None, timeout=10):
        if loop is None:
            loop = asyncio.get_event_loop()
        self.loop = loop

        if not isinstance(key, str):
            raise ValueError('Google Maps API key should be provided')

        self.key = key
        self.base_url = URL('https://maps.googleapis.com/')
        self._response_type = 'json'
        self.timeout = timeout

        if session is None:
            session = aiohttp.ClientSession(loop=loop)
        self.session = session

    async def _request(
        self, route, params, *args,
        method='GET', chunked=False, **kwargs
    ):
        base_params = {
            **params,
            'key': self.key,
        }
        async with async_timeout.timeout(self.timeout):
            async with self.session.request(
                method,
                self.base_url / route.lstrip('/'),
                *args,
                params=base_params,
                **kwargs,
            ) as response:
                if chunked:
                    return response.content.iter_chunks()

                response = await response.json()
                if response['status'] == 'REQUEST_DENIED':
                    raise aiohttp.web.HTTPBadRequest(
                        reason=response['error_message'],
                    )
                return response

    async def close(self):
        await self.session.close()


# Places API
Client.place = place
Client.places_nearby = places_nearby
Client.places_autocomplete = places_autocomplete
Client.places_photo = places_photo
Client.places_radar = places_radar
