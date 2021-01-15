# Maps CLI 

[![Main Actions Status](https://github.com/sackh/maps-cli/workflows/main/badge.svg)](https://github.com/sackh/maps-cli/actions)
[![PyPI - Python Version](https://img.shields.io/pypi/v/maps-cli.svg?logo=pypi)](https://pypi.org/project/maps-cli/)
[![Downloads](https://pepy.tech/badge/maps-cli)](https://pepy.tech/project/maps-cli)
[![PyPI - License](https://img.shields.io/pypi/l/maps-cli)](https://pypi.org/project/maps-cli/)
[![GitHub contributors](https://img.shields.io/github/contributors/sackh/maps-cli)](https://github.com/sackh/maps-cli/graphs/contributors)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![commits since](https://img.shields.io/github/commits-since/sackh/maps-cli/latest.svg)](https://github.com/sackh/maps-cli/commits/master)


A simple command line tool to access services of various map services providers.

## Usage
# ![demo](https://github.com/sackh/maps-cli/raw/main/gifs/demo.gif)

## Installation
```bash
    pip install maps-cli
```

## Test Suite
```bash
    poetry install
    python -m poetry run python -m pytest -v --durations=10 --cov=maps tests
```

### Commands

```bash
    maps -h
    maps show
```

## Maps Service Providers
Currently, this library is supporting following providers.

- [OSM](https://www.openstreetmap.org/)
- [HERE](https://www.here.com/)
- [MapBox](https://www.mapbox.com/)
- [TomTom](https://www.tomtom.com/)

## Services
Currently, all providers support forward and reverse geocoding services.
