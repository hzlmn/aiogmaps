from aiohttp import web


async def test_geocode(aresponses, client):
    aresponses.add(
        'maps.googleapis.com',
        '/maps/api/geocode/json',
        'get',
        aresponses.Response(
            body='{"status": "OK", "results": ["foo"]}',
            status=web.HTTPOk.status_code,
            content_type='application/json',
        ),
    )

    resp = await client.geocode()
    assert resp == ['foo']


async def test_reverse_geocode(aresponses, client):
    aresponses.add(
        'maps.googleapis.com',
        '/maps/api/geocode/json',
        'get',
        aresponses.Response(
            body='{"status": "OK", "results": ["foo"]}',
            status=web.HTTPOk.status_code,
            content_type='application/json',
        ),
    )

    resp = await client.reverse_geocode((10, 10))
    assert resp == ['foo']
