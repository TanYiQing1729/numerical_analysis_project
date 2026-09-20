# Numerical Analysis Coding Exam: group_34
Submit one zip file named exactly `group_34.zip` containing:

```text
exerciseA.py
exerciseB.py
exerciseC.py
report.pdf
```

Each Python file must define `solve(params: dict) -> dict`, must run from the command
line with the corresponding `params_*.json` file, and must print only JSON to stdout.
Use only the provided imports from the course notebooks. Leave the provided imports,
`REQUIRED_KEYS`, and `main()` unchanged. Do not add new imports. Write your algorithm in
`solve(params)` and, if needed, add helper functions that are called from `solve(params)`.

The report should be 4-6 pages and should describe the mathematical formulation,
algorithm, parameters, numerical results, and an error or residual discussion for each
exercise. Your report must be submitted as `report.pdf`.

---

# Exercise A: Composite quadrature

Write the solution in the required Python file for this exercise. Your file must define
`solve(params: dict) -> dict` and must also work from the command line as

```bash
python exerciseA.py params_A.json
```

The program must print only one JSON object to stdout. Use only the provided imports
from the course notebooks.

Leave the provided imports, `REQUIRED_KEYS`, and `main()` unchanged. Do not add new
imports. Implement your numerical method inside `solve(params)`. You may add helper
functions, but they should be called from `solve(params)`.

## Public parameters

```json
{
  "L": -0.5,
  "R": 1.5,
  "a": 2.0,
  "b": -0.5,
  "c": -2.0,
  "d": 3.0,
  "n": 120,
  "p": 0.5
}
```

## Required output schema

```json
{
  "midpoint": "scalar",
  "trapezoid": "scalar",
  "simpson": "scalar"
}
```

## Task

Approximate the integral of

`f(x) = a*exp(b*x) + c*sin(d*x) + p*x**3`

over `[L, R]` using `n` equal subintervals. Return the composite midpoint,
composite trapezoidal, and composite Simpson approximations. The value of `n` is even.

---

# Exercise B: Stationary iterations for a tridiagonal system

Write the solution in the required Python file for this exercise. Your file must define
`solve(params: dict) -> dict` and must also work from the command line as

```bash
python exerciseB.py params_B.json
```

The program must print only one JSON object to stdout. Use only the provided imports
from the course notebooks.

Leave the provided imports, `REQUIRED_KEYS`, and `main()` unchanged. Do not add new
imports. Implement your numerical method inside `solve(params)`. You may add helper
functions, but they should be called from `solve(params)`.

## Public parameters

```json
{
  "epsilon": 1e-06,
  "k": 3,
  "max_iter": 50000,
  "method": "sor",
  "mu": 0.0,
  "n": 40,
  "omega": 1.0
}
```

## Required output schema

```json
{
  "iterations": "int",
  "solution": "array",
  "residual_norm": "scalar",
  "first_residuals": "array"
}
```

## Task

Let `A = tridiag(-1, 2 + mu, -1)` of size `n x n`. Define
`x_true[j] = sin(k*pi*(j+1)/(n+1))` for `j=0,...,n-1`, and `b = A @ x_true`.

Starting from `x0 = 0`, apply the method named by `method`: `jacobi`,
`gauss_seidel`, or `sor`. Stop when the relative residual
`norm(b - A @ x, 2) / norm(b, 2)` is at most `epsilon`, or after `max_iter`.
For SOR use the supplied `omega`. Return the iteration count, the final solution,
the final relative residual, and the first five relative residuals after iteration
steps 1, 2, ... .

---

# Exercise C: Two-dimensional Poisson equation

Write the solution in the required Python file for this exercise. Your file must define
`solve(params: dict) -> dict` and must also work from the command line as

```bash
python exerciseC.py params_C.json
```

The program must print only one JSON object to stdout. Use only the provided imports
from the course notebooks.

Leave the provided imports, `REQUIRED_KEYS`, and `main()` unchanged. Do not add new
imports. Implement your numerical method inside `solve(params)`. You may add helper
functions, but they should be called from `solve(params)`.

## Public parameters

```json
{
  "N": 9,
  "m": 3,
  "n": 3
}
```

## Required output schema

```json
{
  "center_value": "scalar",
  "max_error": "scalar",
  "residual_inf": "scalar"
}
```

## Task

Solve `-Delta u = f` on `(0,1)^2` with zero Dirichlet boundary conditions using
the five-point finite-difference stencil on an `N x N` interior grid. The exact
solution is

`u_exact(x,y) = sin(m*pi*x)*sin(n*pi*y)`.

Use it to construct `f` and to compute the maximum grid error. Return the numerical
solution value at `(1/2, 1/2)`, which is an interior grid point because `N` is odd,
the maximum error, and the infinity norm of the linear-system residual.
