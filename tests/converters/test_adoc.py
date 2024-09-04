from bart.converters.adoc import (
    process_with_asciidoctor,
    process_with_python_asciidoc
    )


def test_process_asciidoctor():
    result = process_with_asciidoctor('This is a _test_')
    assert result
    assert "<p>This is a <em>test</em></p>" in result

def test_process_asciidoc():
    result = process_with_python_asciidoc('This is a _test_')
    assert result
    assert "<p>This is a <em>test</em></p>" in result
