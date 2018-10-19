from aiohttp import web


async def test_directions(aresponses, client):
    aresponses.add(
        'maps.googleapis.com',
        '/maps/api/directions/json',
        'get',
        aresponses.Response(
            body='{"status": "OK", "routes": ["foo"]}',
            status=web.HTTPOk.status_code,
            content_type='application/json',
        ),
    )

    resp = await client.directions(
        origin=(10, 10),
        destination=(10, 12),
    )
    assert resp
