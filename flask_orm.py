import bs4


def _assign_children(children):
    children_html = ""
    for child in children:
        children_html += str(child)
    return children_html


def _get_attributes(attributes):
    attrs = ""
    for key, value in attributes.items():
        attrs += ' {key}="{value}"'.format(key = key, value = value)
    return attrs


class Base:
    """Base class for HTML objects, this includes tags, text, comments, jinja, etc."""

    def __init__(self, wrapper_start, wrapper_end, uses_end_tag = True, **attributes):
        self.children = []
        self.wrapper_start = wrapper_start
        self.wrapper_end = wrapper_end
        self.html = "{wrapper_start}{content}{wrapper_end}"
        self.uses_end_tag = uses_end_tag
        self.attributes = attributes
        self.content = ""

    def __iter__(self):
        for child in self.children:
            with child as child_html:
                yield child_html

    def __rshift__(self, other):
        if isinstance(other, Base):
            self.children.append(other)
        elif isinstance(other, (list, tuple)):
            self.children.extend(other)
        elif isinstance(other, str):
            self.content += other
        return self


class Tag(Base):
    """Base class for HTML tags"""

    def __init__(self, tag, **kwargs):
        super().__init__(**kwargs)
        self.tag = tag

    def __rshift__(self, other):
        if isinstance(other, dict):
            self.attributes.update(other)
            return self
        return super().__rshift__(other)

    def __set__(self, instance, value):
        if instance is None:
            return self
        else:
            self.__rshift__(value)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return str(self)

    def __delete__(self, instance):
        self.attributes = {}
        self.children = []
        self.content = ""


class HTMLTag(Tag):
    def __init__(self, tag, **kwargs):
        super().__init__(
                wrapper_start = "<{tag}{attributes}>",
                wrapper_end = "</{tag}>",
                tag = tag,
                **kwargs
        )

    def __str__(self):
        return self.html.format(
                wrapper_start = self.wrapper_start.format(
                        tag = self.tag,
                        attributes = _get_attributes(self.attributes)
                ),
                content = self.content + _assign_children(self.children),
                wrapper_end = self.wrapper_end.format(tag = self.tag) if self.uses_end_tag else ""
        )


class JinjaBlock(Tag):
    def __init__(self, tag, **kwargs):
        super().__init__(
                wrapper_start = "{% block {block_name} %}",
                wrapper_end = "{% endblock {block_name} %}",
                tag = tag,
                **kwargs
        )

    def __str__(self):
        return self.html.format(
                wrapper_start = self.wrapper_start.replace("{block_name}", self.tag),
                content = self.content + _assign_children(self.children),
                wrapper_end = self.wrapper_end.replace("{block_name}", self.tag),
        )


class JinjaInclude(Tag):
    def __init__(self, tag, **kwargs):
        super().__init__(
                wrapper_start = "{% include '{block_name}' %}",
                wrapper_end = "",
                tag = tag,
                uses_end_tag = False,
                **kwargs
        )

    def __str__(self):
        return self.html.format(
                wrapper_start = self.wrapper_start.replace("{block_name}", self.tag),
                content = self.content + _assign_children(self.children),
                wrapper_end = self.wrapper_end.replace("{block_name}", self.tag),
        )


class JinjaExtends(Tag):
    def __init__(self, tag, **kwargs):
        super().__init__(
                wrapper_start = "{% extends '{block_name}' %}",
                wrapper_end = "",
                tag = tag,
                uses_end_tag = False,
                **kwargs
        )

    def __str__(self):
        return self.html.format(
                wrapper_start = self.wrapper_start.replace("{block_name}", self.tag),
                content = self.content + _assign_children(self.children),
                wrapper_end = self.wrapper_end.replace("{block_name}", self.tag),
        )


class Page:
    """Base class for HTML pages"""
    root = HTMLTag("!DOCTYPE html", uses_end_tag = False)
    head = HTMLTag("head")
    body = HTMLTag("body")

    root >> head >> body

    def __str__(self):
        return str(self.root)

    def __init__(
            self,
            **kwargs
    ):
        if kwargs:
            if "title" in kwargs:
                self.head = HTMLTag("title") >> kwargs["title"]
                kwargs.pop("title")
            if "meta" in kwargs:
                self.meta = HTMLTag("meta", **kwargs["meta"])
                kwargs.pop("meta")
            if "body" in kwargs:
                self.body = kwargs["body"]
                kwargs.pop("body")
            if "head" in kwargs:
                self.head = kwargs["head"]
                kwargs.pop("head")
            if "root" in kwargs:
                self.root = kwargs["root"]
                kwargs.pop("root")


def create_page(**kwargs):
    return Page(**kwargs)


if __name__ == "__main__":
    nav_bar = lambda *links: (HTMLTag("nav") >>
                              HTMLTag("ul") >>
                              [HTMLTag("li", href = link[1]) >> link[0]
                               for link in links])

    page = create_page(
            title = JinjaBlock("title") >> "Hello World",
            meta = {"charset": "utf-8"},
            head = [
                    HTMLTag("link", rel = "stylesheet", href = "style.css"),
                    HTMLTag("script", src = "script.js")
            ],
            body = [
                    JinjaBlock("nav_bar") >> nav_bar(("Home", "#"), ("About", "#"), ("Contact", "#")),
                    JinjaBlock("body") >> "Hello World!",
                    JinjaBlock("footer") >> HTMLTag("footer") >> "© 2022"
            ]
    )
    soup = bs4.BeautifulSoup(str(page), "html.parser")
    print(soup.prettify())
