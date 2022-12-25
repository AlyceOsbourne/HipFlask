from tags import *


def head_template(title, stylesheets = None, scripts = None):
    head = Head()
    head_block = JinjaBlock("head")
    title = Title() >> title
    meta = Meta() >> {
            "charset": "utf-8",
            "name"   : "viewport",
            "content": "width=device-width, initial-scale=1, shrink-to-fit=no",
    }
    if stylesheets is None:
        stylesheets = []
    if scripts is None:
        scripts = []
    return head >> head_block >> title >> meta >> stylesheets >> scripts


def body_template(nav_bar,  footer):
    body = Body()
    body_block = JinjaBlock("body")
    return body >> nav_bar >> body_block >> footer


def nav_bar_template(*pages):
    nav_bar = NavBar()
    ul = Ul()
    for page in pages:
        ul >> (Li >> (A >> {"href": page["href"]} >> page["name"]))
    return nav_bar >> ul


def footer_template():
    footer = Footer()
    footer_block = JinjaBlock("footer")
    return footer >> footer_block


class Page:
    _root = Root()
    _html = Html()
    _head = head_template("Page Title")
    _body = body_template(
            nav_bar_template(
                    {"name": "Home", "href": "/"},
                    {"name": "About", "href": "/about"},
                    {"name": "Contact", "href": "/contact"},
            ),
            footer_template(),
    )

    _root >> _html >> _head >> _body

    def __str__(self):
        return self._root


if __name__ == "__main__":
    print(pretty_print(Page()))
