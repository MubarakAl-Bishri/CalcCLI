import typer
from rich.console import Console
from rich.panel import Panel
from core.calculus import get_gradient, get_lagrange, get_vector_operation
from sympy import sstr

app = typer.Typer(help="Calculus 3 & Magnetism CLI Engine")
console = Console()


@app.command()
def gradient(function: str, showSteps: bool = False):
    """
    Calculate the gradient vector of a 3D surface.
    Example: python3 main.py gradient "x**2 + y**2 - z"
    """
    # console.print(f"[bold blue]Calculating gradient for:[/bold blue] {function}")

    try:
        # Call our math engine
        results = get_gradient(function)

        if showSteps:
            # Format the output nicely using Rich
            steps_text = (
                f"[bold green]Original Equation:[/bold green] f(x,y,z) = {results['equation']}\n\n"
                f"[bold yellow]∂f/∂x:[/bold yellow] {results['dx']}\n"
                f"[bold yellow]∂f/∂y:[/bold yellow] {results['dy']}\n"
                f"[bold yellow]∂f/∂z:[/bold yellow] {results['dz']}"
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


@app.command()
def lagrange(
    objective_function: str, constraint_function: str, showSteps: bool = False
):
    """
    Calculate the Lagrange multipliers for optimization problems
    Example: python3 main.py lagrange "x**2 + y**2 + z**2" "x + y + z - 1"
    """

    # console.print("[bold cyan]Lagrange feature is under construction![/bold cyan]")
    try:
        results = get_lagrange(objective_function, constraint_function)

        # Extract data from the new return structure
        critical_points = results[0]["criticalPoints"]
        optimal_values = results[0]["optimalValues"]
        diff_obj = results[1]["diffObjectiveFunction"]
        diff_const = results[1]["diffConstraintFunction"]
        lembda_eq = results[1]["lembdaEq"]

        # Pair up the critical points with their resulting optimal values for a clean display
        points_and_values = "\n".join(
            f"Point {i}: (x: {pt[0]}, y: {pt[1]}, z: {pt[2]}) ➔ f(x,y,z) = {val}"
            for i, (pt, val) in enumerate(zip(critical_points, optimal_values), start=1)
        )

        if showSteps:
            # Build the detailed step-by-step breakdown
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
            # Build the concise, final-answer summary
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


@app.command()
def vector_operation(v1: str, v2: str, operation: str):
    """
    Perform vector operations (dot, cross, add, subtract) on two 3D vectors.
    Example: python3 main.py vector-operation "x**2 + y**2 + z**2" "x + y + z" "dot"
    """
    try:
        result = get_vector_operation(v1, v2, operation)
        console.print(
            Panel(
                f"[bold green]Result of {operation} operation:[/bold green] {result}",
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

if __name__ == "__main__":
    app()
