# Maps CLI 

[comment]: <> ([![Main Actions Status]&#40;https://github.com/sackh/maps-cli/workflows/main/badge.svg&#41;]&#40;https://github.com/sackh/maps-cli/actions&#41;)
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
