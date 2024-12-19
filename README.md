# py-wago-api
An asynchronous Python wrapper for the [wago.tools](https://wago.tools) API

## Install

```
pip install git+https://github.com/Ghostopheles/py-wago-api.git
```

## Usage

All responses are converted from their usual JSON format into Python objects.

```py
from wago import WagoAPI

async def main():
    client = WagoAPI()

    fdid = 6420120
    file = await client.get_file_by_fdid(fdid)
```

#### Methods

##### Builds
- `WagoAPI.get_all_builds()`: Returns all builds that have been processed by wago.tools
- `WagoAPI.get_latest_build(product)`: Returns the latest build for the specified product
- `WagoAPI.get_latest_build_for_all_products()`: Returns the latest build for all products

##### Files
- `WagoAPI.get_file_by_fdid(fdid)`: Returns the contents of a CASC file by FileDataID
    - Optionally, provide a version to grab the file for the specified build (i.e. "11.0.7.58187")
- `WagoAPI.get_file_info_by_fdid(fdid)`: Returns metadata about a given CASC file by FileDataID
- `WagoAPI.get_all_files()`: Returns all available files in the specified format, or json by default
    - Optionally, specify a version and format
