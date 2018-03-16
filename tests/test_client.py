import pytest

from aiogmaps.client import Client


async def test_throw_on_empty_key(loop):
    with pytest.raises(ValueError):
        Client(None, loop=loop)


async def test_place(client):
    response = await client.place(place_id='ChIJN1t_tDeuEmsRUsoyG83frY4')
    assert response['status']


# async def test_places_photo(client):
#     response = await client.places_photo(
#         'CnRtAAAATLZNl354RwP_9UKbQ_5Psy40texXePv4oAlgP4qNEkdIrkyse7rPXYGd9D_Uj1rVsQdWT4oRz4QrYAJNpFX7rzqqMlZw2h2E2y5IKMUZ7ouD_SlcHxYq1yL4KbKUv3qtWgTK0A6QbGh87GB3sscrHRIQiG2RrmU_jF4tENr9wGS_YxoUSSDrYjWmrNfeEHSGSc3FyhNLlBU',  # noqa
#         max_width=400,
#     )
#     assert response is not None


@pytest.mark.xfail
async def test_places_nearby(client):
    await client.places_nearby({})


@pytest.mark.xfail
async def test_places_radar(client):
    await client.places_radar({})


@pytest.mark.xfail
async def test_places_autocomplete(client):
    await client.places_autocomplete({})
