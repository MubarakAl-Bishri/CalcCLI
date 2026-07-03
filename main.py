import typer
from rich.console import Console
from rich.panel import Panel
from core.calculus import get_gradient

app = typer.Typer(help="Calculus 3 & Magnetism CLI Engine")
console = Console()

@app.command()
def gradient(equation: str):
    """
    Calculate the gradient vector of a 3D surface.
    Example: python main.py gradient "x**2 + y**2 - z"
    """
    console.print(f"[bold blue]Calculating gradient for:[/bold blue] {equation}")

    try:
        # Call our math engine
        results = get_gradient(equation)

        # Format the output nicely using Rich
        output = (
        f"[bold green]Original Equation:[/bold green] f(x,y,z) = {results['equation']}\n\n"
        f"[bold yellow]∂f/∂x:[/bold yellow] {results['dx']}\n"
        f"[bold yellow]∂f/∂y:[/bold yellow] {results['dy']}\n"
        f"[bold yellow]∂f/∂z:[/bold yellow] {results['dz']}"
        )

        console.print(Panel(output, title="Gradient Vector Results", expand=False))

    except Exception as e:
        console.print(f"[bold red]Error parsing math:[/bold red] Make sure to use Python syntax (e.g., 'x**2' not 'x^2').\nDetails: {e}")

@app.command()
def curl():
    """
    Calculate the curl of a vector field (Coming soon!)
    """
    console.print("[bold cyan]Curl feature is under construction![/bold cyan]")

if __name__ == "__main__":
    app()