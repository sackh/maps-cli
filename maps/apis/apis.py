"""This module defines base classes for APIs."""

import urllib.request
from typing import Dict, Optional

import requests

from maps.exceptions import ApiError


class Api:
    """Baseclass for low level http calls."""

    def __init__(self, base_url: str, credentials: Optional[str]):
        self.base_url = base_url
        self.credentials = credentials
        self.cookies: Dict[str, str] = {}
        self.headers: Dict[str, str] = {}

    def __call__(
        self,
        method: str,
        path: Optional[str] = "",
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        cookies: Optional[Dict] = None,
        json: Optional[Dict] = None,
        data: Optional[Dict] = None,
        proxies: Optional[Dict] = None,
    ) -> requests.models.Response:
        """Make an API call with parameters passed to :mod:`requests`.

        :param method: The HTTP method name, e.g. "GET", "PUT", etc.
        :param path: The HTTP path to be appended to the :attr:`server` attribute.
        :param params: A dict holding the HTTP query parameters.
        :param headers: A dict holding the HTTP request headers.
        :param cookies: A dict holding the HTTP request cookies.
        :param json: A JSON object (usually a dict) to be passed as request
            body with content-type ``application/json``.
        :param data: A str to be passed as request body with content-type
            ``application/x-www-form-urlencoded``.
        :param proxies: A dict holding the HTTP proxies to be used.
        :return: The HTTP response returned by the :mod:`requests` package.
        :raises ApiError: If the status code of the HTTP response is not in the
             interval [200, 300).
        """
        url = f"{self.base_url}{path}"

        req_method = getattr(requests, method.lower())
        env_proxies = urllib.request.getproxies()

        resp = req_method(
            url,
            params=params,
            headers=headers or self.headers,
            cookies=cookies or self.cookies,
            proxies=proxies or env_proxies,
            json=json,
            data=data,
        )
        if not (200 <= resp.status_code < 300):
            raise ApiError(resp)
        return resp

    def get(self, **kwargs) -> requests.models.Response:
        """Send a HTTP GET request.

        :param kwargs: Keyword arguments passed when sending the HTTP request.
        :return: The HTTP response.
        """
        return self(method="GET", **kwargs)
