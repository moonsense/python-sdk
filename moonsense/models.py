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

from datetime import datetime
from dateutil import parser as date_parser
from typing import List


class Centroid(object):
    latitude: float
    longitude: float

    def __init__(self, centroid) -> None:
        self.latitude = centroid.get("latitude", 0.0)
        self.longitude = centroid.get("longitude", 0.0)

    def __repr__(self) -> str:
        return f"Centroid(latitude={self.latitude}, longitude={self.longitude})"


class BoundingCircle(object):
    centroid: Centroid
    radius: float

    def __init__(self, circle) -> None:
        self.radius = circle["radius"]
        self.centroid = Centroid(circle["centroid"])

    def __repr__(self) -> str:
        return f"Circle(radius={self.radius}, centroid={self.centroid})"


class Session(object):
    app_id: str
    session_id: str
    region_id: str

    cicle: BoundingCircle
    oldest_event: datetime
    newest_event: datetime
    labels: List[str]

    created_at: datetime

    def __init__(self, session) -> None:
        self.app_id = session["app_id"]
        self.session_id = session["session_id"]
        self.region_id = session.get("region_id", "")

        self.circle = BoundingCircle(session["circle"]) if "circle" in session else None
        self.oldest_event = date_parser.parse(session["oldest_event"])
        self.newest_event = date_parser.parse(session["newest_event"])
        if "labels" in session:
            self.labels = [e["name"] for e in session["labels"]]
        else:
            self.labels = []

        self.created_at = date_parser.parse(session["created_at"])

    def __repr__(self) -> str:
        return (
            f"Session(app_id={self.app_id}, session_id={self.session_id}, region_id={self.region_id}, "
            + f"circle={self.circle}, labels={self.labels}, created_at={self.created_at})"
        )


class Chunk(object):
    chunk_id: str
    md5: str
    session_id: str
    region_id: str
    created_at: datetime

    def __init__(self, session_id, region_id, chunk) -> None:
        self.chunk_id = chunk["chunk_id"]
        self.md5 = chunk["md5"]
        self.session_id = session_id
        self.region_id = region_id
        self.created_at = date_parser.parse(chunk["created_at"])

    def uri(self):
        return f"/v1/sessions/{self.session_id}/chunks/{self.chunk_id}"

    def __repr__(self) -> str:
        return f"Chunk(chunk_id={self.chunk_id}, md5={self.md5}, created_at={self.created_at})"
