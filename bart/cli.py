from pathlib import Path
from bart.config import BartConfig
from bart.exceptions import ProjectDirExistsException, ProjectFileExistsException
from bart.markup.asciidoc_or import read_attributes
from bart.project import BartProject
import typer

from bart.utilites import get_valid_pathname


app = typer.Typer()


@app.command()
def begin(
    project_name: str,
):
    """
    Begin a new project in a <project-name> directory with a
    "00-<project-name>" file in the language specified in your application
    config file (if no config file is found, defaults to a ".txt" extension).

    Note that if you'd like to use spaces in your project name, you need to
    enclose them in quotes, e.g., `bart begin "my great project"`.
    """
    project_dir = Path.cwd() / get_valid_pathname(project_name)

    try:
        BartProject(project_dir, new=True, project_name=project_name)
        print(f"New project created at {project_dir.stem}")

    except ProjectDirExistsException:
        print("Ugh oh! There's already something at {project_dir.stem}!")
        typer.Exit(code=1)


@app.command()
def add(document_name: str,
        document_level: int = 1):
    """
    Adds a file with the specified document name to the end of the project.
    """
    project = BartProject()

    try:
        project.add_document(document_name, document_level)

    except ProjectFileExistsException:
        # this really shouldn't happen, but theoretically possible
        print("Ugh oh! A file already exists with that name. " +
              "How'd you manage that?!") 


@app.command()
def show_descriptions():
    """
    Lists the file with its description attribute per file in the project
    """
    project = BartProject(Path.cwd())
    for file in project.documents:
        description = read_attributes(file).get('description', None)
        print(f"{file.relative_to(project.project_dir)}:\n    {description}\n")


@app.command()
def config():
    """
    List the Bart config options for the current project/directory (or global
    options, if run outside of a project).
    """
    config = BartConfig()

    print("\nBart configuration:")
    for k, v in vars(config).items():
        print(f"  {k}: {v}")

@app.command()
def seed_config():
    """ placeholder for me for testing """
    config = BartConfig()
    config.write_to(Path.cwd() / "bart.toml")

