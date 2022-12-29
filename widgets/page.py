from base import NodeDescriptor
from widgets.widget import Widget
from widgets.head import DefaultHead, JinjaHead


def default_root():
    return NodeDescriptor("DocType"), NodeDescriptor("html")


class Page(Widget):
    root, html = default_root()
    head = DefaultHead()
    body = NodeDescriptor("body")
    footer = NodeDescriptor("footer")

    def __init__(self):
        self.root = self.html
        self.html = self.head, self.body
        self.body = self.footer


class JinjaPage(Page):
    head = JinjaHead()

    def __init__(self, **kwargs):
        super().__init__()
        self.html = self.head, self.body
