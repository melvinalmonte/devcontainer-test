#!/usr/bin/env python3
"""
Enhanced Hello World app demonstrating devcontainer benefits.
This app showcases multiple dependencies and development tools.
"""

import click
import requests
from rich.console import Console
from rich.panel import Panel
from rich.text import Text


console = Console()


def get_random_fact() -> str:
    """Fetch a random fact from an API."""
    try:
        response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
        response.raise_for_status()
        return response.json()["text"]
    except requests.RequestException:
        return "Unable to fetch random fact (network error)"


@click.command()
@click.option("--name", default="World", help="Name to greet")
@click.option("--fact", is_flag=True, help="Include a random fact")
@click.option("--style", type=click.Choice(["simple", "fancy"]), default="fancy", help="Output style")
def hello(name: str, fact: bool, style: str) -> None:
    """Enhanced Hello World with multiple dependencies."""
    greeting = f"Hello, {name}!"
    
    if style == "simple":
        print(greeting)
        if fact:
            print(f"Fun fact: {get_random_fact()}")
    else:
        # Fancy output using rich
        text = Text(greeting, style="bold blue")
        panel = Panel(text, title="🐳 DevContainer Demo", border_style="green")
        console.print(panel)
        
        if fact:
            fact_text = get_random_fact()
            fact_panel = Panel(fact_text, title="🎲 Random Fact", border_style="yellow")
            console.print(fact_panel)


if __name__ == "__main__":
    hello()