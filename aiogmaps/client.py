import asyncio

import aiohttp
import async_timeout
from aiohttp import web
from yarl import URL

from . import __version__
from .places import (place, places, places_autocomplete,  # noqa
                     places_autocomplete_query, places_nearby, places_photo,
                     places_radar)


class Client:
    def __init__(self, key=None, client_id=None, client_secret=None,
                 session=None, verify_ssl=True, request_timeout=10,
                 loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()

        self.loop = loop

        if not key and not (client_secret and client_id):
            raise ValueError('Must provide API key or enterprise credentials '
                             'when creating client.')

        if key and not key.startswith('AIza'):
            raise ValueError('Invalid API key provided.')

        self.key = key
        self.client_id = client_id
        self.client_secret = client_secret
        self.request_timeout = request_timeout

        if session is None:
            session = aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(
                    use_dns_cache=True,
                    loop=loop,
                    verify_ssl=verify_ssl,
                )
            )

        self.session = session

        self.base_url = URL('https://maps.googleapis.com/')
        self._user_agent = 'AsyncGoogleGeoApiClientPython/{}'.format(
            __version__)
        self._headers = {
            'User-Agent': self._user_agent,
        }

    def _get_params(self, params, accepts_clientid=False):
        if accepts_clientid and self.client_id and self.client_secret:
            raise NotImplementedError

        if self.key is not None:
            return {'key': self.key, **params}

    async def _request(self, url, params, base_url=None,
                       method='GET', chunked=False, **kwargs):

        # ? can we use URL here
        if not (base_url and isinstance(base_url, (str, URL))):
            base_url = self.base_url

        params = self._get_params(params)

        async with async_timeout.timeout(self.request_timeout):
            # import pdb; pdb.set_trace()
            async with self.session.request(
                method,
                self.base_url / url.lstrip('/'),
                params=params,
                headers=self._headers,
                **kwargs,
            ) as response:
                if chunked:
                    return response.content.iter_chunks()

                response = await response.json()

                if response['status'] == 'REQUEST_DENIED':
                    raise web.HTTPBadRequest(reason=response['error_message'])

                return response

    async def close(self):
        await self.session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc_info):
        await self.close()


# Places API
Client.place = place
Client.places = places
Client.places_nearby = places_nearby
Client.places_autocomplete = places_autocomplete
Client.places_photo = places_photo
Client.places_radar = places_radar
