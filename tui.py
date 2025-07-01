from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.rule import Rule
from rich.prompt import Prompt

# Initialize a single console object to use for all output
console = Console()


def display_greeting():
    """Displays the initial greeting and usage message."""
    console.print(
        Panel(
            '[bold green]AI Code Assistant[/bold green]\n\n[dim]Provide a prompt to begin. For example:\npython main.py "Refactor the calculator to handle parentheses."[/dim]',
            title="Welcome",
            border_style="dim",
        )
    )


def display_user_prompt(prompt: str):
    """Displays the initial user prompt in a styled panel."""
    console.print(
        Panel(prompt, title="User Prompt", border_style="blue", title_align="left")
    )


def display_plan(plan: str):
    """Displays the agent's plan in a styled panel."""
    console.print(
        Panel(plan, title="Agent's Plan", border_style="yellow", title_align="left")
    )


def display_reflection(reflection: str):
    """Displays the agent's reflection on an error."""
    console.print(
        Panel(
            reflection, title="Reflection", border_style="magenta", title_align="left"
        )
    )


def display_function_call(function_name: str, args: dict):
    """Displays a function call with syntax-highlighted arguments."""
    console.print(Rule(f"Calling Function: [bold cyan]{function_name}[/bold cyan]"))
    if args:
        console.print(
            Syntax(
                str(args),
                "json",
                theme="monokai",
                word_wrap=True,
                background_color="default",
            )
        )


def display_function_response(response: dict):
    """Displays a function's success or error response."""
    if "error" in response:
        error_message = response["error"]
        console.print(
            Panel(
                f"[bold red]Error:[/bold red] {error_message}",
                title="Function Error",
                border_style="red",
                title_align="left",
            )
        )
    else:
        result = str(response.get("result", "[dim]No output.[/dim]"))
        console.print(
            Panel(
                result,
                title="Function Result",
                border_style="green",
                title_align="left",
            )
        )
    console.print(Rule())


def display_final_answer(answer: str):
    """Displays the agent's final answer."""
    console.print(
        Panel(answer, title="Final Answer", border_style="green", title_align="left")
    )


def display_error(message: str):
    """Displays a generic error message."""
    console.print(f"[bold red]ERROR:[/bold red] {message}")


def get_confirmation(prompt: str) -> str:
    """Gets user confirmation."""
    return Prompt.ask(f"[bold]{prompt}[/bold]", choices=["y", "n", "r"], default="y")
