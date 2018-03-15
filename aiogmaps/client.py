import asyncio

import aiohttp
import async_timeout
from yarl import URL


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
        method='GET', chunked=False, **kwargs,
    ):
        url = self.base_url / route
        base_params = {
            **params,
            'key': self.key,
        }
        async with async_timeout.timeout(self.timeout):
            async with self.session.request(
                method,
                url,
                *args,
                params=base_params,
                **kwargs,
            ) as response:
                if chunked:
                    return response.iter_chunks()

                response = await response.json()
                if response['status'] == 'REQUEST_DENIED':
                    raise aiohttp.web.HTTPBadRequest(
                        reason=response['error_message'],
                    )
                return response

    async def place(self, place_id, language=None):
        query = {'placeid': place_id}
        if language is not None:
            query['language'] = language
        return await self._request('maps/api/place/details/json', query)

    async def places_photo(self, reference, max_width=None, max_height=None):
        query = {'photoreference': reference}
        if not (max_width or max_height):
            raise ValueError('Please provide max_width or max_height')
        return await self._request('maps/api/place/photo', query, chunked=True)

    async def close(self):
        await self.session.close()
