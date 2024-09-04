import pytest

from bart.config import DocConverers
from bart.converters.api import text_to_html
from bart.exceptions import DocConverterException


class TestTextToHTML:
    """
    Tests for the text_to_html function
    """

    @pytest.mark.parametrize("converter",[
            DocConverers.ASCIIDOC,
            DocConverers.ASCIIDOCTOR,
            DocConverers.MARKDOWN2,
        ])
    def test_returns_per_converter(self, converter):
        """
        Assert that the converter selects a function and returns HTML
        """
        result = text_to_html("This is a test", converter)
        assert result
        assert "<p>" in result

    def test_exception_bad_converter(self):
        """
        If a converter isn't given or isn't one we know about, raise an
        exception
        """
        with pytest.raises(DocConverterException):
            _ = text_to_html("Something", None)  # type: ignore


