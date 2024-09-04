import pytest
from pathlib import Path
from bart.exceptions import (
    DocumentLevelException,
    MissingProjectRootException,
    NotInProjectException,
    ProjectDirExistsException,
    ReorderingException
    )
from bart.project import BartProject


class TestBartProject:
    """
    Tests around project-level functionality
    """

    def test_not_in_project(self, tmp_path):
        """
        If you're not in a project, raise an exception
        """

        with pytest.raises(NotInProjectException):
            BartProject(tmp_path)

    def test_init_missing_root(self, tmp_path):
        """
        Tests that we can find project files, but no root (unusual, but we need
        that root!)
        """
        project_file = tmp_path / '01-test.adoc'
        project_file.touch()

        with pytest.raises(MissingProjectRootException):
            BartProject(tmp_path)

    def test_begin(self, tmp_path):
        """
        You can start a new project given a path (made a Path by the cli) and a
        project name and that a "project root" is created
        """
        new_project = BartProject((tmp_path / "test"), new=True, project_name="Test")
        assert (tmp_path / "test").exists()
        assert new_project
        assert "00-test.adoc" in [p.name for p in new_project.documents]
        assert new_project.root.name == "00-test.adoc"


    def test_begin_but_dir_exists(self, tmp_path):
        """
        You can start a new project given a path (made a Path by the cli) and a
        project name and that a "project root" is created
        """
        (tmp_path / "test").mkdir()

        with pytest.raises(ProjectDirExistsException):
            BartProject(tmp_path, new=True, project_name="Test")

    def test_project_defaults(self, test_project_adoc):
        """
        We read in a project with a (default by design) config
        """

        assert test_project_adoc.project_dir.stem == 'test'
        assert test_project_adoc.config
        assert test_project_adoc.documents
        assert test_project_adoc.root.name.split('-')[0] == "00"

    def test_get_docs(self, test_project_adoc):
        """
        The expected documents are in the test_project and are ordered as such,
        and that the documents attribute of the project has been updated
        """

        assert len(test_project_adoc.get_project_docs()) == 4
        assert len(test_project_adoc.documents) == \
            len(test_project_adoc.get_project_docs())
        for i in range(0,4):
            assert str(i) in test_project_adoc.get_project_docs()[i].name

    def test_get_project_text(self, test_project_adoc):
        """
        Assert that we can get all the docs in the project. Note that the
        functional tests for this are on the join_docs() function
        """
        result = test_project_adoc.get_project_text()
        assert result


    @pytest.mark.parametrize("level", range(2,6))
    def test_increase_level(self, test_project_adoc, level):
        """
        Tests that, if the doc_levels of the project changes, the
        config and filenames are updated accordingly
        """
        test_project_adoc.increase_doc_levels(level)
        check_doc_number = test_project_adoc.get_project_docs()[1].name.split('-')[0]
        # check the document level
        assert len(check_doc_number) == level
        assert check_doc_number == f"1{'0' * (level-1) }"
        # check the project config
        with (test_project_adoc.project_dir / '.bart.toml').open('rt') as f:
            assert f"doc_levels = {level}\n" in f.readlines()


class TestProjectAdd:
    """
    Tests around adding docs to the project
    """

    def test_add_document(self, test_project_adoc):
        """
        We can add a document and it has the correct prefix
        """
        new_doc = test_project_adoc.add_document(name="test")
        # was created
        assert new_doc.is_file()
        # that it sorts last
        assert test_project_adoc.get_project_docs()[-1] == new_doc
        # has the correct prefix (we subtract 1 for the project root)
        assert (
            int(new_doc.name.split('-')[0]) == 
            len(test_project_adoc.get_project_docs()) - 1
                )
    
    def test_add_document_level_error(self, test_project_adoc):
        """
        We should not be allowed to add docs at an impossibly low level
        """

        with pytest.raises(DocumentLevelException):
            test_project_adoc.add_document("Chapter One", level=100)

class TestProjectReordering:
    """
    Tests around project reordering
    """
    
    def test_reorder_bad_list(self, test_project_adoc):
        """
        If the new list and the old list don't match, don't reorder
        """
        with pytest.raises(ReorderingException):
            new_list = [d for d in test_project_adoc.documents]
            new_list.append(Path("foo"))
            test_project_adoc.reorder_project_documents(new_list)

    def test_reorder_simple_case_level_1(self, test_project_adoc):
        """
        Tests that we can reorder a "simple" doc_levels 1 project
        """
        # setup, reverse the list and replace the root
        new_list = [d for d in test_project_adoc.documents[::-1]]
        new_list.insert(0, new_list.pop(len(new_list) -1))

        reordered_docs = test_project_adoc.reorder_project_documents(new_list)

        for index, doc in enumerate(new_list):
            # ensure that we've actually moved the correct file
            assert reordered_docs[index].name[3:] == doc.name[3:]
            # ensure that the index (0, 1, 2, 3) is in the new numbering
            assert str(index) in reordered_docs[index].name[:3]
