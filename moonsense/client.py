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
import tempfile
import tarfile
import shutil

from google.protobuf import json_format
from typing import Iterable, List

from .models import Session, Chunk, TokenSelfResponse, \
    DataRegionsListResponse, SessionListResponse, ChunksListResponse, \
    CardListResponse, Card, SealedBundle


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
        self._headers = {"headers": {
            "Authorization": f"Bearer {self._secret_token}"}}

    def _build_url(self, region: str) -> str:
        if region == "":
            return f"{self._protocol}://{self._root_domain}"
        else:
            return f"{self._protocol}://{region}.data-api.{self._root_domain}"

    def list_regions(self) -> DataRegionsListResponse:
        """
        Retrieve the list of Data Plane regions in the Moonsense Cloud

        These are used for data ingest and storage. Data is encrypted while at-rest and
        in-transit. Granular data never leaves a region.

        See: https://api.moonsense.cloud/v2/regions

        :return: a list of dictionaries describing the regions
        """
        endpoint = "https://api." + self._root_domain + "/v2/regions"
        return json_format.Parse(requests.get(endpoint).text, DataRegionsListResponse(), ignore_unknown_fields=True)

    def whoami(self) -> TokenSelfResponse:
        """
        Describe the authentication token used to connect to the API

        :return: a 'TokenSelfResponse' object with details
        """
        endpoint = self._build_url(self._default_region) + "/v2/tokens/self"
        r = requests.get(endpoint, **self._headers)
        return json_format.Parse(r.text, TokenSelfResponse(), ignore_unknown_fields=True)

    def list_sessions(self, labels: List[str] = None, client_session_group_id: str = None) -> Iterable[Session]:
        """
        List sessions for the current project

        :return: a generator of 'Session' objects
        """
        endpoint = self._build_url(self._default_region) + "/v2/sessions"
        page = 1
        while True:
            params = [("per_page", "50"), ("page", page)]

            if labels != None:
                params.append(("filter[labels][]", labels))

            if client_session_group_id != None:
                params.append(
                    ("filter[client_session_group_id]", client_session_group_id))

            http_response = requests.get(
                endpoint, params, **self._headers
            )
            if http_response.status_code != 200:
                raise RuntimeError(
                    f"unable to list sessions. status code: {http_response.status_code}"
                )

            response = json_format.Parse(
                http_response.text, SessionListResponse(), ignore_unknown_fields=True)
            if len(response.sessions) == 0:
                return  # no more sessions
            for session in response.sessions:
                yield session

            if response.pagination.current_page < response.pagination.total_pages:
                page = response.pagination.current_page + 1
            else:
                break

    def describe_session(self, session_id, minimal=True) -> Session:
        """
        Describe a specific session

        :param session_id: The ID of the session
        :param minimal: If true, only total values are returned for counters
        :return: a 'Session' object with details
        """
        view = "minimal" if minimal else "full"
        endpoint = self._build_url(
            self._default_region) + f"/v2/sessions/{session_id}?view={view}"

        http_response = requests.get(endpoint, **self._headers)
        if http_response.status_code != 200:
            raise RuntimeError(
                f"unable to describe session. status code: {http_response.status_code}"
            )

        return json_format.Parse(http_response.text, Session(), ignore_unknown_fields=True)

    def update_session_labels(self, session_id, labels: List[str]) -> None:
        """
        Update the label on a session given the session_id.
        Calling this method updates ALL labels for the given session_id.
        """
        endpoint = self._build_url(
            self._default_region) + f"/v2/sessions/{session_id}/labels"

        payload = {
            "labels": []
        }
        for label in labels:
            payload["labels"].append({"name" : label})

        http_response = requests.post(endpoint, json=payload, **self._headers)

        if http_response.status_code != 200:
            raise RuntimeError(
                f"unable to update session labels. status code: {http_response.status_code}"
            )

    def list_chunks(self, session_id) -> Iterable[Chunk]:
        """
        List all the granular data chunks that are part of a session that were persisted in
        in the Moonsense Cloud.

        :param session_id: The ID of the session
        :return: a generator of 'Chunk' objects
        """
        session = self.describe_session(session_id)
        endpoint = (
            self._build_url(session.region_id) +
            f"/v2/sessions/{session_id}/chunks"
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

            response = json_format.Parse(
                http_response.text, ChunksListResponse(), ignore_unknown_fields=True)
            if len(response.chunks) == 0:
                return  # no chunks found for this session
            for chunk in response.chunks:
                yield chunk

            if response.pagination.current_page < response.pagination.total_pages:
                page = response.pagination.current_page + 1
            else:
                break

    def read_chunk(self, session_id, chunk_id) -> Iterable[SealedBundle]:
        """
        Read all the bundles within a data chunk :param chunk: session data chunk object
        :return: generator of bundles. The chunk read had to be persisted in the Moonsense Cloud first.
        """
        session = self.describe_session(session_id)
        endpoint = self._build_url(
            session.region_id) + f"/v2/sessions/{session_id}/chunks/{chunk_id}"
        http_response = requests.get(endpoint, stream=True, **self._headers)
        if http_response.status_code != 200:
            raise RuntimeError(
                f"unable to read: {chunk_id}. status code: {http_response.status_code}"
            )
        for line in http_response.iter_lines(chunk_size=1024 * 1024):
            yield json_format.Parse(line, SealedBundle(), ignore_unknown_fields=True)

    def download_session(self, session_id, output_file) -> None:
        """
        Download and consolidate all data ingested so far for a session into a single file - one JSON per line.

        :param session_id: The ID of the session
        :param output_file: The path to the output file
        """
        session = self.describe_session(session_id)

        endpoint = self._build_url(session.region_id) + f"/v2/sessions/{session_id}/bundles"
        http_response = requests.get(endpoint, stream=True, **self._headers)
        if http_response.status_code != 200:
            raise RuntimeError(
                f"unable to read: {chunk}. status code: {http_response.status_code}")

        # create temporary director for writing and unpacking tar.gz file.
        with tempfile.TemporaryDirectory() as tmpdirname:
            temp_output_file = os.path.join(tmpdirname, "temp-" + session_id + ".tar.gz")

            # write the response of the API to a tar.gz file.
            with open(temp_output_file, "wb") as temp_tar_fd:
                for buffer in http_response.iter_content(chunk_size=1024 * 1024):
                    temp_tar_fd.write(buffer)

            # open the tar file
            with tarfile.open(temp_output_file, mode='r:gz') as temp_tar:
                # choose a path to extract the tar.gz archive.
                temp_extract_path = os.path.join(tmpdirname, "extracted")
                temp_tar_contents = temp_tar.getmembers()
                if len(temp_tar_contents) != 1:
                        raise RuntimeError("Expected to download just one file but got many")

                json_file_name = temp_tar_contents[0].name
                # extract the archive.
                temp_tar.extractall(temp_extract_path)
                # move the only file in the archive to the final user-inputted path.
                shutil.move(os.path.join(tmpdirname, "extracted", json_file_name), output_file)

    def read_session(self, session_id) -> Iterable[SealedBundle]:
        """
        Read all data points from a session that were sent so far.

        :param session_id: The ID of the session
        :return: a generator of dict entries
        """

        with tempfile.TemporaryDirectory() as tmpdirname:
            temp_output_file = os.path.join(tmpdirname, "temp-" + session_id + ".json")
            self.download_session(session_id, temp_output_file)

            with open(temp_output_file, "r") as temp_file:
                for line in temp_file.readlines():
                    yield json_format.Parse(line, SealedBundle(), ignore_unknown_fields=True)

    def list_cards(self, session_id) -> List[Card]:
        """
        List all the cards associated with a session

        :param session_id: The ID of the session
        :return: list of cards
        """
        session = self.describe_session(session_id)
        region = session.region_id if self._default_region != "" else ""

        endpoint = self._build_url(
            region) + "/v2/cards?session_id=" + session_id
        http_response = requests.get(endpoint, **self._headers)

        response = json_format.Parse(
            http_response.text, CardListResponse(), ignore_unknown_fields=True)
        return response.cards

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
