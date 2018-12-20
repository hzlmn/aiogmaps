from aiohttp import web
from googlemaps.client import sign_hmac, urlencode_params

import aiogmaps


async def test_url_signed(aresponses):
    client_id = "foo"
    client_secret = "test"
    address = "Test St."
    client = aiogmaps.Client(client_id=client_id, client_secret=client_secret)
    params = {
        'address': address,
        'client': client_id
    }
    path = "?".join(['/maps/api/geocode/json', urlencode_params(params.items())])
    expected_signature = sign_hmac(client_secret, path)
    aresponses.add(
        'maps.googleapis.com',
        path + '{}{}'.format('&signature=', expected_signature),
        'get',
        aresponses.Response(
            body='{"status": "OK", "results": ["foo"]}',
            status=web.HTTPOk.status_code,
            content_type='application/json',
        ),
        match_querystring=True,
    )
    resp = await client.geocode(address)
    assert resp == ['foo']
