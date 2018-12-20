from aiohttp import web
from googlemaps.client import sign_hmac, urlencode_params

import aiogmaps


async def test_url_signed(aresponses, enterprise_client, credentials):
    address = 'Test St.'
    params = {
        'address': address,
        'client': credentials['client_id']
    }

    path = '?'.join(['/maps/api/geocode/json',
                     urlencode_params(params.items())])
    expected_signature = sign_hmac(credentials['client_secret'], path)

    aresponses.add(
        'maps.googleapis.com',
        path + '&signature={}'.format(expected_signature),
        'get',
        aresponses.Response(
            body='{"status": "OK", "results": ["foo"]}',
            status=web.HTTPOk.status_code,
            content_type='application/json',
        ),
        match_querystring=True,
    )
    resp = await enterprise_client.geocode(address)
    assert resp == ['foo']
