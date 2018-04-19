from googlemaps import convert


async def directions(client, origin, destination,
                     mode=None, waypoints=None, alternatives=False,
                     avoid=None, language=None, units=None, region=None,
                     departure_time=None, arrival_time=None,
                     optimize_waypoints=False,
                     transit_routing_preference=None,
                     transit_mode=None,
                     traffic_model=None):

    params = {
        'origin': convert.latlng(origin),
        'destination': convert.latlng(destination)
    }

    if mode:
        # NOTE(broady): the mode parameter is not validated by the Maps API
        # server. Check here to prevent silent failures.
        if mode not in ['driving', 'walking', 'bicycling', 'transit']:
            raise ValueError('Invalid travel mode.')
        params['mode'] = mode

    if waypoints:
        waypoints = convert.location_list(waypoints)
        if optimize_waypoints:
            waypoints = 'optimize:true|' + waypoints
        params['waypoints'] = waypoints

    if alternatives:
        params['alternatives'] = 'true'

    if avoid:
        params['avoid'] = convert.join_list('|', avoid)

    if language:
        params['language'] = language

    if units:
        params['units'] = units

    if region:
        params['region'] = region

    if departure_time:
        params['departure_time'] = convert.time(departure_time)

    if arrival_time:
        params['arrival_time'] = convert.time(arrival_time)

    if departure_time and arrival_time:
        raise ValueError('Should not specify both departure_time and'
                         'arrival_time.')

    if transit_mode:
        params['transit_mode'] = convert.join_list('|', transit_mode)

    if transit_routing_preference:
        params['transit_routing_preference'] = transit_routing_preference

    if traffic_model:
        params['traffic_model'] = traffic_model

    result = await client._request('/maps/api/directions/json', params)
    return result.get('routes', [])
