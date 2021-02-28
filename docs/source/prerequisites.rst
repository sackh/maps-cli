Prerequisites
=============
Before you install the ``maps-cli`` package make sure you meet the following prerequisites:

- A Python installation, 3.6+ recommended, with the ``pip`` command available to install dependencies.
- Authentication:

    Maps CLI provides access to the below maps services provider in order to use their services you will need an API key/ access token for authentication.

  - ``HERE``

    - A HERE developer account, freely available under `HERE Developer Portal`_.
    - An `HERE API key`_ from the `HERE Developer Portal`_, in an environment variable named ``HERE_APIKEY``.

  - ``MapBox``

    - A MapBox developer account, freely available under `MapBox Developer Account`_.
    - An `access token`_ from the `MapBox Developer Account`_ in an environment variable named ``MAPBOX_APIKEY``.

  - ``TomTom``

    - A TomTom developer account, freely available under `TomTom Developer Portal`_.
    - An `TomTom API key`_ from the `TomTom Developer Portal`_, in an environment variable named ``TOMTOM_APIKEY``.

  - ``OSM``

    - No API key is required.

.. _HERE Developer Portal: https://developer.here.com/
.. _HERE API key: https://developer.here.com/documentation/identity-access-management/dev_guide/topics/dev-apikey.html
.. _MapBox Developer Account: https://account.mapbox.com/
.. _access token: https://docs.mapbox.com/help/getting-started/access-tokens/
.. _TomTom Developer Portal: https://developer.tomtom.com/
.. _TomTom API key: https://developer.tomtom.com/how-to-get-tomtom-api-key