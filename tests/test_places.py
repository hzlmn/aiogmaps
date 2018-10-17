import urllib

import aresponses
from yarl import URL


async def test_place(aresponses, client, api_key):
    place_id = 'placeid'

    patched_url = URL.build(
        path='/maps/api/place/details/json',
        query={
            'key': api_key,
            'placeid': place_id,
        },
    )

    aresponses.add(
        'maps.googleapis.com',
        patched_url.human_repr(),
        'get',
        aresponses.Response(
            body='{"status": "OK"}',
            status=200,
            content_type='application/json'
        ),
        match_querystring=True,
    )

    resp = await client.place(place_id)
    assert resp


async def test_places(aresponses, client, api_key):
    patched_url = URL.build(
        path='/maps/api/place/textsearch/json',
        query={
            'key': api_key,
            'minprice': 0,
            'maxprice': 4,
            'query': 'Google',
        },
    )

    aresponses.add(
        'maps.googleapis.com',
        patched_url.human_repr(),
        'get',
        aresponses.Response(
            body='{"status": "OK"}',
            status=200,
            content_type='application/json'
        ),
        match_querystring=True
    )

    resp = await client.places('Google')
    assert resp


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
