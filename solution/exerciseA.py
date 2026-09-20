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
    """
    使用复合数值积分公式近似计算定积分 ∫[L,R] f(x)dx，
    其中 f(x) = a*exp(b*x) + c*sin(d*x) + p*x**3。

    params 字典包含以下键:
        L, R : 积分上下限
        a, b, c, d, p : 被积函数 f(x) 的系数
        n : 等分子区间数（保证为偶数）

    返回包含三个复合求积近似值的字典:
        "midpoint"  : 复合中点法结果
        "trapezoid" : 复合梯形法结果
        "simpson"   : 复合辛普森法结果
    """
    # ======================== 1. 读取参数 ========================
    L = params["L"]
    R = params["R"]
    a = params["a"]
    b = params["b"]
    c = params["c"]
    d = params["d"]
    p = params["p"]
    n = params["n"]

    # ======================== 2. 定义被积函数 f(x) ========================
    # f(x) = a * exp(b*x) + c * sin(d*x) + p * x**3
    def f(x):
        return a * np.exp(b * x) + c * np.sin(d * x) + p * x**3

    # ======================== 3. 计算步长与节点 ========================
    # 步长 h = (R - L) / n
    h = (R - L) / n
    # 生成 n+1 个等距节点: x0, x1, ..., xn
    x = np.linspace(L, R, n + 1)

    # ======================== 4. 复合中点法 (Composite Midpoint) ========================
    # 公式: M_n = h * Σ_{i=0}^{n-1} f((x_i + x_{i+1}) / 2)
    # 每个子区间的中点: (x[:-1] + x[1:]) / 2
    midpoints = (x[:-1] + x[1:]) / 2.0
    midpoint = float(h * np.sum(f(midpoints)))

    # ======================== 5. 复合梯形法 (Composite Trapezoid) ========================
    # 公式: T_n = h/2 * [f(x0) + 2*Σ_{i=1}^{n-1} f(xi) + f(xn)]
    f_vals = f(x)
    trapezoid = float((h / 2.0) * (f_vals[0] + 2.0 * np.sum(f_vals[1:-1]) + f_vals[-1]))

    # ======================== 6. 复合辛普森法 (Composite Simpson) ========================
    # 公式: S_n = h/3 * [f(x0) + 4*Σ_{i odd} f(xi) + 2*Σ_{i even, i≠0,n} f(xi) + f(xn)]
    # 前提: n 必须为偶数（题目保证满足）
    # 奇数索引 i = 1, 3, 5, ..., n-1  → 权重 4
    # 偶数索引 i = 2, 4, 6, ..., n-2  → 权重 2
    simpson = float(
        (h / 3.0)
        * (
            f_vals[0]                          # f(x0)
            + 4.0 * np.sum(f_vals[1:-1:2])     # 4 * Σ_{奇数索引} f(xi)
            + 2.0 * np.sum(f_vals[2:-1:2])     # 2 * Σ_{偶数索引(不含0,n)} f(xi)
            + f_vals[-1]                        # f(xn)
        )
    )

    # ======================== 7. 返回结果 ========================
    return {
        "midpoint": midpoint,
        "trapezoid": trapezoid,
        "simpson": simpson,
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
