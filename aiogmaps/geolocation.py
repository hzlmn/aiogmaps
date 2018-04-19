from googlemaps import exceptions
from googlemaps.geolocation import _GEOLOCATION_BASE_URL


async def _geolocation_extract(response):
    body = await response.json()
    if response.status in (200, 404):
        return body

    try:
        error = body['error']['errors'][0]['reason']
    except KeyError:
        error = None

    if response.status == 403:
        raise exceptions._OverQueryLimit(response.status, error)
    else:
        raise exceptions.ApiError(response.status, error)


async def geolocate(client, home_mobile_country_code=None,
                    home_mobile_network_code=None, radio_type=None,
                    carrier=None, consider_ip=None, cell_towers=None,
                    wifi_access_points=None):
    params = {}
    if home_mobile_country_code is not None:
        params['homeMobileCountryCode'] = home_mobile_country_code
    if home_mobile_network_code is not None:
        params['homeMobileNetworkCode'] = home_mobile_network_code
    if radio_type is not None:
        params['radioType'] = radio_type
    if carrier is not None:
        params['carrier'] = carrier
    if consider_ip is not None:
        params['considerIp'] = consider_ip
    if cell_towers is not None:
        params['cellTowers'] = cell_towers
    if wifi_access_points is not None:
        params['wifiAccessPoints'] = wifi_access_points

    return await client._request(
        '/geolocation/v1/geolocate',
        {},  # No GET params
        base_url=_GEOLOCATION_BASE_URL,
        extract_body=_geolocation_extract,
        post_json=params,
    )
