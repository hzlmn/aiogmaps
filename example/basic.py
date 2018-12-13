import asyncio

from aiogmaps import Client


async def main(loop):
    api_key = 'xxx'
    async with Client(api_key, loop=loop) as client:
        resp = await client.place(place_id='ChIJN1t_tDeuEmsRUsoyG83frY4')
        print(resp)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
