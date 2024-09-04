import pytest
from bart.config import MarkupLanguages
from bart.exceptions import ProjectFileExistsException
from bart.templates import write_template, named_document_template


@pytest.mark.parametrize("markup,heading_mark", [
        (MarkupLanguages.ASCIIDOC, "= "),
        (MarkupLanguages.MARKDOWN, "# "),
        ("text", "")
    ])
def test_named_document_template(markup, heading_mark):
    """
    For each markup, it should prepend the title with the appropriate
    heading marker (or none)
    """
    assert named_document_template(markup, "My project") == f"{heading_mark}My project"


class TestWriteTemplate:
    """
    Tests the writing of various templates
    """

    def test_file_exists(self, tmp_path):
        """
        Don't overwrite a file that already exists (unlikely edge case, but)
        """
        test_doc = tmp_path / "test.adoc"
        test_doc.touch()
        with pytest.raises(ProjectFileExistsException):
            write_template(named_document_template,
                           test_doc,
                           markup="asciidoc",
                           document_name="Test")


    @pytest.mark.parametrize('level', range(6))
    def test_write_named_document_template(self, tmp_path, level):
        """
        We write a named_document_template
        """
        test_doc = tmp_path / "test.adoc"
        write_template(named_document_template,
                       test_doc,
                       markup=MarkupLanguages.ASCIIDOC,
                       document_name="Test",
                       heading_level=level)

        with test_doc.open('rt') as f:
            assert f.read() == f"""{'=' * level} Test"""
