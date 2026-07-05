import sympy as sp


def get_gradient(equation_str: str):
    """Takes a string equation, converts it xto math, and returns the gradient."""
    # Define our standard symbols
    x, y, z = sp.symbols("x y z")

    local_dict = {"e": sp.E, "exp": sp.exp, "x": x, "y": y, "z": z}
    # Safely convert the user's string into a SymPy expression
    # e.g., "x**2 + y**2" becomes mathematical x^2 + y^2, you dont have to use the ** operator, you can use ^ as well and the sympify function will handle it.
    expr = sp.sympify(equation_str, locals=local_dict)

    # Calculate partial derivatives
    df_dx = sp.diff(expr, x)
    df_dy = sp.diff(expr, y)
    df_dz = sp.diff(expr, z)

    # Return a dictionary with the results
    return {"equation": expr, "dx": df_dx, "dy": df_dy, "dz": df_dz}


def get_lagrange(objectiveFunction: str, constraintFunction: str):
    """Takes a string equation, converts it to math, and returns the critical points and optimal values."""
    x, y, z, lembda = sp.symbols("x y z λ")

    # Clean the strings by removing leading/trailing whitespaces and quotes
    objectiveFunction = sp.sympify(objectiveFunction.strip("\"'"))
    constraintFunction = sp.sympify(constraintFunction.strip("\"'"))

    diffObjectiveFunction = (
        sp.diff(objectiveFunction, x),
        sp.diff(objectiveFunction, y),
        sp.diff(objectiveFunction, z),
    )
    diffConstraintFunction = (
        sp.diff(constraintFunction, x),
        sp.diff(constraintFunction, y),
        sp.diff(constraintFunction, z),
    )

    # df/dx = λ * dg/dx, df/dy = λ * dg/dy, df/dz = λ * dg/dz
    lembdaEq = (
        sp.Eq(diffObjectiveFunction[0] - lembda * diffConstraintFunction[0], 0),
        sp.Eq(diffObjectiveFunction[1] - lembda * diffConstraintFunction[1], 0),
        sp.Eq(diffObjectiveFunction[2] - lembda * diffConstraintFunction[2], 0),
    )

    # Solve system of equations
    solution = sp.solve(lembdaEq + (sp.Eq(constraintFunction, 0),), (x, y, z, lembda))

    # Force the solution into a list format so each result can be processed uniformly
    if isinstance(solution, dict):
        solution = [solution]

    criticalPoints = []
    for sol in solution:
        if isinstance(sol, dict):
            # Linear case: sol is a dictionary, so we can safely extract values using .get() to avoid KeyError if a symbol is missing
            # Safe extraction using .get() with a default fallback of 0 if symbol isn't present
            pt = (sol.get(x, 0), sol.get(y, 0), sol.get(z, 0))
        else:
            # Non-linear case: sol is a tuple, so we can directly access the elements by index
            # Handles fallback if SymPy returns a list of tuples instead
            pt = (sol[0], sol[1], sol[2])
        criticalPoints.append(pt)
    # Evaluate the objective at each critical point
    optimalValues = [
        objectiveFunction.subs({x: pt[0], y: pt[1], z: pt[2]}) for pt in criticalPoints
    ]

    return [{"criticalPoints": criticalPoints, "optimalValues": optimalValues}, {"diffConstraintFunction": diffConstraintFunction, "diffObjectiveFunction": diffObjectiveFunction, "lembdaEq": lembdaEq, "solution": solution}]


if __name__ == "__main__":
    equation1 = input(
        "Enter the objective function in terms of x, y, z (e.g., 'x**2 + y**2 + z**2'): "
    )
    equation2 = input(
        "Enter the constraint function in terms of x, y, z (e.g., 'x + y + z - 1'): "
    )
    print(get_lagrange(equation1, equation2))
