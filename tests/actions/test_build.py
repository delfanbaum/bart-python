from bart.config import DocConverers
from bart.converters.api import text_to_html
from bart.project import BartProject
from bart.actions.build import html_to_pdf_weasyprint


class TestPdfWeasyprint:
    """
    Tests around weasyprint
    """
    def test_smoketest(self, test_project_adoc: BartProject, tmp_path):
        """
        Stuff
        """
        out = tmp_path / "test.pdf"
        css = tmp_path / "test.css"
        with css.open('wt') as f:
            f.write("body {color:blue}")
        text = test_project_adoc.get_project_text()
        html = text_to_html(text, DocConverers.ASCIIDOC)
        result = html_to_pdf_weasyprint(
                html=html,
                target_path=out,
                css_path=css
                )
        assert result
