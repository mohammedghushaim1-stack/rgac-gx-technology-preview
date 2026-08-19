#!/usr/bin/env python3

# -*- coding: utf-8 -*-

"""

RGAC-GX Technology Preview

===========================

A small, public demonstration of selected RGAC-GX concepts.

This preview intentionally provides a limited implementation for:

- Complementary mapping

- Deterministic spatial representation

- Local spatial-neighbor analysis

- Candidate generation

- Confidence scoring

- Batch analysis

- Simple REST API

This is NOT the complete RGAC-GX platform.

"""

import math

import time

from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException

from pydantic import BaseModel, Field

import uvicorn

# ------------------------------------------------------------

# Project information

# ------------------------------------------------------------

APP_NAME = "RGAC-GX Technology Preview"

VERSION = "0.1.0-preview"

# Public preview limits

LEGACY_MAX = 72

GRID_ORDER = 8

MAX_VALUE = 3 * GRID_ORDER * (GRID_ORDER + 1)

SPATIAL_RADIUS = 2.1

MAX_CANDIDATES = 8

# ------------------------------------------------------------

# Complementary mapping

# ------------------------------------------------------------

def complement(value: int) -> int:

    """

    Calculate the complementary mapping for values 1..72.

    Example:

        1  -> 72

        20 -> 53

        72 -> 1

    """

    if not 1 <= value <= LEGACY_MAX:

        raise ValueError(

            "Complementary mapping is defined for values 1..72."

        )

    return 73 - value

# ------------------------------------------------------------

# Spatial representation

# ------------------------------------------------------------

def build_coordinates(order: int = GRID_ORDER) -> Dict[int, tuple]:

    """

    Build a deterministic lightweight spatial representation.

    The representation uses concentric rings.

    This is only a computational demonstration and should not

    be interpreted as a physical or scientific geometry model.

    """

    coordinates: Dict[int, tuple] = {}

    value = 1

    for ring in range(1, order + 1):

        points_in_ring = 6 * ring

        radius = ring * 1.5

        for index in range(points_in_ring):

            angle = (

                2.0

                * math.pi

                * index

                / points_in_ring

            )

            x = radius * math.cos(angle)

            y = radius * math.sin(angle)

            # Small deterministic third dimension

            z = (ring % 3) * 0.3

            coordinates[value] = (

                x,

                y,

                z,

            )

            value += 1

    return coordinates

COORDINATES = build_coordinates()

# ------------------------------------------------------------

# Spatial distance

# ------------------------------------------------------------

def spatial_distance(

    point_a: tuple,

    point_b: tuple,

) -> float:

    return math.sqrt(

        sum(

            (a - b) ** 2

            for a, b in zip(point_a, point_b)

        )

    )

# ------------------------------------------------------------

# Neighbor analysis

# ------------------------------------------------------------

def find_spatial_neighbors(

    value: int,

    radius: float = SPATIAL_RADIUS,

) -> List[Dict[str, Any]]:

    target = COORDINATES.get(value)

    if target is None:

        return []

    results = []

    for other_value, other_point in COORDINATES.items():

        if other_value == value:

            continue

        distance = spatial_distance(

            target,

            other_point,

        )

        if distance <= radius:

            confidence = max(

                0.0,

                min(

                    1.0,

                    1.0 - (distance / 4.0),

                ),

            )

            results.append(

                {

                    "value": other_value,

                    "distance": round(

                        distance,

                        6,

                    ),

                    "confidence": round(

                        confidence,

                        6,

                    ),

                }

            )

    results.sort(

        key=lambda item: (

            item["distance"],

            item["value"],

        )

    )

    return results[:MAX_CANDIDATES]

# ------------------------------------------------------------

# Core analysis

# ------------------------------------------------------------

