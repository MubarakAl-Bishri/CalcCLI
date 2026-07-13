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


def get_vector_operation(input_str_1: Union[str, sp.Expr], input_str_2: Union[str, sp.Expr], operation_type: str) -> dict[str, Any]:    
    """Parses string inputs, calculates the operation, and provides step-by-step logic."""
    x, y, z,theta = sp.symbols('x y z θ')
    symbol_dict = {"x": x, "y": y, "z": z, "theta": theta, "e": sp.E, "exp": sp.exp, "sin": sp.sin, "cos": sp.cos}

    # 'coord_sys' is much clearer than the arbitrary 'N'
    coord_sys = CoordSys3D('coord_sys')
    base_vectors = [coord_sys.i, coord_sys.j, coord_sys.k]
    
    def parse_expression(input_string):
        if not input_string:  # Safely catch the empty string from Typer
            return None
            
        parsed_expression = sp.sympify(str(input_string).strip(), locals=symbol_dict)
        if isinstance(parsed_expression, (list, tuple)):
            return sum((coeff * unit_vec for coeff, unit_vec in zip(parsed_expression, base_vectors)), Vector.zero)
        return parsed_expression

    operand_1 = parse_expression(input_str_1)
    operand_2 = parse_expression(input_str_2)

    # Helper function to extract [x, y, z] components for the step-by-step breakdown
    def extract_components(value):
        if value is None:
            return [None, None, None] # Prevents crashing if v2 is empty
        if isinstance(value, Vector):
            matrix_representation = value.to_matrix(coord_sys)
            return [matrix_representation[0], matrix_representation[1], matrix_representation[2]]
        return [value, value, value]

    components_1 = extract_components(operand_1)
    components_2 = extract_components(operand_2)
    
    solution_steps = {}

    def calculate_dot(vec_a, vec_b):
        if isinstance(vec_a, Vector) and isinstance(vec_b, Vector):
            solution_steps["formula"] = "(x₁ * x₂) + (y₁ * y₂) + (z₁ * z₂)"
            solution_steps["substitution"] = f"({components_1[0]} * {components_2[0]}) + ({components_1[1]} * {components_2[1]}) + ({components_1[2]} * {components_2[2]})"
            return vec_a.dot(vec_b)
        raise ValueError("Mathematical Error: The dot product is only defined between two vectors.")

    def calculate_cross(vec_a, vec_b):
        if isinstance(vec_a, Vector) and isinstance(vec_b, Vector):
            solution_steps["formula"] = "⟨ (y₁z₂ - z₁y₂), (z₁x₂ - x₁z₂), (x₁y₂ - y₁x₂) ⟩"
            solution_steps["substitution"] = f"⟨ ({components_1[1]} * {components_2[2]} - {components_1[2]} * {components_2[1]}), ({components_1[2]} * {components_2[0]} - {components_1[0]} * {components_2[2]}), ({components_1[0]} * {components_2[1]} - {components_1[1]} * {components_2[0]}) ⟩"
            return vec_a.cross(vec_b)
        raise ValueError("Mathematical Error: The cross product is only defined between two vectors.")

    # Standard operations
    def calculate_addition(val_a, val_b):
        solution_steps["formula"] = "⟨ x₁ + x₂, y₁ + y₂, z₁ + z₂ ⟩"
        solution_steps["substitution"] = f"⟨ {components_1[0]} + {components_2[0]}, {components_1[1]} + {components_2[1]}, {components_1[2]} + {components_2[2]} ⟩"
        return val_a + val_b

    def calculate_subtraction(val_a, val_b):
        solution_steps["formula"] = "⟨ x₁ - x₂, y₁ - y₂, z₁ - z₂ ⟩"
        solution_steps["substitution"] = f"⟨ {components_1[0]} - {components_2[0]}, {components_1[1]} - {components_2[1]}, {components_1[2]} - {components_2[2]} ⟩"
        return val_a - val_b
    
    def calculate_length(vec_a, vec_b=None): # vec_b safely absorbs the None
        if isinstance(vec_a, Vector):
            solution_steps["formula"] = "√(x² + y² + z²)"
            # Sympy objects format cleanly inside f-strings
            solution_steps["substitution"] = f"√(({components_1[0]})² + ({components_1[1]})² + ({components_1[2]})²)"
            return vec_a.magnitude()
        raise ValueError("Mathematical Error: Length is only defined for a vector.")
    
    def calculate_angle(vec_a, vec_b):
        if isinstance(vec_a, Vector) and isinstance(vec_b, Vector):
            dot_product = vec_a.dot(vec_b)
            magnitude_product = vec_a.magnitude() * vec_b.magnitude()
            solution_steps["formula"] = "cos(θ) = (A · B) / (|A| * |B|)"
            solution_steps["substitution"] = f"cos(θ) = ({dot_product}) / ({vec_a.magnitude()} * {vec_b.magnitude()})"
            return sp.acos(dot_product / magnitude_product)
        raise ValueError("Mathematical Error: Angle is only defined between two vectors.")

    def calculate_unit(vec_a, vec_b=None):
        if isinstance(vec_a, Vector):
            meg_a = vec_a.magnitude()
            if meg_a == 0:
                raise ValueError("Mathematical Error: Unit vector is only defined for a non-zero vector.")
            unit_vector = vec_a / meg_a
            solution_steps["formula"] = "Unit Vector = A / |A|"
            solution_steps["substitution"] = f"Unit Vector = {vec_a} / {vec_a.magnitude()}"
            return unit_vector
        raise ValueError("Mathematical Error: Unit vector is only defined for a vector.")
            

    def calculate_projection(vec_a, vec_b):
        if isinstance(vec_a, Vector) and isinstance(vec_b, Vector):
            mag_b = vec_b.magnitude()
            if mag_b == 0:
                raise ValueError("Mathematical Error: Cannot project onto a zero vector.")
            projection = (vec_a.dot(vec_b) / mag_b**2) * vec_b
            solution_steps["formula"] = "Projection of A onto B = ((A · B) / |B|²) * B"
            solution_steps["substitution"] = f"Projection = (({components_1[0]} * {components_2[0]} + {components_1[1]} * {components_2[1]} + {components_1[2]} * {components_2[2]}) / ({vec_b.magnitude()}²)) * {vec_b}"
            return projection
        raise ValueError("Mathematical Error: Projection is only defined between two vectors.")

    supported_operations = {
        "add": calculate_addition,
        "subtract": calculate_subtraction,
        "multiply": lambda val_a, val_b: val_a * val_b, 
        "divide": lambda val_a, val_b: val_a / val_b,
        "dot": calculate_dot,
        "cross": calculate_cross,
        "length": calculate_length,
        "angle": calculate_angle,  # Assuming you have a function for angle calculation
        "unit": calculate_unit,
        "projection": calculate_projection,  # Assuming you have a function for projection
    }
    
    if operation_type not in supported_operations:
        raise ValueError(f"Unknown operation: '{operation_type}'")
        
    calculation_result = supported_operations[operation_type](operand_1, operand_2)

    try:
        # Attempt to simplify the result for cleaner output
        numerical_value = sp.N(calculation_result)
    except Exception:
        numerical_value = calculation_result  # Fallback to the original result if simplification fails

    return {
        "result": calculation_result,
        "steps": solution_steps,
    "numerical_value": (float(numerical_value) if numerical_value.is_real else complex(numerical_value)) if isinstance(numerical_value, sp.core.numbers.Number) else numerical_value
    }
# --- Example Usage ---
if __name__ == "__main__":
    scalar_result = get_vector_operation("[4, 5, 6]", "[1, 2, 3]", "angle")
    print(type(scalar_result["numerical_value"]))