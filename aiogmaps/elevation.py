from googlemaps import convert


async def elevation(client, locations):
    params = {'locations': convert.shortest_path(locations)}
    result = await client._request('/maps/api/elevation/json', params)
    return result.get('results', [])


async def elevation_along_path(client, path, samples):
    if type(path) is str:
        path = 'enc:%s' % path
    else:
        path = convert.shortest_path(path)

    params = {
        'path': path,
        'samples': samples
    }

    result = await client._request('/maps/api/elevation/json', params)
    return result.get('results', [])
