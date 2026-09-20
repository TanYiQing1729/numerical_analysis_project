#!/usr/bin/env python3
"""Worked toy example A: transform a vector and return summary values."""

import json
import sys

import numpy as np


REQUIRED_KEYS = ["transformed", "mean", "max_abs"]


def _to_jsonable(value):
    if isinstance(value, dict):
        return {str(k): _to_jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_to_jsonable(v) for v in value]
    if isinstance(value, np.ndarray):
        return _to_jsonable(value.tolist())
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    return value


def solve(params: dict) -> dict:
    values = np.asarray(params["values"], dtype=float)
    scale = float(params["scale"])
    shift = float(params["shift"])

    transformed = scale * values + shift
    return {
        "transformed": transformed,
        "mean": float(np.mean(transformed)),
        "max_abs": float(np.max(np.abs(transformed))),
    }


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python exerciseA.py params_A.json")
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        params = json.load(f)
    result = solve(params)
    if set(result) != set(REQUIRED_KEYS):
        raise SystemExit(f"Output keys must be exactly {REQUIRED_KEYS}")
    print(json.dumps(_to_jsonable(result), allow_nan=False, separators=(",", ":")))


if __name__ == "__main__":
    main()
