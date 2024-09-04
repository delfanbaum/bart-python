from bart.config import DocConverers
from bart.converters.adoc import adoc_to_html 
from bart.converters.md import md_to_html
from bart.exceptions import DocConverterException


def text_to_html(text: str, converter: DocConverers) -> str:
    """
    Takes a markup text str and converts it into HTML
    """
    match converter:
        case DocConverers.ASCIIDOC | DocConverers.ASCIIDOCTOR:
            return adoc_to_html(text, converter)
        case DocConverers.MARKDOWN2:
            return md_to_html(text)
        case _:
            raise DocConverterException

