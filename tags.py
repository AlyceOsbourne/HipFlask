from dataclasses import dataclass
from typing import Optional

from flask_orm import Tag, HTMLTag, JinjaBlock, JinjaInclude
from flask import Blueprint, render_template_string


def pretty_print(html):
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(str(html), "html.parser")
    print(soup.prettify())


generated = Blueprint("generated", __name__, template_folder = "templates")


class Root(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__(
                "doctype html",
                uses_end_tag = False,
                **kwargs
        )


class Html(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__(
                "html",
                **kwargs
        )


class Head(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__(
                "head",
                **kwargs
        )


class Title(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__(
                "title",
                **kwargs
        )


class Body(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__(
                "body",
                **kwargs
        )


class Meta(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__(
                "meta",
                uses_end_tag = False,
                **kwargs
        )


class StyleSheet(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__(
                "link",
                uses_end_tag = False,
                **kwargs
        )


class Style(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__(
                "style",
                **kwargs
        )


class ScriptFile(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__(
                "script",
                uses_end_tag = False,
                **kwargs
        )


class Script(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__(
                "script",
                **kwargs
        )


class Page:
    _root = Root()
    _html = Html()

    _head = Head()

    _title = Title()
    _title_block = JinjaBlock("title")

    _css = JinjaBlock("css")
    _meta = Meta() >> {
            "charset"   : "utf-8",
            "name"      : "viewport",
            "content"   : "width=device-width, initial-scale=1, shrink-to-fit=no",
            "http-equiv": "X-UA-Compatible",
    }

    _body = Body()
    _body_block = JinjaBlock("body")
    _js = JinjaBlock("js")

    _root >> (_html >> (_head >> (_title >> _title_block) >> _css >> _meta) >> (_body >> _body_block >> _js))

    def __init_subclass__(cls, route = None, **kwargs):
        super().__init_subclass__(**kwargs)
        if route is None:
            return

        @generated.route(f"/{route}")
        def view():
            return render_template_string(str(cls._root))

        cls._route = route

    def __str__(self):
        return str(self._root)


@dataclass
class Template(Page):
    title: str
    css: Optional[str | Tag]
    body: Optional[str | Tag]
    js: Optional[str | Tag]

    def __init__(
            self,
            title,
            body = "",
            css = (
                StyleSheet() >> {
                        "rel"        : "stylesheet",
                        "href"       : "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css",
                        "integrity"  : "sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T",
                        "crossorigin": "anonymous",
                },
                StyleSheet() >> {
                        "rel"        : "stylesheet",
                        "href"       : "https://use.fontawesome.com/releases/v5.8.2/css/all.css",
                        "integrity"  : "sha384-oS3vJWv+0UjzBfQzYUhtDYW+Pj2yciDJxpsK1OYPAYjqT085Qq/1cq5FLXAZQ7Ay",
                        "crossorigin": "anonymous",
                },
            ),
            js = (
                ScriptFile() >> {
                        "src"        : "https://code.jquery.com/jquery-3.3.1.slim.min.js",
                        "integrity"  : "sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo",
                        "crossorigin": "anonymous",
                },
                ScriptFile() >> {
                        "src"        : "https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js",
                        "integrity"  : "sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1",
                        "crossorigin": "anonymous",
                },
                ScriptFile() >> {
                        "src"        : "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js",
                        "integrity"  : "sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM",
                        "crossorigin": "anonymous",
                },
            ),
    ):
        self._title_block = title
        self._css = css
        self._body_block = body
        self._js = js


if __name__ == "__main__":
    pretty_print(
        Template(
            title = "Test",
            body = "test",
    ))
