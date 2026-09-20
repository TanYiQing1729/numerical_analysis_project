# Worked Example Coding Exam

This folder is a complete solved example of the submission format. It is not one of the
real group exams, and the tasks are intentionally simpler than
the real exam tasks.

The goal is to show the required file structure, command-line behavior, and JSON output
format without giving away a solution to any real exercise family.

## Files

```text
example_exam/
  exerciseA.py
  exerciseB.py
  exerciseC.py
  params_A.json
  params_B.json
  params_C.json
  expected_outputs.json
  report_example.md
```

In the real exam, each group submits a zip containing:

```text
exerciseA.py
exerciseB.py
exerciseC.py
report.pdf
```

The parameter JSON files are supplied by the instructor and are not submitted unless the
instructor explicitly asks for them.

## Step 1: Inspect the Required Interface

Every exercise file must define:

```python
def solve(params: dict) -> dict:
    ...
```

Every file must also run from the command line and print only one JSON object:

```bash
python exerciseA.py params_A.json
```

Do not print explanations, tables, debug messages, or extra text. The program must print
only one JSON object to stdout.

In the real exam template, leave these parts unchanged:

- the provided imports from the course notebooks;
- `REQUIRED_KEYS`;
- `main()`;
- the final `if __name__ == "__main__": main()` block.

Do not add new imports. Implement the numerical method inside `solve(params)`. You may
add helper functions, constants, or small internal utilities, but they should be called
from `solve(params)`.

## Step 2: Run the Example

From this folder, run:

```bash
python exerciseA.py params_A.json
python exerciseB.py params_B.json
python exerciseC.py params_C.json
```

The output should match `expected_outputs.json`, up to small floating-point differences.

## Step 3: Understand the Three Toy Exercises

Exercise A reads a vector, applies `scale * values + shift`, and returns the transformed
vector plus two summary statistics.

Exercise B evaluates a polynomial at several points using Horner's method. This shows how
to define helper functions outside `solve(params)` and then call them from inside
`solve(params)`.

Exercise C discretizes a Green-kernel integral operator with the midpoint rule and solves
the resulting linear system. It is still short, but it is closer to the type of numerical
method organization used in the real exercises.

These toy tasks are only for demonstrating the interface. The real exam exercises are
more substantial and have different required output keys.

## Step 4: Organize Longer Solutions With Helper Functions

The files `exerciseB.py` and `exerciseC.py` show a useful solution style:

- helper functions are defined before `solve(params)`;
- `solve(params)` reads the input parameters and calls the helper functions;
- imports, `REQUIRED_KEYS`, and `main()` are unchanged;
- no new imports are added.

This is the recommended pattern for longer numerical methods. For example, you may define
functions such as `rk4_step`, `build_matrix`, `residual_norm`, or `newton_iteration`
outside `solve(params)`, then call them inside `solve(params)`.

## Step 5: Prepare a Real Submission

For the real exam, work inside your own group folder.
Keep the filenames exactly:

```text
exerciseA.py
exerciseB.py
exerciseC.py
```

Each script should read its corresponding parameter file when run from the command line:

```bash
python exerciseA.py params_A.json
python exerciseB.py params_B.json
python exerciseC.py params_C.json
```

Before submitting, create a zip named exactly like your group:

```text
group_XX.zip
```

with exactly:

```text
exerciseA.py
exerciseB.py
exerciseC.py
report.pdf
```

## Step 6: Write the Report

Use `report_example.md` as a model for the structure. Your real report should be a PDF
and should include, for each exercise:

- the mathematical problem
- the numerical method
- the parameters used
- the numerical results
- an error or residual discussion

## Common Mistakes

- Returning the wrong keys.
- Hard-coding one numerical answer instead of solving from the input `params`.
- Adding new imports instead of using the imports already provided in the template.
- Editing `REQUIRED_KEYS` or `main()`.
- Forgetting to include `report.pdf` in the zip.
- Renaming files, for example `exercise_a.py` instead of `exerciseA.py`.
