
from googlemaps.distance_matrix import distance_matrix as _distance_matrix


async def distance_matrix(client, origins, destinations,
                          mode=None, language=None, avoid=None, units=None,
                          departure_time=None, arrival_time=None,
                          transit_mode=None, transit_routing_preference=None,
                          traffic_model=None, region=None):

    return await _distance_matrix(
        client, origins, destinations,
        mode=mode, language=language, avoid=avoid, units=units,
        departure_time=departure_time, arrival_time=arrival_time,
        transit_routing_preference=transit_routing_preference,
        traffic_model=traffic_model, region=region,
        transit_mode=transit_mode,
    )
