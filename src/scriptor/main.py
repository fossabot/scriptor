import json
import typer
import os
import scriptor.project as project
from rich import print
from rich.panel import Panel
from typing_extensions import Annotated
from scriptor import __VERSION__, logger

app = typer.Typer(no_args_is_help=True)
app.add_typer(
    project.app,
    name="project",
    help="Subset of Scriptor commands related to project management.",
)


@app.callback()
def callback(
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose", "-v", help="Enables verbose logging for debugging purposes."
        ),
    ] = False,
):
    """
    Scriptor is a open-source CLI tool designed for simple management of your local and cloud environments tailored to your home-labs or business environments
    """
    if verbose:
        # Until a better solution is found, we reconfigure the logger to show debug messages
        import sys

        logger.remove()
        logger.add(sys.stderr, level="DEBUG")
        logger.debug("Verbose logging enabled.")
        logger.add("scriptor.log", rotation="50 MB", level="DEBUG")
    logger.debug(f"Command invoked running {__VERSION__} version of Scriptor.")


@app.command(name="version")
def version():
    """
    Showcases information about scriptor including API and package versions.
    """
    print(Panel.fit(f"Installed Scriptor Version: [red]{__VERSION__}"))


@app.command(name="init")
def initialize(
    override: Annotated[
        bool,
        typer.Option(
            "--override", help="Override existing configuration file if it exists"
        ),
    ] = False,
):
    """
    Initializes a Scriptor project by setting up necessary configurations and directories.
    """
    jsonContent = {
        "name": "example-scriptor-project",
        "version": "0.1.0",
        "developer": "Example Developer",
        "description": "An example Scriptor project initialized using the CLI.",
        "endpoint": "main.py",
        "SCRIPTOR_API_VERSION": "v0",
    }
    logger.debug(
        f"Prepped API version {jsonContent['SCRIPTOR_API_VERSION']} for project initialization."
    )

    if os.path.exists("scriptor.json") and not override:
        logger.warning("Configuration already exists and --override not specified.")
        print(
            "Configuration file already exists, please add --override to recreate the file."
        )
        return
    with open("scriptor.json", "w") as file:
        logger.info("Creating scriptor.json configuration file.")
        file.write(json.dumps(jsonContent, indent=4))

    print(
        "Scriptor compatible project created.\n"
        "Note that Scriptor is still [yellow]under development[/yellow], some features may not work as expected and major changes are expected."
    )
    return


if __name__ == "__main__":
    app()
