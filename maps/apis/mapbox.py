"""This module defines classes for mapbox APIs."""

from typing import List, Optional

import requests

from maps.apis.apis import Api


class MapBoxApi(Api):
    """A class for low level mapbox api calls."""

    def __init__(self, base_url: str, credentials: Optional[str]):
        super().__init__(base_url, credentials)

    def isochrone(
        self,
        profile: str,
        coordinates: List,
        contours_minutes: List,
        contours_colors: Optional[List] = None,
        polygons: bool = False,
        denoise: Optional[float] = 1.0,
    ) -> requests.models.Response:
        """
        Mapbox isochrone api to get reachable area on map.

        :param profile: A Mapbox Directions routing profile ID. valid values are ``driving``,
            ``walking`` and ``cycling``
        :param coordinates: A list of latitude and longitude  around which to center the isochrone
            lines.
        :param contours_minutes: The times in minutes to use for each isochrone contour.
            You can specify up to four contours. Times must be in increasing order.
            The maximum time that can be specified is 60 minutes.
        :param contours_colors: The list of colors to use for each isochrone contour, specified as
            hex values without a leading # (for example, ff0000 for red). If this parameter is
            used, there must be the same number of colors as there are entries in contours_minutes.
            If no colors are specified, the Isochrone API will assign a default rainbow color
            scheme to the output.
        :param polygons: Specify whether to return the contours as GeoJSON polygons (True) or
            linestrings (False, default).
        :param denoise: A float from 0.0 to 1.0 that can be used to remove smaller contours.
            The default is 1.0. A value of 1.0 will only return the largest contour for a given
            time value. A value of 0.5 drops any contours that are less than half the area of the
            largest contour in the set of contours for that same time value.
        :return: The HTTP response returned by the :mod:`requests` package.
        """
        latlng = ",".join([str(coord) for coord in coordinates])
        path = f"/isochrone/v1/mapbox/{profile}/{latlng}"
        params = {
            "contours_minutes": ",".join([str(cm) for cm in contours_minutes]),
            "denoise": str(denoise),
            "polygons": str(polygons).lower(),
            "access_token": self.credentials,
        }
        if contours_colors:
            params["contours_colors"] = ",".join([cc for cc in contours_colors])

        return self.get(path=path, params=params)

    def matrix(
        self,
        profile: str,
        coordinates: str,
        annotations: Optional[str] = None,
        approaches: Optional[str] = None,
        destinations: Optional[str] = None,
    ) -> requests.models.Response:
        """
        The Mapbox Matrix API returns travel times between many points.

        :param profile: A Mapbox Directions routing profile ID.
            `see <https://docs.mapbox.com/api/navigation/matrix/>_`.
        :param coordinates: A semicolon-separated list of {longitude},{latitude} coordinates.
            There must be between two and 25 coordinates. For the mapbox/driving-traffic profile,
            the maximum is 10 coordinates.
        :param annotations: Used to specify the resulting matrices. Possible values are: duration
            (default), distance, or both values separated by a comma.
        :param approaches: A semicolon-separated list indicating the side of the road from which to
            approach waypoints in a requested route. Accepts unrestricted (default, route can
            arrive at the waypoint from either side of the road) or curb (route will arrive at
            the waypoint on the driving_side of the region). If provided, the number of approaches
            must be the same as the number of waypoints. However, you can skip a coordinate and
            show its position in the list with the ; separator.
        :param destinations: Use the coordinates at a given index as destinations. Possible values
            are: a semicolon-separated list of 0-based indices, or all (default).
            The option all allows using all coordinates as destinations.
        :return: The HTTP response returned by the :mod:`requests` package.
        """
        path = f"/directions-matrix/v1/mapbox/{profile}/{coordinates}"
        params = {"access_token": self.credentials}
        if annotations:
            params["destinations"] = destinations
        if approaches:
            params["approaches"] = approaches
        if destinations:
            params["destinations"] = destinations

        return self.get(path=path, params=params)
