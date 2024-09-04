from pathlib import Path
import re
from typing import Tuple


def read_attributes(fn: Path) -> dict:
    """
    Because asciidoc.py doesn't give us a real API to pull attributes from, and
    I don't want to write this app in Ruby just to get hold of the Asciidoctor
    API, we'll home-roll an attribute reader for asciidoc files  
    """

    attributes = {}
    attr = ''
    continuation = False
    
    with fn.open() as f:
        lines = f.readlines()

    for line in lines:
        if line == "\n":  # end of document header
            break

        attr_match = re.match(r'\:(.*?)\: (.*)', line)
        
        if attr_match:
            attr = attr_match.group(1)
            # check if it continues onto the subsequent line
            text, continuation = _check_continue(attr_match.group(2))
            attributes[attr] = text

        elif attr and continuation:
            text, continuation = _check_continue(line)
            attributes[attr] = attributes[attr] + text

    return attributes

def _check_continue(line: str) -> Tuple[str, bool]:
    """
    DRY up checking for continuation marker at the end of a line

    If the final non-whitespace character is a trailing \\, then it's a
    continuation line and we should return it and that it is a continuation
    line, otherwise just strip (clean) and return the line, that it is _not_ a
    continuation line
    """
    if line.strip()[-1] == '\\':
        # remove the continuation character
        return line.strip()[:-1], True
    else:
        return line.strip(), False
