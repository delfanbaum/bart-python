from pathlib import Path
import shutil
from typing import Optional
from bart.actions.build import html_to_pdf_weasyprint

from bart.actions.joins import join_docs
from bart.config import BartConfig, BuildFormats
from bart.converters.api import text_to_html
from bart.exceptions import (
    BuildTargetException,
    NotInProjectException,
    MissingProjectRootException,
    ProjectDirExistsException,
    ProjectFileExistsException,
    ReorderingException
)
from bart.templates import named_document_template, write_template
from bart.utilites import get_doc_number, get_valid_pathname


class BartProject:

    def __init__(self,
                 project_dir: Path = Path.cwd(),
                 new: bool = False,
                 project_name: str = "") -> None:
        self.project_dir = project_dir
        self.config = BartConfig(self.project_dir)

        if new:  # have to "seed" the project before getting docs
            self.begin(project_name)

        self.documents = self.get_project_docs()
        self.root = self.documents[0]
        # infer from project root path stem (name w/o suffix)
        self.name = "-".join(self.root.stem.split("-")[1:]).split('.')

        if not int(self.root.name.split('-')[0]) == 0:
            raise MissingProjectRootException


    def begin(self, project_name):
        """
        "Seeds" a new project with a 00- "root" file and title
        """

        numbering = get_doc_number(self.config.doc_levels)

        if self.project_dir.exists():
            raise ProjectDirExistsException
        else:
            self.project_dir.mkdir()

        project_root = (self.project_dir / (numbering + "-" +
                                            get_valid_pathname(project_name) + "." +
                                            self.config.markup.extension()))
        write_template(named_document_template,
                       project_root,
                       markup=self.config.markup,
                       document_name=project_name,
                       heading_level=1
                       )


    def get_project_docs(self) -> list[Path]:
        """
        Collects the project files for further operations
        """
        self.documents = (
                list(self.project_dir.glob(
                    f"[0-9]*.{self.config.markup.extension()}"))
                )

        if not self.documents:
            raise NotInProjectException

        self.documents.sort()
        return self.documents
    

    def get_project_text(self) -> str:
        """
        Joins the whole project, returning its text
        """
        return join_docs(self.documents)

    def increase_doc_levels(self, new_level):
        """
        Increases the doc levels for the project and renames the docs
        accordingly
        """
        # config changes
        self.config.doc_levels = new_level
        self.config.write_to(self.project_dir / '.bart.toml')

        # bump docs
        for doc in self.documents:
            doc_number = int(doc.name.split('-')[0])
            doc_name = '-'.join(doc.name.split('-')[1:])
            new_fn = f"{doc_number}{'0' * (new_level - 1)}-{doc_name}"
            shutil.move(doc, self.project_dir / new_fn)


    def add_document(self, name: str, level: int = 1, number: Optional[str] = None) -> Path:
        """
        Adds a document at the "section" level (what config.doc_numbering) is set to
        """
        last_doc = self.get_project_docs()[-1]

        if number:
            new_document = (self.project_dir /
                            (f"{number}-{get_valid_pathname(name)}." +
                             f"{self.config.markup.extension()}"))
            if new_document.exists():
                raise ProjectFileExistsException

        else:
            next_number = get_doc_number(self.config.doc_levels,
                                         last_doc,
                                         level)

            new_document = (self.project_dir /
                            (f"{next_number}-{get_valid_pathname(name)}" +
                             f".{self.config.markup.extension()}"))

        write_template(named_document_template,
                       new_document,
                       markup=self.config.markup,
                       document_name=name,
                       heading_level=self.config.doc_levels
                       )
        return new_document
    
    def join_documents(self,
                       docs: list[Path],
                       delmit: bool = False,
                       write: bool = False):
        """
        Joins the text of documents and returns it, adding newlines in between
        the text of each file.
        
        If `delimit` is passed as true, then the resultant text includes
        commented delimiters noting the source of a given chunk of text

        If `write` is true, the documents will be combined into the "first" (in
        terms of order) 
        """
        text = join_docs(docs, delmit)
        if write:
            with docs[0].open('wt') as f:
                f.write(text)  # write to the "new" document
            for d in docs[1:]:  # remove the rest of the docs
                d.unlink()

            # run the reorder to get the numbering correct
            self.get_project_docs()  # refresh list
            self.reorder_project_documents(self.documents)


    def reorder_project_documents(self, new_order: list[Path]) -> list[Path]:
        """
        Reorders (re-prefixes) documents in the project, with a very small
        safeguard that it requires that the members of the new ordering be equal
        to the members of what's currently in the project directory at the time
        of reordering
        """
        if (
                set(new_order) != set(self.get_project_docs()) or
                new_order[0] != self.root
            ):
            raise ReorderingException

        # the first "reordered" doc is still the root
        new_fpath = self.root

        for doc in new_order:
            if doc == self.root:  # skip the root
                continue

            new_numbering = get_doc_number(self.config.doc_levels,
                                           new_fpath)  # the last reordered doc

            new_fpath = self.project_dir / (new_numbering + "-" +
                                            "-".join(doc.name.split('-')[1:]))
            doc.rename(new_fpath)

        return self.get_project_docs()

    def build(self,
              target: BuildFormats = BuildFormats.HTML,
              file: Optional[Path] = None):
        """
        Builds the project (or optionally a single file) to a target build
        format (default is HTML)
        """
        if not target and self.config.default_build:
            target = self.config.default_build

        if file:
            with file.open('rt') as f:
                text = f.read()
            target_path = self.project_dir / file.name.replace(
                        file.suffix,
                        f".{target.name.lower().split('_')[0]}")
        else:
            text = self.get_project_text()
            target_path = (self.project_dir /
                        f"{self.name}.{target.name.lower().split('_')[0]}")
        
        html = text_to_html(text, self.config.default_converter)

        match target:
            case BuildFormats.HTML:
                with target_path.open('wt') as f:
                    f.write(html)
            case BuildFormats.PDF_WP:
                out_path = html_to_pdf_weasyprint(
                        html=html,
                        target_path=target_path,
                        css_path=self.config.css_path
                        )
                print(out_path)
            case BuildFormats.PDF_PJS:
                pass
            case BuildFormats.DOC | BuildFormats.DOCX:
                pass
            case _:
                raise BuildTargetException

    # testing methods
    def _update_config(self):
        """
        Updates the configuration if changed while the project is still in
        memory (for testing)
        """
        self.config = BartConfig(self.project_dir)
