#!/usr/bin/env python3

# -*- coding: utf-8 -*-

"""

RGAC-GX Technology Preview

==========================

Single-file public technical demonstration.

This preview demonstrates:

- Structured relationships

- Deterministic spatial representation

- Complementary mapping

- Local spatial-neighbor analysis

- Basic graph metrics

- JSON export

This is a limited technology preview.

It is NOT the complete RGAC-GX platform.

"""

import json

import math

import time

from dataclasses import dataclass, asdict

from http.server import BaseHTTPRequestHandler, HTTPServer

from urllib.parse import urlparse

# ============================================================

# Data model

# ============================================================

@dataclass

class Node:

    node_id: str

    x: float

    y: float

    value: float = 0.0

    label: str = ""

@dataclass

class Relation:

    source: str

    target: str

    weight: float = 1.0

# ============================================================

# RGAC-GX core

# ============================================================

class RGACGX:

    """

    Minimal deterministic RGAC-GX computational preview.

    The implementation intentionally keeps the public preview

    small and understandable.

    """

    def __init__(self):

        self.nodes = {}

        self.relations = []

    # --------------------------------------------------------

    # Node operations

    # --------------------------------------------------------

    def add_node(self, node_id, x, y, value=0.0, label=""):

        node = Node(

            node_id=str(node_id),

            x=float(x),

            y=float(y),

            value=float(value),

            label=str(label),

        )

        self.nodes[node.node_id] = node

        return node

    def add_relation(self, source, target, weight=1.0):

        source = str(source)

        target = str(target)

        if source not in self.nodes:

            raise ValueError(f"Unknown source node: {source}")

        if target not in self.nodes:

            raise ValueError(f"Unknown target node: {target}")

        relation = Relation(

            source=source,

            target=target,

            weight=float(weight),

        )

        self.relations.append(relation)

        return relation

    # --------------------------------------------------------

    # Spatial calculations

    # --------------------------------------------------------

    def distance(self, a, b):

        """

        Euclidean distance between two nodes.

        """

        if a not in self.nodes:

            raise ValueError(f"Unknown node: {a}")

        if b not in self.nodes:

            raise ValueError(f"Unknown node: {b}")

        n1 = self.nodes[a]

        n2 = self.nodes[b]

        dx = n1.x - n2.x

        dy = n1.y - n2.y

        return math.sqrt(dx * dx + dy * dy)

    def nearest_neighbors(self, node_id, limit=3):

        """

        Return nearest spatial neighbors.

        """

        if node_id not in self.nodes:

            raise ValueError(f"Unknown node: {node_id}")

        candidates = []

        for other_id in self.nodes:

            if other_id == node_id:

                continue

            d = self.distance(node_id, other_id)

            candidates.append({

                "node": other_id,

                "distance": round(d, 6),

            })

        candidates.sort(key=lambda item: item["distance"])

        return candidates[:max(0, int(limit))]

    # --------------------------------------------------------

    # Graph calculations

    # --------------------------------------------------------

    def degree(self, node_id):

        """

        Number of direct relations involving a node.

        """

        count = 0

        for relation in self.relations:

            if relation.source == node_id:

                count += 1

            if relation.target == node_id:

                count += 1

        return count

    def graph_summary(self):

        """

        Produce deterministic graph statistics.

        """

        degrees = {

            node_id: self.degree(node_id)

            for node_id in self.nodes

        }

        total_weight = sum(

            relation.weight

            for relation in self.relations

        )

        return {

            "nodes": len(self.nodes),

            "relations": len(self.relations),

            "total_relation_weight": round(total_weight, 6),

            "degrees": degrees,

        }

    # --------------------------------------------------------

    # Complementary mapping

    # --------------------------------------------------------

    def complementary_map(self):

        """

        Demonstration of a complementary spatial/value mapping.

        The transformation is deterministic and intentionally

        simple for public experimentation.

        """

        if not self.nodes:

            return []

        values = [

            node.value

            for node in self.nodes.values()

        ]

        minimum = min(values)

        maximum = max(values)

        result = []

        for node in self.nodes.values():

            if maximum == minimum:

                normalized = 0.5

            else:

                normalized = (

                    (node.value - minimum)

                    / (maximum - minimum)

                )

            result.append({

                "node": node.node_id,

                "x": round(node.x, 6),

                "y": round(node.y, 6),

                "value": round(node.value, 6),

                "normalized": round(normalized, 6),

                "complement": round(1.0 - normalized, 6),

            })

        return result

    # --------------------------------------------------------

    # Local analysis

    # --------------------------------------------------------

    def local_analysis(self, node_id, radius=10.0):

        """

        Analyze nodes located within a spatial radius.

        """

        if node_id not in self.nodes:

            raise ValueError(f"Unknown node: {node_id}")

        result = []

        for other_id in self.nodes:

            if other_id == node_id:

                continue

            d = self.distance(node_id, other_id)

            if d <= radius:

                result.append({

                    "node": other_id,

                    "distance": round(d, 6),

                    "value": round(

                        self.nodes[other_id].value,

                        6,

                    ),

                })

        result.sort(key=lambda item: item["distance"])

        return {

            "center": node_id,

            "radius": float(radius),

            "neighbors": result,

        }

    # --------------------------------------------------------

    # Complete export

    # --------------------------------------------------------

    def export(self):

        return {

            "technology": "RGAC-GX",

            "preview": True,

            "generated_at": int(time.time()),

            "nodes": [

                asdict(node)

                for node in self.nodes.values()

            ],

            "relations": [

                asdict(relation)

                for relation in self.relations

            ],

            "summary": self.graph_summary(),

            "complementary_mapping":

                self.complementary_map(),

        }

