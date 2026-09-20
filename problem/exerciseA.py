#!/usr/bin/env python3
"""Student template for exercise A (Q1).

Implement solve(params) and return exactly these keys:
["midpoint", "trapezoid", "simpson"]

Do not add imports. Use only the provided imports from the course notebooks.
Do not change REQUIRED_KEYS or main(). You may add helper functions, but call them
from solve(params).
"""

import json
import sys
import math
import time
import warnings

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.linalg as la
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import sympy
from IPython.display import display
from mpl_toolkits.mplot3d import Axes3D
from numpy import finfo, float32
from numpy.polynomial import Polynomial
from scipy.integrate import quad
from scipy.integrate import simpson as sp_simpson
from scipy.integrate import trapezoid as sp_trapezoid
from scipy.special import comb


REQUIRED_KEYS = ["midpoint", "trapezoid", "simpson"]


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
    # Replace this with your implementation.
    raise NotImplementedError("Implement exercise A (Q1).")


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
