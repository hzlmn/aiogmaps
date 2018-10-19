from aiohttp import web


async def test_snap_to_roads(aresponses, client):
    aresponses.add(
        'roads.googleapis.com',
        '/v1/snapToRoads',
        'get',
        aresponses.Response(
            body='{"status": "OK", "snappedPoints": ["foo"]}',
            status=web.HTTPOk.status_code,
            content_type='application/json',
        ),
    )

    resp = await client.snap_to_roads('')
    assert resp == ['foo']


async def test_nearest_roads(aresponses, client):
    aresponses.add(
        'roads.googleapis.com',
        '/v1/nearestRoads',
        'get',
        aresponses.Response(
            body='{"status": "OK", "snappedPoints": ["foo"]}',
            status=web.HTTPOk.status_code,
            content_type='application/json',
        ),
    )

    resp = await client.nearest_roads('')
    assert resp == ['foo']


async def test_speed_limits(aresponses, client):
    aresponses.add(
        'roads.googleapis.com',
        '/v1/speedLimits',
        'get',
        aresponses.Response(
            body='{"status": "OK", "speedLimits": ["foo"]}',
            status=web.HTTPOk.status_code,
            content_type='application/json',
        ),
    )

    resp = await client.speed_limits('')
    assert resp == ["foo"]


async def test_snapped_speed_limits(aresponses, client):
    aresponses.add(
        'roads.googleapis.com',
        '/v1/speedLimits',
        'get',
        aresponses.Response(
            body='{"status": "OK", "speedLimits": ["foo"]}',
            status=web.HTTPOk.status_code,
            content_type='application/json',
        ),
    )

    resp = await client.snapped_speed_limits('')
    assert resp
