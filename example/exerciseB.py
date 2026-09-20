#!/usr/bin/env python3
"""Worked toy example B: evaluate a polynomial with Horner's method."""

import json
import sys

import numpy as np


REQUIRED_KEYS = ["values", "sum_values", "degree"]


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


def horner(coefficients: np.ndarray, x: float) -> float:
    # Coefficients are ordered from constant term to highest degree term.
    value = 0.0
    for coefficient in coefficients[::-1]:
        value = value * x + coefficient
    return float(value)


def evaluate_polynomial(coefficients: np.ndarray, points: np.ndarray) -> np.ndarray:
    return np.array([horner(coefficients, x) for x in points], dtype=float)


def solve(params: dict) -> dict:
    coefficients = np.asarray(params["coefficients"], dtype=float)
    points = np.asarray(params["points"], dtype=float)
    values = evaluate_polynomial(coefficients, points)

    return {
        "values": values,
        "sum_values": float(np.sum(values)),
        "degree": int(len(coefficients) - 1),
    }


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python exerciseB.py params_B.json")
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        params = json.load(f)
    result = solve(params)
    if set(result) != set(REQUIRED_KEYS):
        raise SystemExit(f"Output keys must be exactly {REQUIRED_KEYS}")
    print(json.dumps(_to_jsonable(result), allow_nan=False, separators=(",", ":")))


if __name__ == "__main__":
    main()
