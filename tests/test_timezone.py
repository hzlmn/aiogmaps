from yarl import URL


async def test_timezone(aresponses, client, api_key):
    location = (39.603481, -119.682251)
    timestamp = 1331766000

    patched_path = URL.build(
        path='/maps/api/timezone/json',
        query={
            'location': '{},{}'.format(*location),
            'timestamp': timestamp,
            'key': api_key
        },
    )

    aresponses.add(
        'maps.googleapis.com',
        patched_path.human_repr(),
        'get',
        aresponses.Response(
            body='{"status": "OK"}',
            status=200,
            content_type='application/json',
        ),
        match_querystring=True,
    )

    resp = await client.timezone(location, timestamp)
    assert resp['status'] == 'OK'
