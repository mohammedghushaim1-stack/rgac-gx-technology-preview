#!/usr/bin/env python3

# -*- coding: utf-8 -*-

"""

RGAC-GX Technology Preview

Single-file public demonstration.

This is a limited public Technology Preview.

It is NOT the complete RGAC-GX platform.

"""

import json

import math

import time

from http.server import BaseHTTPRequestHandler, HTTPServer

from urllib.parse import urlparse

APP_NAME = "RGAC-GX Technology Preview"

VERSION = "1.0.0-preview"

LEGACY_MAX = 72

GRID_ORDER = 8

MAX_VALUE = 3 * GRID_ORDER * (GRID_ORDER + 1)

SPATIAL_RADIUS = 2.1

MAX_CANDIDATES = 8

# ------------------------------------------------------------

# Complementary mapping

# ------------------------------------------------------------

def complement(value):

    if not isinstance(value, int) or isinstance(value, bool):

        raise ValueError("value must be an integer")

    if value < 1 or value > LEGACY_MAX:

        raise ValueError("complementary mapping is defined for 1..72")

    return 73 - value

# ------------------------------------------------------------

# Lightweight deterministic spatial representation

# ------------------------------------------------------------

def build_coordinates(order=GRID_ORDER):

    coordinates = {}

    value = 1

    for ring in range(1, order + 1):

        points = 6 * ring

        radius = ring * 1.5

        for index in range(points):

            angle = 2 * math.pi * index / points

            x = radius * math.cos(angle)

            y = radius * math.sin(angle)

            z = (ring % 3) * 0.3

            coordinates[value] = (x, y, z)

            value += 1

    return coordinates

COORDINATES = build_coordinates()

def distance(a, b):

    return math.sqrt(

        sum((x - y) ** 2 for x, y in zip(a, b))

    )

# ------------------------------------------------------------

# Spatial candidate analysis

# ------------------------------------------------------------

def find_neighbors(value):

    if value not in COORDINATES:

        return []

    target = COORDINATES[value]

    results = []

    for other, point in COORDINATES.items():

        if other == value:

            continue

        d = distance(target, point)

        if d <= SPATIAL_RADIUS:

            confidence = max(

                0.0,

                min(1.0, 1.0 - d / 4.0)

            )

            results.append({

                "value": other,

                "distance": round(d, 6),

                "confidence": round(confidence, 6)

            })

    results.sort(

        key=lambda item: (

            item["distance"],

            item["value"]

        )

    )

    return results[:MAX_CANDIDATES]

# ------------------------------------------------------------

# Core RGAC-GX preview analysis

# ------------------------------------------------------------

def analyze(value):

    if not isinstance(value, int) or isinstance(value, bool):

        raise ValueError("value must be an integer")

    if value < 1 or value > MAX_VALUE:

        raise ValueError(

            f"value must be between 1 and {MAX_VALUE}"

        )

    started = time.perf_counter()

    result = {

        "input": value,

        "version": VERSION,

        "preview": True

    }

    # --------------------------------------------------------

    # Complementary analysis

    # --------------------------------------------------------

    if value <= LEGACY_MAX:

        opposite = complement(value)

        result["mode"] = "complementary"

        result["features"] = {

            "value": value,

            "complement": opposite,

            "normalized_value": round(

                value / LEGACY_MAX,

                6

            )

        }

        result["candidates"] = [{

            "value": opposite,

            "confidence": 0.80,

            "evidence": [

                "complementary_mapping"

            ]

        }]

    # --------------------------------------------------------

    # Spatial analysis

    # --------------------------------------------------------

    else:

        point = COORDINATES[value]

        neighbors = find_neighbors(value)

        result["mode"] = "spatial-preview"

        result["coordinates"] = {

            "x": round(point[0], 6),

            "y": round(point[1], 6),

            "z": round(point[2], 6)

        }

        result["features"] = {

            "value": value,

            "neighbor_count": len(neighbors)

        }

        result["candidates"] = [

            {

                "value": item["value"],

                "distance": item["distance"],

                "confidence": item["confidence"],

                "evidence": [

                    "spatial_proximity"

                ]

            }

            for item in neighbors

        ]

    result["latency_ms"] = round(

        (time.perf_counter() - started) * 1000,

        4

    )

    return result

# ------------------------------------------------------------

# HTTP server

# ------------------------------------------------------------

