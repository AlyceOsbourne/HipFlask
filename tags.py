from flask_orm import HTMLTag, JinjaBlock, JinjaInclude, JinjaExtends


def pretty_print(html):
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(str(html), "html.parser")
    return soup.prettify()


class Root(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__("!DOCTYPE html", uses_end_tag=False, **kwargs)


class Html(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__("html", **kwargs)


class Head(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__("head", **kwargs)


class Title(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__("title", **kwargs)


class Body(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__("body", **kwargs)


class Meta(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__("meta", uses_end_tag=False, **kwargs)


class StyleSheet(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__("link", uses_end_tag=False, **kwargs)


class Style(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__("style", **kwargs)


class ScriptFile(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__("script", uses_end_tag=False, **kwargs)


class Script(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__("script", **kwargs)


class NavBar(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__("nav", **kwargs)


class Footer(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__("footer", **kwargs)


class Div(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__("div", **kwargs)


class Span(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__("span", **kwargs)


class P(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__("p", **kwargs)


class H1(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__("h1", **kwargs)


class H2(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__("h2", **kwargs)


class H3(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__("h3", **kwargs)


class H4(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__("h4", **kwargs)


class H5(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__("h5", **kwargs)


class H6(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__("h6", **kwargs)


class Ul(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__("ul", **kwargs)


class Ol(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__("ol", **kwargs)


class Li(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__("li", **kwargs)


class Table(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__("table", **kwargs)


class Small(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__("small", **kwargs)


class Strong(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__("strong", **kwargs)


class Em(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__("em", **kwargs)


class A(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__("a", **kwargs)


class Img(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__("img", uses_end_tag=False, **kwargs)


class Form(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__("form", **kwargs)


class Input(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__("input", uses_end_tag=False, **kwargs)


class Label(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__("label", **kwargs)


class Button(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__("button", **kwargs)


class TextArea(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__("textarea", **kwargs)


class Select(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__("select", **kwargs)


class Option(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__("option", **kwargs)


class Fieldset(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__("fieldset", **kwargs)


class Legend(HTMLTag):
    def __init__(self, **kwargs):
        super().__init__("legend", **kwargs)


if __name__ == "__main__":
    print(
        pretty_print(
            Root
            >> (
                Html
                >> (
                    Head
                    >> (
                        Title >> "Hello World",
                        Meta
                        >> {
                            "charset": "utf-8",
                            "name": "viewport",
                            "content": "width=device-width, initial-scale=1, shrink-to-fit=no",
                            "http-equiv": "X-UA-Compatible",
                        },
                        Style >> "body {background-color: #000;color: #fff;}",
                    ),
                    Body
                    >> (
                        H1 >> "Hello World",
                        P >> "This is a test",
                        Small >> "This is a test",
                        Strong >> "This is a test",
                        Em >> "This is a test",
                        A
                        >> {
                            "href": "https://www.google.com",
                        }
                        >> "This is a test",
                        Img
                        >> {
                            "src": "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
                        },
                        Form
                        >> {
                            "action": "https://www.google.com",
                            "method": "GET",
                        }
                        >> (
                            Input
                            >> {
                                "type": "text",
                                "name": "q",
                                "value": "Hello World",
                            },
                            Button
                            >> {
                                "type": "submit",
                                "name": "btnK",
                                "value": "Google Search",
                            },
                        ),
                    ),
                )
            )
        )
    )
