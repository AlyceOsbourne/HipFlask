from bs4 import BeautifulSoup

from bootstrap_tags import *
from flask_orm import (
    JinjaBlock,
    Tag,
)
import flask

blueprint = flask.Blueprint("easy_site", __name__)


class AnnotationMixin:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        for attr_name, attr_value in cls.__annotations__.items():
            if isinstance(attr_value, str):
                if hasattr(cls, attr_value):
                    getattr(cls, attr_value) >> getattr(cls, attr_name)
            elif isinstance(attr_value, Tag):
                attr_value >> getattr(cls, attr_name)
        return cls


class RenderMixin:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.__render__ = cls.__str__
        return cls


class RouteMixin:
    def __init_subclass__(cls, route=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if route:
            route_type = type(route, (cls,), {
                    "__call__": lambda self: flask.render_template_string(str(self)),
                    '__name__': cls.__name__,
            })
            blueprint.add_url_rule(route, view_func=route_type())
        return cls


class TemplateElement(AnnotationMixin, RenderMixin):
    ...


class EasySite(AnnotationMixin, RouteMixin):
    root = Root()
    html: root = Html()

    head: html = Head()
    title: head = Title()
    meta: head = Meta()
    bootstrap_stylesheet: head = BootstrapStyleSheet()

    body: html = Body()
    bootstrap_jquery: body = BootstrapJQuery()
    bootstrap_script: body = BootStrapScript()
    root_style: html = Style()
    style: root_style = ":root { margin: 0; padding: 0;}"

    def __init__(self, /, *, title = None, html = None, head = None, body = None):
        self.title = title
        self.html = html
        self.head = head
        self.body = body

    def __str__(self):
        soup = BeautifulSoup(str(self.root), "html.parser")
        return soup.prettify()


class NavBar(TemplateElement):
    nav = Nav()
    ul: nav = Ul()

    def __init__(self, *links: tuple[str, str]):
        self.ul = [
                Li() >> [A(href = link) >> text]
                for text, link in links
        ]

    def __str__(self):
        return str(self.nav)

    render = __str__


if __name__ == "__main__":
    nav = NavBar(
            ("Home", "/"),
            ("About", "/about"),
            ("Contact", "/contact"),
    )


    class Base(EasySite):
        nav_bar: 'body' = nav
        content: 'body' = Div()
        footer: 'body' = Footer() >> "© 2022"

        def __init__(self, /, *, content = None, **kwargs):
            super().__init__(**kwargs)
            self.content = content


    class Home(Base, route = "/"):
        def __init__(self, /, **kwargs):
            super().__init__(title = 'Home', **kwargs)
            self.content = "Home"


    class About(Base, route = "/about"):
        def __init__(self, /, **kwargs):
            super().__init__(title = 'About', **kwargs)
            self.content = "About"


    class Contact(Base, route = "/contact"):
        def __init__(self, /, **kwargs):
            super().__init__(title = 'Contact', **kwargs)
            self.content = "Contact"


    app = flask.Flask(__name__)
    app.register_blueprint(blueprint)
    app.run(debug = True)