def analyze_value(

    value: int,

) -> Dict[str, Any]:

    if isinstance(value, bool) or not isinstance(value, int):

        raise ValueError(

            "value must be an integer."

        )

    if value < 1 or value > MAX_VALUE:

        raise ValueError(

            f"value must be between 1 and {MAX_VALUE}."

        )

    start_time = time.perf_counter()

    result: Dict[str, Any] = {

        "input": value,

        "version": VERSION,

        "preview": True,

    }

    # --------------------------------------------------------

    # Legacy complementary mapping

    # --------------------------------------------------------

    if value <= LEGACY_MAX:

        complementary_value = complement(value)

        result["mode"] = "complementary"

        result["features"] = {

            "value": value,

            "complement": complementary_value,

            "normalized_value": round(

                value / LEGACY_MAX,

                6,

            ),

        }

        result["candidates"] = [

            {

                "value": complementary_value,

                "confidence": 0.80,

                "evidence": [

                    "complementary_mapping"

                ],

            }

        ]

    # --------------------------------------------------------

    # Spatial analysis

    # --------------------------------------------------------

    else:

        point = COORDINATES[value]

        neighbors = find_spatial_neighbors(

            value

        )

        result["mode"] = "spatial-preview"

        result["coordinates"] = {

            "x": round(point[0], 6),

            "y": round(point[1], 6),

            "z": round(point[2], 6),

        }

        result["features"] = {

            "value": value,

            "neighbor_count": len(neighbors),

        }

        result["candidates"] = [

            {

                "value": item["value"],

                "distance": item["distance"],

                "confidence": item["confidence"],

                "evidence": [

                    "spatial_proximity"

                ],

            }

            for item in neighbors

        ]

    elapsed = (

        time.perf_counter()

        - start_time

    ) * 1000

    result["latency_ms"] = round(

        elapsed,

        4,

    )

    return result

# ------------------------------------------------------------

# API models

# ------------------------------------------------------------

class AnalyzeRequest(BaseModel):

    value: int = Field(

        ...,

        ge=1,

        le=MAX_VALUE,

        description="Integer value to analyze.",

    )

class BatchRequest(BaseModel):

    values: List[int] = Field(

        ...,

        min_length=1,

        max_length=100,

        description="List of values to analyze.",

    )

# ------------------------------------------------------------

# FastAPI application

# ------------------------------------------------------------

app = FastAPI(

    title=APP_NAME,

    version=VERSION,

    description=(

        "A small and intentionally limited public "

        "demonstration of selected RGAC-GX concepts."

    ),

)

# ------------------------------------------------------------

# Root endpoint

# ------------------------------------------------------------

@app.get("/")

async def root() -> Dict[str, Any]:

    return {

        "name": APP_NAME,

        "version": VERSION,

        "status": "ready",

        "free_preview": True,

        "documentation": "/docs",

        "health": "/health",

        "max_value": MAX_VALUE,

    }

# ------------------------------------------------------------

# Health endpoint

# ------------------------------------------------------------

@app.get("/health")

async def health() -> Dict[str, Any]:

    return {

        "status": "ok",

        "version": VERSION,

        "preview": True,

        "coordinate_count": len(

            COORDINATES

        ),

    }

# ------------------------------------------------------------

# Public scope endpoint

# ------------------------------------------------------------

@app.get("/license")

async def license_info() -> Dict[str, Any]:

    return {

        "type": "free-technology-preview",

        "commercial_license": False,

        "scope": "public technical demonstration",

        "version": VERSION,

    }

# ------------------------------------------------------------

# Single-value analysis

# ------------------------------------------------------------

@app.post("/api/analyze")

async def analyze(

    request: AnalyzeRequest,

) -> Dict[str, Any]:

    try:

        return analyze_value(

            request.value

        )

    except ValueError as error:

        raise HTTPException(

            status_code=400,

            detail=str(error),

        )

# ------------------------------------------------------------

# Batch analysis

# ------------------------------------------------------------

@app.post("/api/batch")

async def batch(

    request: BatchRequest,

) -> Dict[str, Any]:

    try:

        results = [

            analyze_value(value)

            for value in request.values

        ]

        return {

            "count": len(results),

            "preview": True,

            "results": results,

        }

    except ValueError as error:

        raise HTTPException(

            status_code=400,

            detail=str(error),

        )

# ------------------------------------------------------------

# Local execution

# ------------------------------------------------------------

if __name__ == "__main__":

    uvicorn.run(

        "rgac_gx_technology_preview:app",

        host="127.0.0.1",

        port=8080,

        reload=False,

    )
