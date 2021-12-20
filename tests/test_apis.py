"""Test module for APIs."""


from maps.apis.apis import Api
from maps.exceptions import ApiError


def test_apis():
    client = Api(
        base_url="https://api.mapbox.com/isochrone/v1/mapbox/driving/0,0",
        credentials="dummy",
    )
    try:
        client.get()
    except ApiError as err:
        assert str(err) == '401, Unauthorized, {"message":"Not Authorized - No Token"}'
