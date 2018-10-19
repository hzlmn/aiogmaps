from aiohttp import web


async def test_geolocate(aresponses, client):
    aresponses.add(
        'www.googleapis.com',
        '/geolocation/v1/geolocate',
        'post',
        aresponses.Response(
            body='{"status": "OK"}',
            status=web.HTTPOk.status_code,
            content_type='application/json',
        )
    )

    resp = await client.geolocate()
    assert resp
