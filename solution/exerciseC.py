#!/usr/bin/env python3
"""Student template for exercise C (P2D).

Implement solve(params) and return exactly these keys:
["center_value", "max_error", "residual_inf"]

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


REQUIRED_KEYS = ["center_value", "max_error", "residual_inf"]


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

# 手写共轭梯度CG
def conjugate_gradient(A, b, tol=1e-12, max_iter=None):
    M = A.shape[0]
    if max_iter is None:
        max_iter = M
    x = np.zeros_like(b)
    r = b - A @ x
    if np.max(np.abs(r)) < tol:
        return x
    p = r.copy()
    for _ in range(max_iter):
        Ap = A @ p
        denom = np.dot(p, Ap)
        if denom == 0.0:
            break
        alpha = np.dot(r, r) / denom
        x = x + alpha * p
        r_new = r - alpha * Ap
        if np.max(np.abs(r_new)) < tol:
            break
        beta_denom = np.dot(r, r)
        if beta_denom == 0.0:
            break
        beta = np.dot(r_new, r_new) / beta_denom
        p = r_new + beta * p
        r = r_new
    return x

def solve(params: dict) -> dict:
    N = params["N"]
    m = params["m"]
    n = params["n"]
    pi = np.pi
    h = 1.0 / (N + 1)
    M = N * N

    # 网格
    x = np.linspace(h, 1 - h, N)
    y = np.linspace(h, 1 - h, N)
    X, Y = np.meshgrid(x, y, indexing="ij")

    # 右端项
    f = pi**2 * (m**2 + n**2) * np.sin(m * pi * X) * np.sin(n * pi * Y)
    f_flat = f.flatten()
    b = h**2 * f_flat

    # 构造稠密A
    A = np.zeros((M, M), dtype=np.float64)
    for i in range(N):
        for j in range(N):
            row = i * N + j
            A[row, row] = 4.0
            if i > 0:
                A[row, (i-1)*N + j] = -1.0
            if i < N-1:
                A[row, (i+1)*N + j] = -1.0
            if j > 0:
                A[row, i*N + (j-1)] = -1.0
            if j < N-1:
                A[row, i*N + (j+1)] = -1.0

    # ========== 共轭梯度CG迭代求解 ==========
    u_flat = conjugate_gradient(A, b, tol=1e-12)

    u_num = u_flat.reshape(N, N)
    u_exact = np.sin(m * pi * X) * np.sin(n * pi * Y)

    center_idx = N // 2
    center_value = float(u_num[center_idx, center_idx])
    max_error = float(np.max(np.abs(u_num - u_exact)))
    residual_vec = A @ u_flat - b
    residual_inf = float(np.max(np.abs(residual_vec)))

    return {
        "center_value": center_value,
        "max_error": max_error,
        "residual_inf": residual_inf
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
