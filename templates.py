from bootstrap_tags import *
from flask_orm import (
    JinjaBlock,
    Tag,
)


class PageTemplate:
    html: str | Tag = Html()
    head: str | Tag = Head()
    title: str | Tag = Title()
    meta: str | Tag = Meta() >> {
            "charset": "utf-8",
            "name"   : "viewport",
            "content": "width=device-width, initial-scale=1, shrink-to-fit=no",
    }
    body: str | Tag = Body()
    root: str | Tag = Root() >> [html >> [head >> [title, meta], body]]

    def __init__(self, /, *,
                 title = None,
                 html = None,
                 head = None,
                 body = None):
        self.title = title
        self.html = html
        self.head = head
        self.body = body

    def __str__(self):
        return str(self.root)


class BootstrapMixin:
    bootstrap_css: str | Tag = BootstrapStyleSheet()
    bootstrap_js: str | Tag = BootStrapScript()
    jquery: str | Tag = BootstrapJQuery()

    def __init_subclass__(cls, /, *, bootstrap = True, **kwargs):
        # make sure mixin is being applied to a subclass of PageTemplate
        if not issubclass(cls, PageTemplate):
            raise TypeError("BootstrapMixin must be applied to a subclass of PageTemplate")
        super().__init_subclass__(**kwargs)
        if bootstrap:
            if not hasattr(cls, "head"):
                cls.head = Head()
            getattr(cls, "head") >> [getattr(cls, "bootstrap_css")]
            if not hasattr(cls, "body"):
                cls.body = Body()
            getattr(cls, "body") >> [getattr(cls, "bootstrap_js"), getattr(cls, "jquery")]
            if not hasattr(cls, "root"):
                cls.root = Root()
            getattr(cls, "root") >> [getattr(cls, "html") >> [getattr(cls, "head"), getattr(cls, "body")]]
        return cls


class JinjaMixin:
    title_block: str | Tag = JinjaBlock("title")
    head_block: str | Tag = JinjaBlock("head")
    css_block: str | Tag = JinjaBlock("css")
    body_block: str | Tag = JinjaBlock("body")
    js_block: str | Tag = JinjaBlock("js")

    def __init_subclass__(cls, /, *, jinja = True, **kwargs):
        # make sure mixin is being applied to a subclass of PageTemplate
        if not issubclass(cls, PageTemplate):
            raise TypeError("JinjaMixin must be applied to a subclass of PageTemplate")
        super().__init_subclass__(**kwargs)
        if jinja:
            if not hasattr(cls, "title"):
                cls.title = Title()
            getattr(cls, "title") >> getattr(cls, "title_block")
            if not hasattr(cls, "head"):
                cls.head = Head()
            getattr(cls, "head") >> getattr(cls, "head_block")
            if not hasattr(cls, "body"):
                cls.body = Body()
            getattr(cls, "body") >> getattr(cls, "body_block")
            if not hasattr(cls, "root"):
                cls.root = Root()
            getattr(cls, "root") >> [getattr(cls, "html") >> [getattr(cls, "head"), getattr(cls, "body")]]
        return cls


class Page(PageTemplate, BootstrapMixin, JinjaMixin):
    def __init__(self, /, **kwargs):
        super().__init__(**kwargs)


if __name__ == "__main__":
    page = Page(title = "Hello World")
    print(page)
