import pytest

from aiogmaps.client import Client


async def test_throw_on_empty_key(loop):
    with pytest.raises(ValueError):
        Client(None, loop=loop)


async def test_places(client):
    response = await client.places(
        '123 main street',
        location=(42.3675294, -71.186966),
        type='liquor_store',
        language='en-AU',
        radius=100,
    )
    assert response is not None


async def test_places_autocomplete(client):
    response = await client.places_autocomplete('Victo')
    assert isinstance(response, list)


async def test_place(client):
    response = await client.place(place_id='ChIJNX9BrM0LkkYRIM-cQg265e8')
    assert response is not None


async def test_places_photo(client):
    response = await client.places_photo(
        'CnRtAAAATLZNl354RwP_9UKbQ_5Psy40texXePv4oAlgP4qNEkdIrkyse7rPXYGd9D_Uj1rVsQdWT4oRz4QrYAJNpFX7rzqqMlZw2h2E2y5IKMUZ7ouD_SlcHxYq1yL4KbKUv3qtWgTK0A6QbGh87GB3sscrHRIQiG2RrmU_jF4tENr9wGS_YxoUSSDrYjWmrNfeEHSGSc3FyhNLlBU',  # noqa
        max_width=400,
    )
    async for chunk, eof in response:
        pass


async def test_nearest_roads(client):
    response = await client.nearest_roads((60.170880, 24.942795))
    assert response is not None


async def test_speed_limits(client):
    response = await client.speed_limits('ChIJNX9BrM0LkkYRIM-cQg265e8')
    assert response is not None


@pytest.mark.xfail
async def test_places_nearby(client):
    await client.places_nearby({})


@pytest.mark.xfail
async def test_places_radar(client):
    await client.places_radar({})
