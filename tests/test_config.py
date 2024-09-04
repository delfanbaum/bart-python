from bart.config import BART_CONFIG_PATHS, BartConfig, BuildFormats, DocConverers, MarkupLanguages


class TestConfig:
    """
    Specific tests for config; actual coverage of this function is sort of
    everywhere (for now?)
    """

    def test_use_global_config(self, test_config):
        """
        It should pull in global config paths. For this we just append a test
        path to the config
        """
        BART_CONFIG_PATHS.append(test_config)
        config = BartConfig()
        assert config.markup == MarkupLanguages.MARKDOWN
        # we have to explicitly clean this up, otherwise it remains in memory
        BART_CONFIG_PATHS.remove(test_config)

    def test_extends_project(self, test_project_adoc):
        """
        Test that we extend project-level config
        """
        project_dir = test_project_adoc.project_dir
        config_file = project_dir / ".bart.toml"
        with config_file.open('wt') as f:
            f.write("""[bart]
markup = "asciidoc"
default_converter = "asciidoctor"
default_build = "weasyprint"
css_path = "test.css"
doc_levels = 2
""")
        with (project_dir / "test.css").open('wt') as f:
            f.write("body {font-size: 12pt}")

        # update the config
        test_project_adoc._update_config()
        config: BartConfig = test_project_adoc.config
        assert config.markup == MarkupLanguages.ASCIIDOC
        assert config.default_converter == DocConverers.ASCIIDOCTOR
        assert config.doc_levels == 2
        assert config.css_path == test_project_adoc.project_dir / "test.css"
        assert config.default_build == BuildFormats.PDF_WP
