from hip_flask import document, node


@document
class HTML:
    root = node("DocType", is_class_node = True)
    html: "root" = node("html", is_class_node = True)
    head: "html" = node("head", is_class_node = True)
    body: "html" = node("body", is_class_node = True)


class Index(HTML):
    head_title = node("title")
    head_meta = node("meta", charset = "utf-8")

    def __init__(self, *args, **kwargs):
        super().__init__(
                *args,
                head = [self.head_title, self.head_meta],
                **kwargs
        )


print(Index())
