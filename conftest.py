from pathlib import Path
from bart.config import BartConfig, DocConverers, MarkupLanguages
import shutil
import pytest

from bart.project import BartProject


@pytest.fixture()
def test_config(tmp_path) -> Path:
    """
    Test config... for testing. Is set to markdown to ensure that we are not
    just using the defaults
    """
    config_path = tmp_path / 'bart.toml'
    config = BartConfig(use_default=True)
    config.markup = MarkupLanguages.MARKDOWN
    config.write_to(config_path)
    return config_path


@pytest.fixture()
def test_adoc(tmp_path) -> Path:
    """
    Empty asciidoc file path for testing
    """
    test_dir = tmp_path / 'test'
    test_dir.mkdir()
    test_file = test_dir / 'test.adoc'
    test_file.touch()
    return test_file

@pytest.fixture()
def test_project_adoc(tmp_path) -> BartProject:
    """
    Test project with various adoc files with a default config
    """
    test_dir = tmp_path / 'test'
    test_dir.mkdir()

    default_config = BartConfig(use_default=True)
    test_config = test_dir / '.bart.toml'
    default_config.write_to(test_config)

    shutil.copytree('tests/projects/adoc',
                    test_dir,
                    dirs_exist_ok=True)
    return BartProject(test_dir)

@pytest.fixture()
def test_project_md(tmp_path) -> BartProject:
    """
    Test project with various markdown files with a default config
    (accounting for markup language)
    """
    test_dir = tmp_path / 'test'
    test_dir.mkdir()

    default_config = BartConfig(use_default=True)
    default_config.markup = MarkupLanguages.MARKDOWN
    default_config.default_converter = DocConverers.MARKDOWN2
    test_config = test_dir / '.bart.toml'
    default_config.write_to(test_config)

    shutil.copytree('tests/projects/md',
                    test_dir,
                    dirs_exist_ok=True)
    return BartProject(test_dir)

