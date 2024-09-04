import markdown2


def md_to_html(text: str):
    """ takes a markdown str and returns html """

    print("Running input through markdown conversion....")
    html = markdown2.markdown(text, extras=["fenced-code-blocks",
                                            "header-ids",
                                            "footnotes",
                                            "smarty-pants"  # to save a step
                                            ])
    return html

