# aiogmaps
[![Build Status](https://travis-ci.org/hzlmn/aiogmaps.svg?branch=master)](https://travis-ci.org/hzlmn/aiogmaps)

Asyncio client library for Google Maps API Web Services


## Getting Started

```sh
$ pip install aiogmaps
```

## Usage

```python
import asyncio

from aiogmaps import Client

API_KEY = "<your api key>"


async def main(loop):
    gmaps = Client(API_KEY, verify_ssl=False, loop=loop)
    response = await gmaps.place('ChIJN1t_tDeuEmsRUsoyG83frY4')
    assert response is not None
    print(response)
    await gmaps.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))

```


## License

`MIT`
