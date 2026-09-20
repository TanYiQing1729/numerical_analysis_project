# Example Report Structure

This is a Markdown model of the report structure. In the real exam, submit `report.pdf`.

The toy exercises in this folder are deliberately simple. Your real report should follow
the same organization but discuss the actual numerical methods from your assigned exam.

## Exercise A

State the input data and the formula used:

```text
transformed = scale * values + shift
```

Report the transformed vector, its mean, and the maximum absolute value.

## Exercise B

State the polynomial convention. In this example, coefficients are ordered from constant
term to highest degree term:

```text
p(x) = c0 + c1*x + c2*x^2 + ...
```

Explain that Horner's method evaluates the polynomial by processing coefficients from the
highest degree term down to the constant term.

Report the values at the requested points.

## Exercise C

State the integral equation being discretized:

```text
u(x) = integral_0^1 G(x,y) f(y) dy
```

Explain that the midpoint rule turns the Green-kernel integral operator into a matrix.
Report the nodes, quadrature weights, recovered source vector, reconstructed data, and
the infinity norm of the residual.

## Final Comments

For the real exam, this final section should explain whether the numerical results are
reasonable. For example, discuss the size of an error, a residual, or the difference
between two methods.
