import asyncio
import os

import pytest

from aiogmaps.client import Client


@pytest.fixture
def loop():
    return asyncio.get_event_loop()


# This fixture needed for proper work of aresponses
@pytest.fixture
def event_loop(loop):
    return loop


@pytest.fixture
def api_key():
    return os.environ.get('API_KEY')


@pytest.fixture
async def client(loop, api_key):
    client = Client(api_key, verify_ssl=False, loop=loop)
    yield client
    await client.close()
