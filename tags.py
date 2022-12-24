from flask_orm import Tag, HTMLTag, JinjaBlock, JinjaInclude


def pretty_print(html):
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(str(html), "html.parser")
    print(soup.prettify())


class Page:
    _root = HTMLTag("doctype html", uses_end_tag = False)
    _html = HTMLTag("html")
    _head = HTMLTag("head")
    _body = HTMLTag("body")
    _title = HTMLTag("title")

    _root >> _html >> (_head >> _title) >> _body


class BaseTemplate(Page):
    def __init__(
            self,
            title: Tag | str = JinjaBlock("title"),
            head: Tag | str = JinjaBlock('head'),
            body: Tag | str = JinjaBlock("body")
    ):
        self._title = title
        self._head = head
        self._body = body

    def __str__(self):
        return str(self._root)


if __name__ == "__main__":
    pretty_print(BaseTemplate())
