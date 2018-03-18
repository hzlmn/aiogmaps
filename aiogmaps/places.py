import googlemaps
from googlemaps import convert

__ALL__ = (
    'places_nearby',
    'place',
    'place_radar',
    'places_autocomplete',
    'place',
    'places_photo',
)


async def places(client):
    raise NotImplementedError


async def place(client, place_id, language=None):
    return await googlemaps.places.place(client, place_id, language=None)


async def places_nearby(client, location, radius=None, keyword=None,
                        language=None, min_price=None, max_price=None,
                        name=None, open_now=False, rank_by=None,
                        type=None, page_token=None):
    if rank_by == 'distance':
        if not (keyword or name or type):
            raise ValueError('either a keyword, name, or type arg is required '
                             'when rank_by is set to distance')
        elif radius is not None:
            raise ValueError('radius cannot be specified when rank_by '
                             'is set to distance')

    return await googlemaps.places._places(
        client, 'nearby', location=location,
        radius=radius, keyword=keyword, language=language,
        min_price=min_price, max_price=max_price, name=name,
        open_now=open_now, rank_by=rank_by,
        type=type, page_token=page_token,
    )


async def places_radar(client, location, radius, keyword=None,
                       min_price=None, max_price=None, name=None,
                       open_now=False, type=None):

    return await googlemaps.places._places(
        client, location, radius,
        keyword=keyword, min_price=min_price,
        max_price=max_price, name=name,
        open_now=open_now, rank_by=rank_by,
        type=type, page_token=page_token,
    )


async def places_autocomplete(client, *args, **kwargs):
    raise NotImplementedError


async def places_photo(client, reference, max_width=None, max_height=None):
    query = {'photoreference': reference}
    if not (max_width or max_height):
        raise ValueError('Please provide max_width or max_height')
    return await client._request('maps/api/place/photo', query, chunked=True)
