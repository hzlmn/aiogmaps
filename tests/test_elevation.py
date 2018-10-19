from aiohttp import web


async def test_elevation(aresponses, client):
    aresponses.add(
        'maps.googleapis.com',
        '/maps/api/elevation/json',
        'get',
        aresponses.Response(
            body='{"status": "OK", "results": ["foo"]}',
            status=web.HTTPOk.status_code,
            content_type='application/json',
        ),
    )

    resp = await client.elevation([])
    assert resp == ['foo']


async def test_elevation_along_path(aresponses, client):
    aresponses.add(
        'maps.googleapis.com',
        '/maps/api/elevation/json',
        'get',
        aresponses.Response(
            body='{"status": "OK", "results": ["foo"]}',
            status=web.HTTPOk.status_code,
            content_type='application/json',
        ),
    )

    resp = await client.elevation_along_path('', '')
    assert resp == ['foo']
