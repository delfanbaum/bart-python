from bart.exceptions import DocumentLevelException
import pytest
from pathlib import Path

from bart.utilites import (
    get_doc_number,
    get_doc_position,
    get_valid_pathname,
)


def test_get_valid_pathname():
    """
    Ensures that various undesirable characters are flattened to mere dashes
    and are lowercase
    """
    test_name = "ThIs! Title, an example. Or: (also) \\test/case"

    assert get_valid_pathname(test_name) == \
        "this-title-an-example-or-also-test-case"


class TestGetNextDocNumber:
    """
    Tests around the "next doc" getter
    """

    def test_get_doc_number_no_last(self):
        """
        If there is no last doc (i.e., it's a new project), it should be padded
        per level
        """
        # special "1  case
        level_1 = get_doc_number(1)
        assert level_1 == "00"

        # expected subsequent cases
        level_2 = get_doc_number(2)
        assert level_2 == "00"

        level_3 = get_doc_number(3)
        assert level_3 == "000"

    @pytest.mark.parametrize("case,expected",[
           (1, "02"),
           (2, "21"),
           (3, "211"),
        ])
    def test_get_doc_number_levels(self, case, expected):
        """
        If we're adding a doc without a level specified, it should add at the
        "lowest" level with the correct zfill padding
        """
        last_doc = Path(f'{("1" * case).zfill(2)}-example.adoc') 
        numbering = get_doc_number(case, last_doc)
        assert numbering == expected

    @pytest.mark.parametrize("last_number,add_level,expected",[
           ("1000", 4, "1001"), ("1001", 4, "1002"), ("1010", 4, "1011"),
           ("1000", 3, "1010"), ("1001", 3, "1011"), ("1010", 3, "1020"),
           ("1000", 2, "1100"), ("1001", 2, "1101"), ("1010", 2, "1110"),
           ("1000", 1, "2000"), ("1001", 1, "2001"), ("1010", 1, "2010"),
        ])
    def test_get_doc_position_levels(self, last_number, add_level, expected):
        """
        Tests various add_position levels for a high-doc_levels project
        (the assumption being that lower cases will also work)
        """
        last_doc = Path(f'{last_number}-example.adoc') 
        numbering = get_doc_number(4, last_doc, add_level)
        assert numbering == expected

class TestGetDocLevel:
    """
    Tests getting the "level" of a document, descending from the project levels
    e.g., if it's a doc_levels = 3 project, "100" would be "level = 1",
    "010" would be "level = 2", and "001" would be "level = 3"
    """

    def test_get_doc_project_level_1(self):
        """
        If the project level is 1, everything is level 1
        """
        for i in range(0,100):
            doc = Path(f"{str(i).zfill(2)}-example.adoc")
            assert get_doc_position(1, doc) == 1

    @pytest.mark.parametrize("level,number,expected", [
        (2, "11", 2), (2, "10", 1),
        (3, "111", 3), (3, "110", 2), (3, "100", 1), 
        (4, "1111", 4), (4, "1110", 3), (4, "1100", 2), (4, "1000", 1), 
        ])
    def test_get_doc_project_other_levels(self, level, number, expected):
        """
        For a given project level and numbering, do we get the expected result
        (defined in the parametrization)
        """
        doc = Path(f"{number}-example.md")
        assert get_doc_position(level, doc) == expected

    def test_exception(self, tmp_path):
        """
        Test we get our exception
        """
        bad_path = tmp_path / "00000-something.adoc"
        with pytest.raises(DocumentLevelException):
            _ = get_doc_position(2, bad_path)
