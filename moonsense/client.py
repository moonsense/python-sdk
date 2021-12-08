"""
Copyright 2021 Moonsense, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

""" Moonsense Cloud API Client

A simple API client that makes it easy to read data from the Moonsense Cloud and
create Cards that will be displayed back in the Moonsense Recorder.
"""

import os

import requests
import json

from typing import Iterable, List

from .models import Session, Chunk


class Client(object):
    """ Moonsense Cloud API Client """

    def __init__(
        self,
        secret_token: str = None,
        root_domain: str = "moonsense.cloud",
        protocol: str = "https",
        default_region: str = "us-central1.gcp",
    ) -> None:
        """
        Construct a new 'Client' object

        :param secret_token: API secret token generated from the Moonsense Cloud web console
        :param root_domain: Root API domain (defaults to moonsense.cloud)
        :param protocol: Protocol to use when connecting to the API (defaults to https)
        :param default_region: Default Moonsense Cloud Data Plane region to connect to
        """
        if secret_token is None:
            secret_token = os.environ.get("MOONSENSE_SECRET_TOKEN", None)
            if secret_token is None:
                raise RuntimeError(
                    "secret token must either be set as an input param or as an environment variable MOONSENSE_SECRET_TOKEN"
                )
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

    def list_regions(self):
        """
        Retrieve the list of Data Plane regions in the Moonsense Cloud

        These are used for data ingest and storage. Data is encrypted while at-rest and
        in-transit. Granular data never leaves a region.

        See: https://api.moonsense.cloud/v2/regions

        :return: a list of dictionaries describing the regions
        """
        endpoint = "https://api." + self._root_domain + "/v2/regions"
        return requests.get(endpoint).json().get('regions', [])

    def whoami(self):
        """
        Describe the authentication token used to connect to the API

        :return: a dictionary describing the secret token
        """
        endpoint = self._build_url(self._default_region) + "/v2/tokens/self"
        r = requests.get(endpoint, **self._headers)
        return r.json()

    def list_sessions(self, recording_profile: str = None, 
        labels: List[str] = None, client_session_group_id: str = None ) -> Iterable[Session]:
        """
        List sessions for the current project

        :return: a generator of 'Session' objects
        """
        endpoint = self._build_url(self._default_region) + "/v2/sessions"
        page = 1
        while True:
            params=[("per_page", "50"), ("page", page)]

            if recording_profile != None:
                params.append(("filter[recording_profile]", recording_profile))

            if labels != None:
                params.append(("filter[labels][]", labels))

            if client_session_group_id != None:
                params.append(("filter[client_session_group_id]", client_session_group_id))

            http_response = requests.get(
                endpoint, params, **self._headers
            )
            if http_response.status_code != 200:
                raise RuntimeError(
                    f"unable to list sessions. status code: {http_response.status_code}"
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

    def describe_session(self, session_id) -> Session:
        """
        Describe a specific session

        :param session_id: The ID of the session
        :return: a 'Session' object with details
        """
        endpoint = self._build_url(self._default_region) + f"/v2/sessions/{session_id}"

        http_response = requests.get(endpoint, **self._headers)
        if http_response.status_code != 200:
            raise RuntimeError(
                f"unable to describe session. status code: {http_response.status_code}"
            )
        return Session(http_response.json())

    def list_chunks(self, session_id) -> Iterable[Chunk]:
        """
        List all the granular data chunks that are part of a session

        :param session_id: The ID of the session
        :return: a generator of 'Chunk' objects
        """
        session = self.describe_session(session_id)
        endpoint = (
            self._build_url(session.region_id) + f"/v2/sessions/{session_id}/chunks"
        )
        page = 1
        while True:
            http_response = requests.get(
                endpoint, params=[("per_page", "50"), ("page", page)], **self._headers
            )
            if http_response.status_code != 200:
                raise RuntimeError(
                    f"unable to list session chunks. status code: {http_response.status_code}"
                )

            response = http_response.json()
            if not "chunks" in response:
                return  # got an empy page
            for chunk in response["chunks"]:
                yield Chunk(session_id, session.region_id, chunk)

            # Determine if there is another page
            pagination = response["pagination"]
            if (
                "next_page" in pagination
                and pagination["current_page"] < pagination["next_page"]
            ):
                page = pagination["next_page"]
            else:
                break

    def read_chunk(self, chunk: Chunk) -> Iterable[dict]:
        """
        Read all the bundles with a data chunk

        :param chunk: session data chunk object
        :return: generate of bundles
        """
        endpoint = self._build_url(chunk.region_id) + chunk.uri()
        http_response = requests.get(endpoint, stream=True, **self._headers)
        if http_response.status_code != 200:
            raise RuntimeError(
                f"unable to read: {chunk}. status code: {http_response.status_code}"
            )
        for line in http_response.iter_lines(chunk_size=1024 * 1024):
            yield json.loads(line)

    def download_session(self, session_id, output_file) -> None:
        """
        Download and consolidate all the chunks for a session into a single file

        :param session_id: The ID of the session
        :param output_file: The path to the output file
        """
        with open(output_file, "wb") as fd:
            for chunk in self.list_chunks(session_id):
                endpoint = self._build_url(chunk.region_id) + chunk.uri()
                http_response = requests.get(endpoint, stream=True, **self._headers)
                if http_response.status_code != 200:
                    raise RuntimeError(
                        f"unable to read: {chunk}. status code: {http_response.status_code}"
                    )
                for buffer in http_response.iter_content(chunk_size=1024 * 1024):
                    fd.write(buffer)

    def read_session(self, session_id) -> Iterable[dict]:
        """
        Read data points from a session from all the chunks

        :param session_id: The ID of the session
        :return: a generator of dict entries
        """
        for chunk in self.list_chunks(session_id):
            endpoint = self._build_url(chunk.region_id) + chunk.uri()
            http_response = requests.get(endpoint, stream=True, **self._headers)
            if http_response.status_code != 200:
                raise RuntimeError(
                    f"unable to read: {chunk}. status code: {http_response.status_code}"
                )
            for line in http_response.iter_lines(chunk_size=1024 * 1024):
                yield json.loads(line)

    def list_cards(self, session_id):
        """
        List all the cards associated with a session

        :param session_id: The ID of the session
        :return: list of cards
        """
        session = self.describe_session(session_id)
        region = session.region_id if self._default_region != "" else ""

        endpoint = self._build_url(region) + "/v2/cards?session_id=" + session_id
        http_response = requests.get(endpoint, **self._headers)

        response = http_response.json()
        return response["cards"] if "cards" in response else []

    def create_card(self, session_id, title, description, source_type="API") -> None:
        """
        Create a new card associated with this session ID

        :param session_id: The ID of the session
        :return: none
        """
        session = self.describe_session(session_id)
        region = session.region_id if self._default_region != "" else ""
        endpoint = self._build_url(region) + "/v2/cards"

        http_response = requests.post(
            endpoint,
            json={
                "session_id": session.session_id,
                "title": title,
                "description": description,
                "source_type": source_type,
            },
            **self._headers,
        )

        if http_response.status_code != 200:
            raise RuntimeError(
                f"unable to create card. status code: {http_response.status_code} body: {http_response.text}"
            )
