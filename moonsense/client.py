import requests

from typing import Iterable

from .models import Session


class Client(object):
    """ Moonsense Cloud API client """

    def __init__(
        self,
        secret_token: str,
        root_domain: str = "moonsense.dev",
        protocol: str = "https",
        default_region: str = "us-central1.gcp",
    ) -> None:
        self._root_domain = root_domain
        self._protocol = protocol
        self._default_region = default_region

        self._secret_token = secret_token
        self._headers = {"headers": {"Authorization": f"Bearer {self._secret_token}"}}

    def _build_url(self, region: str) -> str:
        if region == "":
            return f"{self._protocol}://{self._root_domain}"
        else:
            return f"{self._protocol}://{region}.data-api.{self._root_domain}"

    def regions(self):
        " Retrieve the list of regions in the Moonsense Cloud used for data ingest and storage "
        endpoint = "https://api." + self._root_domain + "/v1/regions"
        return requests.get(endpoint).json()

    def whoami(self):
        endpoint = self._build_url(self._default_region) + "/v1/tokens/self"
        r = requests.get(endpoint, **self._headers)
        return r.json()

    def sessions(self) -> Iterable[Session]:
        endpoint = self._build_url(self._default_region) + "/v1/sessions"
        page = 1
        while True:
            http_response = requests.get(
                endpoint, params=[("per_page", "50"), ("page", page)], **self._headers
            )
            if http_response.status_code != 200:
                raise RuntimeError(
                    "unable to list sessions. status code: " + http_response.status_code
                )

            response = http_response.json()
            if not "sessions" in response:
                return  # got an empy page
            for session in response["sessions"]:
                yield Session(session)

            # Determine if there is another page
            pagination = response["pagination"]
            if (
                "next_page" in pagination
                and pagination["current_page"] < pagination["next_page"]
            ):
                page = pagination["next_page"]
            else:
                break

    def chunks(self, session_id):
        pass
