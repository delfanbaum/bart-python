import subprocess
import sys
from typing import Literal

from bart.config import DocConverers


def process_with_asciidoctor(text) -> str:
    """
    Converts asciidoc to html via asciidoctor (ruby)
    """
    result = subprocess.run(['asciidoctor', '-a', "stylesheet!",
                             "-o", "-", "-"],
                            input=text,
                            capture_output=True,
                            text=True)

    if result.stderr == '':
        return result.stdout

    else:
        sys.exit(f'\nError in Asciidoctor conversion: {result.stderr}')


def process_with_python_asciidoc(text) -> str:
    result = subprocess.run(['asciidoc', '-b', 'html5', '-a', 'linkcss',
                             '-a', 'disable-javascript', "-o", "-", "-"],
                            input=text,
                            capture_output=True,
                            text=True)
    if result.returncode == 0:
        html = result.stdout
        # remove linked stylesheet....
        html = html.replace(
            '<link rel="stylesheet" href="./asciidoc.css" type="text/css">', ''
            )
        return html

    else:
        sys.exit(f'Error code {result.returncode}: {result.stderr}')


def adoc_to_html(text, converter: Literal[DocConverers.ASCIIDOC,
                                          DocConverers.ASCIIDOCTOR]) -> str:
    """
    Takes an adoc file and converts it; this function is more a helper/makes all
    the converter code look similar
    """
    match converter:
        case DocConverers.ASCIIDOC:
            return process_with_python_asciidoc(text)
        case DocConverers.ASCIIDOCTOR:
            return process_with_asciidoctor(text)
