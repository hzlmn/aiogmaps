import googlemaps
from googlemaps import convert


async def places(client, query, location=None, radius=None, language=None,
                 min_price=0, max_price=4, open_now=False, type=None,
                 page_token=None):

    return await googlemaps.places.places(
        client, query, location=location, radius=radius, language=language,
        min_price=min_price, max_price=max_price, open_now=open_now,
        type=type, page_token=page_token,
    )


async def place(client, place_id, language=None):
    return await googlemaps.places.place(client, place_id, language=None)


async def places_radar(client, location, radius, keyword=None, min_price=0,
                       max_price=4, name=None, open_now=False, type=None):

    return await googlemaps.places.places_radar(
        client, location, radius, keyword=keyword,
        min_price=min_price, max_price=max_price,
        name=name, open_now=open_now, type=type,
    )


async def places_nearby(client, location, radius=None, keyword=None,
                        language=None, min_price=0, max_price=4,
                        name=None, open_now=False, rank_by=None,
                        type=None, page_token=None):

    return await googlemaps.places.places_nearby(
        client, location=location, radius=radius,
        keyword=keyword, language=language, name=name,
        min_price=min_price, max_price=max_price,
        open_now=open_now, rank_by=rank_by,
        type=type, page_token=page_token,
    )


async def places_autocomplete(client, input_text, offset=None, location=None,
                              radius=None, language=None, types=None,
                              components=None, strict_bounds=False):

    return await _autocomplete(
        client, '', input_text,
        offset=offset, location=location,
        radius=radius, language=language,
        types=types, components=components,
        strict_bounds=strict_bounds,
    )


async def places_autocomplete_query(client, input_text,
                                    offset=None, location=None,
                                    radius=None, language=None):
    return await _autocomplete(
        client, 'query', input_text,
        offset=offset, location=location,
        radius=radius, language=language,
    )


async def _autocomplete(client, url_part, input_text,
                        offset=None, location=None, radius=None,
                        language=None, types=None, components=None,
                        strict_bounds=False):

    params = {'input': input_text}

    if offset:
        params['offset'] = offset
    if location:
        params['location'] = convert.latlng(location)
    if radius:
        params['radius'] = radius
    if language:
        params['language'] = language
    if types:
        params['types'] = types
    if components:
        params['components'] = convert.components(components)
    if strict_bounds:
        params['strictbounds'] = 'true'

    url = '/maps/api/place/%sautocomplete/json' % url_part
    result = await client._request(url, params)
    return result['predictions']


async def places_photo(client, photo_reference,
                       max_width=None, max_height=None):
    if not (max_width or max_height):
        raise ValueError('a max_width or max_height arg is required')

    params = {'photoreference': photo_reference}

    if max_width:
        params['maxwidth'] = max_width
    if max_height:
        params['maxheight'] = max_height

    return await client._request('/maps/api/place/photo', params, chunked=True)