# ============================================================

# Example dataset

# ============================================================

def build_demo():

    gx = RGACGX()

    gx.add_node(

        "A",

        0,

        0,

        value=10,

        label="Origin",

    )

    gx.add_node(

        "B",

        4,

        2,

        value=30,

        label="North",

    )

    gx.add_node(

        "C",

        8,

        1,

        value=20,

        label="East",

    )

    gx.add_node(

        "D",

        3,

        7,

        value=50,

        label="Upper",

    )

    gx.add_node(

        "E",

        9,

        6,

        value=40,

        label="Far",

    )

    gx.add_relation("A", "B", 1.0)

    gx.add_relation("B", "C", 0.8)

    gx.add_relation("A", "D", 1.2)

    gx.add_relation("D", "E", 0.9)

    gx.add_relation("C", "E", 1.1)

    return gx

# ============================================================

# JSON API

# ============================================================

GX = build_demo()

class RGACHandler(BaseHTTPRequestHandler):

    def send_json(self, payload, status=200):

        body = json.dumps(

            payload,

            ensure_ascii=False,

            indent=2,

        ).encode("utf-8")

        self.send_response(status)

        self.send_header(

            "Content-Type",

            "application/json; charset=utf-8",

        )

        self.send_header(

            "Content-Length",

            str(len(body)),

        )

        self.end_headers()

        self.wfile.write(body)

    def do_GET(self):

        path = urlparse(self.path).path

        if path == "/":

            self.send_json({

                "technology": "RGAC-GX",

                "preview": True,

                "message":

                    "RGAC-GX public technology preview",

                "endpoints": [

                    "/health",

                    "/summary",

                    "/nodes",

                    "/mapping",

                    "/neighbors/A",

                    "/export",

                ],

            })

            return

        if path == "/health":

            self.send_json({

                "status": "ok",

                "technology": "RGAC-GX",

                "preview": True,

            })

            return

        if path == "/summary":

            self.send_json(

                GX.graph_summary()

            )

            return

        if path == "/nodes":

            self.send_json({

                "nodes": [

                    asdict(node)

                    for node in GX.nodes.values()

                ]

            })

            return

        if path == "/mapping":

            self.send_json({

                "mapping":

                    GX.complementary_map()

            })

            return

        if path.startswith("/neighbors/"):

            node_id = path.split(

                "/neighbors/",

                1,

            )[1]

            try:

                result = GX.local_analysis(

                    node_id,

                    radius=10,

                )

                self.send_json(result)

            except ValueError as exc:

                self.send_json(

                    {"error": str(exc)},

                    status=404,

                )

            return

        if path == "/export":

            self.send_json(

                GX.export()

            )

            return

        self.send_json(

            {

                "error": "Not found",

                "path": path,

            },

            status=404,

        )

    def log_message(self, format, *args):

        return

# ============================================================

# Local execution

# ============================================================

def main():

    host = "127.0.0.1"

    port = 8080

    server = HTTPServer(

        (host, port),

        RGACHandler,

    )

    print("=" * 60)

    print("RGAC-GX Technology Preview")

    print("=" * 60)

    print(f"Server: http://{host}:{port}")

    print()

    print("Available endpoints:")

    print("  /health")

    print("  /summary")

    print("  /nodes")

    print("  /mapping")

    print("  /neighbors/A")

    print("  /export")

    print()

    print("Press Ctrl+C to stop.")

    print("=" * 60)

    try:

        server.serve_forever()

    except KeyboardInterrupt:

        print("\nStopping RGAC-GX preview...")

    finally:

        server.server_close()

if __name__ == "__main__":

    main()
