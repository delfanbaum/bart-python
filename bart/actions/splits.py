from bart.exceptions import MarkupNotAllowedException
from bart.config import MarkupLanguages
from bart.utilites import get_valid_pathname
from pathlib import Path


"""
This all needs to be reworked given the project paradigm!
"""


def get_delimiter(file: Path):
    """
    TODO: allow users to config their own delimiters per filetype
    """
    match file.suffix[1:]:  # remove the dot
        case MarkupLanguages.MARKDOWN.value:
            return "#"
        case MarkupLanguages.ASCIIDOC.value:
            return "="
        case _:
            raise MarkupNotAllowedException(
                    "This operation is not available for this type of markup.")


def write_split(split_lines: list,
                delimeter: str,
                numbering: int,
                suffix: str) -> int:
    section_title = split_lines[0].split(delimeter)[-1]
    text = "".join(split_lines)
    out_fn = str(numbering) + "-" + get_valid_pathname(section_title) + suffix

    with open(out_fn, 'wt') as f:
        print(f"Writing {out_fn}...")
        f.write(text)

    return numbering + 1


def split_at_headings(fn):
    file = Path(fn)
    delimeter = get_delimiter(file)
    numbering = None  # todo
    current_split = []

    with file.open('rt') as f:
        text_lines = f.readlines()

    for num, line in enumerate(text_lines):
        # next heading
        if line.find(delimeter) == 0 and text_lines[num+1] == "\n":
            if current_split:
                numbering = write_split(current_split,
                                        delimeter,
                                        numbering,
                                        file.suffix)

            current_split = [line]
        else:
            current_split.append(line)

    # write final split
    write_split(current_split, delimeter, numbering, file.suffix)
