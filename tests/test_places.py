from operator import itemgetter

import pytest
from aiohttp import web
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
            status=web.HTTPOk.status_code,
            content_type='application/json',
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
            status=web.HTTPOk.status_code,
            content_type='application/json',
        ),
        match_querystring=True,
    )

    resp = await client.places('Google')
    assert resp


async def test_places_radar(aresponses, client, api_key):
    aresponses.add(
        'maps.googleapis.com',
        '/maps/api/place/radarsearch/json',
        'get',
        aresponses.Response(
            body='{"status": "OK"}',
            status=web.HTTPOk.status_code,
            content_type='application/json',
        ),
    )

    resp = await client.places_radar((10, -10), radius=100, keyword='test')
    assert resp


async def test_places_nearby(aresponses, client):
    aresponses.add(
        'maps.googleapis.com',
        '/maps/api/place/nearbysearch/json',
        'get',
        aresponses.Response(
            body='{"status": "OK"}',
            status=web.HTTPOk.status_code,
            content_type='application/json',
        ),
    )

    resp = await client.places_nearby('loc', radius=100)
    assert resp


async def test_places_photo(aresponses, client, api_key):
    aresponses.add(
        'maps.googleapis.com',
        '/maps/api/place/photo',
        'get',
        aresponses.Response(
            body='{"status": "OK"}',
            status=web.HTTPOk.status_code,
            content_type='application/json',
        ),
    )

    resp = await client.places_photo('id', max_width=100)
    assert resp


@pytest.mark.parametrize('query_type,handler', [
    ('', itemgetter('places_autocomplete')),
    ('query', itemgetter('places_autocomplete_query'))
])
async def test_autocomplete(aresponses, client, api_key, query_type, handler):
    patched_url = URL.build(
        path=f'/maps/api/place/{query_type}autocomplete/json',
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
            status=web.HTTPOk.status_code,
            content_type='application/json',
        ),
        match_querystring=True
    )

    places = await handler(client)('Google')
    assert places == ["foo"]
