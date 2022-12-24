from flask import Blueprint, render_template_string

from flask_orm import JinjaBlock
from tags import Body, Footer, Head, Html, Meta, NavBar, pretty_print, Root, ScriptFile, StyleSheet, Title

generated = Blueprint("generated", __name__, template_folder = "templates")


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



class Template(Page):
    def __init__(
        self,
        title: str,
    ):
        self._title_block = title
        self._body_block = (
            NavBar >> JinjaBlock("navbar"),
            JinjaBlock("content"),
            Footer >> JinjaBlock("footer"),
        )

        self._css = (
            StyleSheet
            >> {
                "rel": "stylesheet",
                "href": "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css",
                "integrity": "sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T",
                "crossorigin": "anonymous",
            },
            StyleSheet
            >> {
                "rel": "stylesheet",
                "href": "https://use.fontawesome.com/releases/v5.8.2/css/all.css",
                "integrity": "sha384-oS3vJWv+0UjzBfQzYUhtDYW+Pj2yciDJxpsK1OYPAYjqT085Qq/1cq5FLXAZQ7Ay",
                "crossorigin": "anonymous",
            },
        )

        self._js = (
            ScriptFile
            >> {
                "src": "https://code.jquery.com/jquery-3.3.1.slim.min.js",
                "integrity": "sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo",
                "crossorigin": "anonymous",
            },
            ScriptFile
            >> {
                "src": "https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js",
                "integrity": "sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1",
                "crossorigin": "anonymous",
            },
            ScriptFile
            >> {
                "src": "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js",
                "integrity": "sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM",
                "crossorigin": "anonymous",
            },
        )


if __name__ == "__main__":
    pretty_print(
        Template(
            title="Test",
        )
    )
