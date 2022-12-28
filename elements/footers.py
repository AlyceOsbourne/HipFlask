from base import document, node


@document(init=False)
class SimpleFooter:
    root = node(
            "footer",
            is_class_node = True
    )

    copyright: 'root' = node(
            "p",
            is_class_node = True
    )

    def __init__(self, text):
        self.copyright = text


