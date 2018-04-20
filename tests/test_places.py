import urllib

import aresponses
from yarl import URL


async def test_places(aresponses, client, api_key):
    pass


async def test_autocomplete(aresponses, client, api_key):
    location = (-33.86746, 151.207090)
    language = 'en-AU'
    region = 'AU'
    radius = 100

    query = {
        'key': api_key,
        'intput': 'Google',
        'offset': 3,
        'location': '-33.86746,151.20709',
        'radius': 100,
        'language': 'en-AU',
        'types': 'geocode',
        'components': 'country:au',
        'strictbounds': 'true',
    }

    patched_url = URL.build(
        host='maps.googleapis.com',
        path='/maps/api/place/autocomplete/json',
        query=query,
    )

    aresponses.add(
        patched_url.host,
        patched_url.path_qs,
        'get',
        aresponses.Response(
            body='{"status": "OK", "predictions": []}',
            status=200,
            content_type='application/json',
        )
    )

    places = await client.places_autocomplete(
        'Google', offset=3,
        location=location,
        radius=radius,
        language=language,
        types='geocode',
        components={'country': 'au'},
        strict_bounds=True,
    )
    assert places is not None
