from pathlib import Path
import subprocess
import sys
from typing import Optional

from bart.config import BART_TEMPLATES_DIR, BuildFormats

from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration


def html_to_pdf_weasyprint(html: str, target_path: Path, css_path: Path):
    """
    Does what it says on the tin
    """
    try:
        font_config = FontConfiguration()
        HTML(string=html).write_pdf(
            target=target_path,
            stylesheets=[CSS(filename=css_path)],
            font_config=font_config)
        # return the target path if success
        return target_path
    except AttributeError as ae:
        print(ae)
    except Exception as unk_e:
        print(f"There was an error building the PDF.\n{Exception}\n{unk_e}")


def html_to_pdf_pagedjs(html: str):
    """
    Does what it says on the tin
    """
    pass

"""
Subprocess we're borrowing: 

pandoc _builds/src/buildfile.html --from html --to docx --data-dir=library/templates --output _builds/$INPUT_NAME.docx
"""

def html_to_pandoc_target(html: str,
                          target: BuildFormats,
                          target_path: Path,
                          data_dir: Optional[Path] = BART_TEMPLATES_DIR):
    """
    Takes an html string and converts it into the desired target format with a
    pandoc subprocess call
    """

    result = subprocess.run(["pandoc",
                            "--from",
                            "html",
                            "--to",
                            target.name.lower(),  # doc or docx
                            f"--data-dir={str(data_dir)}",
                            "--output",
                            f"{str(target_path)}"
                            ],
                            input=html,
                            capture_output=True,
                            text=True
                            )
    if result.stderr == '':
        print(f"Success! Document created at {str(target_path)}")
    else:
        sys.exit(f"""Ugh oh! Something went wrong:

Error code {result.returncode}: {result.stderr}')
""")

def html_to_docx(html: str):
    """
    Test
    """
    # html2docx() returns an io.BytesIO() object. The HTML must be valid.
    buf = html2docx(html, title="My Document")

    with open("my.docx", "wb") as fp:
        fp.write(buf.getvalue())
