from pathlib import Path

def join_docs(docs: list[Path],
              delimit: bool = False) -> str:
    """
    Joins the text of documents and returns it, adding newlines in between
    the text of each file and returns the text.
    
    If `delimit` is passed as true, then the resultant text includes
    commented delimiters noting the source of a given chunk of text
    """
    text = ''
    for doc in docs:
        with doc.open('rt') as f:
            doc_text = f.read() + "\n"

            if delimit:
                match doc.suffix:
                    case ".adoc":
                        doc_text = f"""
# tag::{doc.name}[]
{doc_text}
# end::{doc.name}[]
"""
                    case ".md":
                        doc_text = f"""
<!-- {doc.name} -->
{doc_text}
<!-- end {doc.name} -->
"""
                    case _:  # TODO: figure out what to do with text files
                        doc_text = doc_text

            text += doc_text
    
    return text
