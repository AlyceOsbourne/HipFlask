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

    def __init__(self, wrapper_start, wrapper_end, tag, uses_end_tag = True, **attributes):
        self.children = []
        self.wrapper_start = wrapper_start
        self.wrapper_end = wrapper_end
        self.html = "{wrapper_start}{content}{wrapper_end}"
        self.uses_end_tag = uses_end_tag
        self.attributes = attributes
        self.content = ""
        self.tag = tag

    def __rshift__(self, other):
        if isinstance(other, Base):
            self.children.append(other)
        elif isinstance(other, (list, tuple)):
            for thing in other:
                self.__rshift__(thing)
        elif isinstance(other, str):
            self.content += other
        elif isinstance(other, dict):
            self.attributes.update(other)
        elif other is None:
            pass
        else:
            raise TypeError("Cannot add {} to HTML object".format(type(other)))
        return self


class Tag(Base):
    """Descriptor Wrapper for the Base class"""

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


