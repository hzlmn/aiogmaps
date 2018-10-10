import urllib

import aresponses
from yarl import URL


async def test_autocomplete(aresponses, client, api_key):
    patched_url = URL.build(
        path='/maps/api/place/autocomplete/json',
        query={
            'key': api_key,
            'input': 'Google',
        },
    )

    aresponses.add(
        'maps.googleapis.com',
        patched_url.human_repr(),
        'get',
        aresponses.Response(
            body='{"status": "OK", "predictions": ["foo"]}',
            status=200,
            content_type='application/json',
        ),
        match_querystring=True
    )

    places = await client.places_autocomplete('Google')
    assert places == ["foo"]
