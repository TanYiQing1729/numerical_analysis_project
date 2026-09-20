#!/usr/bin/env python3
"""Worked toy example C: solve a Green-kernel integral equation."""

import json
import sys

import numpy as np


REQUIRED_KEYS = ["nodes", "weights", "operator", "source", "reconstructed_u", "residual_inf"]


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


def green_kernel(x: float, y: float) -> float:
    if x <= y:
        return (1.0 - y) * x
    return (1.0 - x) * y


def midpoint_nodes_and_weights(n: int) -> tuple[np.ndarray, np.ndarray]:
    nodes = (np.arange(n, dtype=float) + 0.5) / n
    weights = np.full(n, 1.0 / n, dtype=float)
    return nodes, weights


def build_forward_operator(nodes: np.ndarray, weights: np.ndarray) -> np.ndarray:
    operator = np.empty((nodes.size, nodes.size), dtype=float)
    for i, x in enumerate(nodes):
        for j, y in enumerate(nodes):
            operator[i, j] = weights[j] * green_kernel(float(x), float(y))
    return operator


def residual_inf(operator: np.ndarray, source: np.ndarray, u_values: np.ndarray) -> float:
    residual = operator @ source - u_values
    return float(np.max(np.abs(residual)))


def solve(params: dict) -> dict:
    n = int(params["n"])
    u_values = np.asarray(params["u_values"], dtype=float)

    nodes, weights = midpoint_nodes_and_weights(n)
    operator = build_forward_operator(nodes, weights)
    source = np.linalg.solve(operator, u_values)
    reconstructed_u = operator @ source

    return {
        "nodes": nodes,
        "weights": weights,
        "operator": operator,
        "source": source,
        "reconstructed_u": reconstructed_u,
        "residual_inf": residual_inf(operator, source, u_values),
    }


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python exerciseC.py params_C.json")
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        params = json.load(f)
    result = solve(params)
    if set(result) != set(REQUIRED_KEYS):
        raise SystemExit(f"Output keys must be exactly {REQUIRED_KEYS}")
    print(json.dumps(_to_jsonable(result), allow_nan=False, separators=(",", ":")))


if __name__ == "__main__":
    main()
