from aiohttp import web


async def test_distance_matrix(aresponses, client):
    aresponses.add(
        'maps.googleapis.com',
        '/maps/api/distancematrix/json',
        'get',
        aresponses.Response(
            body='{"status": "OK"}',
            status=web.HTTPOk.status_code,
            content_type='application/json',
        ),
    )

    resp = await client.distance_matrix([], [])
    assert resp
