import sympy as sp
from sympy.vector import CoordSys3D, Vector
from typing import Any, Union

def get_gradient(equation: Union[str, sp.Expr]) -> dict[str, Any]:
    """Takes a string equation, converts it to math, and returns the gradient."""
    x, y, z = sp.symbols("x y z")
    local_dict = {"e": sp.E, "exp": sp.exp, "x": x, "y": y, "z": z}

    # Safely handle both strings and existing SymPy objects
    if isinstance(equation, str):
        expr = sp.sympify(equation.strip("\"'"), locals=local_dict)
    else:
        expr = equation  

    # Calculate the gradient vector with SymPy
    gradient_vector = sp.derive_by_array(expr, (x, y, z))

    return {
        "equation": expr,
        "vector": gradient_vector,  
        "dx": gradient_vector[0],
        "dy": gradient_vector[1],
        "dz": gradient_vector[2],
    }

def get_lagrange(objective_function: Union[str, sp.Expr], constraint_function: Union[str, sp.Expr]) -> dict[str, Any]:
    """Calculates critical points and optimal values using Lagrange multipliers."""
    x, y, z, lembda = sp.symbols("x y z λ")

    obj_data = get_gradient(objective_function)
    const_data = get_gradient(constraint_function)

    objective_expr = obj_data["equation"]
    constraint_expr = const_data["equation"]

    diff_objective = obj_data["vector"]
    diff_constraint = const_data["vector"]

    lembda_eq = tuple(
        sp.Eq(diff_objective[i] - lembda * diff_constraint[i], 0)
        for i in range(3)
    )

    # Force dict=True so SymPy ALWAYS returns a predictable list of dictionaries
    solution = sp.solve(lembda_eq + (sp.Eq(constraint_expr, 0),), (x, y, z, lembda), dict=True)

    # Because dict=True is used, we can safely assume 'solution' is a list of dicts
    critical_points = [
        (sol.get(x, 0), sol.get(y, 0), sol.get(z, 0)) for sol in solution
    ]

    optimal_values = [
        objective_expr.subs({x: pt[0], y: pt[1], z: pt[2]}) for pt in critical_points
    ]

    # Return a single, well-structured dictionary
    return {
        "critical_points": critical_points, 
        "optimal_values": optimal_values,
        "details": {
            "diff_constraint_function": diff_constraint,
            "diff_objective_function": diff_objective,
            "lembda_eq": lembda_eq,
            "solution": solution,
        }
    }

def get_vector_operation(v1_str: Union[str, sp.Expr], v2_str: Union[str, sp.Expr], operation: str) -> dict[str, Any]:    
    """Parses string inputs, calculates the operation, and provides step-by-step logic."""
    x, y, z = sp.symbols('x y z')
    local_dict = {"x": x, "y": y, "z": z}

    N = CoordSys3D('N')
    unit_vectors = [N.i, N.j, N.k]
    
    def parse_input(val_str):
        parsed_val = sp.sympify(str(val_str).strip(), locals=local_dict)
        if isinstance(parsed_val, list) or isinstance(parsed_val, tuple):
            return sum((c * u for c, u in zip(parsed_val, unit_vectors)), Vector.zero)
        return parsed_val

    val1 = parse_input(v1_str)
    val2 = parse_input(v2_str)

    # Helper function to extract [x, y, z] components for the step-by-step breakdown
    def get_components(v):
        if isinstance(v, Vector):
            mat = v.to_matrix(N)
            return [mat[0], mat[1], mat[2]]
        return [v, v, v] # Fallback if a scalar is passed

    c1 = get_components(val1)
    c2 = get_components(val2)
    
    steps = {}

    def safe_dot(a, b):
        if isinstance(a, Vector) and isinstance(b, Vector):
            steps["formula"] = "(x₁ * x₂) + (y₁ * y₂) + (z₁ * z₂)"
            steps["substitution"] = f"({c1[0]} * {c2[0]}) + ({c1[1]} * {c2[1]}) + ({c1[2]} * {c2[2]})"
            return a.dot(b)
        raise ValueError("Mathematical Error: The dot product is only defined between two vectors.")

    def safe_cross(a, b):
        if isinstance(a, Vector) and isinstance(b, Vector):
            steps["formula"] = "⟨ (y₁z₂ - z₁y₂), (z₁x₂ - x₁z₂), (x₁y₂ - y₁x₂) ⟩"
            steps["substitution"] = f"⟨ ({c1[1]} * {c2[2]} - {c1[2]} * {c2[1]}), ({c1[2]} * {c2[0]} - {c1[0]} * {c2[2]}), ({c1[0]} * {c2[1]} - {c1[1]} * {c2[0]}) ⟩"
            return a.cross(b)
        raise ValueError("Mathematical Error: The cross product is only defined between two vectors.")

    # Standard operations
    def op_add(a, b):
        steps["formula"] = "⟨ x₁ + x₂, y₁ + y₂, z₁ + z₂ ⟩"
        steps["substitution"] = f"⟨ {c1[0]} + {c2[0]}, {c1[1]} + {c2[1]}, {c1[2]} + {c2[2]} ⟩"
        return a + b

    def op_sub(a, b):
        steps["formula"] = "⟨ x₁ - x₂, y₁ - y₂, z₁ - z₂ ⟩"
        steps["substitution"] = f"⟨ {c1[0]} - {c2[0]}, {c1[1]} - {c2[1]}, {c1[2]} - {c2[2]} ⟩"
        return a - b

    operations = {
        "add": op_add,
        "subtract": op_sub,
        "multiply": lambda a, b: a * b, # Keeping these simple as they usually involve scalars
        "divide": lambda a, b: a / b,
        "dot": safe_dot,
        "cross": safe_cross
    }
    
    if operation not in operations:
        raise ValueError(f"Unknown operation: '{operation}'")
        
    result = operations[operation](val1, val2)

    return {
        "result": result,
        "steps": steps
    }

# --- Example Usage ---
if __name__ == "__main__":
    scalar_result = get_vector_operation("[x, y, z]", "[1, 2, 3]", "dot")
    print(get_gradient(scalar_result))