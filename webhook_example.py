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

import logging

from moonsense.models import WebhookPayload
from moonsense.util import json_format

from http.server import BaseHTTPRequestHandler, HTTPServer


class WebhookHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        self._set_response()
        self.wfile.write(
            "Please configure this endpoint as webhook in "
            "Moonsense for testing. POST requests will be logged.".encode("utf-8")
        )

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        request_body = self.rfile.read(content_length).decode("utf-8")

        logging.info(
            "POST request,\nPath: %s\nHeaders:\n%s",
            str(self.path),
            str(self.headers),
        )

        # Important: Before accepting the input it's important to validate the 
        # request signature. This example is kept simple on purpose.

        payload = json_format.Parse(request_body, WebhookPayload())
        logging.info("Type: %s, Session ID: %s, App ID: %s", 
            payload.event_type, payload.session_id, payload.app_id)

        # Extract basic features for mouse & touch gestures
        envelope = payload.bundle
        if envelope is not None:
            gesture = envelope.bundle.pointer_data
            if len(gesture) > 5:
                min_pressure, max_pressure = min_max([d.pressure for d in gesture])
                logging.info("Min/Max Pressure: %s / %s", min_pressure, max_pressure)

                min_radius, max_radius = min_max([d.size for d in gesture])
                logging.info("Min/Max Pointer Radius: %s / %s\n", min_radius, max_radius)

                # Run a heuristic or a model using the computed features

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode("utf-8"))

def min_max(values):
    return min(values), max(values)

def run(server_class=HTTPServer, handler_class=WebhookHandler, port=8000):
    logging.basicConfig(level=logging.INFO)

    server_address = ("", port)
    httpd = server_class(server_address, handler_class)

    logging.info("Starting httpd...\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    logging.info("Stopping httpd...\n")


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
