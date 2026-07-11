from sympy.vector import CoordSys3D, Vector
import sympy as sp
from typing import Any
from typing import Any, Union

def get_gradient(equation: Union[str, sp.Expr]) -> dict[str, Any]:
    """Takes a string equation, converts it to math, and returns the gradient."""
    x, y, z = sp.symbols("x y z")
    local_dict = {"e": sp.E, "exp": sp.exp, "x": x, "y": y, "z": z}

    # Safely handle both strings and existing SymPy objects
    if isinstance(equation, str):
        expr = sp.sympify(equation.strip("\"'"), locals=local_dict)
    else:
        expr = equation  # It's already a SymPy expression!

    # Calculate the gradient vector with SymPy
    gradient_vector = sp.derive_by_array(expr, (x, y, z))

    return {
        "equation": expr,
        "vector": gradient_vector,  
        "dx": gradient_vector[0],
        "dy": gradient_vector[1],
        "dz": gradient_vector[2],
    }

def get_lagrange(objectiveFunction: Union[str, sp.Expr], constraintFunction: Union[str, sp.Expr]) -> list[dict[str, Any]]:
    """Takes a string equation, converts it to math, and returns the critical points and optimal values."""
    x, y, z, lembda = sp.symbols("x y z λ")

    obj_data = get_gradient(objectiveFunction)
    const_data = get_gradient(constraintFunction)

    objectiveExpr = obj_data["equation"]
    constraintExpr = const_data["equation"]

    diffObjectiveFunction = obj_data["vector"]
    diffConstraintFunction = const_data["vector"]

    lembdaEq = tuple(
        sp.Eq(diffObjectiveFunction[i] - lembda * diffConstraintFunction[i], 0)
        for i in range(3)
    )

    solution = sp.solve(lembdaEq + (sp.Eq(constraintExpr, 0),), (x, y, z, lembda))

    if isinstance(solution, dict):
        solution = [solution]

    criticalPoints = []
    for sol in solution:
        if isinstance(sol, dict):
            pt = (sol.get(x, 0), sol.get(y, 0), sol.get(z, 0))
        else:
            pt = (sol[0], sol[1], sol[2])
        criticalPoints.append(pt)

    optimalValues = [
        objectiveExpr.subs({x: pt[0], y: pt[1], z: pt[2]}) for pt in criticalPoints
    ]

    return [
        {"criticalPoints": criticalPoints, "optimalValues": optimalValues},
        {
            "diffConstraintFunction": diffConstraintFunction,
            "diffObjectiveFunction": diffObjectiveFunction,
            "lembdaEq": lembdaEq,
            "solution": solution,
        },
    ]

def get_vector_operation(v1_str: Union[str, sp.Expr], v2_str: Union[str, sp.Expr], operation: str) -> Union[Vector, sp.Expr]:    
    """
    Parses string inputs and calculates the specified vector operation.
    """
    x, y, z = sp.symbols('x y z')
    local_dict = {"x": x, "y": y, "z": z}

    N = CoordSys3D('N')
    unit_vectors = [N.i, N.j, N.k]
    
    def parse_input(val_str):
        val_str = str(val_str).strip()
        if val_str.startswith('[') and val_str.endswith(']'):
            components = val_str[1:-1].split(',')
            return sum(
                (sp.sympify(c, locals=local_dict) * u for c, u in zip(components, unit_vectors)), 
                Vector.zero
            )
        return sp.sympify(val_str, locals=local_dict)

    val1 = parse_input(v1_str)
    val2 = parse_input(v2_str)

    def safe_dot(a, b):
        if isinstance(a, Vector) and isinstance(b, Vector):
            return a.dot(b)
        raise ValueError("Mathematical Error: The dot product is only defined between two vectors.")

    def safe_cross(a, b):
        if isinstance(a, Vector) and isinstance(b, Vector):
            return a.cross(b)
        raise ValueError("Mathematical Error: The cross product is only defined between two vectors.")

    # Dictionary mapping string commands to mathematical operations
    operations = {
        "add": lambda a, b: a + b,
        "subtract": lambda a, b: a - b,
        "multiply": lambda a, b: a * b,
        "divide": lambda a, b: a / b,
        "dot": safe_dot,
        "cross": safe_cross
    }
    return operations[operation](val1, val2)

# --- Example Usage ---
if __name__ == "__main__":
    # We use "dot" here because it returns a scalar expression (like x + 2*y + 3*z)
    # which get_gradient can easily process.
    scalar_result = get_vector_operation("[x, y, z]", "[1, 2, 3]", "dot")
    print(get_gradient(str(scalar_result)))