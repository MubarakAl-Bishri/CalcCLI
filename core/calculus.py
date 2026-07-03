import sympy as sp

def get_gradient(equation_str: str):
    """Takes a string equation, converts it to math, and returns the gradient."""
    # Define our standard symbols
    x, y, z = sp.symbols('x y z')


    local_dict = {'e': sp.E, 'exp': sp.exp, 'x': x, 'y': y, 'z': z}
    # Safely convert the user's string into a SymPy expression
    # e.g., "x**2 + y**2" becomes mathematical x^2 + y^2
    expr = sp.sympify(equation_str, locals=local_dict)

    # Calculate partial derivatives
    df_dx = sp.diff(expr, x)
    df_dy = sp.diff(expr, y)
    df_dz = sp.diff(expr, z)

    # Return a dictionary with the results
    return {
    "equation": expr,
    "dx": df_dx,
    "dy": df_dy,
    "dz": df_dz
    }

if __name__ == "__main__":
    # Example usage
    equation = input("Enter a mathematical equation in terms of x, y, z (e.g., 'x**2 + y**2 + z**2'): ")
    print(get_gradient(equation))
    