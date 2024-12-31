import json
import httpx

from typing import Optional, Union

from .models import Build, Version, FileInfo

WAGO_TOOLS_BASE_URL = "https://wago.tools/api"


class WagoToolsAPI:
    """A synchronous wrapper class for the wago.tools API"""

    def __init__(self, client: Optional[httpx.Client] = None):
        if client is None:
            client = self.__get_default_client()

        self.client = client

    @staticmethod
    def __get_default_client() -> httpx.Client:
        return httpx.Client(base_url=WAGO_TOOLS_BASE_URL, http2=True)

    def make_request(
        self,
        endpoint: str,
        params: Optional[httpx.QueryParams] = None,
        raw: Optional[bool] = False,
        timeout: Optional[int] = None,
    ):
        res = self.client.get(endpoint, params=params, timeout=timeout)
        res.raise_for_status()

        try:
            data = res.read() if raw else res.json()
            return data
        except json.decoder.JSONDecodeError:
            return res.read()
        except UnicodeDecodeError:
            return res.read()

    def get_all_builds(self) -> dict[str, list[Build]]:
        """Returns all builds that have been processed by wago.tools"""

        endpoint = "/builds"
        res = self.make_request(endpoint)
        processed_builds = {}
        for name, builds in res.items():
            processed_builds[name] = [Build.from_json(build) for build in builds]

        return processed_builds

    def get_latest_build(self, product: str) -> Build:
        """Returns the latest build for the specified product"""

        endpoint = f"/builds/{product}/latest"
        res = self.make_request(endpoint)
        return Build.from_json(res)

    def get_latest_build_for_all_products(self) -> dict[str, Build]:
        """Returns the latest build for all products"""

        endpoint = "/builds/latest"
        res = self.make_request(endpoint)
        latest_builds = {}
        for name, build in res.items():
            latest_builds[name] = Build.from_json(build)

        return latest_builds

    def get_file_by_fdid(
        self,
        fdid: int,
        version: Optional[str | Version] = None,
    ) -> Union[str, bytes]:
        """Returns the contents of a CASC file by FileDataID"""
        endpoint = f"/casc/{fdid}"

        params = httpx.QueryParams()
        if version is not None:
            params.add("version", str(version))

        res = self.make_request(endpoint, params=params)
        return res

    def get_file_info_by_fdid(self, fdid: int) -> FileInfo:
        """Returns metadata about a given CASC file by FileDataID"""

        endpoint = f"/info/{fdid}"
        res = self.make_request(endpoint)
        return FileInfo.from_json(res)

    def get_all_files(
        self, version: Optional[str | Version] = None, format: Optional[str] = None
    ) -> dict[str, str]:
        """Returns all available files in json format, if `format` is not specified.
        Valid formats: csv, json"""

        endpoint = "/files"

        params = httpx.QueryParams()
        if version is not None:
            params.add("version", str(version))

        if format is not None:
            params.add("format", format)

        return self.make_request(endpoint, params, timeout=120)


class AsyncWagoToolsAPI:
    """An asynchronous wrapper class for the wago.tools API"""

    def __init__(self, client: Optional[httpx.AsyncClient] = None):
        if client is None:
            client = self.__get_default_client()

        self.client = client

    @staticmethod
    def __get_default_client() -> httpx.AsyncClient:
        return httpx.AsyncClient(base_url=WAGO_TOOLS_BASE_URL, http2=True)

    async def make_request(
        self,
        endpoint: str,
        params: Optional[httpx.QueryParams] = None,
        raw: Optional[bool] = False,
        timeout: Optional[int] = None,
    ):
        res = await self.client.get(endpoint, params=params, timeout=timeout)
        res.raise_for_status()

        try:
            data = res.read() if raw else res.json()
            return data
        except json.decoder.JSONDecodeError:
            return res.read()
        except UnicodeDecodeError:
            return res.read()

    async def get_all_builds(self) -> dict[str, list[Build]]:
        """Returns all builds that have been processed by wago.tools"""

        endpoint = "/builds"
        res = await self.make_request(endpoint)
        processed_builds = {}
        for name, builds in res.items():
            processed_builds[name] = [Build.from_json(build) for build in builds]

        return processed_builds

    async def get_latest_build(self, product: str) -> Build:
        """Returns the latest build for the specified product"""

        endpoint = f"/builds/{product}/latest"
        res = await self.make_request(endpoint)
        return Build.from_json(res)

    async def get_latest_build_for_all_products(self) -> dict[str, Build]:
        """Returns the latest build for all products"""

        endpoint = "/builds/latest"
        res = await self.make_request(endpoint)
        latest_builds = {}
        for name, build in res.items():
            latest_builds[name] = Build.from_json(build)

        return latest_builds

    async def get_file_by_fdid(
        self,
        fdid: int,
        version: Optional[str | Version] = None,
    ) -> Union[str, bytes]:
        """Returns the contents of a CASC file by FileDataID"""
        endpoint = f"/casc/{fdid}"

        params = httpx.QueryParams()
        if version is not None:
            params.add("version", str(version))

        res = await self.make_request(endpoint, params=params)
        return res

    async def get_file_info_by_fdid(self, fdid: int) -> FileInfo:
        """Returns metadata about a given CASC file by FileDataID"""

        endpoint = f"/info/{fdid}"
        res = await self.make_request(endpoint)
        return FileInfo.from_json(res)

    async def get_all_files(
        self, version: Optional[str | Version] = None, format: Optional[str] = None
    ) -> dict[str, str]:
        """Returns all available files in json format, if `format` is not specified.
        Valid formats: csv, json"""

        endpoint = "/files"

        params = httpx.QueryParams()
        if version is not None:
            params.add("version", str(version))

        if format is not None:
            params.add("format", format)

        return await self.make_request(endpoint, params, timeout=120)
