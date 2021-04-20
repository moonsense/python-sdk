from datetime import datetime
from dateutil import parser as date_parser
from typing import List


class Centroid(object):
    latitude: float
    longitude: float

    def __init__(self, centroid) -> None:
        self.latitude = centroid.get('latitude', 0.0)
        self.longitude = centroid.get('longitude', 0.0)

    def __repr__(self) -> str:
        return f"Centroid(latitude={self.latitude}, longitude={self.longitude})"


class BoundingCircle(object):
    centroid: Centroid
    radius: float

    def __init__(self, circle) -> None:
        self.radius = circle["radius"]
        self.centroid = Centroid(circle['centroid'])

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
        if 'labels' in session:
            self.labels = [e['name'] for e in session['labels']]
        else:
            self.labels = []

        self.created_at = date_parser.parse(session["created_at"])

    def __repr__(self) -> str:
        return (
            f"Session(app_id={self.app_id}, session_id={self.session_id}, region_id={self.region_id}, "
            + f"circle={self.circle}, labels={self.labels}, created_at={self.created_at})"
        )
