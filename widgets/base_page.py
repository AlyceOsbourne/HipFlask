from base import ClassNode, Node, Widget


class Document(Widget):
    root = ClassNode('DocType')

    def __init__(self, html = None, **kwargs):
        self.root = self.html = html or Node('html')
        super().__init__(**kwargs)
