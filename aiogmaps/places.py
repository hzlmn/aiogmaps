import googlemaps.places as places_
from googlemaps import convert

__ALL__ = (
    'places_nearby',
    'place',
    'place_radar',
    'places_autocomplete',
    'place',
    'places_photo',
)


async def _places(self, url_part, query=None, location=None, radius=None,
                  keyword=None, language=None, min_price=0, max_price=4, name=None,
                  open_now=False, rank_by=None, type=None, page_token=None):
    params = {'minprice': min_price, 'maxprice': max_price}

    if query:
        params['query'] = query
    if location:
        params['location'] = convert.latlng(location)
    if radius:
        params['radius'] = radius
    if keyword:
        params['keyword'] = keyword
    if language:
        params['language'] = language
    if name:
        params['name'] = convert.join_list(' ', name)
    if open_now:
        params['opennow'] = 'true'
    if rank_by:
        params['rankby'] = rank_by
    if type:
        params['type'] = type
    if page_token:
        params['pagetoken'] = page_token

    return await client._request(
        'maps/api/place/{url_part}/json'.format(url_part=url_part),
        params,
    )


async def places_nearby(client, location, radius=None, keyword=None, language=None,
                        min_price=None, max_price=None, name=None, open_now=False,
                        rank_by=None, type=None, page_token=None):
    if rank_by == 'distance':
        if not (keyword or name or type):
            raise ValueError('either a keyword, name, or type arg is required '
                             'when rank_by is set to distance')
        elif radius is not None:
            raise ValueError('radius cannot be specified when rank_by is set to '
                             'distance')

    return await client._places(client, 'nearby', location=location, radius=radius,
                                keyword=keyword, language=language, min_price=min_price,
                                max_price=max_price, name=name, open_now=open_now,
                                rank_by=rank_by, type=type, page_token=page_token)


async def places_radar(client, *args, **kwargs):
    raise NotImplementedError


async def places_autocomplete(client, *args, **kwargs):
    raise NotImplementedError


async def place(client, place_id, language=None):
    return await places_.place(client, place_id, language=None)


async def places_photo(client, reference, max_width=None, max_height=None):
    query = {'photoreference': reference}
    if not (max_width or max_height):
        raise ValueError('Please provide max_width or max_height')
    return await client._request('maps/api/place/photo', query, chunked=True)
