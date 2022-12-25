from tags import *
from bs4 import BeautifulSoup


def nav_bar(*links):
    nav = Nav()
    ul = Ul()
    for link in links:
        ul >> [Li() >> [A(href = link[1]) >> link[0]]]  # noqa
    return nav >> ul


def default_head_structure():
    title = Title()
    meta = Meta(
            charset = "utf-8",
            name = "viewport",
            content = "width=device-width, initial-scale=1.0",
    )
    return title, meta


def default_file_structure():
    root = Root()
    html = Html()
    head = Head()
    body = Body()
    title, meta = default_head_structure()

    return (
            root >> [html >> [head >> [title, meta], body]],
            html,
            head,
            title,
            meta,
            body,
    )


def bootstrap():
    bootstrap_css = StyleSheet(
            href = "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css",
            integrity = "sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T",
            crossorigin = "anonymous",
    )
    bootstrap_js = Script(
            src = "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js",
            integrity = "sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM",
            crossorigin = "anonymous",
    )
    jquery = Script(
            src = "https://code.jquery.com/jquery-3.3.1.slim.min.js",
            integrity = "sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo",
            crossorigin = "anonymous",
    )
    popper = Script(
            src = "https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js",
            integrity = "sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1",
            crossorigin = "anonymous",
    )
    return bootstrap_css, bootstrap_js, jquery, popper


class Page:
    root, html, head, title, meta, body = default_file_structure()

    def __init__(
            self, /, *, root = None, html = None, head = None, body = None, title = None, meta = None
    ):
        self.root = root
        self.html = html
        self.head = head
        self.body = body
        self.title = title
        self.meta = meta

    def __str__(self):
        return str(self.root)


if __name__ == "__main__":
    page = Page(
            title = JinjaBlock("title") >> "Hello World",
            head = [bootstrap(), JinjaBlock("head")],
            body = [
                    nav_bar(("Home", "/"), ("About", "/about"), ("Contact", "/contact")),
                    JinjaBlock("content"),
                    Footer() >> "© 2022",
            ],
    )
    soup = BeautifulSoup(str(page), "html.parser")
    print(soup.prettify())