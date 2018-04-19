from googlemaps import convert


async def geocode(client, address=None, components=None,
                  bounds=None, region=None,
                  language=None):

    params = {}

    if address:
        params['address'] = address

    if components:
        params['components'] = convert.components(components)

    if bounds:
        params['bounds'] = convert.bounds(bounds)

    if region:
        params['region'] = region

    if language:
        params['language'] = language

    result = await client._request('/maps/api/geocode/json', params)
    return result.get('results', [])


async def reverse_geocode(client, latlng, result_type=None, location_type=None,
                          language=None):

    if convert.is_string(latlng) and ',' not in latlng:
        params = {'place_id': latlng}
    else:
        params = {'latlng': convert.latlng(latlng)}

    if result_type:
        params['result_type'] = convert.join_list('|', result_type)

    if location_type:
        params['location_type'] = convert.join_list('|', location_type)

    if language:
        params['language'] = language

    result = await client._request('/maps/api/geocode/json', params)
    return result.get('results', [])