class RGACHandler(BaseHTTPRequestHandler):

    def send_json(self, data, status=200):

        body = json.dumps(

            data,

            indent=2,

            ensure_ascii=False

        ).encode("utf-8")

        self.send_response(status)

        self.send_header(

            "Content-Type",

            "application/json; charset=utf-8"

        )

        self.send_header(

            "Content-Length",

            str(len(body))

        )

        self.end_headers()

        self.wfile.write(body)

    def send_html(self, html):

        body = html.encode("utf-8")

        self.send_response(200)

        self.send_header(

            "Content-Type",

            "text/html; charset=utf-8"

        )

        self.send_header(

            "Content-Length",

            str(len(body))

        )

        self.end_headers()

        self.wfile.write(body)

    def read_json(self):

        length = int(

            self.headers.get(

                "Content-Length",

                0

            )

        )

        if length <= 0:

            return {}

        raw = self.rfile.read(length)

        return json.loads(

            raw.decode("utf-8")

        )

    # --------------------------------------------------------

    # GET

    # --------------------------------------------------------

    def do_GET(self):

        path = urlparse(

            self.path

        ).path

        if path == "/":

            self.send_json({

                "name": APP_NAME,

                "version": VERSION,

                "status": "ready",

                "free_preview": True,

                "endpoints": [

                    "/health",

                    "/license",

                    "/docs",

                    "/api/analyze",

                    "/api/batch"

                ]

            })

            return

        if path == "/health":

            self.send_json({

                "status": "ok",

                "version": VERSION,

                "preview": True,

                "coordinate_count": len(

                    COORDINATES

                )

            })

            return

        if path == "/license":

            self.send_json({

                "type": "free-technology-preview",

                "commercial_license": False,

                "scope": "public technical demonstration",

                "version": VERSION

            })

            return

        if path == "/docs":

            self.send_html("""

<!DOCTYPE html>

<html>

<head>

<meta charset="utf-8">

<title>RGAC-GX Technology Preview</title>

</head>

<body>

<h1>RGAC-GX Technology Preview</h1>

<h2>Available endpoints</h2>

<ul>

<li>GET /</li>

<li>GET /health</li>

<li>GET /license</li>

<li>POST /api/analyze</li>

<li>POST /api/batch</li>

</ul>

<h2>Example</h2>

<p>POST /api/analyze</p>

<pre>

{

  "value": 20

}

</pre>

<p>

For values 1..72 the preview demonstrates

the complementary relationship:

</p>

<pre>

73 - value

</pre>

<p>

This is an intentionally limited public

Technology Preview.

</p>

</body>

</html>

""")

            return

        self.send_json({

            "error": "endpoint not found"

        }, 404)

    # --------------------------------------------------------

    # POST

    # --------------------------------------------------------

    def do_POST(self):

        path = urlparse(

            self.path

        ).path

        try:

            data = self.read_json()

        except Exception:

            self.send_json({

                "error": "invalid JSON"

            }, 400)

            return

        # ----------------------------------------------------

        # Single analysis

        # ----------------------------------------------------

        if path == "/api/analyze":

            if "value" not in data:

                self.send_json({

                    "error": "missing value"

                }, 400)

                return

            try:

                value = data["value"]

                result = analyze(value)

                self.send_json(result)

            except ValueError as error:

                self.send_json({

                    "error": str(error)

                }, 400)

            return

        # ----------------------------------------------------

        # Batch analysis

        # ----------------------------------------------------

        if path == "/api/batch":

            values = data.get("values")

            if not isinstance(values, list):

                self.send_json({

                    "error": "values must be a list"

                }, 400)

                return

            if len(values) == 0:

                self.send_json({

                    "error": "values list is empty"

                }, 400)

                return

            if len(values) > 100:

                self.send_json({

                    "error": "maximum batch size is 100"

                }, 400)

                return

            try:

                results = [

                    analyze(value)

                    for value in values

                ]

                self.send_json({

                    "count": len(results),

                    "preview": True,

                    "results": results

                })

            except ValueError as error:

                self.send_json({

                    "error": str(error)

                }, 400)

            return

        self.send_json({

            "error": "endpoint not found"

        }, 404)

# ------------------------------------------------------------

# Start server

# ------------------------------------------------------------

def main():

    host = "127.0.0.1"

    port = 8080

    server = HTTPServer(

        (host, port),

        RGACHandler

    )

    print("")

    print("=" * 60)

    print("RGAC-GX Technology Preview")

    print("=" * 60)

    print(f"Version : {VERSION}")

    print(f"Server  : http://{host}:{port}")

    print(f"Docs    : http://{host}:{port}/docs")

    print("")

    print("Press Ctrl+C to stop.")

    print("=" * 60)

    print("")

    try:

        server.serve_forever()

    except KeyboardInterrupt:

        print("\nStopping server...")

    finally:

        server.server_close()

if __name__ == "__main__":

    main()
