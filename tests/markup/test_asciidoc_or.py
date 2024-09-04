from bart.markup.asciidoc_or import read_attributes


class TestReadAttrs:
    """
    Tests for reading attributes from asciidoc files
    """

    def test_read_single_attr(self, test_adoc):
        """
        Test can we read an attribute
        """
        test_adoc.write_text("""= Title
:attr: some text
""")
        attrs = read_attributes(test_adoc)
        assert attrs["attr"] == "some text"

    def test_read_multiple_attrs(self, test_adoc):
        """
        Test we can read multiple attributes
        """
        test_adoc.write_text("""= Title
:attr: some text
:attr2: some other text
:description: some third text
""")
        attrs = read_attributes(test_adoc)
        assert len(attrs.keys()) == 3
        assert attrs["attr"] == "some text"
        assert attrs["attr2"] == "some other text"
        assert attrs["description"] == "some third text"

    def test_read_multiline_attrs(self, test_adoc):
        """
        Test we can read in multiline attributes
        """
        test_adoc.write_text(r"""= Title
:description: some text that goes on longer than \
it really is meant to \
and ongoing
""")
        attrs = read_attributes(test_adoc)
        assert attrs["description"] == ("some text that goes on " +
                                        "longer than it really is meant to " +
                                        "and ongoing") 

    def test_read_multiline_with_other_after(self, test_adoc):
        """
        Test we can still read regular attrs before and after multiline ones
        """
        test_adoc.write_text(r"""= Title
:before: something
:description: some text that goes on longer than \
it really is meant to \
and ongoing
:after: something else
""")
        attrs = read_attributes(test_adoc)
        assert attrs["before"] == "something"
        assert attrs["description"] == ("some text that goes on " +
                                        "longer than it really is meant to " +
                                        "and ongoing") 
        assert attrs["after"] == "something else"

    def test_breaks_after_newline(self, test_adoc):
        """
        According to the asciidoctor spec, document attributes can only be set
        until there is a new line (assuming that after this it's just the text);
        we want to follow this also
        """
        test_adoc.write_text(r"""= Title
:attr: test

some other text...before a secret attr that we should ignore

:attr-2: test
""")
        attrs = read_attributes(test_adoc)
        assert len(attrs) == 1
