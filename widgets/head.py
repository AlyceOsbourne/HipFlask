from base import *
from widgets.widget import Widget


def default():
    root = NodeDescriptor("head")
    title = NodeDescriptor("title")
    meta = NodeDescriptor(
            "meta",
            charset = "utf-8",
            name = "viewport",
            content = "width=device-width, initial-scale=1, shrink-to-fit=no"
    )
    return root, title, meta


def jinja():
    head = NodeDescriptor('block', "head")
    title = NodeDescriptor('block', "title")
    css = NodeDescriptor('block', "css")
    meta = NodeDescriptor('block', "meta")
    return head, title, css, meta


class DefaultHead(Widget):
    root, title, meta = default()

    def __init__(self):
        self.root = self.title, self.meta


class JinjaHead(DefaultHead):
    head_block, title_block, css_block, meta_block = jinja()

    def __init__(self):
        super().__init__()
        self.head = self.head_block, self.meta_block, self.css_block
        self.title = self.title_block
