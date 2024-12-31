import json
import httpx

from pathlib import Path
from typing import Optional, Union

from .models import WagoAddonMetadata, WagoAddonsGameVersions, WagoAddonsAddonCategory

WAGO_ADDONS_BASE_URL = "https://addons.wago.io/api"


class WagoAddonsAPI:
    """A synchronous wrapper class for the addons.wago.io API"""

    def __init__(
        self, client: Optional[httpx.Client] = None, api_key: Optional[str] = None
    ):
        if client is None:
            client = self.__get_default_client()

        self.client = client
        self.api_key = api_key

    @staticmethod
    def __get_default_client() -> httpx.Client:
        return httpx.Client(base_url=WAGO_ADDONS_BASE_URL, http2=True)

    def make_request(self, endpoint: str, *args, **kwargs):
        res = self.client.get(endpoint, *args, **kwargs)
        res.raise_for_status()

        try:
            data = res.json()
            return data
        except json.decoder.JSONDecodeError:
            return res

    def make_post_request(self, endpoint: str, *args, **kwargs):
        res = self.client.post(endpoint, *args, **kwargs)
        res.raise_for_status()

        try:
            data = res.json()
            return data
        except json.decoder.JSONDecodeError:
            return res

    def validate_metadata(self, metadata: WagoAddonMetadata):
        supported_versions = self.get_supported_game_versions()

        def is_valid(patch: str, flavor: str) -> bool:
            return patch in getattr(supported_versions, flavor)

        flavors = ["retail", "cata", "wotlk", "bc", "classic"]
        for flavor in flavors:
            key = f"supported_{flavor}_patches"
            attr = getattr(metadata, key)
            if attr is not None and len(attr) > 0:
                for patch in attr:
                    if not is_valid(patch, flavor):
                        raise ValueError(
                            f"Invalid patch version for flavor '{flavor}': {patch}"
                        )

    def upload_addon(
        self,
        project_id: str,
        release_path: Union[str, Path],
        metadata: WagoAddonMetadata,
    ) -> bool:
        if self.api_key is None:
            raise Exception("A Wago Addons API key is required to upload an addon")

        endpoint = f"/projects/{project_id}/version"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }

        if not Path(release_path).exists():
            raise FileNotFoundError(f"File not found: {release_path}")

        self.validate_metadata(metadata)

        with open(release_path, "rb") as f:
            files = {
                "file": (release_path, f),
                "metadata": (None, metadata.to_json()),
            }
            res = self.make_post_request(
                endpoint, method="post", headers=headers, files=files
            )

        return res.status_code == 200

    def get_supported_game_versions(self) -> WagoAddonsGameVersions:
        endpoint = "/data/game"
        res = self.make_request(endpoint)
        return WagoAddonsGameVersions.from_dict(res["patches"])

    def get_addon_categories(self) -> list[WagoAddonsAddonCategory]:
        endpoint = "/data/categories"
        res = self.make_request(endpoint)
        return [WagoAddonsAddonCategory.from_dict(x) for x in res]
