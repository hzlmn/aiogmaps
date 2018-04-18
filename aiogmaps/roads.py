import googlemaps
from googlemaps import convert
from googlemaps.roads import _ROADS_BASE_URL


async def snap_to_roads(client, path, interpolate=False):
    params = {'path': convert.location_list(path)}

    if interpolate:
        params['interpolate'] = 'true'

    result = await client._request(
        '/v1/snapToRoads',
        params,
        base_url=_ROADS_BASE_URL,
        accepts_clientid=False,
        extract_body=_roads_extract,
    )

    return result.get('snappedPoints', [])


async def nearest_roads(client, points):
    params = {'points': convert.location_list(points)}

    result = await client._request(
        '/v1/nearestRoads',
        params,
        base_url=_ROADS_BASE_URL,
        accepts_clientid=False,
        extract_body=_roads_extract,
    )

    return result.get('snappedPoints', [])


async def speed_limits(client, place_ids):
    params = [('placeId', place_id) for place_id in convert.as_list(place_ids)]

    result = await client._request(
        '/v1/speedLimits',
        params,
        base_url=_ROADS_BASE_URL,
        accepts_clientid=False,
        extract_body=_roads_extract,
    )

    return result.get('speedLimits', [])


async def snapped_speed_limits(client, path):
    params = {'path': convert.location_list(path)}

    return await client._request(
        '/v1/speedLimits',
        params,
        base_url=_ROADS_BASE_URL,
        accepts_clientid=False,
        extract_body=_roads_extract,
    )


async def _roads_extract(response):
    try:
        result = await response.json()
    except Exception:
        if response.status != 200:
            raise googlemaps.exceptions.HTTPError(response.status)

        raise googlemaps.exceptions.ApiError('UNKNOWN_ERROR',
                                             'Received a malformed response.')

    if 'error' in result:
        error = result['error']
        status = error['status']

        if status == 'RESOURCE_EXHAUSTED':
            raise googlemaps.exceptions._OverQueryLimit(status,
                                                        error.get('message'))

        raise googlemaps.exceptions.ApiError(status, error.get('message'))

    if response.status != 200:
        raise googlemaps.exceptions.HTTPError(response.status_code)

    return result
