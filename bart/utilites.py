import io
import re
from pathlib import Path
from typing import Optional, Union
from bart.config import DocConverers
from bart.exceptions import DocumentLevelException, DocConverterException


def get_valid_pathname(name) -> str:
    """
    Returns a valid pathname of lowercase letters and dashes
    """
    s = re.sub(r'[^a-zA-Z\d]', '-', name)
    s = re.sub(r'-+', '-', s)
    return s.lower().strip()


def get_doc_number(project_levels: int,
                   last_doc: Optional[Path] = None,
                   add_level: int = 1) -> str:
    """
    Given a document path and the section document numbering; returns the "next"
    number if given a "last doc"

    The "add_level" int is whatever "project level" you're adding. Top-levels
    would be "level 1", second levels down an outline "level 2", etc.
    """
    if not last_doc:
        next_number = "0" * project_levels

    elif 0 < add_level <= project_levels:
        next_number = str(int(last_doc.name.split('-')[0]) +
                          (10 ** (project_levels - add_level)))
    else:
        raise DocumentLevelException
    
    if project_levels == 1:  # special case for 01, 02, etc.
        return next_number.zfill(2)
    else:
        return next_number.zfill(project_levels)


def get_doc_position(project_levels, doc: Path) -> int:
    """
    Gets the "position" of the document, i.e., is it a main doc? Is it a
    sub-doc? Etc. 
    e.g., if it's a doc_levels = 3 project, "100" would be "level = 1",
    "010" would be "level = 2", and "001" would be "level = 3"
    """
    doc_numbering = doc.name.split('-')[0]

    if (project_levels == 1):
        return 1

    for index, char in enumerate(doc_numbering[::-1]):
        if char == "0":
            pass
        else:
            return project_levels - index
    # if we can't find anything at all, no numbering, etc.
    raise DocumentLevelException
