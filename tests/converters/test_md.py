from bart.converters.md import md_to_html


class TestMarkdownConversion:
    """
    Tests around markdown conversion
    """
    def test_basic(self):
        """
        We can convert a string
        """
        result = md_to_html("This is a _test_.")
        assert result
        assert result == "<p>This is a <em>test</em>.</p>\n"

    def test_quotes(self):
        """
        Smartypants is on
        """
        result = md_to_html('This is a "test".')
        assert result == "<p>This is a &#8220;test&#8221;.</p>\n"
