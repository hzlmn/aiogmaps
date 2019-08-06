import asyncio
import logging
import re

import aiohttp
import googlemaps
from yarl import URL

from . import __version__
from .directions import directions
from .distance_matrix import distance_matrix
from .elevation import elevation, elevation_along_path
from .geocoding import geocode, reverse_geocode
from .geolocation import geolocate
from .places import (place, places, places_autocomplete,  # noqa
                     places_autocomplete_query, places_nearby, places_photo,
                     places_radar, find_place)
from .roads import (nearest_roads, snap_to_roads, snapped_speed_limits,
                    speed_limits)
from .timezone import timezone

logger = logging.getLogger('aiogmaps')

aiohttp3 = aiohttp.__version__.startswith('3.')


class Client:
    def __init__(self, key=None, client_id=None, client_secret=None,
                 session=None, close_session=False, verify_ssl=True,
                 request_timeout=10, channel=None, loop=None):
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

        if channel:
            if not client_id:
                raise ValueError("The channel argument must be used with a "
                                 "client ID")
            if not re.match("^[a-zA-Z0-9._-]*$", channel):
                raise ValueError("The channel argument must be an ASCII "
                                 "alphanumeric string. "
                                 "The period (.), underscore (_)"
                                 "and hyphen (-) characters are allowed.")
        self.channel = channel

        self.close_session = close_session
        self.verify_ssl = verify_ssl

        if session is None:
            if aiohttp3:
                session = aiohttp.ClientSession(loop=self.loop)
            else:
                session = aiohttp.ClientSession(
                    connector=aiohttp.TCPConnector(
                        loop=self.loop,
                        verify_ssl=self.verify_ssl,
                    )
                )
            self.close_session = True

        self.session = session

        self.base_url = URL('https://maps.googleapis.com')
        self._user_agent = 'AsyncGoogleGeoApiClientPython/{}'.format(
            __version__)
        self._headers = {
            'User-Agent': self._user_agent,
        }

    def __getitem__(self, name):
        return getattr(self, name)

    async def _request(
        self,
        url,
        params,
        data=None,
        base_url=None,
        extract_body=None,
        method='GET',
        chunked=False,
        accepts_clientid=True,
        post_json=None,
        **kwargs
    ):
        if extract_body and not callable(extract_body):
            raise TypeError('extract_body should be callable')

        if not (base_url and isinstance(base_url, (str, URL))):
            base_url = self.base_url

        base_url = URL(base_url)
        authed_url = googlemaps.Client._generate_auth_url(
            self, '/' + url.lstrip('/'), params, accepts_clientid
        )

        if aiohttp3:
            # https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientSession.request
            kwargs.update({'ssl': self.verify_ssl})

        combined_url = URL(str(base_url) + authed_url, encoded=True)

        if post_json is not None:
            method = 'POST'
            data = post_json
        try:
            response = await self.session.request(
                method,
                combined_url,
                data=data,
                headers=self._headers,
                timeout=self.request_timeout,
                **kwargs,
            )
        except aiohttp.ClientError as exc:
            logger.exception(exc, exc_info=exc)
            raise

        if chunked:
            return response.content.iter_chunks()

        if extract_body is not None:
            result = extract_body(response)
            if asyncio.iscoroutine(result):
                result = await result
        else:
            result = await self._get_body(response)

        return result

    async def _get_body(self, response):
        if response.status != 200:
            raise googlemaps.exceptions.HTTPError(response.status)

        body = await response.json()

        api_status = body['status']
        if api_status == 'OK' or api_status == 'ZERO_RESULTS':
            return body

        if api_status == 'OVER_QUERY_LIMIT':
            raise googlemaps.exceptions._OverQueryLimit(
                api_status, body.get('error_message'))

        raise googlemaps.exceptions.ApiError(api_status,
                                             body.get('error_message'))

    async def close(self):
        if self.close_session:
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
Client.places_autocomplete_query = places_autocomplete_query
Client.places_photo = places_photo
Client.places_radar = places_radar
Client.find_place = find_place

# Roads API
Client.speed_limits = speed_limits
Client.nearest_roads = nearest_roads
Client.snap_to_roads = snap_to_roads
Client.snapped_speed_limits = snapped_speed_limits

# Timezone API
Client.timezone = timezone

# Directions API
Client.directions = directions

Client.distance_matrix = distance_matrix

Client.elevation = elevation
Client.elevation_along_path = elevation_along_path

Client.geocode = geocode
Client.reverse_geocode = reverse_geocode

Client.geolocate = geolocate
