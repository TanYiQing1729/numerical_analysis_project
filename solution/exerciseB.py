#!/usr/bin/env python3
"""Student template for exercise B (SOR1).

Implement solve(params) and return exactly these keys:
["iterations", "solution", "residual_norm", "first_residuals"]

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


REQUIRED_KEYS = ["iterations", "solution", "residual_norm", "first_residuals"]


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
    # Extract parameters
    epsilon = params["epsilon"]
    k = params["k"]
    max_iter = params["max_iter"]
    method = params["method"].lower()  # robust against case variations
    mu = params["mu"]
    n = params["n"]
    omega = params["omega"]

    d = 2.0 + mu


    # Generate exact solution and right-hand side
    j = np.arange(n)
    x_true = np.sin(k * np.pi * (j + 1) / (n + 1))

    # Compute b = A @ x_true for tridiagonal A: diag(-1, d, -1)
    # Inner formula: (A x)_i = d*x_i - x_{i-1} - x_{i+1} with zero boundaries
    b = d * x_true.copy()
    if n > 1:
        b[0] -= x_true[1]          # no left neighbor
        b[1:-1] -= (x_true[:-2] + x_true[2:])
        b[-1] -= x_true[-2]        # no right neighbor
    # if n == 1, b = d * x_true, which is already correct

    norm_b = np.linalg.norm(b, 2)
    if abs(d) < 1e-15:
        # The stationary updates divide by the diagonal entry d.
        # For mu = -2 this form is undefined, so return the zero
        # initial guess with a finite initial residual instead of NaN/Inf.
        return {
            "iterations": 0,
            "solution": np.zeros(n),
            "residual_norm": 0.0 if norm_b == 0.0 else 1.0,
            "first_residuals": [],
        }
    if norm_b == 0.0:
        # trivial case (should not happen for k>0)
        return {
            "iterations": 0,
            "solution": np.zeros(n),
            "residual_norm": 0.0,
            "first_residuals": [],
        }

    x = np.zeros(n, dtype=np.float64)
    first_residuals = []
    iterations = 0
    relres = 1.0  # initial residual norm is norm(b)

    while iterations < max_iter and relres > epsilon:
        if method == "jacobi":
            # x_new[i] = (b[i] + x[i-1] + x[i+1]) / d, neighbours = 0 at boundaries
            x_new = (b + np.roll(x, 1) + np.roll(x, -1)) / d
            if n > 1:
                x_new[0] = (b[0] + x[1]) / d
                x_new[-1] = (b[-1] + x[-2]) / d
            elif n == 1:
                x_new[0] = b[0] / d
            x = x_new

        elif method == "gauss_seidel":
            if n == 1:
                x[0] = b[0] / d
            else:
                x[0] = (b[0] + x[1]) / d
                for i in range(1, n - 1):
                    x[i] = (b[i] + x[i - 1] + x[i + 1]) / d
                x[-1] = (b[-1] + x[-2]) / d

        elif method == "sor":
            if n == 1:
                x_gs = b[0] / d
                x[0] = (1.0 - omega) * x[0] + omega * x_gs
            else:
                x_gs = (b[0] + x[1]) / d
                x[0] = (1.0 - omega) * x[0] + omega * x_gs
                for i in range(1, n - 1):
                    x_gs = (b[i] + x[i - 1] + x[i + 1]) / d
                    x[i] = (1.0 - omega) * x[i] + omega * x_gs
                x_gs = (b[-1] + x[-2]) / d
                x[-1] = (1.0 - omega) * x[-1] + omega * x_gs

        else:
            raise ValueError(f"Unknown method: {method}")

        iterations += 1

        # Residual r = b - A * x
        # A*x = d*x - (roll(x,1)+roll(x,-1))   (with corrections at boundaries)
        r = b - (d * x - (np.roll(x, 1) + np.roll(x, -1)))
        if n > 1:
            r[0] = b[0] - (d * x[0] - x[1])
            r[-1] = b[-1] - (d * x[-1] - x[-2])
        elif n == 1:
            r[0] = b[0] - d * x[0]

        norm_r = np.linalg.norm(r, 2)
        relres = norm_r / norm_b

        if iterations <= 5:
            first_residuals.append(float(relres))

    return {
        "iterations": iterations,
        "solution": x,
        "residual_norm": float(relres),
        "first_residuals": first_residuals,
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
