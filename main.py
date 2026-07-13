import typer
from rich.console import Console
from rich.panel import Panel
from core.calculus import get_gradient, get_lagrange, get_vector_operation
from sympy import sstr
from enum import Enum

app = typer.Typer(help="Calculus 3 & Magnetism CLI Engine")
console = Console()


# Enum creates strict choices for the CLI argument, preventing typos!
class VectorOp(str, Enum):
    add = "add"
    subtract = "subtract"
    multiply = "multiply"
    divide = "divide"
    dot = "dot"
    cross = "cross"
    length = "length"
    angle = "angle"
    unit = "unit"  
    projection = "projection"  


@app.command()
def gradient(function: str, show_steps: bool = False):
    """
    Calculate the gradient vector of a 3D surface.
    Example: python3 main.py gradient "x**2 + y**2 - z"
    """
    try:
        results = get_gradient(function)

        if show_steps:
            steps_text = (
                f"[bold green]Original Equation:[/bold green] f(x,y,z) = {results['equation']}\n\n"
                f"[bold yellow]∂f/∂x:[/bold yellow] {results['dx']}\n"
                f"[bold yellow]∂f/∂y:[/bold yellow] {results['dy']}\n"
                f"[bold yellow]∂f/∂z:[/bold yellow] {results['dz']}\n\n"  # Added missing newlines here
                f"[bold green]Gradient ∇f:[/bold green] \\[ {results['dx']}, {results['dy']}, {results['dz']} ]"
            )
            console.print(
                Panel(steps_text, title="Gradient Vector Results", expand=False)
            )
        else:
            console.print(
                f"[bold green]Gradient ∇f:[/bold green] \\[ {results['dx']}, {results['dy']}, {results['dz']} ]"
            )
    except Exception as e:
        console.print(
            f"[bold red]Error parsing math:[/bold red] Make sure to use Python syntax (e.g., 'x**2' not 'x^2').\nDetails: {e}"
        )
        raise typer.Exit(code=1)


@app.command()
def lagrange(
    objective_function: str, constraint_function: str, show_steps: bool = False
):
    """
    Calculate the Lagrange multipliers for optimization problems
    Example: python3 main.py lagrange "x**2 + y**2 + z**2" "x + y + z - 1"
    """
    try:
        results = get_lagrange(objective_function, constraint_function)

        # Extract data using the refactored, single-dictionary structure
        critical_points = results["critical_points"]
        optimal_values = results["optimal_values"]
        details = results["details"]

        diff_obj = details["diff_objective_function"]
        diff_const = details["diff_constraint_function"]
        lembda_eq = details["lembda_eq"]

        if not critical_points:
            points_and_values = (
                "[italic]No real critical points found for this system.[/italic]"
            )
        else:
            points_and_values = "\n".join(
                f"Point {i}: (x: {pt[0]}, y: {pt[1]}, z: {pt[2]}) ➔ f(x,y,z) = {val}"
                for i, (pt, val) in enumerate(
                    zip(critical_points, optimal_values), start=1
                )
            )

        if show_steps:
            steps_text = (
                f"[bold green]Objective Function:[/bold green] f(x,y,z) = {objective_function}\n"
                f"[bold green]Constraint Function:[/bold green] g(x,y,z) = {constraint_function}\n\n"
                f"[bold cyan]1. Gradients:[/bold cyan]\n"
                f"∇f = ⟨ {diff_obj[0]}, {diff_obj[1]}, {diff_obj[2]} ⟩\n"
                f"∇g = ⟨ {diff_const[0]}, {diff_const[1]}, {diff_const[2]} ⟩\n\n"
                f"[bold cyan]2. System of Equations (∇f = λ∇g):[/bold cyan]\n"
                f"• {sstr(lembda_eq[0].lhs)} = {sstr(lembda_eq[0].rhs)}\n"
                f"• {sstr(lembda_eq[1].lhs)} = {sstr(lembda_eq[1].rhs)}\n"
                f"• {sstr(lembda_eq[2].lhs)} = {sstr(lembda_eq[2].rhs)}\n"
                f"• {constraint_function} = 0\n\n"
                f"[bold cyan]3. Solutions (Critical Points & Optimal Values):[/bold cyan]\n"
                f"{points_and_values}"
            )
            console.print(
                Panel(
                    steps_text,
                    title="Lagrange Multipliers (Step-by-Step)",
                    expand=False,
                )
            )

        else:
            summary_text = (
                f"[bold green]Objective:[/bold green] {objective_function} | "
                f"[bold green]Constraint:[/bold green] {constraint_function}\n"
                f"[bold yellow]Results:[/bold yellow]\n{points_and_values}"
            )
            console.print(
                Panel(
                    summary_text,
                    title="Lagrange Multipliers (Final Answer)",
                    expand=False,
                )
            )
    except Exception as e:
        console.print(
            f"[bold red]Error parsing math:[/bold red] Make sure to use Python syntax (e.g., 'x**2' not 'x^2').\nDetails: {e}"
        )
        raise typer.Exit(code=1)


@app.command()
def vector_operation(
    v1: str,
    operation: VectorOp,
    v2: str = typer.Argument(
        default="",
        help="Second vector (leave empty for single-vector operations like length)",
    ),
    show_steps: bool = False,
):
    """
    Perform vector operations (dot, cross, add, subtract, length, angle) on two 3D vectors.
    Example: python3 main.py vector-operation "[x, y, z]" dot "[1, 2, 3]"  --show-steps
    """
    try:
        data = get_vector_operation(v1, v2, operation.value)
        result = data["result"]
        steps = data["steps"]
        numerical_value = data["numerical_value"]

        if show_steps and steps:
            # 1. Determine the numerical value line first without breaking f-string rules
            if isinstance(numerical_value, (int, float, complex)):
                num_val_text = f"[bold blue]4. Numerical Value:[/bold blue]\n{numerical_value}"
            else:
                num_val_text = "[bold red]4. No Numerical Value Available[/bold red]\n"
                
            if operation.value == "angle" and isinstance(numerical_value, (int, float)):
                num_val_text += "\n\n[italic]Note: Angle is in radians. Convert to degrees if needed.[/italic]"
            
            # 2. Safely evaluate the unit suffix to avoid quote collisions inside the f-string
            unit_suffix = " rad" if operation.value == "angle" else ""

            # 3. Safely inject everything into the main multi-line string
            steps_text = (
                f"[bold cyan]1. General Formula ({operation.value}):[/bold cyan]\n"
                f"{steps.get('formula', 'N/A')}\n\n"
                f"[bold cyan]2. Component Substitution:[/bold cyan]\n"
                f"{steps.get('substitution', 'N/A')}\n\n"
                f"[bold green]3. Final Result:[/bold green]\n"
                f"{result}{unit_suffix}\n\n"
                f"{num_val_text}"
            )

            console.print(
                Panel(
                    steps_text,
                    title="Vector Operation (Step-by-Step)",
                    expand=False,
                )
            )
        else:

            console.print(
                Panel(
                    f"[bold green]Result of {operation.value}:[/bold green] {numerical_value}",
                    title="Vector Operation Result",
                    expand=False,
                )
            )
    except Exception as e:
        console.print(
            Panel(
                f"[bold red]Error performing vector operation:[/bold red] {e}",
                title="Error",
                expand=False,
            )
        )
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
