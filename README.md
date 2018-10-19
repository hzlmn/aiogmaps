# aiogmaps
[![Build Status](https://travis-ci.org/hzlmn/aiogmaps.svg?branch=master)](https://travis-ci.org/hzlmn/aiogmaps)

Asyncio client library for Google Maps API Web Services

## Requirements

- [googlemaps](https://github.com/googlemaps/google-maps-services-python) >= 3.0


## Getting Started

```sh
pip install aiogmaps
```

## Usage

```python
import asyncio

from aiogmaps import Client

async def main(loop):
    api_key = 'xxx'
    async with Client(api_key, loop=loop) as client:
        resp = client.place(place_id='ChIJN1t_tDeuEmsRUsoyG83frY4')
        print(resp)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))

```

For detailed API reference
- https://developers.google.com/maps/documentation/
- https://googlemaps.github.io/google-maps-services-python/docs/
