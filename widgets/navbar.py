from widgets.widget import Widget
from base import *


class SimpleNavbar(Widget):
    root = NodeDescriptor('nav')
    brand = NodeDescriptor('a')
    ul = NodeDescriptor('ul')

    def __init__(self, **links):
        self.ul = (
            Node('li', Node('a', href=href)).append(Node(text))
            for href, text in links.items()
        )
